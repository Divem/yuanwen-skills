---
name: docs-organizer
author: wen.yuan
description: "文档目录管理。Init: 初始化 docs/ 结构。Diagnose: 诊断现有文档。跨工具通用 — 支持 Claude Code、OpenCode、Cursor、Cline 等。仅手动触发。"
---
# docs-organizer

Standardized documentation management for any project. Two modes: **init** (bootstrap), **diagnose** (audit). **手动触发 only** — must be explicitly invoked by user.

## Quick Start

When the user invokes `/docs-organizer`, determine the mode:

| User says... | Mode |
|:---|:---|
| "初始化文档", "setup docs", "新建 docs 规范" | `init` |
| "诊断文档", "整理 docs", "audit docs", project already has docs/ | `diagnose` |
| No clear intent → has `docs/` | `diagnose` |
| No clear intent → no `docs/` | `init` |

---

## Configuration

Load config from project root `.claude/docs-organizer.yaml` if it exists. If not found, use defaults and offer to create one.

### Config Schema

```yaml
# .claude/docs-organizer.yaml
language: zh                # zh or en — language for docs-guide.md
protected_dirs:             # Directories inside docs/ that are managed by frameworks/tools — never modify
  - superpowers
  - .vuepress
  - .docusaurus
enabled_dirs:               # Which standard directories to create. Uncomment to customize.
  - prd
  - tech
  - design
  - handover
  - research
  - reports
  - planning
  - archive
  - raw-source
extra_dirs:                 # Custom directories beyond the standard set
  # - decisions           # example: architecture decision records
```

### Config Resolution Order

1. `.claude/docs-organizer.yaml` in project root
2. Interactive Q&A (first run, then save to config)
3. Built-in defaults

---

## Mode: init

Initialize docs management for a project that has no (or minimal) docs/ structure.

### Steps

1. **Detect existing state**
   - Check if `docs/` exists
   - If yes, list top-level contents
   - Check if CLAUDE.md exists and already has docs rules

2. **Collect preferences** (skip if config file exists)
   - Ask which standard directories to enable (show descriptions from `references/directory-mapping.md`)
   - Ask about protected directories: "Are there framework-managed dirs in docs/ (e.g., superpowers/)?"
   - Ask language preference (zh/en)
   - Save answers to `.claude/docs-organizer.yaml`

3. **Create directory structure**
   ```bash
   mkdir -p docs/{prd,tech,design,handover,research,reports,planning,archive}
   # Only create directories listed in enabled_dirs config
   ```

4. **Generate docs-guide.md**
   - Load `references/full-guide-template.md`
   - Replace template variables: `{{project_name}}`, `{{enabled_dirs}}`, `{{protected_dirs}}`
   - Write to `docs/docs-guide.md`

5. **Create README.md index in each directory**
   - Each README.md has a table header ready for entries
   - Format: `| File | Topic | Last Updated |`

6. **Inject CLAUDE.md rules**
   - Load `references/claude-md-snippet.md`
   - If no CLAUDE.md → create one with the snippet
   - If CLAUDE.md exists without docs rules → insert after "开发规则" or "自检" section
   - If CLAUDE.md already has docs rules → merge: keep custom rules + add missing items

7. **Report results**
   ```
   ✓ Created docs/ structure (prd/, tech/, design/, ...)
   ✓ Generated docs/docs-guide.md
   ✓ Created directory README.md indexes
   ✓ Injected docs rules into CLAUDE.md (line XX)
   ✓ Saved config to .claude/docs-organizer.yaml
   ```

---

## Mode: diagnose

Audit an existing docs/ directory and produce a migration report.

### Steps

1. **Load config** (or create interactively)

2. **Scan docs/**
   - Recursively list all files
   - Classify each file:
     - ✓ Compliant (correct directory + valid naming)
     - ⚠ Non-compliant (wrong dir, bad naming, missing cross-ref)
     - ⊘ Protected (in a protected_dirs path)

3. **Compliance checks**
   For each file, verify against `references/directory-mapping.md`:

   | Check | Rule |
   |:---|:---|
   | Directory | File type matches expected directory |
   | Naming | No spaces, no parens, no version numbers, kebab-case |
   | Cross-ref | PRD ↔ tech design docs have mutual links |
   | Index | Directory README.md lists the file |
   | Stale | Files in planning/ that are older than 3 months |

4. **Generate report**
   ```
   Scanned docs/ — 23 files found:

   ✓ Compliant (14):
     docs/tech/database-schema.md
     docs/prd/dashboard-requirements.md
     ...

   ⚠ Non-compliant (7):
     docs/PRD.md              → rename to prd/requirements.md
     docs/技术方案.md          → move to tech/, rename to {topic}-design.md
     docs/old-plan.md         → archive to archive/old-plan.md

   ⊘ Protected (2):
     docs/superpowers/        (framework directory, skipped)
   ```

5. **Interactive migration** (if user confirms)
   - Use `git mv` for each file to preserve history
   - Update directory README.md indexes
   - Add cross-references where missing

---

## Template Variable Reference

When generating files from templates, replace these variables:

| Variable | Source | Example |
|:---|:---|:---|
| `{{project_name}}` | Directory name or `package.json` name | "coder-friends" |
| `{{enabled_dirs}}` | Config `enabled_dirs` | "prd, tech, design" |
| `{{protected_dirs}}` | Config `protected_dirs` | "superpowers" |
| `{{language}}` | Config `language` | "zh" |
| `{{date}}` | Current date | "2026-04-23" |

---

## File References

Load these on demand — do NOT load them into context unless the current mode needs them:

| File | When to load |
|:---|:---|
| `references/full-guide-template.md` | init mode — generating docs-guide.md |
| `references/claude-md-snippet.md` | init mode — injecting CLAUDE.md rules |
| `references/directory-mapping.md` | all modes — validating file placement and naming |