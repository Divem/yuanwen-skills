---
name: jianying-draft
description: 把成片或分轨素材生成剪映专业版（Mac）可二次编辑的草稿：画面按镜头切段，配乐 / 旁白 / 音效 / 字幕分轨，音量按成片母带还原，在剪映首页直接打开。用户要把视频「转成剪映草稿 / 剪映工程 / 导进剪映二次编辑」，或排查剪映草稿打不开、素材丢失、草稿不见了时使用。guizang 宣传片工程一条命令导出；其他来源按 timeline.json 规格组织素材。
metadata:
  author: wen.yuan
---

# 剪映草稿

把一支视频变成剪映里能继续剪的工程，而不是一个导进去的 MP4。已在**剪映专业版 Mac 10.5.0** 上实际打开验证；Windows 版剪映和 CapCut 没验证过。

三个脚本，都用 `uv run` 执行，依赖写在脚本头部，不用事先建环境：

| 脚本 | 做什么 |
|---|---|
| `scripts/from_guizang.py` | guizang 宣传片工程 → 草稿：切镜头、还原混音、切字幕、组时间线，再调核心写草稿，最后比对画面和声音 |
| `scripts/jianying_draft.py` | 核心：`timeline.json` → 草稿。剪映格式的坑都集中在这里处理 |
| `scripts/check_draft.py` | 只读诊断：生成来源、剪映有没有打开 / 改名、素材在不在、边界整不整帧，可与成片比画面 |

## 动手前（红线）

1. **剪映常开在后台，不要关它。** 先看哪些草稿正开着：`find "$HOME/Movies/JianyingPro/User Data/Projects/com.lveditor.draft" -maxdepth 2 -name .locked`。
2. **用户在剪映里打开或编辑过的草稿，脚本默认拒绝覆盖。** 要加 `--force` 前先问用户：剪映保存的内容是加密的，覆盖后无法找回。
3. **先生成到临时目录试跑**：`--root /tmp/jy-test`，指标正常再写进剪映的草稿目录。
4. **剪映正在用时不要操作它的界面。** 要在剪映里验证，先确认它停在首页、用户没在用，做法见 `references/verify-in-app.md`。

## guizang 宣传片工程

```bash
uv run ~/.claude/skills/jianying-draft/scripts/from_guizang.py <工程目录> [--video 成片.mp4] [--root 草稿目录] [--force]
```

- **工程约定**：`plan.json`、`renders/*.mp4`、`assets/{bed,vo-stem,music-ducked,sfx-stem,master}.wav`、`assets/vo/norm/vNN.wav`、`evidence/audio-mix.json`，也就是 guizang 起步工程跑完 `bed.py` 和 `mix_audio.py` 后的产物。缺了哪个会直接报出来。
- **可选配置**：工程根目录放一份 `jianying.json`：

| 字段 | 作用 | 默认 |
|---|---|---|
| `draft_name` | 剪映首页显示的草稿名 | 工程目录名 |
| `shots` | 镜头 id → 片段文件名 | 镜头 headline 截 12 个字 |
| `cover` | `{"image": "covers/cover-16x9.png"}` 或 `{"at": 12.8}`（从成片截一帧） | 有 `covers/cover-16x9.png` 就用它，否则取第一个镜头结束前 0.5 秒 |
| `subtitle_fixes` | 配音稿为读音改写的字 → 字幕写法，比如 `{"Chat Page": "ChatPage", "Alt 加 A 键": "Alt+A", "艾特": "@"}` | 不替换 |
| `sub_width` | 一条字幕最多的字宽（汉字 1，字母 / 数字 / 空格 0.5） | 17 |

- **生成的轨道**：画面（主轨，按镜头逐帧切开的无声片段）/ 配乐（人声和音效处的避让已做进文件）/ 旁白（一句一段）/ 音效（重叠的自动分到第二条轨）/ 字幕（**默认隐藏**，点轨道头的眼睛显示；另存一份 `字幕.srt`）。原始配乐拷在 `素材/配乐/配乐-原始.wav`，换曲时用。
- **输出指标怎么看**：

