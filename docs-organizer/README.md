# docs-organizer

Standardized documentation directory management for any project. Works as a Claude Code skill that bootstraps and audits your `docs/` folder. **Manual trigger only — never auto-activates**.

## What it does

- **Init** — Bootstrap a standardized `docs/` structure for new projects: directory scaffold, `docs-guide.md`, README indexes, and CLAUDE.md injection
- **Diagnose** — Audit existing `docs/` directories, detect naming violations, misplaced files, missing cross-references, and produce a migration report

## Usage

Invoke in any project:

```
/docs-organizer
```

The skill auto-detects the right mode:

| Situation | Mode |
|:---|:---|
| No `docs/` directory | `init` |
| Existing `docs/` directory | `diagnose` |

### Init mode

Creates the full documentation structure:

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

Plus:
- `README.md` index in each directory
- Documentation rules injected into `CLAUDE.md`
- Config saved to `.claude/docs-organizer.yaml`

### Diagnose mode

Scans `docs/` and reports:

```
✓ Compliant (14):
  docs/tech/database-schema.md
  ...

⚠ Non-compliant (7):
  docs/PRD.md              → rename to prd/requirements.md
  docs/技术方案.md          → move to tech/, rename to kebab-case
  docs/old-plan.md         → archive to archive/old-plan.md

⊘ Protected (2):
  docs/superpowers/        (framework directory, skipped)
```

Interactive migration with `git mv` to preserve history.

## Configuration

Per-project config at `.claude/docs-organizer.yaml`:

```yaml
language: zh                          # zh or en
protected_dirs:                       # Framework directories — never modify
  - superpowers
  - .vuepress
enabled_dirs:                         # Which standard directories to create
  - prd
  - tech
  - design
  - handover
  - research
  - reports
  - planning
  - archive
  - raw-source
extra_dirs:                           # Custom directories beyond the standard set
  # - decisions
```

If no config exists, the skill runs an interactive Q&A on first use and saves the result.

### Protected directories

Directories listed in `protected_dirs` are completely off-limits:

- Never moved, renamed, or restructured
- Excluded from diagnose scans

This handles framework-managed directories like `superpowers/`, `.vuepress/`, `.docusaurus/`, etc.

## Directory conventions

| Directory | Purpose |
|:---|:---|
| `prd/` | Product requirements, feature specs |
| `tech/` | Technical docs, design docs (`-design` suffix), schema |
| `design/` | UI/UX assets, brand, wireframes, reference images |
| `handover/` | Module handoff docs for developers taking over |
| `research/` | Forward-looking: tech research, feasibility, competitor analysis |
| `reports/` | Retrospective: progress reports, code reviews |
| `planning/` | Milestone plans, roadmaps (date-prefixed) |
| `archive/` | Deprecated but retained docs |
| `raw-source/` | External reference material (API docs, CLI manuals) |

## Naming rules

- English kebab-case, no spaces or parentheses
- No version suffixes (`v1`, `v2`, `final`) — Git tracks history
- Tech design docs use `-design` suffix: `tech/{topic}-design.md`
- Planning/reports use date prefix: `{YYYY-MM-DD}-{topic}-plan.md`
- PRD ↔ tech design docs must have bidirectional links at file head

## CLAUDE.md integration

When `init` runs, a condensed rules section (~30 lines) is injected into the project's `CLAUDE.md`:

- No CLAUDE.md → created with the snippet
- Existing CLAUDE.md without docs rules → section inserted
- Existing CLAUDE.md with docs rules → merged (preserves custom rules, fills gaps)

## File structure

```
docs-organizer/
├── SKILL.md                         # Main entry point
├── README.md                        # This file
├── references/
│   ├── full-guide-template.md       # Parameterized docs-guide.md template
│   ├── claude-md-snippet.md         # CLAUDE.md injection snippet
│   └── directory-mapping.md         # Directory ↔ doc type mapping + naming patterns
└── scripts/
    └── diagnose.sh                  # CLI diagnostic script
```
