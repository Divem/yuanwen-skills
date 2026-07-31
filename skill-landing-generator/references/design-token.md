# build-and-deploy Skill 介绍页设计规范

> 本规范源自 `landing-template.html`（落地页）、`manual-template.html`（用户手册）与 `source-template.html`（SKILL.md 源文档页）的联合设计系统，用于统一 Skill 介绍类页面的视觉语言。

---

## 1. 设计原则

| 原则 | 说明 |
|------|------|
| **极简克制** | 以黑白灰为底，单一蓝色为强调，拒绝多余装饰 |
| **信息密度优先** | 技术文档场景，留白适度，内容为王 |
| **开发者友好** | 等宽字体用于代码/命令，清晰的可扫描性 |
| **响应式优先** | 从桌面端到移动端无缝降级，核心断点 880px / 640px |

---

## 2. 色彩系统

### 2.1 基础色板

```css
--bg:        #ffffff;   /* 页面主背景 */
--bg-soft:   #f7f7f5;   /* 卡片/交替区块背景 */
--paper:     #ffffff;   /* 浮层面板背景 */
--ink:       #111111;   /* 主标题/正文 */
--ink-soft:  #555555;   /* 次要描述文字 */
--ink-mute:  #8a8a87;   /* 注释/辅助信息 */
--line:      #e6e6e3;   /* 边框/分割线 */
--line-soft: #ededea;   /* 悬停背景/弱边框 */
```

### 2.2 强调色板（仅用于代码高亮与交互状态）

```css
--accent:       #2563eb;  /* 主强调：链接、关键词、按钮激活态 - 蓝 */
--accent-soft:  #eaf0ff;  /* 浅蓝背景：badge、callout、hover 底色 */
--hl-string:    #059669;  /* 字符串/成功状态 - 翡翠绿 */
--hl-number:    #d97706;  /* 数字/警告 - 琥珀 */
--hl-comment:   #8a8a87;  /* 注释 - 灰 */
```

### 2.3 语义色板（手册页专用）

```css
--warn:       #d97706;  --warn-soft: #fef3c7;  /* 警告 callout */
--info:       #2563eb;  --info-soft: #eaf0ff;  /* 信息 callout */
```

### 2.4 使用规则

- **禁止**：使用红色、紫色、粉色等非功能性色彩
- **强调色使用范围**：仅用于链接、代码关键字、active 状态、图标背景
- **边框统一**：全部使用 `1px solid var(--line)`，无阴影边框
- **hover 反馈**：背景色过渡到 `var(--bg-soft)` 或 `var(--accent-soft)`

### 2.5 浏览器图标 (Favicon)

所有页面使用内联 SVG favicon，与导航栏 logo 保持一致（蓝色圆角方底 + 白色闪电）：

```html
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg width='28' height='28' viewBox='0 0 28 28' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Crect width='28' height='28' rx='7' fill='%232563eb'/%3E%3Cpath d='M16.5 4L9 15h4.5L11.5 24 20 12h-5z' fill='%23fff' stroke='%23fff' stroke-width='0.5' stroke-linejoin='round'/%3E%3Ccircle cx='8.5' cy='6.5' r='1.2' fill='%23fff' opacity='.6'/%3E%3Ccircle cx='20.5' cy='22' r='1' fill='%23fff' opacity='.4'/%3E%3C/svg%3E">
```

- 使用 data URI 编码，无需外部图片文件
- 放置在 `<title>` 标签之后

---

## 3. 字体系统

### 3.1 字体栈

```css
--sans: "Inter", "PingFang SC", "Microsoft YaHei", system-ui, sans-serif;
--mono: "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
```

### 3.2 字号层级

| 级别 | 用途 | 桌面端 | 移动端 | 字重 | 字体 |
|------|------|--------|--------|------|------|
| H1 | 落地页主标题 | clamp(36px, 4.6vw, 64px) | clamp(32px, 9vw, 44px) | 700 | sans |
| H2 | 区块标题 | clamp(28px, 4vw, 44px) | - | 700 | sans |
| H3 | 子区块标题 | clamp(22px, 3vw, 30px) | - | 700 | sans |
| H4 | 卡片标题 | 16px | - | 600 | sans |
| Body | 正文 | clamp(15px, 1.3vw, 17px) | - | 400 | sans |
| Lede | 引导段落 | clamp(16px, 1.5vw, 19px) | - | 400 | sans |
| Mono | 代码/命令 | 13px ~ 13.5px | - | 400/500 | mono |
| Label | 标签/badge | 11px ~ 12px | - | 600 | mono |