| 字段 | 正常范围 | 不正常说明什么 |
|---|---|---|
| `mix.vo_stem_error` / `mix.duck_envelope_error` | 小于 1e-3 / 2e-3（通常是 1e-7 量级） | 脚本会直接报错：混音链路不是 guizang 的，改用 timeline.json |
| `remix_vs_master.region_rms_diff_db` | 各段在 ±0.5 dB 内，通常偏正 0.1～0.5 | 原片在音效处把人声压低 2～3 dB，草稿里人声没压，所以略响 |
| `remix_vs_master.peak_dbfs` | ≤ -1.5 | 压峰没压住，检查 `peak_capped_db` |
| `remix_vs_master.corr` | 0.88～1.0 | 音效起点对齐到帧（最多偏半帧、17 ms），音效越多越低，不影响听感 |
| `video_psnr_db` | 平均 ≈ 60、最低 > 50 | 最低掉到二十几 dB 说明切点错了一帧 |

还原方法（写在 `from_guizang.py` 头注释里）：纯配乐 = `music.gain × (bed − k × 人声) × 音效避让 × 淡入淡出 × 母带增益曲线`，不需要知道 bed.py 里的配乐系数；母带增益曲线是从 `master.wav` 反推的，线性归一时是常数，动态归一时随时间变化。

## 其他来源

先把素材整理成 `timeline.json`（规格和例子见 `references/timeline.md`），再调用核心：

```bash
uv run ~/.claude/skills/jianying-draft/scripts/jianying_draft.py timeline.json [--root 草稿目录] [--force]
```

核心负责的是剪映格式的部分：写明文 `draft_info.json`、边界取整到帧、素材拷进草稿文件夹、隐藏 / 静音 / 锁定轨道、防覆盖、沿用剪映登记的草稿 ID。音量怎么定、字幕怎么切，由调用方决定。

## 检查与排障

```bash
uv run ~/.claude/skills/jianying-draft/scripts/check_draft.py <草稿名> [--video 成片.mp4]
```

| 现象 | 原因与处理 |
|---|---|
| 新草稿没出现在剪映首页 | 剪映停在编辑界面时不扫描草稿目录，回首页或重启剪映 |
| 按原名找不到草稿 | 用户在剪映里改过名，文件夹跟着改了；`check_draft.py` 会从剪映操作日志里追出新名字 |
| 改名后提示素材丢失 | 素材写的是绝对路径。在剪映里「重新链接」，指到草稿文件夹下的 `素材/`；`--portable` 改用剪映的草稿目录占位符，理论上能根治，但**还没实测**，用之前先在剪映里验证 |
| 字幕看不见 | 字幕轨默认隐藏，点轨道头的眼睛 |
| 同一轨上的片段被挪进新轨道 | 边界没落在整帧上，剪映吸附后重叠了；核心已按帧取整，自己拼 JSON 时注意 |

## 交付时告诉用户

- 能改：剪辑顺序、删减镜头、各轨音量、换配乐、改字幕、加剪映自带的转场和贴纸。改不了：渲染进画面的文字、界面和动画，要回工程改代码、重新渲染、再生成草稿。
- 声音和成片的差别：人声在音效处没有压低，整体略响 0.1～0.5 dB；音效起点最多偏半帧。
- 草稿只在这台电脑上能直接打开，素材是绝对路径，拷到别的电脑要重新链接；在剪映里改名也可能导致同样的问题。
- 生成后草稿在剪映里打开过，再生成就需要 `--force`，而且会冲掉在剪映里做的修改。

## 参考

- `references/format.md`：剪映草稿的格式和行为，都是实测结果（加密、登记、位掩码、帧吸附、沙盒、操作日志、占位符）
- `references/timeline.md`：`timeline.json` 规格
- `references/verify-in-app.md`：在剪映里验证的做法（截屏定位、Quartz 点击、关闭回首页、恢复前台，以及不打开界面也能确认剪映读取成功的办法）
