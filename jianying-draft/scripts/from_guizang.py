# /// script
# requires-python = ">=3.11"
# dependencies = ["pyJianYingDraft==0.3.0", "numpy", "soundfile"]
# ///
"""guizang 宣传片工程 → 剪映专业版可编辑草稿：画面按镜头切段，配乐 / 旁白 / 音效 / 字幕分轨，音量按成片母带还原。

用法：uv run from_guizang.py <工程目录> [--video 成片.mp4] [--root 草稿目录] [--force] [--portable]

工程约定（guizang-product-video-skill 起步工程的产物）：
  plan.json                   shots[{id,start,end,headline}]、voice.starts、audio.music/cues、fps、duration、width、height
  renders/final.mp4           成片；也可用 --video 指定，renders/ 下只有一个 mp4 时自动用它
  assets/bed.wav              配乐 + 人声预混（bed.py：人声期间配乐 -8 dB，峰值超过 0.89 时整体缩放）
  assets/vo-stem.wav          未缩放的人声（bed.py 同时输出）
  assets/vo/norm/vNN.wav      每句配音
  assets/music-ducked.wav、assets/sfx-stem.wav、assets/master.wav、evidence/audio-mix.json   mix_audio.py 的产物
  jianying.json（可选）       draft_name、shots（镜头 id → 片段名）、cover（{"image": 路径} 或 {"at": 秒}）、
                              subtitle_fixes（配音稿为读音改写的字 → 字幕写法，按顺序替换）、sub_width（字幕字宽上限，默认 17）
  evidence/vo-clauses.json（可选）配音分句；没有就现算（标点切分、按字数估起点、吸附到实测停顿）并存进去

还原方法：
  纯配乐 = music.gain × (bed − k × 人声) × 音效避让包络 × 首尾淡变 × 母带增益曲线。k 是 bed.py 的整体缩放，bed 峰值没到 0.89 就是 1。
  母带增益曲线 = master 与（music-ducked + sfx-stem）的 1 秒滑窗能量比：线性归一时是常数，动态归一时随时间变化。
  旁白片段音量 = music.gain × k × 该时段的曲线均值；音效片段音量 = cue.gain × 该时段的曲线均值。
  单声道素材按成片的升声道方式转双声道：人声满幅复制（同 bed.py），音效每声道 ×0.7071（同 mix_audio 的 aformat）。
  模拟整条混音，超过 -1.5 dBFS 的地方只压当时贡献最大的音效（相当于母带限幅器），单个音效最多压 12 dB。
  原片在音效处还把人声压低 2~3 dB，草稿里人声保持原样，所以整体会比成片响 0.1~0.5 dB。
"""
import argparse
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
import soundfile as sf

sys.path.insert(0, str(Path(__file__).resolve().parent))
import jianying_draft as core  # noqa: E402

R = 48000
SEC = core.SEC
FFMPEG_UPMIX = 0.5 ** 0.5        # ffmpeg aformat 单声道→双声道的默认声道增益（实测 0.7071）
BREAK = tuple('，。；：！？')        # 短语的收尾标点；顿号不算，并列项先粘在一起
STRONG = tuple('。？！；…')        # 以这些结尾的短语不和下一个合并（冒号后面常紧跟引语，允许合并）
GUIZANG_MIX = Path.home() / '.claude/skills/guizang-product-video-skill/scripts/mix_audio.py'


class ProjectError(Exception):
    pass


def need(path, why):
    if not path.exists():
        raise ProjectError(f'缺少 {path}（{why}）。这个工程不是标准的 guizang 起步工程产物，按 references/timeline.md 自己组织 timeline.json。')
    return path


def find_video(base, given):
    if given:
        return need(Path(given).expanduser().resolve(), '--video 指定的成片')
    if (base / 'renders/final.mp4').exists():
        return base / 'renders/final.mp4'
    mp4s = sorted((base / 'renders').glob('*.mp4'))
    if len(mp4s) == 1:
        return mp4s[0]
    raise ProjectError(f'找不到成片：renders/ 下有 {len(mp4s)} 个 mp4，用 --video 指定。')


def read_stereo(path, N):
    x, sr = sf.read(str(path), always_2d=True)
    if sr != R:
        raise ProjectError(f'{path.name} 采样率 {sr}，应为 {R}')
    if x.shape[1] == 1:
        x = np.repeat(x, 2, axis=1)
    return x[:N] if len(x) >= N else np.pad(x, ((0, N - len(x)), (0, 0)))