### 3.3 排版规则

- 标题使用 `letter-spacing: -0.02em` 增加紧凑感
- 等宽文本使用 `line-height: 1.85`（代码块）
- 正文使用 `line-height: 1.65 ~ 1.7`
- 代码内联样式：`font-size: 0.88em`，`padding: 2px 6px`，圆角 3~4px

---

## 4. 间距系统

### 4.1 核心变量

```css
--gutter: clamp(20px, 4vw, 72px);   /* 页面水平边距 */
--radius: 10px;                      /* 统一圆角 */
--sidebar: 260px;                    /* 手册页侧边栏宽度 */
```

### 4.2 区块间距

| 场景 | 桌面端 | 移动端 |
|------|--------|--------|
| Section padding | clamp(70px, 11vw, 120px) | 减少约 30% |
| Hero padding-top | clamp(70px, 12vw, 130px) | - |
| 卡片 gap | 12px ~ 18px | 14px |
| 网格 gap | clamp(28px, 5vw, 56px) | - |

### 4.3 容器规则

- **落地页**：`.frame` 全宽 + `padding: 0 var(--gutter)`；`.narrow` 最大 980px 居中
- **手册页**：两栏布局 `260px | 1fr`，主内容区 `max-width: 1100px` 居中

---

## 5. 组件规范

### 5.1 导航栏 (Nav / Topbar)

```
┌─────────────────────────────────────────────────────┐
│ 🔺 brand     link link link link link link    [CTA] │  height: 60px
│                                                     │  border-bottom: 1px solid var(--line)
└─────────────────────────────────────────────────────┘  sticky, top: 0, z-index: 30+
```

- **品牌区**：等宽字体，SVG 闪电 logo(28×28) + 文字，font-weight: 700
- **链接区**：font-size: 14px，color: var(--ink-soft)，hover → var(--ink)
- **CTA按钮**：等宽字体，13px，边框按钮，hover 反色填充
- **移动端**：< 760px 隐藏链接区，显示 ☰ 菜单按钮（手册页）

### 5.2 Hero 区域

```
┌────────────────────────┬────────────────────────────┐
│ repo-badge（来源链接） │                            │
│ 一句中文，             │   ┌────────────────────┐   │
│ 把前端发到远程服务器   │   │  terminal          │   │
│                        │   │  $ /build-and-...  │   │
│ lede 描述文字...       │   │  › 解析参数...     │   │
│                        │   └────────────────────┘   │
│ [主按钮] [次按钮]      │                            │
└────────────────────────┴────────────────────────────┘
        grid: 1.05fr | 1fr    gap: clamp(40px, 6vw, 80px)
```

- 标题中的关键词使用 `color: var(--accent)` 文字颜色高亮
- 双按钮布局：主按钮深色填充，次按钮边框风格
- 移动端：< 1024px 单列堆叠

**Repo Badge（Hero 顶部来源链接徽章）**
- 仅当 skill 有远程来源链接时显示（GitHub 仓库、SkillHub 页面等）；无链接则不渲染
- 结构：`[图标 + 地址（可点击跳转） | 复制按钮]`，单一边框容器（`border: 1px solid var(--line)`，radius 6px，`background: var(--bg-soft)`）
- 图标按域名选择：`github.com` → GitHub 图标；其他远程链接 → 通用链接图标
- 地址文本：等宽 12px，去除 `https://` 前缀展示，超长省略号截断
- 复制按钮：左边框分隔，点击复制完整 URL，成功显示 ✓（绿色）1.5s 后还原
- hover：文字/图标变 `var(--accent)`，底色 `var(--accent-soft)`

### 5.3 终端模拟器 (Terminal)

