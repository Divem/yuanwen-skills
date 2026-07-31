---
name: agents-md
description: 为项目创建和优化 AGENTS.md（AI agent 行为指南文件，Claude Code / Codex 等通用）。两种模式——(1) 初始化：为新项目生成高质量 AGENTS.md + CLAUDE.md，基于痛点驱动最佳实践（动机层 / 通用编码原则 / 项目红线规则 / 命令速查 / 架构 Gotchas / 提交前自检清单）；(2) 诊断：审查现有 AGENTS.md 的 10 个维度（动机、原则检验标准、红线可执行性、命令准确性、Gotchas 信息密度、自检清单可执行性、CLAUDE.md 关系、篇幅结构、文档适配、可维护性），输出分级报告与优化建议。适用于：新建项目需 AGENTS.md、已有 AGENTS.md 想检查质量、AGENTS.md 过时需优化、CLAUDE.md 与 AGENTS.md 内容重复需收敛。触发场景——用户说"初始化/创建/生成/写一份 AGENTS.md""诊断/检查/审查/优化 AGENTS.md""AGENTS.md 写得怎么样/好不好""帮我的项目定 agent 规则""CLAUDE.md 和 AGENTS.md 怎么组织"。
---

# AGENTS.md 初始化与诊断

为项目生成或优化 `AGENTS.md`——这个文件定义所有 AI agent（Claude Code、Codex 等）在本仓库的行为规则。

## 模式判断

先判断用户要哪种模式：

| 信号 | 模式 |
|---|---|
| 项目里**没有** AGENTS.md（或只有空壳）；说"初始化/创建/生成/写一份 AGENTS.md" | **初始化模式** |
| 项目里**已有** AGENTS.md；说"诊断/检查/审查/优化 AGENTS.md""写得怎么样" | **诊断模式** |

边界情况：用户已有 AGENTS.md 但想"重做"——走诊断模式先评估，再按需重写，不要直接覆盖既有内容（其中可能有真实的项目知识）。

## 核心设计理念（两种模式共用）

一份高质量 AGENTS.md 必须做到四点，初始化时主动满足，诊断时对照检查：

1. **痛点驱动**：每条规则绑定一个"LLM 写代码的陷阱"，有 Why，不是教条。
2. **三层分离**：
   - 通用编码原则层（编码前思考 / 简洁优先 / 精准修改 / 目标驱动）——跨项目稳定
   - 项目红线规则层——项目特定硬约束
   - 项目操作知识层（命令 / Gotchas / 自检）——随项目演化
3. **可验证**：每条原则都有 `**检验标准：**`，能客观判断"是否遵守"。
4. **单一规则源**：`CLAUDE.md` 用 `@AGENTS.md` 引用，只补 Claude 特化项，不复制通用规则。

详见 `references/anatomy.md`（13 章节解剖图与取舍决策）和 `references/principles.md`（4 条通用原则全文 + 红线设计指南）。

---

## 初始化模式工作流

1. **采集项目信息**（实际核对，不臆测——臆测出的命令/路径会成为文档腐烂的源头）：
   - 项目定位 + 技术栈（读 README / package.json / Cargo.toml / go.mod 等）
   - 实际可跑的命令（查 `package.json` scripts / `Makefile` / `Cargo.toml`）
   - 项目规模判定（小/中/大 → 决定章节取舍）
   - 四类红线（一致性 / 工作流 / 安全 / 硬编码）逐一排查
   - "不看就会错"的架构 Gotchas（查 README / 架构文档 / 问用户）
   - 提交规范（`git log --oneline -20` 看实际风格）

2. **基于模板填充**：复制 `assets/AGENTS.template.md` 到项目根，替换所有 `{{占位符}}`。搜索 `{{` 定位所有待填项。

3. **通用原则层原样采用**：直接用模板里的 4 条原则 + 检验标准（见 `references/principles.md`），这是跨项目验证的最佳实践，不要自作聪明重写。

