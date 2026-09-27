# /// script
# requires-python = ">=3.11"
# dependencies = ["pyJianYingDraft==0.3.0"]
# ///
"""timeline.json → 剪映专业版可编辑草稿（剪映专业版 Mac 10.5 实测）。

用法：uv run jianying_draft.py timeline.json [--root 草稿目录] [--force] [--portable]
也可以 import 后调用 write_draft(timeline, root, force, portable)。

timeline.json 的规格见 ../references/timeline.md，剪映草稿的格式规律见 ../references/format.md。要点：
- 写明文草稿：Mac 读 draft_info.json，另留一份 draft_content.json（剪映 6 起自己保存的是加密的，但读得了明文）。
- 所有片段边界取整到帧：剪映会把边界吸附到帧，不在帧上的相邻片段可能重叠一帧，被它挪进新轨道。
- 素材拷进草稿文件夹的「素材/<轨道名>/」：沙盒里的剪映只能读 ~/Movies 这类授权目录。
- 轨道 attribute 是位掩码：1 静音、2 隐藏、4 锁定（pyJianYingDraft 只会写静音位，其余位这里补）。
- 草稿在剪映里打开过（draft_info.json 与上次生成的不一致）或正开着时拒绝覆盖，确认覆盖加 --force。
- 剪映发现新草稿文件夹会自己登记一个 ID（root_meta_info.json），元信息沿用它；还没登记时用 uuid5。
"""
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import time
import uuid
from pathlib import Path

import pyJianYingDraft as jy

DEFAULT_ROOT = Path.home() / 'Movies/JianyingPro/User Data/Projects/com.lveditor.draft'
SEC = 1_000_000
GUARD = '.jianying-draft-generated'          # 上次生成的 draft_info.json 的 sha256
LEGACY_GUARDS = ('.chatpage-generated',)     # 技能化之前各工程脚本写的标记，一样认
ATTR = {'mute': 1, 'hidden': 2, 'locked': 4}
# 剪映程序里的草稿目录占位符（二进制里搜到 26 处）。素材路径改用它理论上改名 / 搬家不断链，尚未在剪映里实测
PLACEHOLDER = '##_draftpath_placeholder_0E685133-18CE-45ED-8CB8-2904A212EC80_##'
KEEP = {'draft_content.json', 'draft_info.json', 'draft_meta_info.json', 'draft_cover.jpg', '素材', '.backup',
        GUARD, *LEGACY_GUARDS}
TRACK_TYPES = {'video': jy.TrackType.video, 'audio': jy.TrackType.audio, 'text': jy.TrackType.text}


class DraftError(Exception):
    pass


def fus(frame, fps):
    """第 frame 帧起点的微秒数；片段一律用 [fus(a), fus(b)) 表示，相邻片段首尾严格相接。"""
    return round(frame * SEC / fps)


def frames_in(dur_us, fps):
    """素材时长能容纳的整帧数（向下取整）。"""
    return dur_us * fps // SEC


def check_guard(draft, force):
    if force or not draft.exists():
        return
    if (draft / '.locked').exists():
        raise DraftError(f'{draft.name} 正在剪映里打开，先在剪映里关掉这个草稿再生成（确认要覆盖加 --force）。')
    info = draft / 'draft_info.json'
    if not info.exists():
        return
    marks = [draft / g for g in (GUARD, *LEGACY_GUARDS) if (draft / g).exists()]
    digest = hashlib.sha256(info.read_bytes()).hexdigest()
    if not any(m.read_text().strip() == digest for m in marks):
        raise DraftError(f'{draft.name} 在剪映里打开或编辑过（或不是本技能生成的），重新生成会覆盖这些改动。'
                         '确认覆盖加 --force，或换一个草稿名。')


def clean_draft(draft, extra_keep=()):
    """原地覆盖：剪映在监听草稿目录，整个删掉再建会被当成另一个草稿。它打开过留下的状态文件（多数加密）一并清掉，.backup 保留。"""
    draft.mkdir(parents=True, exist_ok=True)
    keep = KEEP | set(extra_keep)
    for old in draft.iterdir():
        if old.name not in keep:
            shutil.rmtree(old) if old.is_dir() else old.unlink()
    shutil.rmtree(draft / '素材', ignore_errors=True)


