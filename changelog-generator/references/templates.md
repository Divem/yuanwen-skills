# 品牌风格模板库

7 种 changelog 风格的完整定义。每种含：**风格说明**、**模板骨架**、**完整示例**。

> 生成时只需读取用户选中的那一节，不必全读。所有示例用同一个虚拟变更场景，方便横向对比同一组变更在不同风格下的呈现差异。

## 目录

- [统一示例场景](#统一示例场景)
- [1. Linear（丰富叙述型）](#1-linear丰富叙述型)
- [2. Raycast（Emoji 分类 + semver）](#2-raycastemoji--semver)
- [3. Stripe（极简索引型）](#3-stripe极简索引型)
- [4. Notion（对话式 + UI 路径）](#4-notion对话式--ui-路径)
- [5. Framer（Added/Improved/Fixed 三段式）](#5-frameraddedimprovedfixed-三段式)
- [6. GitHub（标题索引 + 发布类型标签）](#6-github标题索引--发布类型标签)
- [7. 标准通用（最大公约数）](#7-标准通用最大公约数)
- [通用占位符说明](#通用占位符说明)
- [风格选择决策树](#风格选择决策树)

---

## 统一示例场景

下文 7 个示例都基于这组变更（一个知识管理 App 的某次发布）：

- **New**：新增暗色模式（`Settings → Appearance`）
- **Improved**：全局搜索速度提升约 3 倍
- **Fixed**：导出 PDF 时嵌入图片丢失
- **Breaking**：API 字段 `userId` 重命名为 `user_id`

---

## 1. Linear（丰富叙述型）

### 风格说明

**特征**：每个重大功能单独成段叙述，配截图位；用 `Fixes` / `Improvements` 子标题把次要变更分组；UI 元素加粗、命令内联代码、内联文档链接。

**设计意图**："展示 > 讲述"。截图把枯燥的功能列表变成引人入胜的故事，适合想讲好产品故事、重用户教育的产品。

**最适合**：面向终端用户的 SaaS、协作工具、功能密度高的产品。

**日期/版本**：完整日期（`YYYY-MM-DD`），不强调版本号。

### 模板骨架

```markdown
## YYYY-MM-DD

### [功能标题]
![截图描述](图片地址)

[1-2 句引言：这个功能解决什么问题、带来什么价值]

- **功能点 A**：描述（`UI 路径`）
- **功能点 B**：描述

#### Improvements
- **功能名**：改进描述

#### Fixes
- 修复描述
```

### 完整示例

```markdown
## 2026-07-19

### Dark mode, finally
![暗色模式切换演示](assets/dark-mode.png)

长时间码字写文档，眼睛会累。现在你可以在 `Settings → Appearance` 切换暗色模式，跟着系统自动切换也可以。

- **自动跟随系统**：勾选后随系统主题变化
- **手动三档**：浅色 / 暗色 / 跟随系统

#### Improvements
- **搜索**：全局搜索速度提升约 3 倍，万条笔记下基本秒出结果

#### Fixes
- 修复导出 PDF 时嵌入图片丢失的问题
```

> ⚠️ Breaking change 在 Linear 风格里通常单独发一条公告或在 API 子站说明，不混在面向用户的更新里。如确需写入，加 `#### Breaking` 子标题 + 迁移指引。

---

## 2. Raycast（Emoji + semver）

### 风格说明

**特征**：标题带 semver 版本号（`vX.Y.Z`）；用 Emoji 前缀的 H2 分类（`✨ New` / `💎 Improvements` / `🐞 Fixes` / `🧪 Experiments`）；列表项 `**功能名**：描述`，命令名用内联代码。

**设计意图**：Emoji 提升可扫描性，semver 让版本可追踪。设计质量即产品质量的信号。适合有设计追求的开发者工具。

**最适合**：开发者工具、桌面应用、命令行增强、重视觉品质的产品。

**日期/版本**：`# vX.Y.Z — YYYY-MM-DD` 双标识。

### 模板骨架

```markdown
# vX.Y.Z — YYYY-MM-DD

## ✨ New
- **功能名**：描述（`命令名`）

## 💎 Improvements
- **功能名**：改进描述

## 🐞 Fixes
- **功能名**：修复描述

## 🧪 Experiments （可选，实验性功能）
- **功能名**：描述

## ⚠️ Breaking （如有）
- **功能名**：变更说明 + 迁移指引
```

### 完整示例

```markdown
# v2.4.0 — 2026-07-19

## ✨ New
- **Dark Mode**：在 `Settings → Appearance` 切换，可跟随系统主题

## 💎 Improvements
- **Global Search**：索引重建后搜索速度提升约 3 倍

## 🐞 Fixes
- **Export PDF**：修复导出时嵌入图片丢失的问题

## ⚠️ Breaking
- **API**：字段 `userId` 重命名为 `user_id`。迁移：将请求体中的 `userId` 批量替换为 `user_id`，旧字段将在 v2.6.0 移除
```

---

## 3. Stripe（极简索引型）

### 风格说明

**特征**：极致简洁。每条一句话；用 `[产品域]` 前缀标注归属；整条描述本身就是指向文档的链接；纯文本，无媒体。

**设计意图**：高频更新也能扩展。技术用户要的是"改了什么、去哪看详情"，不需要花哨叙述。

**最适合**：API 服务、基础设施、高频更新、开发者为主的产品。

**日期/版本**：日期分组（`YYYY-MM` 或 `YYYY-MM-DD`），不用版本号。

### 模板骨架

```markdown
## YYYY-MM-DD

- **[产品域]** [一句话描述，整条作为链接](文档地址)
- **[产品域]** [一句话描述](文档地址)

## ⚠️ Breaking changes
- **[产品域]** [变更 + 迁移指引链接](迁移指南地址)
```

### 完整示例

```markdown
## 2026-07-19

- **[App]** [Dark mode is now available in Appearance settings](/docs/appearance)
- **[Search]** [Global search is ~3x faster](/docs/search)
- **[Export]** [Fixed missing images in PDF export](/docs/export#pdf)
- **[API]** ⚠️ Breaking: [`userId` renamed to `user_id`](/docs/migration/user-id)
```

> 若项目没有文档站，链接可省略，保留前缀 + 一句话即可。

---

## 4. Notion（对话式 + UI 路径）

### 风格说明

**特征**：对话式语气，像在跟用户聊天；重利益导向的短段落；UI 路径用代码样式（`Settings → Connections`）；行动导向的链接文本带箭头（`Try it now →`）；加粗强调关键词。

**设计意图**：让更新像一篇轻松的小博客，帮用户理解"这对我有什么用"。

**最适合**：SaaS、消费级产品、面向非技术用户、重产品教育。

**日期/版本**：完整日期，大版本偶尔带版本号。

### 模板骨架

```markdown
## YYYY-MM-DD

### [功能标题，口语化]

[2-3 句对话式段落：先说场景和痛点，再说新功能怎么解决]

- **加粗的关键要点**
- 操作路径：`Settings → 某设置 → 某选项`
- [行动导向链接 →](地址)

#### Also improved / Also fixed
- 简短描述
```

### 完整示例

```markdown
## 2026-07-19

### Say hello to dark mode 🌙

深夜赶文档的时候，白底看着确实刺眼。现在去 `Settings → Appearance` 就能切到暗色模式，也能设置成跟随系统自动切换。

- 支持**手动切换**和**跟随系统**两种模式
- [去试试 →](settings/appearance)

#### Also improved
- 全局搜索**快了约 3 倍**，大库也不卡了

#### Also fixed
- 顺手修了导出 PDF 时图片不见的问题

> ⚠️ 给接入方的同学：API 字段 `userId` 改名为 `user_id`，详见[迁移说明](docs/migration)。
```

---

## 5. Framer（Added/Improved/Fixed 三段式）

### 风格说明

**特征**：单段概述 + 三个 H6 子标题（`Added` / `Improved` / `Fixed`）下的列表；无媒体（或仅大版本配视频）；UI 元素用内联代码。干净、克制。

**设计意图**：结构清晰、信息密度高、不喧宾夺主。适合小步快跑、频繁发版的产品。

**最适合**：设计工具、创意产品、SaaS 小版本更新、希望保持克制专业感的产品。

**日期/版本**：日期作为标题下方的纯文本（`Published YYYY-MM-DD`），大版本在 URL/标题体现。

### 模板骨架

```markdown
## [更新标题]

Published YYYY-MM-DD

[1-2 句概述：本次更新主旨]

###### Added
- 新增内容

###### Improved
- 改进内容

###### Fixed
- 修复内容
```

### 完整示例

```markdown
## Appearance & Search Update

Published 2026-07-19

这次主要补上了暗色模式，顺手把搜索提速了一截。

###### Added
- Dark mode，可在 `Settings → Appearance` 开启，支持跟随系统

###### Improved
- Global search 速度提升约 3 倍

###### Fixed
- Export PDF 嵌入图片丢失

###### Breaking
- API：`userId` → `user_id`（见迁移指南）
```

---

## 6. GitHub（标题索引 + 发布类型标签）

### 风格说明

**特征**：索引式——每条以标题为主，配**发布类型标签**（`Release` / `Improvement` / `Fix` / `Retired`）和领域标签；可选作者署名；正文简短，详情靠链接。引用社区请求可建立信任。

**设计意图**：大规模分类日志，让用户能按类型/领域筛选，快速定位关心的变更。

**最适合**：开源项目、平台型产品、更新极多需要分类的产品。

**日期/版本**：标题带日期前缀（如 `Jul.19 Release`）。

### 模板骨架

```markdown
### [功能标题]
**Tags:** Release, 领域标签  
**Author:** 作者名  
日期: YYYY-MM-DD

[一句话描述]。[了解更多 →](详情地址)

*基于社区反馈实现（可选）*
```

### 完整示例

```markdown
### Dark mode
**Tags:** Release, Appearance  
**Author:** Darwin  
2026-07-19

暗色模式上线，支持跟随系统。在 `Settings → Appearance` 开启。[了解更多 →](/docs/appearance)

### Faster global search
**Tags:** Improvement, Search  
**Author:** Darwin  
2026-07-19

全局搜索速度提升约 3 倍。

### PDF export image loss
**Tags:** Fix, Export  
2026-07-19

修复导出 PDF 时嵌入图片丢失的问题。

### API field rename
**Tags:** Breaking, API  
2026-07-19

`userId` 重命名为 `user_id`，旧字段将在下个大版本移除。[迁移指南 →](/docs/migration)
```

---

## 7. 标准通用（最大公约数）

### 风格说明

**特征**：融合调研提炼的最通用模式——版本/日期标题 + Emoji 四段分类（New / Improved / Fixed / Breaking）+ 功能名加粗 + UI 路径代码化 + 底部相关链接。不偏向任何单一品牌，稳妥百搭。

**设计意图**：当不确定产品调性时的安全默认。结构清晰、信息完整、不会出错。

**最适合**：通用项目、首次接入本 skill、不想绑定特定品牌风格的产品。

**日期/版本**：`## [版本] — YYYY-MM-DD`，版本可选。

### 模板骨架

```markdown
## [版本] — YYYY-MM-DD

### [功能标题]（可选，重大功能才用）
[1-2 句利益导向概述]

#### ✨ New
- **功能名**：描述（`UI 路径`）

#### 💎 Improved
- **功能名**：描述

#### 🐞 Fixed
- **功能名**：修复描述

#### ⚠️ Breaking（如有）
- 描述 + 迁移指引

---
相关链接：[文档](地址) | [讨论](地址)
```

### 完整示例

```markdown
## v2.4.0 — 2026-07-19

#### ✨ New
- **暗色模式**：在 `Settings → Appearance` 开启，支持跟随系统主题

#### 💎 Improved
- **全局搜索**：索引重建后速度提升约 3 倍

#### 🐞 Fixed
- **导出 PDF**：修复嵌入图片丢失的问题

#### ⚠️ Breaking
- **API**：字段 `userId` 重命名为 `user_id`。迁移：批量替换请求体字段名，旧字段将在 v2.6.0 移除。[迁移指南 →](docs/migration)

---
相关链接：[暗色模式文档](docs/appearance) | [更新讨论](discussions/123)
```

---

## 通用占位符说明

| 占位符 | 含义 | 示例 |
|--------|------|------|
| `YYYY-MM-DD` | 发布日期，默认取当天或用户指定 | `2026-07-19` |
| `vX.Y.Z` | semver 版本号，从 git tag 推断或用户指定 | `v2.4.0` |
| `[功能标题]` | 一句话功能名，口语化、利益导向 | `Dark mode, finally` |
| `[产品域]` | 变更所属产品领域 | `Search`、`API`、`Export` |
| `UI 路径` | 菜单/设置路径，用内联代码 | `Settings → Appearance` |
| 图片地址 | 截图/GIF；无素材时留占位符或省略 | `assets/dark-mode.png` |

---

## 风格选择决策树

不确定选哪个时，按项目类型推荐：

```
你的项目是？
├─ API / 基础设施 / SDK          → Stripe（极简）
├─ 开发者工具 / 桌面应用 / CLI   → Raycast（Emoji + semver）
├─ 开源项目 / 更新极多           → GitHub（索引 + 标签）
├─ 面向终端用户的 SaaS
│   ├─ 想讲故事、重教育          → Linear 或 Notion
│   └─ 想克制、频繁小版本        → Framer
├─ 设计 / 创意工具               → Framer 或 Linear
└─ 不确定 / 通用                 → 标准通用（最稳妥默认）
```

无论选哪种，都遵守 SKILL.md 的"关键原则"：利益先行、UI 路径代码化、功能名加粗、Breaking 突出、倒序排列。
