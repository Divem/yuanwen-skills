# Feishu Doc Copier

Batch copy Feishu documents (cloud docs / Wiki) to specified locations, preserving original formatting completely.

## Features

- **Batch copy**: Support copying multiple documents at once
- **Format preservation**: Perfectly retain Markdown format, heading levels, list styles
- **Easy to use**: Based on lark-cli, no complex configuration needed
- **Progress display**: Real-time display of copy progress and status
- **Error handling**: Failure of a single document does not affect others

## Installation

### Option 1: Using lark-cli (recommended)

**Pros**: Simple, best format preservation

```bash
# 1. Install lark-cli
npm install -g @larksuite/cli

# 2. Log in to Feishu
lark-cli auth login

# 3. Install this tool
pip install -r requirements.txt
```

### Option 2: Pure Python API (no lark-cli needed)

**Use case**: Environments where npm/nodejs cannot be installed

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Create Feishu app
# Visit https://open.feishu.cn/app to create an app
# Enable permissions: docx:document:readonly, docx:document:write

# 3. Configure credentials
cp .env.example .env
# Edit .env, fill in your App ID and App Secret
```

### Quick Start

```bash
# Clone repository
git clone <repository-url>
cd feishu-doc-copier

# Install dependencies
pip install -r requirements.txt

# Configure (if not using lark-cli)
cp .env.example .env
# Edit .env with credentials

# Test
python scripts/copy_docs.py --help
```

## Two Working Modes

This tool supports two working modes, automatically detected and selected by priority:

### Mode 1: lark-cli mode (high priority)

**Characteristics:**
- Most complete format preservation (headings, lists, code blocks, etc.)
- Supports all Feishu document features
- Simple and reliable implementation

**Requirements:**
- Install Node.js and lark-cli
- Log in to Feishu account

**Auto-detection:** The tool auto-detects if `lark-cli` is installed

### Mode 2: Pure Python API mode (fallback)

**Characteristics:**
- Zero extra dependencies (only Python + requests)
- No Node.js installation needed
- Some complex formats may not convert completely

**Requirements:**
- Create Feishu app (obtain App ID / App Secret)
- Configure environment variables or .env file

**Use cases:**
- Environments where Node.js cannot be installed
- Server/container environments
- Rapid prototyping

### Mode Switching

Tool automatically selects available mode:
```
1. Detect lark-cli → Use CLI mode if available
2. Detect API credentials → Use API mode if available
3. Neither available → Error and prompt for configuration
```

Force specific mode (future version support):
```bash
# Force CLI mode
python scripts/copy_docs.py --mode cli <source> <target>

# Force API mode
python scripts/copy_docs.py --mode api <source> <target>
```

## Usage

### Option 1: Python API (recommended)

```python
from scripts.copy_docs import batch_copy, copy_document

# Batch copy multiple documents
doc_mappings = [
    ("source_token_1", "target_token_1", "Chapter 1: Quick Start"),
    ("source_token_2", "target_token_2", "Chapter 2: Advanced Tips"),
    ("source_token_3", "target_token_3", "Chapter 3: Real-world Cases"),
]

result = batch_copy(doc_mappings)
print(f"Successfully copied {result['success']}/{result['total']} documents")

# Copy single document
ok, msg = copy_document("source_token", "target_token")
print(f"{'✓' if ok else '✗'} {msg}")
```

### Option 2: Config file

1. Create config file `config.json`:

```json
{
  "folder_token": "URd6fDrTllhkVodVFj7cNfd9ndw",
  "documents": [
    {
      "name": "Chapter 1: Quick Start",
      "source": "UTF0w8yt8iIs2Pks3e6cfazOnYc",
      "target": "Fb13dBVX4oj4yZx1z7VcfEz8nUh"
    },
    {
      "name": "Chapter 2: Advanced Tips",
      "source": "WK3DwtPRJiSB34k3zURceqmcnAK",
      "target": "Veu9dbTj4oWu7Ax9CzVcakgxnZg"
    }
  ]
}
```

2. Read config and copy:

```python
import json
from scripts.copy_docs import batch_copy