def to_stereo(src, dst, gain):
    """素材一律写成双声道，按成片的升声道方式定电平，剪映怎么处理单声道都不影响结果。"""
    x, sr = sf.read(str(src), always_2d=True)
    if sr != R:
        raise ProjectError(f'{src.name} 采样率 {sr}，应为 {R}')
    if x.shape[1] == 1:
        x = np.repeat(x * gain, 2, axis=1)
    sf.write(str(dst), x, R, subtype='PCM_24')


def shot_names(plan, cfg):
    names = cfg.get('shots', {})
    out = {}
    for s in plan['shots']:
        # 文件名里不能有 / 和 :，换成全角保留原意；其余标点和空白去掉，太长的截到 12 个字
        head = (s.get('headline') or '').replace('/', '／').replace(':', '：')
        head = re.sub(r'[\\*?"<>|，。、；！？“”‘’（）()·\s]+', '', head)[:12]
        out[s['id']] = names.get(s['id']) or head or s['id']
    return out


def cut_shots(plan, video, out_dir, names):
    """一次解码，按帧号把纯画面切成每镜一个文件（trim 按帧计，不受浮点时间取整影响）。"""
    fps, shots = plan['fps'], plan['shots']
    parts, maps, files = [f'[0:v]split={len(shots)}' + ''.join(f'[s{i}]' for i in range(len(shots)))], [], []
    for i, s in enumerate(shots):
        a, b = round(s['start'] * fps), round(s['end'] * fps)
        parts.append(f'[s{i}]trim=start_frame={a}:end_frame={b},setpts=PTS-STARTPTS[o{i}]')
        f = out_dir / f'{i:02d}-{names[s["id"]]}.mp4'
        maps += ['-map', f'[o{i}]', '-c:v', 'libx264', '-preset', 'slow', '-crf', '12', '-pix_fmt', 'yuvj420p',
                 '-r', str(fps), '-movflags', '+faststart', str(f)]
        files.append((a, b - a, f))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(video), '-filter_complex', ';'.join(parts), *maps], check=True)
    for a, n, f in files:
        got = int(subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-count_frames',
                                           '-show_entries', 'stream=nb_read_frames', '-of', 'csv=p=0', str(f)],
                                          text=True).strip().split(',')[0])
        if got != n:
            raise ProjectError(f'{f.name}：切出 {got} 帧，应为 {n}')
    return files


def duck_windows(base, plan):
    """成片混音实际用的音效避让窗口：优先读 evidence/audio-mix.json 的记录，没有再用 guizang 的 mix_audio 现算。"""
    rec = json.load(open(need(base / 'evidence/audio-mix.json', 'mix_audio 的混音报告'), encoding='utf-8'))
    windows = rec.get('ducking', {}).get('windows')
    if windows is not None:
        return windows
    spec = importlib.util.spec_from_file_location('mix_audio', GUIZANG_MIX)
    mix = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mix)
    return mix.duck_windows(plan['audio'], plan['audio']['cues'], plan['duration'])


def master_curve(base, N):
    """成片母带的逐时增益：master 与归一前混音（music-ducked + sfx-stem）的 1 秒滑窗能量比，静音处插值。"""
    md = read_stereo(need(base / 'assets/music-ducked.wav', 'mix_audio 输出'), N)
    sx = read_stereo(need(base / 'assets/sfx-stem.wav', 'mix_audio 输出'), N)
    ms = read_stereo(need(base / 'assets/master.wav', '成片母带'), N)
    raw = md + sx
    hop, win = int(0.05 * R), R
    e_raw = np.convolve((raw ** 2).sum(1), np.ones(win), 'same')[::hop]
    e_ms = np.convolve((ms ** 2).sum(1), np.ones(win), 'same')[::hop]
    g = np.sqrt(e_ms / np.maximum(e_raw, 1e-12))
    ok = e_raw / win > 10 ** (-60 / 10)
    g = np.interp(np.arange(N), (np.arange(len(g)) * hop)[ok], g[ok])
    return np.clip(g, 0.3, 2.0), ms


