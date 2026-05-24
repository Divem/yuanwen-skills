# Douyin Search Scraper

Search Douyin videos by keyword, extract video metadata (title, author, likes, duration, publish time, link), optionally write to Feishu spreadsheet.

## Features

- Search Douyin videos by keyword
- Extract title, author, likes, duration, publish time, link
- Support export to JSON or Feishu spreadsheet
- Headless / headed browser mode options

## Prerequisites

- Node.js
- Playwright (`npm i playwright`)
- Valid Douyin cookie (needs periodic refresh)
- lark-cli (when exporting to Feishu)

## Cookie Setup

Create `cookies.json`:

```json
[
  { "name": "sessionid", "value": "<your_value>", "domain": ".douyin.com", "path": "/" },
  { "name": "sessionid_ss", "value": "<your_value>", "domain": ".douyin.com", "path": "/" },
  { "name": "ttwid", "value": "<your_value>", "domain": ".douyin.com", "path": "/" }
]
```

Minimum required: `sessionid`, `sessionid_ss`

## Usage

```bash
node scripts/douyin_search.js <keyword> [options]
```

Options:

| Option | Description |
|--------|-------------|
| `--target N` | Max videos to collect (default: 50) |
| `--output PATH` | JSON output file path |
| `--feishu` | Also write to Feishu spreadsheet |
| `--cookies PATH` | Cookie file path |
| `--headless` | Headless mode (default: headed) |

Examples:

```bash
node scripts/douyin_search.js openclaw --feishu
node scripts/douyin_search.js "AI programming" --target 30 --output ai_videos.json
node scripts/douyin_search.js short-drama --headless --feishu
```

## Output Format

### JSON Fields

- `title` — Video title
- `author` — Author nickname
- `likes` — Like count (e.g., "38K", "183")
- `duration` — Video duration (e.g., "07:40")
- `time` — Relative publish time (e.g., "2 weeks ago")
- `videoId` — Douyin video ID
- `url` — Full video link

### Feishu Spreadsheet

Columns: Video Title | Author | Likes | Duration | Publish Time | Link

## Notes

- Douyin DOM selectors use obfuscated class names, may change with updates
- Built-in 2-3.5s random delay to prevent rate limiting
- Default headed mode for easy debugging

---

[中文版](README.md)
