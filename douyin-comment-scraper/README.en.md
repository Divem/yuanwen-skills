# Douyin Comment Scraper

Scrape Douyin (TikTok China) video comments and write them to Feishu spreadsheet via lark-cli.

## Features

- Playwright headed browser mode to simulate real user behavior
- Auto-expand comment section, scroll loading, and deduplication
- Extract comment nickname, content, like count, time, and region
- Auto-write to Feishu spreadsheet

## Prerequisites

- Node.js
- Playwright (`npm install playwright`)
- lark-cli (`npm install -g @larksuite/cli`)
- Douyin login cookies

## Cookie Setup

Log in to Douyin via browser → F12 → Application → Cookies → `douyin.com`, extract the following cookies:

| Cookie | Required |
|--------|----------|
| `sessionid` | Recommended |
| `sessionid_ss` | Recommended |
| `passport_csrf_token` | Recommended |
| `uid_tt` | Recommended |
| `odin_tt` | Recommended |
| `ttwid` | Required |

## Usage

### Scrape Comments

```bash
node scripts/scrape_comments.js \
  --url "https://www.douyin.com/video/<ID>" \
  --cookies @cookies.json \
  --count 100 \
  --output douyin_comments.json
```

`--cookies` supports two formats:
- JSON array string: `--cookies '[{"name":"sessionid",...}]'`
- File path: `--cookies @cookies.json`

### Upload to Feishu Spreadsheet

```bash
node scripts/upload_to_feishu.js \
  --input douyin_comments.json \
  --title "Douyin Video Comments-20260412"
```

## Notes

- Douyin may pop up security verification; the script auto-dismisses it. Repeated triggers may require manual handling.
- Comments are lazy-loaded; each scroll loads about 10-20 comments.
- Auto-stops after 5 consecutive rounds with no new comments.
- Douyin frontend updates frequently; if extraction fails, check DOM selectors.

---

[中文版](README.md)