def music_track(base, plan, vo_files, curve, out_file):
    """纯配乐 = gain ×（bed − k × 人声）× 音效避让 × 首尾淡变 × 母带曲线，并校验人声轨、避让包络都能复现成片。"""
    N = int(plan['duration'] * R)
    t = np.arange(N) / R
    gain = plan['audio']['music'].get('gain', 1.0)
    bed = read_stereo(need(base / plan['audio']['music']['file'], 'plan.audio.music'), N)
    starts = plan.get('voice', {}).get('starts', [])
    vo_err, k = 0.0, 1.0
    vo_stem = np.zeros((N, 2))
    if starts:
        vo_stem = read_stereo(need(base / 'assets/vo-stem.wav', 'bed.py 输出的人声轨'), N)
        vo = np.zeros(N)
        for f, t0 in zip(vo_files, starts):
            x, _ = sf.read(str(f))
            x = x if x.ndim == 1 else x.mean(1)
            a = int(t0 * R)
            n = min(len(x), N - a)
            vo[a:a + n] += x[:n]
        vo_err = float(np.abs(vo_stem[:, 0] - vo).max())
        if vo_err > 1e-3:
            raise ProjectError(f'逐句配音按 voice.starts 摆放后与 vo-stem.wav 不一致（误差 {vo_err:.2e}）')
        # bed.py 峰值超过 0.89 时会把配乐和人声一起缩放；没到 0.89 就没缩放。缩放过时用最小二乘估 k（音乐与人声不相关，偏差可忽略）
        if np.abs(bed).max() >= 0.8899:
            k = float((bed * vo_stem).sum() / (vo_stem * vo_stem).sum())
    tb = (np.arange(N) // 240) * 240 / R     # mix_audio 用 volume eval=frame + asetnsamples=240
    env = np.ones(N)
    for w in duck_windows(base, plan):
        a, b, c, d = w['start'], w['attackEnd'], w['holdEnd'], w['end']
        g = 10 ** (-w['db'] / 20)
        x = np.ones(N)
        if b > a:
            x = np.where((tb >= a) & (tb < b), 1 - (1 - g) * (tb - a) / (b - a), x)
        x = np.where((tb >= b) & (tb < c), g, x)
        if d > c:
            x = np.where((tb >= c) & (tb < d), g + (1 - g) * (tb - c) / (d - c), x)
        env = np.minimum(env, x)
    env = env * np.minimum(np.minimum(1, t / 0.025), np.clip((plan['duration'] - t) / 0.5, 0, 1))
    ref = read_stereo(base / 'assets/music-ducked.wav', N)
    env_err = float(np.abs(gain * bed * env[:, None] - ref).max())
    if env_err > 2e-3:
        raise ProjectError(f'音效避让包络复现不出 music-ducked.wav（误差 {env_err:.2e}），混音链路和 guizang 起步工程不同')
    sf.write(str(out_file), gain * (bed - k * vo_stem) * (env * curve)[:, None], R, subtype='PCM_24')
    return gain, k, vo_err, env_err


def cap_peaks(placements, N, limit_db=-1.5):
    """模拟剪映的混音（各片段 × 音量叠加），超过上限的地方只压当时贡献最大的音效，相当于母带限幅器做的事。"""
    cache, parts = {}, []
    for pl in placements:
        if pl['file'] not in cache:
            cache[pl['file']] = sf.read(str(pl['file']), always_2d=True)[0]
        x = cache[pl['file']]
        a = round(pl['start_us'] / SEC * R)
        n = min(round(pl['dur_us'] / SEC * R), len(x), N - a)
        parts.append((a, n, x[:n]))
    total = np.zeros((N, 2))
    for pl, (a, n, x) in zip(placements, parts):
        total[a:a + n] += x * pl['volume']
    T = 10 ** (limit_db / 20)
    sfx = [j for j, pl in enumerate(placements) if pl['kind'] == 'sfx']
    cut = {}
    for _ in range(1000):
        peaks = np.abs(total).max(axis=1)
        i = int(peaks.argmax())
        if peaks[i] <= T:
            break
        ch = int(np.abs(total[i]).argmax())
        cover = [j for j in sfx if parts[j][0] <= i < parts[j][0] + parts[j][1]]
        if not cover:
            break                              # 人声 / 配乐自己超限的不在这里处理
        j = max(cover, key=lambda j: abs(parts[j][2][i - parts[j][0], ch] * placements[j]['volume']))
        a, n, x = parts[j]
        pl = placements[j]
        c = x[i - a, ch] * pl['volume']
        k = (np.sign(total[i, ch]) * T * 0.999 - (total[i, ch] - c)) / c if c else 1.0
        k = min(max(k, 0.9), 0.999)            # 每次最多压 0.9 dB，逐步逼近
        if cut.get(pl['label'], 1.0) * k < 0.25:
            k = 0.25 / cut.get(pl['label'], 1.0)
            if k >= 0.999:
                break
        total[a:a + n] += x * pl['volume'] * (k - 1)
        pl['volume'] *= k
        cut[pl['label']] = cut.get(pl['label'], 1.0) * k
    return total, [(label, round(20 * np.log10(v), 2)) for label, v in cut.items()]


def pauses(f):
    out = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', str(f), '-af', 'silencedetect=noise=-38dB:d=0.12',
                          '-f', 'null', '-'], capture_output=True, text=True).stderr
    return [float(x) for x in re.findall(r'silence_end: ([0-9.]+)', out)]


