# jianying-draft

把视频成片或分轨素材生成**剪映专业版可二次编辑的草稿**：画面按镜头切成片段，配乐、旁白、音效、字幕各占一条轨道，音量按成片母带还原，生成后在剪映首页直接打开就能继续剪。作为 Claude Code Skill 使用，说「转成剪映草稿」「导进剪映二次编辑」时触发；排查剪映草稿打不开、素材丢失、草稿不见了也用它。

已在 **剪映专业版 Mac 10.5.0** 上实际打开验证。Windows 版剪映和 CapCut 没有验证过。

## 功能特性

- **宣传片工程一条命令导出**：guizang-product-video-skill 做出来的工程，按分镜逐帧切开画面，从预混音里还原出纯配乐，一句旁白一个片段，音效重叠时自动分轨，字幕按配音实测停顿切分（默认隐藏）。
- **声音按原片还原**：从成片母带反推出响度曲线（线性或动态归一都行），各轨音量照着设；原片限幅器压过的音效峰值单独调低，导出不会爆音。
- **生成后自动校验**：画面拼回去和成片逐帧比 PSNR，声音叠起来和母带比各段响度。
- **通用的时间线格式**：其他来源的视频，把素材整理成一份 `timeline.json` 就能生成草稿，剪映格式的细节由技能处理。
- **防止冲掉你的编辑**：草稿在剪映里打开或改过之后，再生成会被拒绝，确认要覆盖才加 `--force`。
- **只读诊断**：查一份草稿有没有被剪映打开、改没改名（读剪映的操作日志）、素材在不在、时间边界对不对。

## 环境要求

| 依赖 | 说明 |
|:---|:---|
| macOS + 剪映专业版 | 草稿写到 `~/Movies/JianyingPro/User Data/Projects/com.lveditor.draft/` |
| [uv](https://docs.astral.sh/uv/) | 所有脚本用 `uv run` 执行，Python 依赖（pyJianYingDraft 0.3、numpy、soundfile）写在脚本头部，首次运行自动安装 |
| ffmpeg / ffprobe | 切镜头、截封面、算停顿、比对画面 |

## 使用方法

### 宣传片工程

```bash
uv run ~/.claude/skills/jianying-draft/scripts/from_guizang.py <工程目录>
```

| 参数 | 作用 |
|:---|:---|
| `--video 成片.mp4` | 指定成片；默认用 `renders/final.mp4`，`renders/` 下只有一个 mp4 时自动用它 |
| `--root 目录` | 生成到别的目录，试跑时用，比如 `--root /tmp/jy-test` |
| `--force` | 覆盖已经在剪映里打开或编辑过的草稿（会冲掉剪映里的改动） |
| `--portable` | 素材路径写成剪映的草稿目录占位符，改名、搬家不断链（实验功能，尚未在剪映里实测） |

工程需要有 `plan.json`、成片、`assets/` 下的预混音 / 人声轨 / 母带等文件，也就是 guizang 起步工程跑完 `bed.py` 和 `mix_audio.py` 之后的产物；缺哪个会直接提示。

生成的草稿：

| 轨道 | 内容 |
|:---|:---|
| 画面（主轨） | 按镜头逐帧切开的无声片段，文件名是镜头名 |
| 配乐 | 人声段和音效处的压低已做进文件；原始配乐另放一份在 `素材/配乐/配乐-原始.wav`，换曲用 |
| 旁白 | 一句一个片段 |
| 音效 | 每个动作音效一个片段，时间重叠的放到第二条轨 |
| 字幕 | 默认隐藏，点轨道头的眼睛显示；同一份另存为 `字幕.srt` |

### 其他来源

把素材整理成 `timeline.json`（格式见 `references/timeline.md`），然后：

```bash
uv run ~/.claude/skills/jianying-draft/scripts/jianying_draft.py timeline.json
```

### 检查一份草稿

```bash
uv run ~/.claude/skills/jianying-draft/scripts/check_draft.py <草稿名> [--video 成片.mp4]
```

输出示例：

```
剪映操作日志：09-27 08:35:54 从「ChatPage-资料搬运工」改名为「ChatPage Agent」
剪映：打开并保存过（draft_info.json 已加密……）
素材：39 个，缺失 39 个
  素材路径指向旧文件夹 …/ChatPage-资料搬运工，文件还在当前草稿的 素材/ 里（多半是在剪映里改过名）。
  剪映打开时如果提示素材丢失，用「重新链接」指到 …/ChatPage Agent/素材 即可
轨道：text  字幕  65 段（隐藏）
时间线：144.60 秒，30 帧/秒；不在整帧的边界 0 处，吸附到帧后重叠 0 处
```

## 配置

宣传片工程可以在根目录放一份 `jianying.json`，都是可选项：

```json
{
  "draft_name": "ChatPage-用户篇",
  "cover": {"at": 12.8},
  "shots": {"hook": "复制粘贴再解释", "brand": "按下Alt+A"},
  "subtitle_fixes": {"Alt 加 A 键": "Alt+A", "Chat Page": "ChatPage", "艾特": "@"},
  "sub_width": 17
}
```

| 字段 | 作用 | 默认 |
|:---|:---|:---|
| `draft_name` | 剪映首页显示的草稿名 | 工程目录名 |
| `cover` | `{"image": 路径}` 或 `{"at": 秒}`（从成片截一帧） | 有 `covers/cover-16x9.png` 就用它 |
| `shots` | 镜头 id → 片段文件名 | 镜头标题截 12 个字 |
| `subtitle_fixes` | 配音稿为了读音改写的字 → 字幕里的写法 | 不替换 |
| `sub_width` | 一条字幕最多的字宽（汉字算 1，字母、数字、空格算 0.5） | 17 |

## 注意事项

- **剪映常开在后台，技能不会去关它。** 你正在剪映里编辑时，新生成的草稿要等你回到首页才会出现在列表里。
- **在剪映里改名可能导致素材丢失。** 剪映改名会重命名文件夹，而草稿里的素材是绝对路径。遇到素材丢失，用「重新链接」指到草稿文件夹下的 `素材/`。
- **草稿只在生成它的电脑上能直接打开**，拷到别的电脑同样要重新链接素材。
- **改不了渲染进画面的内容**：镜头里的文字、界面和动画是像素，要改得回到视频工程里改代码、重新渲染，再生成草稿。
- 声音和成片的细微差别：原片在音效处把人声压低 2～3 dB，草稿里人声没压，整体略响 0.1～0.5 dB；音效起点对齐到帧，最多偏 17 毫秒。

## 目录结构

```
jianying-draft/
├── SKILL.md                    # 技能定义
├── README.md                   # 本文件
├── scripts/
│   ├── from_guizang.py         # 宣传片工程 → 草稿
│   ├── jianying_draft.py       # 核心：timeline.json → 草稿
│   ├── check_draft.py          # 只读诊断
│   └── click.py                # 在剪映里验证时发真实鼠标点击
└── references/
    ├── format.md               # 剪映草稿格式与行为（实测）
    ├── timeline.md             # timeline.json 规格
    └── verify-in-app.md        # 在剪映里验证的做法
```
