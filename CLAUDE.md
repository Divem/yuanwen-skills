# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

达尔文自定义 Skills 合集。每个 skill 是一个独立工具，通过 `/skill-name` 斜杠命令调用。

## Skill 结构标准

```
skill-name/
├── SKILL.md              # Claude 使用的技能定义（必需，frontmatter + 正文）
├── README.md             # 给用户的使用说明（必需，中文）
├── scripts/              # 可执行脚本
└── ...
```

- SKILL.md frontmatter 必须包含 `name` 和 `description` 字段
- SKILL.md 语言不限（中文或英文均可）
- README.md 使用中文

## 开发工作流

Skills 在 `~/.claude/skills/<name>/` 开发和测试，完成后通过 skill-backup 或手动复制到本仓库。

## 提交规范

使用 conventional commits + scope：

```
feat(scope): 新功能
fix(scope): 修复
docs(scope): 文档更新
chore: 杂项
```

scope 为 skill 目录名（如 `feishu-sync`、`douyin-search`）。

**重要规则：提交到 GitHub 前必须检查并更新 README.md**，确保文档与代码同步。

## 关键依赖

| Skill | 依赖 |
|-------|------|
| feishu-sync / feishu-send / feishu-doc-copier / feishu-doc-download | lark-cli（需 auth login 授权对应 scope） |
| douyin-comment-scraper | Node.js, playwright |
| bilibili-comment-crawler | Python |
| deploy-and-send | Python |

## 飞书 API 已知限制

- `/open-apis/drive/v1/files` 的 `folder_token` 参数不生效，始终返回根目录内容
- `docs +search` 的 `--filter folder_tokens` 被接受但无实际效果
- 新文件检测通过 `docs +search` + `create_time` 时间过滤实现
- `lark-cli api DELETE` 需要 `--params '{"type":"docx"}'`（非 `--data`）

## Release Notes 规范

**标题格式：** `Coder Friends v{版本号}`

```markdown
## Coder Friends v{版本号}

> 一句话版本摘要，说明这个版本的核心主题或推荐升级理由。

### 新增功能
- 功能描述

### 修复问题
- 修复了 xxx 的问题

### 优化改进
- 优化了 xxx
```

**写作规则：**
- 用用户能理解的语言，不要出现 commit hash、函数名、文件路径
- 每个条目说清楚"用户能感知到什么变化"
- `git log --oneline` 的输出只用于自己梳理，不要原样复制到 Release Notes
- 没有内容的分类直接跳过，不留空标题
