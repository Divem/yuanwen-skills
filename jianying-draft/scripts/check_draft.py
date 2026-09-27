# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""检查一份剪映草稿的现状：是不是本技能生成的、剪映有没有打开 / 改名、素材在不在、边界是否整帧、哪些轨道隐藏；
可选把画面轨拼起来与成片比 PSNR。只读，不改任何文件。

用法：uv run check_draft.py <草稿名或草稿文件夹> [--root 草稿目录] [--video 成片.mp4]
退出码：没发现问题 0，有问题 1。
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

DEFAULT_ROOT = Path.home() / 'Movies/JianyingPro/User Data/Projects/com.lveditor.draft'
ACTION_LOG = Path.home() / 'Library/Containers/com.lemon.lvpro/Data/Movies/JianyingPro/User Data/Log/draft_acion_watch.json'
GUARDS = ('.jianying-draft-generated', '.chatpage-generated')
PLACEHOLDER = '##_draftpath_placeholder_0E685133-18CE-45ED-8CB8-2904A212EC80_##'
ATTR = {1: '静音', 2: '隐藏', 4: '锁定'}


def load_json(path):
    try:
        return json.load(open(path, encoding='utf-8'))
    except (OSError, ValueError):
        return None


def actions():
    """剪映的草稿操作日志：每行一条 JSON（copy_draft_external / rename_draft / create_draft / delete_draft_external …）。"""
    out = []
    if ACTION_LOG.exists():
        for line in open(ACTION_LOG, encoding='utf-8', errors='replace'):
            try:
                out.append(json.loads(line))
            except ValueError:
                pass
    return out


def find_draft(arg, root):
    p = Path(arg).expanduser()
    if p.is_dir():
        return p.resolve(), []
    draft = root / arg
    if draft.is_dir():
        return draft, []
    # 可能在剪映里改过名：按操作日志找这个名字后来变成了什么
    notes, name = [], arg
    for a in actions():
        old, new = a.get('old_draft_info') or {}, a.get('new_draft_info') or {}
        if a.get('type') == 'rename_draft' and old.get('draft_name') == name:
            notes.append(f"剪映操作日志：{fmt_time(a)} 从「{name}」改名为「{new.get('draft_name')}」")
            name = new.get('draft_name')
    if name != arg and (root / name).is_dir():
        return root / name, notes
    return None, notes


def fmt_time(a):
    return time.strftime('%m-%d %H:%M:%S', time.localtime(a.get('time_nsec', 0) / 1e6))