def clause_timings(base):
    """每句配音的分句起点（相对句首）：有 evidence/vo-clauses.json 就用，没有就现算并存进去。"""
    path = base / 'evidence/vo-clauses.json'
    if path.exists():
        return json.load(open(path, encoding='utf-8'))
    lines = json.load(open(need(base / 'scripts/vo-lines.json', '配音稿'), encoding='utf-8'))
    durs = json.load(open(need(base / 'assets/vo/durations.json', '配音时长'), encoding='utf-8'))['lines']
    weight = lambda s: len(re.sub(r'[，。；：、！？\s]', '', re.sub(r'[A-Za-z]+', 'XX', s)))  # 英文词按两个字估
    res = []
    for i, line in enumerate(lines):
        text = line if isinstance(line, str) else line['text']
        d, ps = durs[i]['dur'], pauses(base / durs[i]['file'])
        segs = [s for s in re.split(r'(?<=[，。；：、！？])', text) if s.strip()]
        total, acc, out = sum(weight(s) for s in segs), 0, []
        for s in segs:
            est = acc / total * d
            snap = min(ps, key=lambda p: abs(p - est)) if ps else est
            out.append({'start': round(snap if acc and abs(snap - est) <= 0.6 else est, 2), 'text': s})
            acc += weight(s)
        res.append({'line': i + 1, 'dur': d, 'clauses': out})
    path.parent.mkdir(exist_ok=True)
    json.dump(res, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'已按停顿现算配音分句并存到 {path}', file=sys.stderr)
    return res


def sub_width(s):
    return sum(0.5 if c.isascii() and (c.isalnum() or c == ' ') else 1 for c in s)


def sub_clean(s):
    return s.strip().rstrip('，。；、：,.;:').replace('，', ' ').strip()


