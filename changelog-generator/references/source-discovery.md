# 素材扫描指南

各 AI 编码工具开发日志的存放位置、定位本项目的方法、解析要点。

> **核心原则**：这些日志是**原始素材**，噪音很大（大量探索、试错、回滚）。扫描阶段只做"发现 + 列清单"，提炼交给第 5 步。不要把整个 session 读进上下文——先按时间筛选，再抓关键信号。

## 目录

- [一图速查：各工具路径](#一图速查各工具路径)
- [定位本项目的方法](#定位本项目的方法)
- [逐工具解析要点](#逐工具解析要点)
- [快速发现命令（可直接复制）](#快速发现命令可直接复制)
- [git 区间](#git-区间)
- [变更计划类文档](#变更计划类文档)
- [降噪与去重](#降噪与去重)

---

## 一图速查：各工具路径

| 工具 | 日志位置 | 定位本项目方式 |
|------|---------|---------------|
| Claude Code | `~/.claude/projects/<项目hash>/*.jsonl` | 项目绝对路径的 `/` 全替换为 `-` |
| Codex | `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl` | 解析 jsonl，按 `cwd` 字段过滤 |
| OpenCode | `~/.local/share/opencode/storage/session/<hash>/ses_*.json` | 先读 `storage/project/<hash>.json` 反查项目→hash |
| Qoder | `~/.qoder/plans/*.md` + 项目内 `.qoder/` | plans 按项目组织；项目内 `.qoder/` 直接读 |
| WorkBuddy | `~/.workbuddy/{traces,plans,tasks}/` + 项目内 `.workbuddy/` | 按 workspace/时间筛选 |

> 路径会随工具版本变化。若某路径不存在，问用户该工具的日志存在哪，或直接用 git log + 用户口述。

---

## 定位本项目的方法

skill 执行时，当前工作目录通常就是项目根（`$PWD`）。各工具用不同方式关联项目：

### Claude Code

把项目绝对路径的所有 `/` 替换为 `-`，即为目录名：

```bash
# 项目 /Users/foo/myapp → 目录 -Users-foo-myapp
PROJECT_HASH="${PWD//\//-}"
ls -t ~/.claude/projects/"$PROJECT_HASH"/*.jsonl
```

### Codex

rollout 文件里 `cwd` 字段（可能嵌套在 `turn_context` / `session_meta`）记录工作目录。需解析后过滤：

```bash
# 列出近期 rollout 中包含本项目路径的文件
grep -l "\"$PWD\"" ~/.codex/sessions/*/*/*/rollout-*.jsonl 2>/dev/null
```

### OpenCode

`storage/project/<hash>.json` 存了 hash → 项目路径的映射：

```bash
# 反查本项目对应的 session hash
grep -rl "$PWD" ~/.local/share/opencode/storage/project/*.json
```

拿到 hash 后读 `storage/session/<hash>/ses_*.json`。也可直接查 `opencode.db`（sqlite）。

### Qoder / WorkBuddy

plans/traces 多为 markdown 或按项目分目录。直接列文件、读内容判断归属即可。

---

## 逐工具解析要点

### Claude Code（`.jsonl`）

每行一个事件。**有价值的信号**：

- `tool_use` 中 `name=Edit|Write|MultiEdit`：实际改了哪些文件 → 推断功能模块
- `tool_use` 中 `name=Bash` 含 `git commit`：提取 commit message
- `user` / `assistant` 的总结性消息：往往直接说出"做了什么"
- 文件路径模式：`src/features/search/*` → 搜索相关改动

**忽略**：`Read`、探索性的 `Grep`/`Glob`、来回试错、被打断的任务。

### Codex（rollout `.jsonl`）

记录按 `type` 字段分类：`session_meta`、`event_msg`、`response_item`、`turn_context`。

- `response_item` 里的 function call（如改文件、跑命令）= 实际动作
- `event_msg` 里的 commit / completion = 里程碑
- 用 `cwd` 过滤出本项目

### OpenCode（`ses_*.json`）

session 是结构化 JSON，含消息列表和 tool 调用。提取逻辑同 Claude Code：抓"改了哪些文件 + 用户/助手的总结"。

### Qoder（`.md` plans）

plans 是人/ agent 可读的 markdown，通常直接写明"本次要做什么"。**这是高质量素材**——变更计划往往就是 changelog 的草稿。直接读全文。

### WorkBuddy

- `traces/`：开发过程记录（类似 session）
- `plans/`：变更计划（同 Qoder，高质量）
- `tasks/`：任务列表，能反映"完成了哪些"

---

## 快速发现命令（可直接复制）

下面这段会列出本项目近 7 天、各工具的候选素材。把 `DAYS=7` 改成你要的区间：

```bash
DAYS=7
PROJECT_HASH="${PWD//\//-}"

echo "### Claude Code sessions"
find ~/.claude/projects/"$PROJECT_HASH" -name '*.jsonl' -mtime -$DAYS 2>/dev/null | head -20

echo "### Codex rollouts (本项目)"
grep -l "\"$PWD\"" ~/.codex/sessions/*/*/*/rollout-*.jsonl 2>/dev/null | xargs -I{} sh -c 'test $(($(date +%s) - $(date -r "{}" +%s))) -lt $((DAYS*86400)) && echo {}' 2>/dev/null | head -20

echo "### OpenCode sessions (本项目)"
grep -rl "$PWD" ~/.local/share/opencode/storage/project/*.json 2>/dev/null

echo "### Qoder plans"
find ~/.qoder/plans -name '*.md' -mtime -$DAYS 2>/dev/null
find "$PWD/.qoder" -type f 2>/dev/null | head

echo "### WorkBuddy traces/plans/tasks"
find ~/.workbuddy/{traces,plans,tasks} -mtime -$DAYS 2>/dev/null | head -20
find "$PWD/.workbuddy" -type f 2>/dev/null | head

echo "### 项目内变更计划文档"
find "$PWD" -maxdepth 3 \( -path '*/node_modules/*' -o -path '*/.git/*' \) -prune -o -type f \( -iname '*plan*' -o -path '*openspec/changes*' -o -iname '*proposal*' \) -mtime -$DAYS -print 2>/dev/null | head -20
```

> 命令只为**列清单**，不要把所有文件内容一次性读进来。拿到清单后，逐个判断是否相关，相关再读。

---

## git 区间

git log 是最可靠的"客观变更"来源，优先级高。确定区间方法：

```bash
# 方法1：从最近的 tag/版本到现在（最常用）
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null)
git log ${LAST_TAG}..HEAD --oneline --no-merges

# 方法2：最近 N 天
git log --since="$DAYS days ago" --oneline --no-merges

# 方法3：按日期（已知上次 changelog 日期）
git log --since="2026-07-12" --oneline --no-merges

# 看改了哪些文件（推断功能模块）
git log ${LAST_TAG}..HEAD --name-only --pretty=format: | sort -u | grep -v '^$'
```

commit message 是技术视角，提炼时要翻译成用户视角（见 `writing-rules.md`）。

---

## 变更计划类文档

这些是**高质量素材**，因为它们本就是"打算做什么"的陈述，往往接近 changelog 草稿：

| 类型 | 常见位置 |
|------|---------|
| OpenSpec | `openspec/changes/*/`（proposal、tasks、spec） |
| Qoder plans | `~/.qoder/plans/*.md`、项目内 `.qoder/` |
| WorkBuddy plans | `~/.workbuddy/plans/` |
| 通用 plan 文档 | 项目内 `*.md`（含 plan/proposal/roadmap/design） |

读这些时注意区分"计划"和"已落地"——计划里写了的不一定都做了。结合 git log 和工具日志交叉验证"实际完成的部分"。

---

## 降噪与去重

原始素材的常见噪音，扫描时主动过滤：

1. **探索性操作**：`Read`、`Grep`、`Glob`、来回查看——不算变更。
2. **试错与回滚**：改了又改回的，最终状态以 git 为准。
3. **重复出现**：同一功能在 Claude Code、Codex、git 里都出现——只取最完整的描述，写一次。
4. **环境/配置琐碎**：装依赖、改 lint 配置——除非影响用户，否则不写。
5. **调试过程**：打印日志、临时注释——不写。

**交叉验证**：以 git log 为客观骨架（确实改了），用工具日志补充"为什么改、用户价值"（git message 通常写不出这些）。
