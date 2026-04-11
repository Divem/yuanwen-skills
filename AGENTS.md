# AGENTS.md

## Repository Overview

**Multi-project workspace** containing two distinct sub-projects:

1. **zhongseed (种点什么)** - WeChat Mini Program
   - Location: `miniprogram/`, `cloudfunctions/`
   - Type: Agriculture adoption platform (用户认养蔬菜，农夫种植)
   - Tech: WeChat Mini Program + Cloud Functions

2. **feishu-doc-copier** - Python Skill/Tool
   - Location: `feishu-doc-copier/`
   - Type: Lark/Feishu document batch copying utility
   - Tech: Python with dual-mode support (CLI + API)

## Working on feishu-doc-copier (most recent/active)

### Setup
```bash
cd feishu-doc-copier
pip install -r requirements.txt

# Option A: Use lark-cli (recommended, best format preservation)
npm install -g @larksuite/cli
lark-cli auth login

# Option B: Use API mode (fallback, no Node.js required)
cp .env.example .env
# Edit .env: FEISHU_APP_ID=xxx FEISHU_APP_SECRET=xxx
```

### Quick Usage
```bash
# Single document
python scripts/copy_docs.py <source_token> <target_token>

# Batch via Python
python -c "
from scripts.copy_docs import batch_copy
batch_copy([
    ('src_token_1', 'tgt_token_1', 'Doc 1'),
    ('src_token_2', 'tgt_token_2', 'Doc 2'),
])
"
```

### Key Implementation Notes

- **Dual-mode architecture**: Auto-detects lark-cli → falls back to REST API
- **Format preservation**: CLI mode keeps markdown perfectly; API mode may lose complex formatting
- **Never use shell pipes** for content: `echo "$content" | cmd` destroys formatting
- **Always pass content as Python variable** to `subprocess.run(..., text=True)`

### Entry Points
- `scripts/copy_docs.py:FeishuDocCopier` - Main class with auto-mode detection
- `scripts/copy_docs.py:copy_document()` - Single doc copy
- `scripts/copy_docs.py:batch_copy()` - Batch copy with progress

### Testing a Copy
```python
# Test with one doc first
from scripts.copy_docs import copy_document
ok, msg = copy_document("UTF0w8...", "Fb13d...")
print(f"{'✓' if ok else '✗'} {msg}")
```

## WeChat Mini Program (zhongseed)

### Structure
- `miniprogram/` - Mini program source
  - `pages/user/*` - User-facing pages (home, garden, profile)
  - `pages/farmer/*` - Farmer-facing pages (workbench, upload)
  - `pages/common/*` - Shared pages (orders)
- `cloudfunctions/` - WeChat Cloud Functions (Node.js)
- `project.config.json` - WeChat DevTools config

### Development
- Open in WeChat Developer Tools
- AppID placeholder: `YOUR_APPID` (replace for actual deployment)

## Global Notes

- **No shared dependencies** between miniprogram and feishu-doc-copier
- **No build/test scripts** defined at root level
- **Git tracking**: Each sub-project should be considered independently
- **Skill packaging**: `feishu-doc-copier/` can be packaged as `.skill` file via `skill-creator` tooling
