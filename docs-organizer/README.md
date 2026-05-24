# docs-organizer

标准化文档目录管理工具。作为 Claude Code Skill 使用，为新项目快速搭建 `docs/` 结构，或对已有文档目录进行诊断审计。**仅支持手动触发，不会自动激活**。

## 功能特性

- **Init** — 为新建项目搭建标准 `docs/` 结构：目录骨架、`docs-guide.md`、各目录索引 README，以及向 `CLAUDE.md` 注入文档管理规则
- **Diagnose** — 审计现有 `docs/` 目录，检测命名违规、文件错位、缺失交叉引用，并生成迁移报告

## 使用方法

在任意项目中调用：

```
/docs-organizer
```

Skill 自动检测当前情况并选择合适模式：

| 情况 | 模式 |
|:---|:---|
| 无 `docs/` 目录 | `init` |
| 已有 `docs/` 目录 | `diagnose` |

### Init 模式

创建完整文档结构：

```
docs/
├── docs-guide.md
├── prd/
├── tech/
├── design/
├── handover/
├── research/
├── reports/
├── planning/
├── archive/
└── raw-source/
```

额外创建：
- 每个子目录的 `README.md` 索引
- 文档规则注入到项目的 `CLAUDE.md`
- 配置保存到 `.claude/docs-organizer.yaml`

### Diagnose 模式

扫描 `docs/` 并输出报告：

```
✓ 合规 (14):
  docs/tech/database-schema.md
  ...

⚠ 不合规 (7):
  docs/PRD.md              → rename to prd/requirements.md
  docs/技术方案.md          → move to tech/, rename to kebab-case
  docs/old-plan.md         → archive to archive/old-plan.md

⊘ 受保护 (2):
  docs/superpowers/        (框架目录，跳过)
```

支持交互式迁移，使用 `git mv` 保留历史记录。

## 配置

每个项目的配置文件位于 `.claude/docs-organizer.yaml`：

```yaml
language: zh                          # zh 或 en
protected_dirs:                       # 框架目录 — 绝不修改
  - superpowers
  - .vuepress
enabled_dirs:                         # 启用哪些标准目录
  - prd
  - tech
  - design
  - handover
  - research
  - reports
  - planning
  - archive
  - raw-source
extra_dirs:                           # 标准目录之外的自定义目录
  # - decisions
```

若不存在配置，首次运行时将进行交互式问答并保存结果。

### 受保护目录

`protected_dirs` 中列出的目录完全不可触碰：

- 不移动、不更名、不重构
- 诊断扫描时排除

用于处理框架管理的目录，如 `superpowers/`、`.vuepress/`、`.docusaurus/` 等。

## 目录规范

| 目录 | 用途 |
|:---|:---|
| `prd/` | 产品需求、功能规格 |
| `tech/` | 技术文档、设计文档（`-design` 后缀）、Schema |
| `design/` | UI/UX 素材、品牌、线框图、参考图 |
| `handover/` | 模块交接文档，供接手开发者使用 |
| `research/` | 前瞻性：技术研究、可行性分析、竞品分析 |
| `reports/` | 回顾性：进度报告、代码评审 |
| `planning/` | 里程碑计划、路线图（日期前缀） |
| `archive/` | 已废弃但保留的文档 |
| `raw-source/` | 外部参考资料（API 文档、CLI 手册） |

## 命名规则

- 英文 kebab-case，不含空格或括号
- 不加版本后缀（`v1`、`v2`、`final`）— Git 已记录历史
- 技术设计文档使用 `-design` 后缀：`tech/{topic}-design.md`
- 计划/报告使用日期前缀：`{YYYY-MM-DD}-{topic}-plan.md`
- PRD ↔ 技术设计文档必须在文件头部有双向链接

## CLAUDE.md 集成

`init` 运行时会将精简的规则片段（约 30 行）注入项目 `CLAUDE.md`：

- 无 `CLAUDE.md` → 创建并写入片段
- 已有 `CLAUDE.md` 但无文档规则 → 插入规则段落
- 已有 `CLAUDE.md` 含文档规则 → 合并（保留自定义规则，填补缺失项）

## 文件结构

```
docs-organizer/
├── SKILL.md                         # 主入口
├── README.md                        # 本文件
├── references/
│   ├── full-guide-template.md       # 参数化 docs-guide.md 模板
│   ├── claude-md-snippet.md         # 注入 CLAUDE.md 的代码片段
│   └── directory-mapping.md         # 目录 ↔ 文档类型映射 + 命名规范
└── scripts/
    └── diagnose.sh                  # CLI 诊断脚本
```

---

[English Version](README.en.md)
