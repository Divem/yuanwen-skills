---
name: douyin-search
description: >
  Use Playwright to search Douyin (抖音) by keyword and extract video metadata
  (title, author, likes, duration, publish time, URL). Optionally write results
  to a Feishu (Lark) spreadsheet via lark-cli. Requires valid Douyin cookies
  for authenticated search. Use when user mentions "搜索抖音", "抖音搜索",
  "douyin search", "抓取抖音视频", "抖音爬虫", or asks to search/scrape
  videos from Douyin with a specific keyword.
metadata:
  author: wen.yuan
---
# Douyin Keyword Search Scraper

Search Douyin by keyword, extract video metadata, optionally export to Feishu.

## Prerequisites

- `playwright` npm package installed (`npm i playwright`)
- Valid Douyin cookies (sessionid, etc.) — cookies expire and must be refreshed
- `lark-cli` on PATH (only if exporting to Feishu)

## Usage

Run the bundled script:

```bash
node scripts/douyin_search.js <keyword> [options]
```

Options:
- `--target N` — max videos to collect (default: 50)
- `--output PATH` — JSON output file (default: `douyin_search_<keyword>.json`)
- `--feishu` — also write results to a Feishu spreadsheet
- `--cookies PATH` — path to a JSON file containing cookie array (see Cookie Config below)
- `--headless` — run in headless mode (default: headed)

Examples:
```bash
node scripts/douyin_search.js openclaw --feishu
node scripts/douyin_search.js "AI编程" --target 30 --output ai_videos.json
node scripts/douyin_search.js 短剧 --headless --feishu
```

## Cookie Config

Create a JSON file (e.g. `cookies.json`) with the required Douyin cookies:

```json
[
  { "name": "sessionid", "value": "<your_value>", "domain": ".douyin.com", "path": "/" },
  { "name": "sessionid_ss", "value": "<your_value>", "domain": ".douyin.com", "path": "/" },
  { "name": "ttwid", "value": "<your_value>", "domain": ".douyin.com", "path": "/" }
]
```

Minimum required cookies: `sessionid`, `sessionid_ss`. Include `ttwid`, `passport_csrf_token`, `sid_guard` if available.

If no `--cookies` flag is provided, the script checks for `douyin_cookies.json` in the current working directory.

## Output

### JSON format

Each entry contains:
- `title` — video title/description
- `author` — creator display name
- `likes` — like count (raw string, e.g. "3.8万", "183")
- `duration` — video length (e.g. "07:40")
- `time` — relative publish time (e.g. "2周前", "12小时前")
- `videoId` — Douyin video ID
- `url` — full video URL

### Feishu spreadsheet

Columns: 视频标题 | 作者 | 点赞数 | 时长 | 发布时间 | 链接
Sheet title: `抖音搜索 - <keyword> (<date>)`

## Notes

- DOM selectors (`.VDYK8Xd7`, `.z2lFLtJ0`, `.ckopQfVu`, `.dW_QmDH1`) use obfuscated class names that may change with Douyin updates. If extraction returns empty results, inspect the page structure and update selectors in `scripts/douyin_search.js`.
- Scroll pagination: the script scrolls the search results page to load more videos. Rate-limited with 2-3.5s random delays.
- The script runs in **headed** mode by default for debugging visibility.
