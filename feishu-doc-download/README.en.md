# Feishu Document Downloader

Download Feishu documents via Open API, parse block structure, and generate formatted local Markdown files.

## Features

- Preserve headings, lists, bold, code blocks, quotes, tables, and other formatting
- Use blocks API (not the `raw_content` plain text interface)
- Support document and image download
- Support knowledge base documents (wiki)

## Prerequisites

- Python 3
- Feishu app credentials (`app_id`, `app_secret`)

### Required API Permissions

- `docx:document:readonly` — Read document content
- `wiki:node:read` — Knowledge base documents

## Usage

Simply tell Claude:

```
"Download this Feishu document"
"Save Feishu document to local"
"Export Feishu document as Markdown"
```

And provide the Feishu document URL.

## Key Notes

1. **Do NOT use `raw_content` API**: It only returns plain text, with no formatting
2. **Do NOT rely on feishu CLI**: `feishu auth device-flow` often times out or errors
3. **Use tenant_access_token + blocks API directly**: Stable and reliable

## Block Type Support

| Type | Markdown Output |
|------|----------------|
| Heading 1-9 | `#` to `#########` |
| Normal text | Paragraph |
| Unordered list | `- item` |
| Ordered list | `1. item` |
| Code block | ```lang ... ``` |
| Quote | `> text` |
| Todo | `- [ ] text` / `- [x] text` |
| Divider | `---` |
| Image | `![image](url)` |
| Table | Markdown table |

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Auth error | Wrong app_id/app_secret | Check credential file |
| Document access denied | App lacks permission | Enable `docx:document:readonly`, share document with app |
| Empty content | Document empty or insufficient permission | Check if blocks response is empty |
| Format lost | Used `raw_content` API | Switch to blocks API |

---

[中文版](README.md)
