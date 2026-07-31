<!--
CLAUDE.md 模板 —— 由 agents-md skill 生成

核心原则：单一规则源。
- 通用规则全部写在 AGENTS.md（Codex 等其他 agent 也读它）
- 本文件只做两件事：① 用 @AGENTS.md 引用规则源 ② 补充 Claude Code 特化项
- 不要在本文件复制 AGENTS.md 的内容，避免两份文件不同步

如果项目还用其他 agent（Codex / Cursor / Gemini / Copilot），
检查它们的规则文件（.cursorrules / GEMINI.md / .github/copilot-instructions.md），
统一收敛到 AGENTS.md，各自只留特化引用。
-->

@AGENTS.md

# CLAUDE.md

> 项目规则统一在 [AGENTS.md](./AGENTS.md)。本文件只补充 Claude Code 特化项。
> 单一规则源原则：修改项目规则请改 `AGENTS.md`，不要在两份文件之间复制粘贴。

## Claude Code 特化项

### Slash Commands 速查

<!-- 列出本项目用到的 Claude Code slash commands / skills。按类别分组。
     只列项目实际在用的，不堆砌全部。如未启用可删此节。 -->

- **{{流程辅助}}**：{{如 "/openspec-propose、/opsx:apply、/opsx:archive"}}
- **{{调试 / QA}}**：{{如 "/investigate、/qa、/review"}}
- **{{发布}}**：{{如 "/ship、/land-and-deploy"}}

{{启用 superpowers skills（brainstorming、tdd-workflow、systematic-debugging 等）时，遵循其内置流程。}}

### Hooks

<!-- 适用条件：项目有自定义 Claude Code hooks 时才保留。否则删此节 -->

- {{项目与 Claude Code 的集成方式，如 "应用通过 Unix socket 与 hooks 通信，实现见 [路径]"}}
- {{修改 hook 协议时需同步更新 ~/.claude/settings.json}}

### 自检命令速查

<!-- 与 AGENTS.md 的命令速查呼应，但这里只放 Claude Code 会话内最常用的快速验证。
     避免与 AGENTS.md 重复——AGENTS.md 放全集，这里放高频子集。 -->

```bash
{{typecheck 命令}}                      # 类型检查（会话内高频）
{{check 命令}}                          # 快速验证（如改了 trait / 核心逻辑）
{{dev 命令}}                            # 启动应用做手动验证
```
