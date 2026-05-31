# AGENTS.md

## 项目概述

达尔文自定义 Skills 合集。每个 skill 是一个独立工具，通过 `/skill-name` 斜杠命令调用。

## Skill 结构标准

```
skill-name/
├── SKILL.md              # Claude 使用的技能定义（必需，frontmatter + 正文）
│   ├── YAML frontmatter (name, description 必需)
│   └── Markdown 指令
├── README.md             # 给用户的使用说明（必需，中文）
└── bundled/              # 可选资源
    ├── scripts/          # 可执行脚本（确定性/重复性任务）
    ├── references/       # 按需加载的参考文档
    └── assets/           # 输出模板、图标、字体等资源
```

- SKILL.md frontmatter 必须包含 `name` 和 `description` 字段
- SKILL.md 语言不限（中文或英文均可）
- README.md 使用中文

### 渐进式加载

Skills 使用三级加载系统，控制上下文大小：

| 层级 | 内容 | 加载时机 | 建议大小 |
|------|------|----------|----------|
| 1. Metadata | `name` + `description` | 始终加载 | ~100 字 |
| 2. SKILL.md 正文 | Markdown 指令 | Skill 触发时加载 | <500 行 |
| 3. 资源文件 | scripts/references/assets | 按需加载 | 无限制 |

**最佳实践：**
- SKILL.md 正文控制在 500 行以内；超过时添加层级结构，用清晰的指针引导下一步
- 从 SKILL.md 清楚引用参考文件，说明何时读取
- 大参考文件 (>300 行) 必须包含目录
- 按域组织参考文件（如 `references/aws.md`、`references/gcp.md`）

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

**每次代码改动后必须立即 commit**，不要积攒多个改动一次性提交。这样便于：
- 随时回滚到任意版本
- 清晰追踪每次改动的内容和原因
- 对比不同版本的效果

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

## 严格要求

### 修改前确认
对任何 skill 进行修改前，必须先向用户说明修改内容和范围，等待用户确认后再执行。

### 修改后同步检查
每次修改完成后，执行以下检查：

1. 检查 `/Users/dawinyuan/.cursor/skills/` 下是否存在同名 skill
2. 如存在，对比两个目录的内容差异（可用 `diff -rq`）
3. 如存在差异，向用户报告：
   > "发现 `.cursor/skills/<name>` 与当前仓库存在差异，是否使用 skill-backup 进行同步？"
4. 等待用户确认后再执行同步操作

### 知识库同步检查
修改完成后，如存在知识库同步关系，检查是否需要同步更新相关文档。