def main():
    ap = argparse.ArgumentParser(description='检查剪映草稿现状（只读）')
    ap.add_argument('draft', help='草稿名（剪映首页显示的名字）或草稿文件夹路径')
    ap.add_argument('--root', default=str(DEFAULT_ROOT))
    ap.add_argument('--video', help='成片路径：把画面轨按时间线拼接后与它逐帧比 PSNR')
    args = ap.parse_args()
    root = Path(args.root).expanduser()
    draft, notes = find_draft(args.draft, root)
    problems = []
    for n in notes:
        print(n)
    if not draft:
        sys.exit(f'找不到草稿「{args.draft}」（草稿目录 {root}）')
    print(f'草稿文件夹：{draft}')

    # 状态：是不是本技能生成的、剪映有没有保存过、是否正开着、是否登记
    guard = next((draft / g for g in GUARDS if (draft / g).exists()), None)
    info_raw = (draft / 'draft_info.json').read_bytes() if (draft / 'draft_info.json').exists() else b''
    info_plain = load_json(draft / 'draft_info.json')
    if guard is None:
        print('来源：不是本技能生成的草稿（没有生成标记），只检查剪映侧的状态')
    elif hashlib.sha256(info_raw).hexdigest() == guard.read_text().strip():
        print('剪映：还没打开过（draft_info.json 与生成时一致）')
    elif info_plain is None:
        print('剪映：打开并保存过（draft_info.json 已加密，里面的改动读不到；下面的结构检查按生成时的副本 draft_content.json）')
    else:
        print('剪映：打开并升级保存过（draft_info.json 仍是明文）')
    if (draft / '.locked').exists():
        print('剪映：现在正开着这个草稿（有 .locked）')
    reg = load_json(root / 'root_meta_info.json') or {}
    entry = next((e for e in reg.get('all_draft_store', []) if e.get('draft_fold_path') == str(draft)), None)
    if entry:
        print(f"剪映登记：已登记为「{entry.get('draft_name')}」，时长 {entry.get('tm_duration', 0) / 1e6:.1f} 秒")
    else:
        print('剪映登记：还没登记（剪映停在编辑界面时不扫描草稿目录，回首页或重启剪映后会出现）')
    ids = {entry.get('draft_id')} if entry else set()
    for a in actions():
        new, old = a.get('new_draft_info') or {}, a.get('old_draft_info') or {}
        if new.get('draft_id') in ids or new.get('draft_folder_path') == str(draft):
            extra = f"（原名「{old.get('draft_name')}」）" if old else ''
            print(f"剪映操作日志：{fmt_time(a)} {a.get('type')} → 「{new.get('draft_name')}」{extra}")

    # 结构：以明文为准（剪映保存过就只能看生成时的副本）
    content = info_plain or load_json(draft / 'draft_content.json')
    if content is None:
        print('结构：没有可读的明文草稿，跳过结构检查')
        sys.exit(1 if problems else 0)
    fps = content.get('fps', 30)
    F = 1e6 / fps
    mats = {m['id']: m for k in ('videos', 'audios') for m in content['materials'].get(k, [])}
    missing, moved = [], set()
    for m in mats.values():
        p = m.get('path', '')
        real = str(draft) + p[len(PLACEHOLDER):] if p.startswith(PLACEHOLDER) else p
        if not Path(real).exists():
            missing.append(real)
            alt = draft / '素材' / Path(real).parent.name / Path(real).name
            if alt.exists():
                moved.add(str(Path(real).parents[2]))
    placeholder = sum(m.get('path', '').startswith(PLACEHOLDER) for m in mats.values())
    print(f'素材：{len(mats)} 个，缺失 {len(missing)} 个' + (f'，其中 {placeholder} 个用草稿目录占位符' if placeholder else ''))
    if moved:
        problems.append('moved')
        for old in moved:
            print(f'  素材路径指向旧文件夹 {old}，文件还在当前草稿的 素材/ 里（多半是在剪映里改过名）。'
                  f'剪映打开时如果提示素材丢失，用「重新链接」指到 {draft / "素材"} 即可')
    elif missing:
        problems.append('missing')
        for p in missing[:5]:
            print(f'  缺失：{p}')
    off = overl = 0
    for t in content['tracks']:
        segs = sorted(t['segments'], key=lambda s: s['target_timerange']['start'])
        for s in segs:
            a, n = s['target_timerange']['start'] / F, s['target_timerange']['duration'] / F
            off += abs(a - round(a)) > 1e-3 or abs(n - round(n)) > 1e-3
        for x, y in zip(segs, segs[1:]):
            overl += round(x['target_timerange']['start'] / F) + round(x['target_timerange']['duration'] / F) > \
                round(y['target_timerange']['start'] / F)
        flags = '、'.join(v for k, v in ATTR.items() if t.get('attribute', 0) & k)
        print(f"轨道：{t['type']:5} {t.get('name', ''):8} {len(segs):3} 段" + (f'（{flags}）' if flags else ''))
    print(f'时间线：{content["duration"] / 1e6:.2f} 秒，{fps} 帧/秒；不在整帧的边界 {off} 处，吸附到帧后重叠 {overl} 处')
    if off or overl:
        problems.append('frames')

    if args.video:
        vt = next((t for t in content['tracks'] if t['type'] == 'video'), None)
        segs = sorted(vt['segments'], key=lambda s: s['target_timerange']['start']) if vt else []
        contiguous = segs and segs[0]['target_timerange']['start'] == 0 and all(
            x['target_timerange']['start'] + x['target_timerange']['duration'] == y['target_timerange']['start']
            for x, y in zip(segs, segs[1:]))
        if not contiguous:
            print('画面比对：画面轨不是从 0 开始首尾相接的一串片段，跳过')
        else:
            with tempfile.TemporaryDirectory() as tmp:
                lst = Path(tmp) / 'concat.txt'
                lines = []
                for s in segs:
                    p = mats[s['material_id']]['path']
                    p = str(draft) + p[len(PLACEHOLDER):] if p.startswith(PLACEHOLDER) else p
                    lines.append(f"file '{p}'\n")
                lst.write_text(''.join(lines), encoding='utf-8')
                out = subprocess.run(['ffmpeg', '-v', 'info', '-f', 'concat', '-safe', '0', '-i', str(lst),
                                      '-i', str(Path(args.video).expanduser()), '-lavfi', '[0:v][1:v]psnr', '-f', 'null', '-'],
                                     capture_output=True, text=True).stderr
            m = re.search(r'average:([0-9.]+|inf) min:([0-9.]+|inf)', out)
            if m:
                print(f'画面比对：PSNR 平均 {m.group(1)} dB，最低 {m.group(2)} dB（最低低于 35 dB 说明有切点错位）')
                if m.group(2) != 'inf' and float(m.group(2)) < 35:
                    problems.append('psnr')
            else:
                print('画面比对失败：' + out[-300:])
                problems.append('psnr')
    print('结论：' + ('没发现问题' if not problems else '有问题，见上'))
    sys.exit(1 if problems else 0)


if __name__ == '__main__':
    main()