4. **项目层按采集信息填**：红线、命令、Gotchas、自检清单——每条都要具体、可执行、带路径。

5. **同步生成 CLAUDE.md**：用 `assets/CLAUDE.template.md`，只放 `@AGENTS.md` 引用 + Claude 特化项（slash commands / hooks / 高频自检命令）。检查是否还有 `.cursorrules` / `GEMINI.md` / `.github/copilot-instructions.md` 需收敛到 AGENTS.md。

6. **信息不足留 TODO**：宁可留 `<!-- TODO: 待补充 -->` 占位让用户填，也不要编造。说明哪些项需要用户补充。

**篇幅控制**：小项目 50–100 行，中型 150–250 行，大型 250–400 行。超 400 行考虑拆分到 `docs/` 并用"关键参考"索引。

---

## 诊断模式工作流

1. **完整读** AGENTS.md 及 CLAUDE.md（确认引用关系）。通览项目结构，识别项目类型与规模。

2. **逐维度执行 10 维度检查**——**必须实际验证，不臆测**：
   - 命令是否可跑：`cat package.json | jq .scripts` / 读 Makefile / Cargo.toml
   - 文件是否存在：`ls docs/tech/*.md` / `test -f path`
   - 链接是否有效：实际检查"关键参考"里的路径
   - CLAUDE.md 是否与 AGENTS.md 重复：diff 两份文件
   - commit 规范是否与 git 历史一致：`git log --oneline -20`

   10 维度详见 `references/diagnostic.md`：动机层 / 原则检验标准 / 红线质量 / 命令准确性 / Gotchas 信息密度 / 自检清单可执行性 / CLAUDE.md 关系 / 篇幅结构 / 文档适配 / 可维护性。

3. **分级**：每个发现标记 🔴 高（致命）/ 🟡 中（重要）/ 🟢 低（优化）。

4. **输出诊断报告**——按 `references/diagnostic.md` 的报告格式：总览（健康度评分）→ 🔴 致命问题 → 🟡 重要问题 → 🟢 优化项 → 亮点 → 修复优先级。每个问题给**具体位置**和**可执行修复建议**，含可直接套用的改写示例。必须有"亮点"段落（告诉用户哪些不用动，避免过度修改）。

5. **优化优先级**（问题多时按此序）：删腐烂 → 补检验标准 → 红线具体化 → 收敛规则源 → 补动机层 → 补反例表 → 补 Gotchas → 拆过载内容。

---

## 何时读哪个文件

| 文件 | 何时读 |
|---|---|
| `references/anatomy.md` | 两种模式都需要——初始化时按章节填，诊断时对照查缺。含 13 章节解剖 + 章节取舍决策表 + 好坏示例 |
| `references/principles.md` | 初始化模式必读——4 条通用原则全文（可直接复制）+ 通用反例表 + 红线四类来源与设计指南 + 项目适配 checklist |
| `references/diagnostic.md` | 诊断模式必读——10 维度检查矩阵 + 严重度分级 + 常见病症库（6 类）+ 报告输出格式 + 优化优先级 |
| `assets/AGENTS.template.md` | 初始化模式——复制到项目根作为起点，替换 `{{占位符}}` |
| `assets/CLAUDE.template.md` | 初始化模式——生成配套 CLAUDE.md（@AGENTS.md 引用 + Claude 特化项） |

## 关键约束

- **不臆测**：所有命令、路径、技术栈必须实际核对。填不出的留 TODO 占位。
- **不破坏既有内容**：诊断模式不直接改写，先报告再按用户指示优化。重做时保留既有真实项目知识。
- **单一规则源**：通用规则只进 AGENTS.md；CLAUDE.md / .cursorrules / GEMINI.md 收敛为引用。
- **匹配项目语言**：AGENTS.md 用项目主语言（中文项目用中文，英文项目用英文）。模板是中文，按需转写。
