# Skill Landing Generator

为 Claude Skill 生成统一风格的落地页（Landing）和手册页（Manual）HTML，确保所有 Skill 介绍页面视觉语言一致。

## 功能特性

- **落地页生成**：基于统一设计规范，生成包含 Hero、前置条件、核心功能、工作流程、用法示例等区块的营销落地页
- **手册页生成**：生成包含侧边栏导航、ScrollSpy、目录联动等技术文档手册页
- **设计一致性**：严格遵循统一设计 token（色彩、字体、间距、圆角、交互），确保跨 Skill 页面风格统一
- **响应式适配**：覆盖 1024px / 980px / 880px / 760px / 680px / 640px / 540px 多档断点
- **中文优先**：默认中文文案，`<html lang="zh-CN">`
- **互相链接**：落地页和手册页自动互相引用

## 使用方法

```
/skill-landing-generator <skill-name>
```

例如为 `feishu-sync` 生成页面：

```
/skill-landing-generator feishu-sync
```

## 生成产物

| 文件 | 说明 |
|------|------|
| `{skill-name}-landing.html` | 营销落地页，包含 Hero、功能卡片、工作流程、用法示例 |
| `{skill-name}-manual.html` | 技术手册页，包含侧边栏导航、命令详解、进阶主题 |

## 目录结构

```
skill-landing-generator/
├── SKILL.md                        # 技能定义
├── README.md                       # 使用说明
├── assets/
│   ├── landing-template.html       # 落地页模板
│   └── manual-template.html        # 手册页模板
└── references/
    └── design-token.md             # 统一设计规范
```