with open("config.json") as f:
    config = json.load(f)

doc_mappings = [
    (doc["source"], doc["target"], doc["name"])
    for doc in config["documents"]
]

batch_copy(doc_mappings)
```

### Option 3: Command line

```bash
# Copy single document
python scripts/copy_docs.py <source_token> <target_token>

# Example
python scripts/copy_docs.py UTF0w8yt8iIs2Pks3e6cfazOnYc Fb13dBVX4oj4yZx1z7VcfEz8nUh
```

## Complete Example

### Example: Copy a full tutorial set

```python
#!/usr/bin/env python3
"""
Copy Claude Code tutorial to personal space
"""

from scripts.copy_docs import batch_copy

# Define document mappings (source → target)
CHAPTERS = [
    ("UTF0w8yt8iIs2Pks3e6cfazOnYc", "Fb13dBVX4oj4yZx1z7VcfEz8nUh", "Chapter 1: Quick Start"),
    ("WK3DwtPRJiSB34k3zURceqmcnAK", "Veu9dbTj4oWu7Ax9CzVcakgxnZg", "Chapter 2: Integrating Domestic LLMs"),
    ("I0ekw6ODHiDrNNkxvJIcPqAgnKf", "MikXdQMs1oHIxNx6YDYcjwihnGh", "Chapter 3: Basic Operations"),
    ("GiigwIdtyiaQeKkzxLvcGFbKnwf", "NcWidexnhotRL4xzumkcf5rJn5p", "Chapter 4: Text Processing and Creation"),
]

# Execute batch copy
result = batch_copy(CHAPTERS)

# Output results
print("\nCopy Results:")
for doc in result['results']:
    status = "✅" if doc['success'] else "❌"
    print(f"{status} {doc['name']}: {doc['message']}")
```

## How to Get Document Tokens and API Credentials

### Get Document Token

Extract from Feishu document URL:
- Cloud doc: `https://your-domain.feishu.cn/docx/DOC_TOKEN` → `DOC_TOKEN`
- Wiki: `https://your-domain.feishu.cn/wiki/TOKEN` → `TOKEN`

**Example:**
```
URL: https://example.feishu.cn/docx/UTF0w8yt8iIs2Pks3e6cfazOnYc
Token: UTF0w8yt8iIs2Pks3e6cfazOnYc
```

### Get API Credentials (API mode only)

