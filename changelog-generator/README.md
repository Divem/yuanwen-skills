# Changelog Generator

> 把散落在各 AI 编码工具里的开发痕迹，提炼成给用户看的更新日志。

## 这是什么

一个帮你写**项目 changelog** 的 skill。它会自动扫描你在 Claude Code、Codex、OpenCode、Qoder、WorkBuddy 等工具里留下的开发日志、变更计划和 git 提交，提炼出用户能感知的变更，按你选定的品牌风格生成一条更新日志，并追加到项目的 `CHANGELOG.md` 顶部。

风格库基于 features.vote 对 20 款产品（Linear、Raycast、Stripe、Notion 等）changelog 的调研提炼。

## 触发方式

在 Claude Code 里直接说人话即可：

- "帮我写这周的更新日志"
- "整理一下 v1.2.0 到现在的变更，发个 changelog"
- "发布前生成 release notes"
- "汇总一下最近在 Codex 和 Claude Code 里做的改动"

## 工作流程

1. **确认范围**：版本区间、目标读者、要强调/回避的点
2. **扫描素材**：自动发现各工具的开发日志、plans、git 提交
3. **确认清单**：列出发现的素材，你勾选/增删
4. **选风格**：从 7 种品牌风格里选一个（可锁定）
5. **提炼变更**：翻译成"用户能感知的变化"，归类 New/Improved/Fixed/Breaking
6. **生成并追加**：套用模板生成，追加到 `CHANGELOG.md` 顶部（写入前会给你过目）

## 7 种风格

| # | 风格 | 特征 | 适合 |
|---|------|------|------|
| 1 | **Linear** | 丰富叙述 + 截图位 + 分类子标题 | SaaS、讲产品故事 |
| 2 | **Raycast** | ✨💎🐞 Emoji + semver + 命令代码化 | 开发者工具、桌面应用 |
| 3 | **Stripe** | 极简索引 + `[产品域]` 前缀 + 一句话链接 | API / 基础设施 |
| 4 | **Notion** | 对话式 + UI 路径代码化 + 利益导向 | SaaS、消费级 |
| 5 | **Framer** | Added/Improved/Fixed 三段式 | 设计工具、小版本 |
| 6 | **GitHub** | 标题索引 + 发布类型标签 + 作者 | 开源项目 |
| 7 | **标准通用** | Emoji 四段式（最大公约数） | 通用默认 |

每种风格的完整模板和示例见 `references/templates.md`。

## 项目配置（可选）

在项目根目录放 `.changelog.yml` 锁定偏好，就不用每次都选：

```yaml
style: raycast            # linear / raycast / stripe / notion / framer / github / standard
date_format: YYYY-MM-DD
version_strategy: date    # date / semver / manual
language: auto            # auto / zh / en
include_git: true
```

## 输出

- 默认追加到项目 `CHANGELOG.md` 顶部（倒序，最新在上）
- 文件不存在时自动用骨架创建
- 语言跟随项目主语言（检测不到默认中文）

## 核心理念

这份 skill 始终遵循几条原则（来自 20 款产品的最佳实践）：

- **利益先行**：先说用户能得到什么
- **每条回答 "So What"**：用户读完知道这对自己意味着什么
- **UI 路径代码化**：`Settings → Appearance` 而不是"在设置里"
- **Breaking 必须突出**：附迁移指引
- **不夸大**：用具体数字，不用"革命性"

## 文件结构

```
changelog-generator/
├── SKILL.md                       # 主指令（工作流 + 风格速览）
├── README.md                      # 本文件
├── references/
│   ├── templates.md               # 7 种品牌风格完整模板
│   ├── source-discovery.md        # 各工具日志扫描路径
│   └── writing-rules.md           # 写作规则 + 追加规则
└── assets/
    └── changelog-skeleton.md      # CHANGELOG.md 首次创建骨架
```

## 已知限制

- 各工具日志路径会随版本变化，路径失效时会请你补充
- 工具日志噪音大，需你确认有效变更清单
- 截图/媒体需你自行补充，skill 只留占位符
- WorkBuddy 等较新工具的日志结构可能需要你指认位置