```
┌──────────────────────────────────────────────┐
│ ○ ○ ○          ~ /build-and-deploy           │  标题栏
├──────────────────────────────────────────────┤
│ $ /build-and-deploy 将本地文件...             │
│ › 解析参数    操作=部署 · 主机=prod           │  内容区
│ › 项目识别    检测到 vite + React...          │  font-family: mono
│ › SSH 预检    ✔ 密钥认证通过                  │  white-space: pre
│ ✔ 部署完成 · http://...                       │
└──────────────────────────────────────────────┘
```

- 边框：`1px solid var(--line)`，圆角 `var(--radius)`
- 标题栏：三个圆点 + 居中标题，底部边框分隔
- 内容区：padding 22px 28px，行高 1.85
- 色彩编码：prompt(蓝)、cmd(黑)、arg(蓝)、str(绿)、ok(绿+粗)、warn(琥珀)

### 5.4 特性卡片 (Feature Card)

```
┌─────────────────────┐
│ ┌─────┐             │  图标区：32×32，边框+背景，圆角 4px
│ │ 🔍  │             │         color: var(--accent)
│ └─────┘             │
│ 自动识别项目         │  标题：16px, weight 600
│ 读取 package.json... │  描述：14px, color: var(--ink-soft)
└─────────────────────┘
        border-right + border-bottom
```

- 网格布局：3 列（桌面）→ 1 列（< 880px）
- 边框式网格：外边框 + 单元格右/下边框，无 gap
- hover：背景过渡到 `var(--bg-soft)`

### 5.5 步骤卡片 (Step Card)

```
┌─────────────────────┐
│          01         │  右上角：计数器(decimal-leading-zero)
│ [tag]               │  标签：等宽字体，边框+背景，color: accent
│ 解析与识别           │
│ 从自然语言或 flag... │
└─────────────────────┘
```

- 网格：`repeat(auto-fit, minmax(240px, 1fr))`，自适应列数，不限制步骤数量。桌面端自然呈现 4 列，随视口缩小自动换行
- 标签样式：11px，1px 边框，accent 色

### 5.6 用法示例卡片 (Usage Card)

```
┌──────────────────────────────┐
│ 默认：编译 + 部署    [最常用] │  头部：flex 两端对齐，背景 bg-soft
├──────────────────────────────┤
│ /build-and-deploy            │  内容：等宽字体，pre-wrap
│ → 构建并部署 ./dist          │  命令高亮：accent 色 + 粗体
│    到 nginx@...              │  字符串：emerald 色
└──────────────────────────────┘
```

- 头部标签(pill)：11px，accent 边框+背景
- 网格：`repeat(auto-fit, minmax(320px, 1fr))`，自适应列数，不限制卡片数量。桌面端自然呈现 3 列，随视口缩小自动换行

### 5.7 配置展示 (Config)

```
┌───────────────────────┬──────────────────────────┐
│ {                     │                          │
│   "default": {        │  host     服务器 IP       │  左：代码块
│     "host": "10..."   │  port     SSH 端口        │  右：字段说明列表
│   }                   │  user     登录用户名       │
│ }                     │                          │
└───────────────────────┴──────────────────────────┘
```

- 代码块：语法高亮（k=蓝, s=绿, n=琥珀, p=灰）
- 字段列表：双列网格（code | span），移动端单列

### 5.8 资源卡片 (Resource Card)

```
┌────────────────────────────────────────┐
│ 📖 参考文档                            │  标签：等宽 11px，accent 色
│ 飞书文档：SSH 配置手册                  │  标题：17px, weight 600
│ 本工具的配套阅读...                     │  描述：14px, ink-soft
│ weikezhijia.feishu.cn/...              │  URL：等宽 12px，accent 色
└────────────────────────────────────────┘
        hover: border-color → accent, background → accent-soft
```

### 5.9 Callout 提示框（手册页）

| 类型 | 背景 | 边框 | 文字色 | 图标背景 |
|------|------|------|--------|----------|
| warn | #fef3c7 | #fcd34d | #78350f | amber |
| info | #eaf0ff | #93c5fd | #1e3a8a | blue |
| tip | #eaf0ff | #86efac | #14532d | blue |

布局：`28px icon | 1fr content`，圆角 10px

### 5.10 手册页专用组件

