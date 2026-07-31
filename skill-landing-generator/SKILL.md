---
name: skill-landing-generator
author: wen.yuan
description: 为 Agent Skill 生成统一的落地页（landing）、手册页（manual）和 SKILL.md 源文档页（source）HTML。基于统一设计规范，确保所有 Skill 介绍页面视觉语言一致。触发场景：(1) 用户要求为某个 skill 生成 landing/介绍页面；(2) 用户要求为某个 skill 生成 manual/手册/文档页面；(3) 用户要求展示或渲染 SKILL.md 原文；(4) 用户要求生成 skill 介绍页、文档页或源码页。输入：skill 名称 + skill 文档内容。输出：三个互相链接的 HTML 文件。
---
# Skill Landing Generator

为任意 Agent Skill 生成一组统一风格的 HTML 页面：**落地页** + **手册页** + **SKILL.md 源文档页**。

## 设计规范

所有页面必须严格遵循 `references/design-token.md` 中的设计规范。生成前**必须先读取**该文件。

设计规范涵盖：色彩系统、字体系统、间距系统、组件规范、布局规范、交互规范、代码高亮规范、命名约定。

## 生成流程

### 1. 收集信息

读取目标 skill 的文档（SKILL.md / README.md），提取：

- **名称**：skill 名称（用于文件命名和页面标题）
- **一句话描述**：用于 hero 区域和 meta description
- **前置条件**：需要安装的工具、权限、环境
- **核心功能**：完整特性点（图标 + 标题 + 描述），不限制数量，尽可能详细覆盖全部功能
- **工作流程**：完整工作流程（tag + 标题 + 描述），不限制步骤数量，尽可能详细覆盖全部子流程
- **命令/用法**：主要命令及参数说明
- **配置/状态标记**：配置项、状态标记、输出格式等
- **注意事项/限制**：已知限制和使用注意

### 2. 生成落地页

参考 `assets/landing-template.html` 的结构。顶部导航必须同时包含手册页和 `SKILL.md` 源文档页入口。

**Hero 徽章规则**：如果 skill 有远程来源链接（GitHub 仓库、SkillHub 页面等），Hero 顶部显示来源链接徽章（`.repo-badge`，等宽字体展示地址，左侧点击跳转，右侧按钮一键复制地址，复制成功显示 ✓ 反馈）。图标按域名选择：`github.com` 用 GitHub 图标，其他远程链接用通用链接图标。如果没有来源链接，则完全不显示徽章。

核心区块：

```
Nav (sticky)
├── Hero（双栏：文案 + 终端模拟器）
├── 前置条件（双栏：说明 + 代码块）
├── 核心功能（完整特性卡片网格，3 列 auto-fit）
├── 工作流程（完整步骤卡片，auto-fit 自适应网格）
├── 用法示例（全部用法卡片，auto-fit 自适应网格）
├── 状态/配置说明（可选，按需）
├── CTA（居中号召）
└── Footer
```

文件命名：`{skill-name}-landing.html`

### 3. 生成手册页

参考 `assets/manual-template.html` 的结构。顶部栏必须同时包含落地页和 `SKILL.md` 源文档页入口。

**Page Meta 规则**：页头 meta 行除版本/更新日期外——SKILL.md frontmatter 有 `author` 字段时显示作者信息，无则省略；有远程来源链接（GitHub / SkillHub 等）时显示来源链接（新标签页打开，链接文案统一为 `来自 GitHub` / `来自 SkillHub` 格式），无则省略。

核心区块：

```
Topbar (sticky, blur backdrop)
├── Sidebar（260px，分组导航，ScrollSpy 高亮当前章节）
└── Main（1fr，max-width 1100px，居中）
    ├── Page Header（eyebrow + h1 + lede + meta）
    ├── 概述
    ├── 前置条件
    ├── 快速开始
    ├── 各命令详解（h2，含参数表、流程表）
    ├── 进阶主题（文件处理、冲突、映射文件等）
    ├── 限制与注意
    └── Prev/Next 导航 + Footer
```

文件命名：`{skill-name}-manual.html`

### 4. 生成 SKILL.md 源文档页

参考 `assets/source-template.html` 的结构。

1. 读取目标 Skill 的 `SKILL.md` 完整原文，包括 YAML frontmatter。
2. 在生成阶段把 Markdown 转换为语义化 HTML，写入 Source 页正文；不要在浏览器运行时通过 `fetch()` 请求本地 Markdown。
3. 同时把经过 HTML 转义的完整原文写入“原文”视图，确保读者可以在“渲染结果 / 原文”之间切换。
4. 保留原文顺序、标题层级、列表、表格、引用、代码块、链接和行内代码；不得省略、改写或补写源文档内容。
5. Source 页底部必须包含统一品牌页脚。

文件命名：`{skill-name}-source.html`，页面入口文案统一使用 `SKILL.md`，索引卡片入口文案统一使用 `Source`。

### 5. 互相链接

- 落地页 nav 中链接到手册页和 Source 页
- 手册页 topbar 中链接回落地页和 Source 页
- Source 页 topbar 中链接回落地页和手册页
- 三个页面放在同一目录，全部使用相对路径

### 6. 更新索引卡片

如果输出目录中存在 `index.html`，并且索引卡片由 Skill 数据生成：

- 为当前 Skill 的数据项设置 `source: true`
- 在卡片链接区按 `source` 字段条件渲染 `<a href="{skill-name}-source.html">Source</a>`
- 不要为尚未生成 Source 页的旧 Skill 显示入口，避免产生 404 链接

## 一致性检查清单

生成后逐项验证：

- [ ] CSS 变量完全使用设计规范中的 `:root` 变量，无硬编码颜色
- [ ] 字体栈为 `var(--sans)` / `var(--mono)`，未使用其他字体
- [ ] 边框统一 `1px solid var(--line)`，无阴影
- [ ] 圆角统一 `var(--radius)`（10px）
- [ ] hover 过渡统一 140ms
- [ ] 代码高亮类名使用 `.prompt` `.cmd` `.arg` `.str` `.ok` `.info` `.warn` `.mute`（落地页）和 `.tk-c` `.tk-k` `.tk-s` `.tk-n` `.tk-cm` `.tk-p`（手册页）
- [ ] 响应式断点覆盖：1024px / 980px / 880px / 760px / 680px / 640px / 540px
- [ ] 手册页包含 ScrollSpy + 进度条 + 移动端 ☰ 菜单 JS
- [ ] Source 页完整包含 SKILL.md 的渲染结果和经过转义的原文，内容无删改
- [ ] Source 页不使用 `fetch()` 读取 Markdown，可直接作为静态单文件部署
- [ ] `prefers-reduced-motion` 媒体查询已包含
- [ ] 三个页面互相链接正确，顶部入口文案为 `SKILL.md`
- [ ] 有 Source 页的索引卡片显示 `Source`，无 Source 页的卡片不显示
- [ ] `<html lang="zh-CN">`，所有文案为中文
- [ ] 三个页面的 Footer 格式正确：左侧 `© 2026 imyuanwen@gmail.com`，右侧包含「Skill 说明书生成器」GitHub 链接 + 「即刻主页」链接，使用 flex 两端对齐，`border-top` + `max-width: 1240px` 居中