1. **Create Feishu app**
   - Visit [Feishu Open Platform](https://open.feishu.cn/app)
   - Click "Create enterprise self-built app"
   - Fill in app name and description

2. **Enable permissions**
   - Go to app details → Permission Management
   - Search and add the following permissions:
     - `docx:document:readonly` - Read documents
     - `docx:document:write` - Write documents

3. **Get credentials**
   - App details → Credentials and Basic Info
   - Copy `App ID` and `App Secret`

4. **Configure credentials**
   ```bash
   cp .env.example .env
   # Edit .env file
   FEISHU_APP_ID=cli_xxxxxxxxxxxxxxxx
   FEISHU_APP_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

5. **Publish app (important)**
   - App details → Version Management and Release
   - Click "Create version" → "Apply for release"
   - Admin approval required before use

### Create Target Document

If the target document does not exist, create it first:

```bash
lark-cli api POST /open-apis/docx/v1/documents \
  --data '{"title": "Document Title", "folder_token": "YOUR_FOLDER_TOKEN"}'
```

**Response example:**
```json
{
  "code": 0,
  "data": {
    "document": {
      "document_id": "Fb13dBVX4oj4yZx1z7VcfEz8nUh"
    }
  }
}
```

## Notes

1. **Permission requirements**
   - Source document: Read permission required
   - Target location: Write permission required

2. **Format compatibility**
   - ✅ Heading levels (# ## ###)
   - ✅ Ordered/unordered lists
   - ✅ Code blocks
   - ✅ Blockquotes
   - ⚠️ Images: references retained, but ensure target space can access them
   - ⚠️ Internal links: retained, but cross-document links need manual updating

3. **Content limits**
   - Single document size limit: ~50MB
   - Batch copy recommendation: no more than 50 documents at once

## Troubleshooting

### Problem 1: No available copy mode

**Symptom:** `Cannot use any copy mode`

**Solution:**
```bash
# Option A: Install lark-cli
npm install -g @larksuite/cli

# Option B: Configure API credentials
cp .env.example .env
# Edit .env, fill in App ID and App Secret
```

### Problem 2: Incomplete format in API mode

**Symptom:** Some formatting lost after API mode copy

**Cause:** Feishu API returns structured block data; conversion to Markdown may not be complete

**Solution:**
```bash
# Prefer lark-cli mode (best format preservation)
npm install -g @larksuite/cli
lark-cli auth login

# Then re-copy
python scripts/copy_docs.py <source> <target>
```

### Problem 3: Get content failed

**Symptom:** `Failed to get source document`

**Solution:**
```bash
# 1. Check if logged in
lark-cli auth status

# 2. If not logged in, re-login
lark-cli auth login

# 3. Check if document is shared with you
# Open the document in Feishu and confirm access permission
```

### Problem 4: Update failed

**Symptom:** `Failed to update target document`

**Solution:**
```bash
# 1. Check if target document exists
lark-cli api GET /open-apis/docx/v1/documents/TARGET_TOKEN

# 2. Check folder permissions
# Ensure you have write permission to the target folder

# 3. Re-create target document
lark-cli api POST /open-apis/docx/v1/documents \
  --data '{"title": "New Document", "folder_token": "FOLDER_TOKEN"}'
```

### Problem 5: Format lost

**Symptom:** Headings, lists, etc. are not formatted correctly

**Cause:** Content was piped causing format loss

**Correct approach:**
```python
# ✅ Correct: Use Python variables
content = fetch_doc(source_token)
update_doc(target_token, content)

# ❌ Wrong: Piping causes format loss
echo "$content" | lark-cli docs +update ...
```

## How It Works

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Source     │     │  lark-cli    │     │  Target     │
│  (Feishu)   │────▶│  +fetch      │────▶│  (Feishu)   │
└─────────────┘     └──────────────┘     └─────────────┘
                            │
                            ▼
                    ┌──────────────┐
                    │  JSON response│
                    │  markdown    │
                    └──────────────┘
                            │
                            ▼
                    ┌──────────────┐
                    │  lark-cli    │
                    │  +update     │
                    └──────────────┘
```

1. **Fetch**: `lark-cli docs +fetch --doc <token> --format json`
2. **Extract**: Parse JSON, extract `data.markdown`
3. **Update**: `lark-cli docs +update --mode overwrite`

## API Reference

### `copy_document(source_token, target_token)`

Copy a single document.

**Parameters:**
- `source_token` (str): Source document token
- `target_token` (str): Target document token

**Returns:**
- `(bool, str)`: (success flag, message)

**Example:**
```python
ok, msg = copy_document("UTF0w...", "Fb13d...")
# Output: (True, "Copy successful (19250 characters)")
```

### `batch_copy(doc_mappings, verbose=True)`

Batch copy multiple documents.

**Parameters:**
- `doc_mappings` (List[Tuple[str, str, str]]): [(source, target, name), ...]
- `verbose` (bool): Whether to print detailed info, default True

**Returns:**
- `dict`: {"total": int, "success": int, "failed": int, "results": List[dict]}

**Example:**
```python
mappings = [
    ("src1", "tgt1", "Document 1"),
    ("src2", "tgt2", "Document 2"),
]
result = batch_copy(mappings)
# Output: {"total": 2, "success": 2, "failed": 0, "results": [...]}
```

## License

MIT License — free to use and modify

## Contributing

Issues and PRs welcome!

## Tips

1. **First time**: Test by copying 1-2 documents first
2. **Batch copy**: Recommend batching, no more than 20 per batch
3. **Important documents**: Spot-check formatting after copy
4. **Regular backups**: For important documents, perform backup copies regularly

---

**Made with ❤️ for Feishu/Lark users**

[中文版](README.md)