def copy_materials(timeline, draft):
    """每条轨道的素材拷进 素材/<轨道名>/，同一个源文件只拷一次，重名时加序号。返回 源路径 → 草稿内路径。"""
    mapping, used = {}, set()
    for track in timeline['tracks']:
        if track['type'] == 'text':
            continue
        folder = draft / '素材' / track.get('folder', track['name'])
        folder.mkdir(parents=True, exist_ok=True)
        for clip in track['clips']:
            src = str(Path(clip['file']).expanduser().resolve())
            if src in mapping:
                continue
            if not Path(src).is_file():
                raise DraftError(f'素材不存在：{src}')
            dst, n = folder / Path(src).name, 1
            while str(dst) in used:
                dst = folder / f'{Path(src).stem}-{n}{Path(src).suffix}'
                n += 1
            shutil.copy2(src, dst)
            used.add(str(dst))
            mapping[src] = dst
    for extra in timeline.get('extra_files', []):
        dst = draft / '素材' / extra['to']
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(Path(extra['file']).expanduser(), dst)
    return mapping


def split_overlaps(clips, fps):
    """同一条轨道上片段不能重叠：按起点排好，放进第一条放得下的子轨道（边界按帧比较）。"""
    lanes, ends = [], []
    for clip in sorted(clips, key=lambda c: c['start']):
        a = round(clip['start'] * fps)
        k = next((i for i, e in enumerate(ends) if e <= a), None)
        if k is None:
            lanes.append([])
            ends.append(0)
            k = len(lanes) - 1
        lanes[k].append(clip)
        ends[k] = round((clip['start'] + clip['duration']) * fps)
    return lanes


def srt_time(x):
    ms = int(round(x * 1000))
    return f'{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}'


def build(timeline, mapping, draft):
    fps = timeline.get('fps', 30)
    script = jy.ScriptFile(timeline.get('width', 1920), timeline.get('height', 1080), fps, True)  # 主轨磁吸，同剪映默认
    counts, flags, mats = {}, {}, {}

    def span(clip):
        a = round(clip['start'] * fps)
        b = round((clip['start'] + clip['duration']) * fps)
        if b <= a:
            b = a + 1
        return a, b

    for track in timeline['tracks']:
        kind = track['type']
        lanes = split_overlaps(track['clips'], fps) if track.get('split_overlaps') else [track['clips']]
        for li, lane in enumerate(lanes):
            name = track['name'] if len(lanes) == 1 and not track.get('split_overlaps') else f"{track['name']} {li + 1}"
            ref = script.append_track(jy.TrackSpec(TRACK_TYPES[kind], name))
            flags[name] = sum(v for k, v in ATTR.items() if track.get(k))
            counts[name] = len(lane)
            last = -1
            for clip in sorted(lane, key=lambda c: c['start']):
                a, b = span(clip)
                if kind == 'text':
                    a = max(a, last)
                    b = max(b, a + 1)
                    st = track.get('style', {})
                    border = st.get('border', {'color': [0, 0, 0], 'width': 40})
                    seg = jy.TextSegment(
                        clip['text'], jy.trange(fus(a, fps), fus(b, fps) - fus(a, fps)),
                        style=jy.TextStyle(size=st.get('size', 7.0), color=tuple(st.get('color', (1.0, 1.0, 1.0))),
                                           align=st.get('align', 1), auto_wrapping=True,
                                           max_line_width=st.get('max_line_width', 0.82)),
                        border=jy.TextBorder(color=tuple(border['color']), width=border['width']) if border else None,
                        clip_settings=jy.ClipSettings(transform_y=st.get('y', -0.82)))
                    last = b
                else:
                    dst = mapping[str(Path(clip['file']).expanduser().resolve())]
                    if str(dst) not in mats:
                        mats[str(dst)] = (jy.VideoMaterial if kind == 'video' else jy.AudioMaterial)(str(dst))
                    mat = mats[str(dst)]
                    sa = round(clip.get('source_start', 0) * fps)
                    n = min(b - a, frames_in(mat.duration, fps) - sa)
                    if n <= 0:
                        raise DraftError(f'{dst.name}：截取范围超出素材时长')
                    if b - a - n > 1:
                        print(f'注意：{dst.name} 比时间线上要的短 {(b - a - n) / fps:.2f} 秒，已按素材长度截短', file=sys.stderr)
                    target = jy.trange(fus(a, fps), fus(a + n, fps) - fus(a, fps))
                    source = jy.trange(fus(sa, fps), fus(sa + n, fps) - fus(sa, fps))
                    cls = jy.VideoSegment if kind == 'video' else jy.AudioSegment
                    seg = cls(mat, target, source_timerange=source, volume=clip.get('volume', 1.0))
                script.add_segment(seg, ref)
            if kind == 'text' and track.get('srt'):
                with open(draft / track['srt'], 'w', encoding='utf-8') as fp:
                    for i, clip in enumerate(sorted(lane, key=lambda c: c['start']), 1):
                        a, b = span(clip)
                        fp.write(f"{i}\n{srt_time(a / fps)} --> {srt_time(b / fps)}\n{clip['text']}\n\n")
    return script, counts, flags