#### 侧边栏 (Sidebar)
- 宽度：260px，sticky，高度 `calc(100vh - 60px)`
- 分组标题：等宽 11px，大写，letter-spacing: 0.14em
- 链接：14px，左边框 2px 透明，active → 蓝底+左边框

#### 阅读进度条
- 固定顶部，高度 2px，蓝色，width 随滚动变化

#### 表格滚动容器 (Table Scroll)
- 类名：`.table-scroll`
- 桌面端：无特殊效果，表格自然宽度
- 移动端：`overflow-x: auto; -webkit-overflow-scrolling: touch;`，表格设 `min-width: 480px` 保证可读性
- 所有手册页 `<table>` 必须包裹在 `<div class="table-scroll">` 中

### 5.11 SKILL.md 源文档页专用组件

- 顶部栏包含返回落地页、手册页两个入口，当前页面名称显示为 `SKILL.md`
- 主内容区最大宽度 980px，使用 `.source-shell` 和 `.markdown-body`
- 提供“渲染结果 / 原文”两个切换按钮，默认显示渲染结果
- 渲染结果使用语义化 HTML；原文使用 `<pre><code>` 并对完整 `SKILL.md` 做 HTML 转义
- 内容在生成阶段直接嵌入 HTML，禁止通过 `fetch()` 在运行时读取 Markdown
- Markdown 标题、列表、表格、引用、链接、行内代码和代码块均需有对应样式
- 页面底部使用与 landing/manual 一致的品牌页脚

---

## 6. 布局规范

### 6.1 落地页结构

```
Nav (sticky)
├── Hero (两栏：文案 + 终端)
├── Prereq (两栏：说明 + 代码)
├── Server Policy (3 列卡片)
├── Features (3×3 网格)
├── Flow (N 步骤，auto-fit 网格)
├── Usage (N 列卡片，auto-fit 网格)
├── Keynote (两栏：关键词 + 示例)
├── Config (两栏：代码 + 字段)
├── Resources (2 列链接)
├── CTA (居中)
└── Footer
```

### 6.2 手册页结构

```
Topbar (sticky, blur backdrop)
├── Sidebar (260px, 滚动追踪)
└── Main (1fr, max-width 1100px, 居中)
    ├── Page Header (eyebrow + h1 + lede + meta)
    ├── h2/h3 内容区块
    ├── Tables / Code blocks / Callouts
    └── Prev/Next 导航 + Footer
```

### 6.3 SKILL.md 源文档页结构

```
Topbar (sticky)
├── Brand
├── Landing / Manual 导航
└── 当前页标记 SKILL.md
Main (max-width 980px)
├── Page Header
├── 渲染结果 / 原文切换
├── Rendered Markdown
├── Escaped Raw Markdown
└── Brand Footer
```

### 6.4 响应式断点

| 断点 | 变化 |
|------|------|
| 1024px | Hero 双栏 → 单栏 |
| 980px | 特性网格 3 列 → 2 列；手册页 Policy 3 列 → 1 列 |
| 880px | 手册页隐藏 Sidebar，显示 ☰ 菜单；Keynote/Config 双栏 → 单栏 |
| 760px | 落地页隐藏 nav-links；资源卡片 2 列 → 1 列 |
| 680px | Usage 卡片自动换行 |
| 640px | Hero 标题缩小 |
| 540px | Flow 步骤自动换行；手册页底部导航双列 → 单列；移动端专项优化（见下） |

### 6.5 移动端专项优化（≤540px）

**落地页：**
- Section 垂直间距从 `clamp(70px, 11vw, 120px)` 降至 `48px`
- Hero 区 padding 缩减至 `48px / 36px`
- Terminal / Code block 内边距缩减至 `16px 18px`，字号降至 `12px`
- Feature / Step / Usage 卡片内边距缩减
- CTA 区 padding 降至 `48px`
- Footer 改为 `flex-direction: column` 居中堆叠

**手册页：**
- `.main` 内边距降至 `32px 20px`
- h2 间距从 `56px` 降至 `40px`
- Page header margin 降至 `32px`
- Code block 内边距缩减至 `16px 18px`，字号降至 `12px`
- 所有表格通过 `.table-scroll` 容器横向滚动，`min-width: 480px`

---

## 7. 交互规范