def phrases(clauses, limit):
    """分句（按含顿号的标点切开）→ 短语：以逗号句号等收尾；超过字宽上限的短语再按顿号拆成大致等宽的几段。"""
    joined = lambda cs: ''.join(c['text'] for c in cs)
    groups, cur = [], []
    for c in clauses:
        cur.append(c)
        if c['text'].rstrip().endswith(BREAK):
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    out = []
    for grp in groups:
        width = sub_width(sub_clean(joined(grp)))
        if width <= limit:
            out.append((grp[0]['start'], joined(grp)))
            continue
        target = width / -(-width // limit)
        part = []
        for c in grp:
            wider = sub_width(sub_clean(joined(part) + c['text'])) if part else 0
            if part and (wider > limit or (sub_width(sub_clean(joined(part))) >= target * 0.8 and wider > target)):
                out.append((part[0]['start'], joined(part)))
                part = []
            part.append(c)
        out.append((part[0]['start'], joined(part)))
    return out


def subtitles(base, plan, cfg):
    """配音分句 → 字幕条（帧号）：短语放得下就合并，句末标点去掉、句内逗号换成空格。"""
    fps, limit = plan['fps'], cfg.get('sub_width', 17)
    items, last = [], 0
    for line, t0 in zip(clause_timings(base), plan['voice']['starts']):
        clauses = []
        for c in line['clauses']:
            text = c['text'].strip()
            for k, v in cfg.get('subtitle_fixes', {}).items():
                text = text.replace(k, v)
            clauses.append({'start': c['start'], 'text': text})
        chunks = []
        for start, text in phrases(clauses, limit):
            if chunks and not chunks[-1][1].endswith(STRONG) and sub_width(sub_clean(chunks[-1][1] + text)) <= limit:
                chunks[-1][1] += text
            else:
                chunks.append([start, text])
        for j, (s, text) in enumerate(chunks):
            end = chunks[j + 1][0] if j + 1 < len(chunks) else line['dur']
            fa = max(round((t0 + s) * fps), last)
            fb = max(round((t0 + end) * fps), fa + 1)
            items.append((fa, fb, sub_clean(text)))
            last = fb
    return items


def video_psnr(files, video):
    """把切好的镜头按顺序拼回去，与成片逐帧比 PSNR：切点错一帧，最低值会掉到二十几 dB。"""
    with tempfile.TemporaryDirectory() as tmp:
        lst = Path(tmp) / 'concat.txt'
        lst.write_text(''.join(f"file '{f}'\n" for f in files), encoding='utf-8')
        out = subprocess.run(['ffmpeg', '-v', 'info', '-f', 'concat', '-safe', '0', '-i', str(lst), '-i', str(video),
                              '-lavfi', '[0:v][1:v]psnr', '-f', 'null', '-'], capture_output=True, text=True).stderr
    m = re.search(r'average:([0-9.]+|inf) min:([0-9.]+|inf)', out)
    return {'average': m.group(1), 'min': m.group(2)} if m else out[-300:]


def build(base, video, root, force, portable):
    import pyJianYingDraft as jy
    plan = json.load(open(need(base / 'plan.json', '分镜与音频计划'), encoding='utf-8'))
    cfg = json.load(open(base / 'jianying.json', encoding='utf-8')) if (base / 'jianying.json').exists() else {}
    fps, N = plan['fps'], int(plan['duration'] * R)
    total_frames = round(plan['duration'] * fps)
    starts = plan.get('voice', {}).get('starts', [])
    vo_src = [need(base / f'assets/vo/norm/v{i + 1:02d}.wav', '逐句配音') for i in range(len(starts))]
    curve, master = master_curve(base, N)
    seg_gain = lambda a, n: float(curve[round(core.fus(a, fps) / SEC * R):round(core.fus(a + n, fps) / SEC * R)].mean())

    with tempfile.TemporaryDirectory(prefix='jianying-draft-') as tmp:
        stage = Path(tmp)
        for sub in ('画面', '配乐', '旁白', '音效'):
            (stage / sub).mkdir()
        shots = cut_shots(plan, video, stage / '画面', shot_names(plan, cfg))
        vo_files = []
        for i, f in enumerate(vo_src):
            dst = stage / '旁白' / f'旁白{i + 1:02d}.wav'
            to_stereo(f, dst, 1.0)
            vo_files.append(dst)
        bed_file = stage / '配乐' / '配乐-已避让.wav'
        gain, k, vo_err, env_err = music_track(base, plan, vo_src, curve, bed_file)
        for f in sorted({c['file'] for c in plan['audio']['cues']}):
            to_stereo(need(base / f, 'audio.cues 里的音效'), stage / '音效' / Path(f).name, FFMPEG_UPMIX)

        # 声音片段先按帧排好、模拟混音压峰，再交给核心写草稿
        dur_us = lambda f: jy.AudioMaterial(str(f)).duration
        placements = [{'kind': 'music', 'file': bed_file, 'frame': 0,
                       'frames': min(core.frames_in(dur_us(bed_file), fps), total_frames), 'volume': 1.0, 'label': '配乐'}]
        for i, (f, t0) in enumerate(zip(vo_files, starts)):
            a = round(t0 * fps)
            n = core.frames_in(dur_us(f), fps)
            placements.append({'kind': 'vo', 'file': f, 'frame': a, 'frames': n,
                               'volume': gain * k * seg_gain(a, n), 'label': f'旁白{i + 1:02d}'})
        sfx_dur = {}
        for c in sorted(plan['audio']['cues'], key=lambda c: c['at']):
            f = stage / '音效' / Path(c['file']).name
            sfx_dur.setdefault(f, dur_us(f))
            a = round(c['at'] * fps)        # 取到最近的帧，与成片偏差不超过半帧（17 ms）
            n = min(core.frames_in(sfx_dur[f], fps), total_frames - a)
            placements.append({'kind': 'sfx', 'file': f, 'frame': a, 'frames': n,
                               'volume': c.get('gain', 1) * seg_gain(a, n), 'label': c['actionId']})
        for pl in placements:
            pl['start_us'] = core.fus(pl['frame'], fps)
            pl['dur_us'] = core.fus(pl['frame'] + pl['frames'], fps) - pl['start_us']
        remix, capped = cap_peaks(placements, N)

        clip = lambda pl: {'file': str(pl['file']), 'start': pl['frame'] / fps, 'duration': pl['frames'] / fps,
                           'volume': pl['volume']}
        tracks = [
            {'type': 'video', 'name': '画面', 'clips': [{'file': str(f), 'start': a / fps, 'duration': n / fps}
                                                       for a, n, f in shots]},
            {'type': 'audio', 'name': '配乐', 'clips': [clip(p) for p in placements if p['kind'] == 'music']},
        ]
        if starts:
            tracks.append({'type': 'audio', 'name': '旁白', 'clips': [clip(p) for p in placements if p['kind'] == 'vo']})
        tracks.append({'type': 'audio', 'name': '音效', 'split_overlaps': True,
                       'clips': [clip(p) for p in placements if p['kind'] == 'sfx']})
        subs = subtitles(base, plan, cfg) if starts else []
        if subs:
            tracks.append({'type': 'text', 'name': '字幕', 'hidden': True, 'srt': '字幕.srt',
                           'clips': [{'text': t, 'start': a / fps, 'duration': (b - a) / fps} for a, b, t in subs]})
        cover = cfg.get('cover')
        if cover and 'image' in cover:
            cover = {'image': str(base / cover['image'])}
        elif cover and 'at' in cover:
            cover = {'video': str(video), 'at': cover['at']}
        elif (base / 'covers/cover-16x9.png').exists():
            cover = {'image': str(base / 'covers/cover-16x9.png')}
        else:
            cover = {'video': str(video), 'at': max(0.0, plan['shots'][0]['end'] - 0.5)}
        timeline = {'name': cfg.get('draft_name') or base.name, 'width': plan.get('width', 1920),
                    'height': plan.get('height', 1080), 'fps': fps, 'cover': cover, 'tracks': tracks}
        if (base / 'assets/music.wav').exists():
            timeline['extra_files'] = [{'file': str(base / 'assets/music.wav'), 'to': '配乐/配乐-原始.wav'}]
        result = core.write_draft(timeline, root, force, portable)
        shot_paths = [result['paths'][str(Path(f).resolve())] for _, _, f in shots]

    rms = lambda x: 20 * np.log10(np.sqrt((x ** 2).mean()) + 1e-12)
    edges = np.linspace(0, plan['duration'], 6).round(1)
    result.pop('paths')
    result.update({
        'mix': {'music_gain': gain, 'bed_scale_k': round(k, 4), 'vo_stem_error': vo_err, 'duck_envelope_error': env_err,
                'master_curve_db': {f'{s}s': round(20 * np.log10(curve[min(N - 1, int(s * R))]), 2) for s in (0, 10, 60)}},
        'peak_capped_db': capped,
        'remix_vs_master': {
            'peak_dbfs': round(20 * np.log10(np.abs(remix).max()), 2),
            'corr': round(float(np.corrcoef(remix.ravel(), master.ravel())[0, 1]), 4),
            'region_rms_diff_db': {f'{a}-{b}s': round(rms(remix[int(a * R):int(b * R)]) - rms(master[int(a * R):int(b * R)]), 2)
                                   for a, b in zip(edges, edges[1:])}},
        'subtitles': len(subs),
        'video_psnr_db': video_psnr(shot_paths, video),
    })
    return result


def main():
    ap = argparse.ArgumentParser(description='guizang 宣传片工程 → 剪映专业版草稿')
    ap.add_argument('project', help='工程目录（含 plan.json）')
    ap.add_argument('--video', help='成片路径，默认 renders/final.mp4')
    ap.add_argument('--root', default=str(core.DEFAULT_ROOT), help='草稿目录，测试时可指到临时目录')
    ap.add_argument('--force', action='store_true', help='覆盖在剪映里打开 / 编辑过的草稿')
    ap.add_argument('--portable', action='store_true', help='素材路径写成草稿目录占位符（实验，尚未在剪映里实测）')
    args = ap.parse_args()
    base = Path(args.project).expanduser().resolve()
    try:
        result = build(base, find_video(base, args.video), args.root, args.force, args.portable)
    except (ProjectError, core.DraftError) as e:
        sys.exit(str(e))
    print(json.dumps(result, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