def registered_id(root, draft):
    try:
        store = json.load(open(root / 'root_meta_info.json', encoding='utf-8'))['all_draft_store']
    except (OSError, ValueError, KeyError):
        return None
    return next((e['draft_id'] for e in store if e.get('draft_fold_path') == str(draft)), None)


def write_cover(cover, draft):
    out = draft / 'draft_cover.jpg'
    if not cover:
        return
    if 'image' in cover:
        src = str(Path(cover['image']).expanduser())
        if shutil.which('sips'):
            subprocess.run(['sips', '-s', 'format', 'jpeg', '-Z', '640', src, '--out', str(out)], check=True,
                           capture_output=True)
        else:
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-vf', 'scale=640:-2', str(out)], check=True)
    else:
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(cover['at']), '-i', str(Path(cover['video']).expanduser()),
                        '-frames:v', '1', '-vf', 'scale=640:-2', '-q:v', '3', str(out)], check=True)


def write_draft(timeline, root=DEFAULT_ROOT, force=False, portable=False):
    root = Path(root).expanduser()
    draft = root / timeline['name']
    check_guard(draft, force)
    clean_draft(draft, extra_keep=[t['srt'] for t in timeline['tracks'] if t.get('srt')])
    mapping = copy_materials(timeline, draft)
    script, counts, flags = build(timeline, mapping, draft)

    content = json.loads(script.dumps())
    for t in content['tracks']:
        if flags.get(t.get('name')):
            t['attribute'] = flags[t['name']]
    if portable:
        prefix = str(draft)
        for group in ('videos', 'audios'):
            for m in content['materials'].get(group, []):
                if m.get('path', '').startswith(prefix):
                    m['path'] = PLACEHOLDER + m['path'][len(prefix):]
    text = json.dumps(content, ensure_ascii=False)
    for name in ('draft_content.json', 'draft_info.json'):
        (draft / name).write_text(text, encoding='utf-8')
    (draft / GUARD).write_text(hashlib.sha256(text.encode('utf-8')).hexdigest())
    for legacy in LEGACY_GUARDS:
        (draft / legacy).unlink(missing_ok=True)
    write_cover(timeline.get('cover'), draft)

    meta_path = draft / 'draft_meta_info.json'
    # 每次从模板重写：剪映保存过的元信息是加密的读不了；素材库等字段剪映打开时会自己补
    shutil.copy(jy.assets.get_asset_path('DRAFT_META_TEMPLATE'), meta_path)
    meta = json.load(open(meta_path, encoding='utf-8'))
    now = int(time.time() * SEC)
    reg = registered_id(root, draft)
    meta.update(draft_fold_path=str(draft), draft_root_path=str(root), draft_name=timeline['name'],
                draft_id=reg or str(uuid.uuid5(uuid.NAMESPACE_URL, str(draft))).upper(),
                draft_cover=str(draft / 'draft_cover.jpg') if timeline.get('cover') else '',
                tm_draft_create=now, tm_draft_modified=now, tm_duration=script.duration)
    json.dump(meta, open(meta_path, 'w', encoding='utf-8'), ensure_ascii=False)
    return {'draft': str(draft), 'duration_s': script.duration / SEC, 'tracks': counts,
            'registered_by_jianying': bool(reg), 'portable_paths': portable,
            'paths': {str(k): str(v) for k, v in mapping.items()}}


def main():
    ap = argparse.ArgumentParser(description='timeline.json → 剪映专业版草稿')
    ap.add_argument('timeline')
    ap.add_argument('--root', default=str(DEFAULT_ROOT), help='草稿目录，测试时可指到临时目录')
    ap.add_argument('--force', action='store_true', help='覆盖在剪映里打开 / 编辑过的草稿')
    ap.add_argument('--portable', action='store_true', help='素材路径写成草稿目录占位符（实验，尚未在剪映里实测）')
    args = ap.parse_args()
    timeline = json.load(open(args.timeline, encoding='utf-8'))
    try:
        result = write_draft(timeline, args.root, args.force, args.portable)
    except DraftError as e:
        sys.exit(str(e))
    result.pop('paths')
    print(json.dumps(result, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
