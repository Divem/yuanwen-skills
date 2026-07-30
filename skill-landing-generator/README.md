# Skill Landing Generator

为 Agent Skill 生成统一设计风格的三页静态 HTML：

- `{skill-name}-landing.html`：功能介绍与核心用法
- `{skill-name}-manual.html`：完整使用手册
- `{skill-name}-source.html`：完整渲染 `SKILL.md`，并提供原文视图

三个页面使用相对路径互相链接。其中 landing 和 manual 顶部显示 `SKILL.md` 入口，Source 页可返回落地页与使用手册。

## 使用方式

提供目标 Skill 名称以及 `SKILL.md` 或 `README.md` 内容，调用：

```text
/skill-landing-generator <skill-name>
```

生成前会读取 `references/design-token.md` 和三个页面模板：

```text
assets/landing-template.html
assets/manual-template.html
assets/source-template.html
```

Source 页在生成阶段读取并嵌入完整 `SKILL.md`，不会在浏览器运行时通过 `fetch()` 加载 Markdown，因此可以直接作为静态单文件部署。

如果目标目录存在由数据生成卡片的 `index.html`，生成器会为当前 Skill 设置 `source: true` 并显示 `Source` 链接；未生成 Source 页的旧卡片不会显示入口。