### 7.1 过渡动画

```css
transition: background 140ms, color 140ms, border-color 140ms;
```

- 所有 hover 状态统一 140ms
- 手册页 nav-card hover：`transform: translateY(-2px)`，180ms
- 移动端 Sidebar 展开：240ms ease

### 7.2 滚动行为

```css
html { scroll-behavior: smooth; }
```

- 锚点跳转平滑滚动
- 标题 `scroll-margin-top: 80px`（避开 sticky nav）

### 7.3 ScrollSpy（手册页）

- 监听 `main section[id]` 进入视口
- offset: 120px
- 同步高亮 Sidebar 当前章节
- 进度条：`width = scrollTop / (scrollHeight - clientHeight) * 100%`

### 7.4 无障碍

```css
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  .feature, .btn, .nav-cta, .resource { transition: none; }
  .nav-card:hover { transform: none; }
}
```

---

## 8. 代码高亮规范

### 8.1 终端内高亮

| 类名 | 颜色 | 用途 |
|------|------|------|
| `.prompt` | accent (蓝) | 命令提示符 `$` |
| `.cmd` | ink (黑) | 主命令 |
| `.arg` | accent (蓝) | 参数/选项 |
| `.str` | hl-string (绿) | 字符串/路径 |
| `.ok` | hl-string (绿) + 600 | 成功提示 |
| `.info` | accent (蓝) + 600 | 信息前缀 `›` |
| `.warn` | hl-number (琥珀) | 警告/询问 |
| `.mute` | ink-mute (灰) | 辅助描述 |

### 8.2 代码块高亮（手册页）

| 类名 | 颜色 | 用途 |
|------|------|------|
| `.tk-c` | hl-comment (灰) + italic | 注释 |
| `.tk-k` | accent (蓝) + 600 | 关键字/键名 |
| `.tk-s` | hl-string (绿) | 字符串值 |
| `.tk-n` | hl-number (琥珀) | 数字 |
| `.tk-cm` | accent (蓝) + 700 | 命令/可执行 |
| `.tk-p` | ink (黑) | 标点 |

---

## 9. 命名约定

### 9.1 CSS 类名规范

| 前缀/模式 | 用途 |
|-----------|------|
| `.frame` | 全宽容器 |
| `.narrow` | 受限宽度容器 |
| `.sec-*` | Section 级别元素 |
| `.btn-*` | 按钮变体 |
| `.tk-*` | Token 高亮类 |
| `.callout.*` | 提示框类型 |

### 9.2 文件命名

| 模式 | 用途 |
|------|------|
| `*-landing.html` | 落地介绍页 |
| `*-manual.html` | 用户手册页 |
| `*-source.html` | SKILL.md 源文档页 |

---

## 10. 快速参考：新建 Skill 介绍页

### 10.1 最小落地页结构

```html
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{skill-name} · {一句话描述}</title>
  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,...">
  <link href="Google Fonts: Inter + JetBrains Mono" rel="stylesheet">
  <style>
    /* 1. 引入上述完整 CSS 变量系统 */
    /* 2. 引入 Nav + Hero + Section + Footer 基础样式 */
    /* 3. 根据内容选择需要的组件样式 */
  </style>
</head>
<body>
  <nav class="nav">...</nav>
  <header class="hero">...</header>
  <section id="features">...</section>
  <section id="usage">...</section>
  <section class="cta-final">...</section>
  <footer>...</footer>
</body>
</html>
```

### 10.2 最小手册页结构

```html
<!-- 在落地页基础上增加： -->
<div class="layout">
  <aside class="sidebar">...</aside>
  <main id="content">...</main>
</div>
<script>
  // Mobile menu + ScrollSpy（基于 section[id]）
</script>
```

### 10.3 最小 SKILL.md 源文档页结构

```html
<nav class="topbar">...</nav>
<main class="source-shell">
  <header class="source-header">...</header>
  <div class="view-switch">...</div>
  <article id="renderedSource" class="markdown-body">...</article>
  <pre id="rawSource" class="raw-source" hidden><code>...</code></pre>
  <footer>...</footer>
</main>
```

---

*规范版本：v1.1*
*© 2026 imyuanwen@gmail.com*
