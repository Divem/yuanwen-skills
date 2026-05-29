---
name: skill-landing-generator
description: 为 Claude Skill 生成统一的落地页（landing）和手册页（manual）HTML。基于统一设计规范，确保所有 Skill 介绍页面视觉语言一致。触发场景：(1) 用户要求为某个 skill 生成 landing/介绍页面；(2) 用户要求为某个 skill 生成 manual/手册/文档页面；(3) 用户要求生成 skill 介绍页、文档页。输入：skill 名称 + skill 文档内容。输出：两个 HTML 文件。
---

# Skill Landing Generator

为任意 Claude Skill 生成一对统一风格的 HTML 页面：**落地页** + **手册页**。

## 设计规范

所有页面必须严格遵循 `references/design-token.md` 中的设计规范。生成前**必须先读取**该文件。

设计规范涵盖：色彩系统、字体系统、间距系统、组件规范、布局规范、交互规范、代码高亮规范、命名约定。

## 生成流程

### 1. 收集信息

读取目标 skill 的文档（SKILL.md / README.md），提取：

- **名称**：skill 名称（用于文件命名和页面标题）
- **一句话描述**：用于 hero 区域和 meta description
- **前置条件**：需要安装的工具、权限、环境
- **核心功能**：3-6 个特性点（图标 + 标题 + 描述）
- **工作流程**：3-5 步流程（tag + 标题 + 描述）
- **命令/用法**：主要命令及参数说明
- **配置/状态标记**：配置项、状态标记、输出格式等
- **注意事项/限制**：已知限制和使用注意

### 2. 生成落地页

参考 `assets/landing-template.html` 的结构。核心区块：

```
Nav (sticky)
├── Hero（双栏：文案 + 终端模拟器）
├── 前置条件（双栏：说明 + 代码块）
├── 核心功能（3×N 特性卡片网格）
├── 工作流程（3-5 步骤卡片）
├── 用法示例（3 列命令卡片）
├── 状态/配置说明（可选，按需）
├── CTA（居中号召）
└── Footer
```

文件命名：`{skill-name}-landing.html`

### 3. 生成手册页

参考 `assets/manual-template.html` 的结构。核心区块：

```
Topbar (sticky, blur backdrop)
├── Sidebar（260px，分组导航）
├── Main（1fr，max-width 1100px）
│   ├── Page Header（eyebrow + h1 + lede + meta）
│   ├── 概述
│   ├── 前置条件
│   ├── 快速开始
│   ├── 各命令详解（h2，含参数表、流程表）
│   ├── 进阶主题（文件处理、冲突、映射文件等）
│   ├── 限制与注意
│   ├── Prev/Next 导航 + Footer
└── TOC（220px，JS 自动生成，ScrollSpy 联动）
```

文件命名：`{skill-name}-manual.html`

### 4. 互相链接

- 落地页 nav 中链接到手册页
- 手册页 topbar 中链接回落地页
- 落地页和手册页文件放在同一目录

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
- [ ] `prefers-reduced-motion` 媒体查询已包含
- [ ] 两页面互相链接正确
- [ ] `<html lang="zh-CN">`，所有文案为中文
- [ ] Footer 包含 `© 2026 imyuanwen@gmail.com`
