# docs-organizer

为任意项目建立标准化的文档目录管理体系。作为 Claude Code skill 运行，支持初始化、诊断两种模式。**仅手动触发，不自动激活**。

## 功能概览

- **初始化（init）** — 为新项目搭建标准 `docs/` 目录结构：目录骨架、`docs-guide.md`、README 索引、CLAUDE.md 规则注入
- **诊断（diagnose）** — 审计现有 `docs/` 目录，检测命名违规、文件错放、缺失交叉引用，输出迁移报告

## 使用方式

在任意项目中调用：

```
/docs-organizer
```

Skill 自动判断工作模式：

| 场景 | 模式 |
|:---|:---|
| 项目没有 `docs/` 目录 | `init` |
| 项目已有 `docs/` 目录 | `diagnose` |

### 初始化模式

创建完整的文档目录结构：

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

同时完成：
- 每个目录生成 `README.md` 索引文件
- 文档管理规则注入 `CLAUDE.md`
- 配置保存到 `.claude/docs-organizer.yaml`

### 诊断模式

扫描 `docs/` 并输出报告：

```
✓ 已合规 (14):
  docs/tech/database-schema.md
  ...

⚠ 不规范 (7):
  docs/PRD.md              → 重命名为 prd/requirements.md
  docs/技术方案.md          → 移动到 tech/，重命名为 kebab-case
  docs/old-plan.md         → 归档到 archive/old-plan.md

⊘ 受保护 (2):
  docs/superpowers/        (框架目录，跳过)
```

支持交互式迁移，使用 `git mv` 保留文件历史。

## 配置

每个项目通过 `.claude/docs-organizer.yaml` 自定义：

```yaml
language: zh                          # zh 或 en
protected_dirs:                       # 受保护目录 — 框架/工具链管理的目录，禁止修改
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
extra_dirs:                           # 标准以外的自定义目录
  # - decisions
```

首次使用时如果不存在配置文件，skill 会通过问答收集偏好并自动保存。

### 受保护目录

`protected_dirs` 中列出的目录完全不受干预：

- 不被移动、重命名或重组
- 诊断扫描时自动跳过

适用于 `superpowers/`、`.vuepress/`、`.docusaurus/` 等框架管理的目录。

## 目录约定

| 目录 | 用途 |
|:---|:---|
| `prd/` | 产品需求、功能规格 |
| `tech/` | 技术文档、设计文档（`-design` 后缀）、数据库 schema |
| `design/` | UI/UX 设计资源、品牌素材、线框图、参考图片 |
| `handover/` | 模块交接文档，面向接手开发者 |
| `research/` | 前瞻性内容：技术调研、可行性分析、竞品分析 |
| `reports/` | 回顾性内容：进度报告、代码审查 |
| `planning/` | 开发计划、里程碑（日期前缀） |
| `archive/` | 废弃但需保留的文档 |
| `raw-source/` | 外部原始参考资料（API 文档、CLI 手册） |

## 命名规则

- 英文 kebab-case，禁止空格和括号
- 禁止版本后缀（`v1`、`v2`、`final`）—— Git 管理历史
- 技术设计文档用 `-design` 后缀：`tech/{topic}-design.md`
- 计划/报告类用日期前缀：`{YYYY-MM-DD}-{topic}-plan.md`
- PRD 与技术设计文档必须在文件头部双向链接

## CLAUDE.md 集成

`init` 运行时，会将精简的文档规则（约 30 行）注入项目的 `CLAUDE.md`：

- 无 CLAUDE.md → 创建新文件并写入规则
- 有 CLAUDE.md 但无文档规则 → 在合适位置插入
- 有 CLAUDE.md 且已有文档规则 → 智能合并（保留自定义规则，补充缺失项）

## 文件结构

```
docs-organizer/
├── SKILL.md                         # 主入口
├── README.md                        # 英文说明
├── README.zh-CN.md                  # 本文件
├── references/
│   ├── full-guide-template.md       # docs-guide.md 参数化模板
│   ├── claude-md-snippet.md         # CLAUDE.md 注入片段
│   └── directory-mapping.md         # 目录 ↔ 文档类型映射 + 命名速查
└── scripts/
    └── diagnose.sh                  # 命令行诊断脚本
```
