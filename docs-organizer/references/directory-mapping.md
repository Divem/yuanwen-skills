# 目录-文档类型映射表

## 标准目录

| 目录 | 存放内容 | 典型文件 |
|:---|:---|:---|
| `prd/` | 产品需求、功能规格、业务逻辑说明 | `dashboard-requirements.md` |
| `tech/` | 技术实现、数据 schema、代码逻辑说明、**技术设计文档**、开发者操作规范 | `database-schema.md`, `sync-engine-design.md` |
| `design/` | UI/UX 规范、品牌、配色、线框图、交互说明、开发参考素材 | `design-token-current.md` |
| `handover/` | 技术交接文档：模块完成后的全貌说明 | `sync-engine.md` |
| `research/` | 调研与分析：技术方案调研、可行性分析、POC 验证、竞品分析 | `tauri-v2-migration-research.md` |
| `reports/` | 回顾性报告：开发进度报告、代码审查报告 | `2026-04-19-progress-report.md` |
| `planning/` | 开发计划、里程碑、路线图 | `2026-04-18-mvp-plan.md` |
| `archive/` | 过时但仍需保留的历史文档 | `old-database-schema.md` |
| `raw-source/` | 外部原始参考资料 | `tauri-api-ref.md` |

## design/ 子目录

| 子目录 | 用途 |
|:---|:---|
| `design/reference/` | 开发参考图片：竞品截图、排版参考 |
| `design/logos/` | Logo/品牌资源 |
| `design/wireframes/` | 线框图/原型 |

## 命名模式速查

### prd/

| 文档类型 | 命名模式 | 示例 |
|:---|:---|:---|
| 产品需求文档 | `{module}-requirements.md` | `dashboard-requirements.md` |
| 功能规格说明 | `{feature}-spec.md` | `session-monitor-spec.md` |

### tech/

| 文档类型 | 命名模式 | 示例 |
|:---|:---|:---|
| 技术设计文档 | `{topic}-design.md` | `sync-engine-design.md` |
| 数据库文档 | `database-schema.md` | `database-schema.md` |
| 数据字段映射 | `data-fields-{source}.md` | `data-fields-claude-code.md` |
| 代码逻辑说明 | `{component}-logic.md` | `hook-socket-logic.md` |
| 经验教训 | `{topic}-lesson.md` | `position-adaptation-lesson.md` |
| 借鉴参考 | `{source}-reference.md` | `design-system-reference.md` |
| 开发者操作规范 | `{topic}-guide.md` | `time-handling-guide.md` |
| 配置手册 | `{tool}-setup.md` | `hooks-setup.md` |

### design/

| 文档类型 | 命名模式 | 示例 |
|:---|:---|:---|
| 设计 Token | `design-token-{scope}.md` | `design-token-current.md` |
| Logo/品牌资源 | `{number}-{name}.{ext}` | `01-logo.svg` |
| 配色方案 | `color-scheme-{theme}.md` | `color-scheme-dark.md` |
| 线框图 | `{screen}-wireframe.{ext}` | `dashboard-wireframe.png` |
| 交互说明 | `{feature}-interaction.md` | `session-panel-interaction.md` |
| 开发参考素材 | 保留原始文件名 | `reference-screenshot.png` |

### research/

| 文档类型 | 后缀 | 示例 |
|:---|:---|:---|
| 技术方案调研 | `-research.md` | `migration-research.md` |
| 可行性分析 | `-feasibility.md` | `feature-feasibility.md` |
| POC 验证记录 | `-poc.md` | `editor-integration-poc.md` |
| 竞品/产品分析 | `-analysis.md` | `competitor-analysis.md` |

### reports/

| 文档类型 | 命名模式 | 示例 |
|:---|:---|:---|
| 代码审查 | `{scope}-code-review.md` | `dashboard-code-review.md` |
| 开发进度报告 | `{date}-progress-report.md` | `2026-04-19-progress-report.md` |

### planning/

| 文档类型 | 命名模式 | 示例 |
|:---|:---|:---|
| 开发计划 | `{date}-{topic}-plan.md` | `2026-04-18-mvp-plan.md` |

### handover/

| 文档类型 | 命名模式 | 示例 |
|:---|:---|:---|
| 技术交接文档 | `{module}.md` | `sync-engine.md` |

### raw-source/

| 文档类型 | 命名模式 | 示例 |
|:---|:---|:---|
| API 文档 | `{platform}-api-ref.md` | `tauri-api-ref.md` |
| CLI 手册 | `{tool}-cli-ref.md` | `claude-code-cli-ref.md` |
| OpenAPI 规范 | `{service}-openapi-spec.yaml` | `dashboard-openapi-spec.yaml` |
| SDK 参考 | `{sdk}-sdk-ref.md` | `tauri-sdk-ref.md` |

## UI 设计 vs 技术设计判断

| 问题 | UI 设计 → `design/` | 技术设计 → `tech/` |
|:---|:---|:---|
| 主要是截图、色值、间距、字体？ | ✅ | ❌ |
| 描述用户看到的界面和操作流程？ | ✅ | ❌ |
| 描述模块职责、接口契约、数据流转？ | ❌ | ✅ |
| 读者是设计师或前端开发者？ | ✅ | ❌ |
| 读者是后端开发者或架构师？ | ❌ | ✅ |

> **简单法则**：涉及"长什么样、怎么点"→ `design/`；涉及"怎么实现、数据怎么流"→ `tech/`。

## 命名合规检查清单

- [ ] 无空格（用连字符替代）
- [ ] 无括号 `()` `[]`
- [ ] 无版本后缀 `v1` `v2` `final` `最新`
- [ ] 英文部分全小写 kebab-case
- [ ] 无下划线（除非代码相关文件）
- [ ] 扩展名正确：`.md` / `.html` / `.png` / `.svg` / `.yaml`
- [ ] 计划/报告类有日期前缀 `YYYY-MM-DD-`
- [ ] tech/ 下设计文档有 `-design` 后缀
