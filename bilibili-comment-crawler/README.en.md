# Bilibili Comment Crawler

Collect comment data from Bilibili videos. Supports pagination, sub-reply expansion, and writing to Feishu spreadsheet.

## Features

- **Pagination**: Auto-fetch all comments by page (20 per page)
- **Sub-reply expansion**: Extract sub-replies under top-level comments
- **Feishu export**: Write results to Feishu spreadsheet
- **Data cleaning**: Auto-strip HTML tags and newlines

## Prerequisites

- Python 3
- curl (for API requests)
- Bilibili login cookie (only 3 comments available without login)
- lark-cli (when writing to Feishu spreadsheet)

## Cookie Setup

### How to Obtain

1. Open bilibili.com in Chrome and log in
2. F12 → Application → Cookies → `www.bilibili.com`
3. Copy these 4 items: `SESSDATA`, `bili_jct`, `DedeUserID`, `DedeUserID__ckMd5`

### Configuration (choose one)

**Option 1: Config file (recommended)**

Edit `~/.claude/skills/bilibili-comment-crawler/cookie.json`:

```json
{
  "SESSDATA": "xxx",
  "bili_jct": "xxx",
  "DedeUserID": "xxx",
  "DedeUserID__ckMd5": "xxx"
}
```

**Option 2: Environment variable**

```bash
export BILIBILI_COOKIE="SESSDATA=xxx; bili_jct=xxx; DedeUserID=xxx; DedeUserID__ckMd5=xxx"
```

**Option 3: Command-line argument**

```bash
--cookie "SESSDATA=xxx; ..."
```

## Usage

### Crawl Comments

```bash
python3 scripts/bilibili_comments.py <BV or URL> [options]
```

Common options:

| Option | Description |
|--------|-------------|
| `--cookie` | Cookie string |
| `--limit` | Max comment count (default: 100) |
| `--sort` | Sort mode, `2`=by time (default), `1`=by popularity |
| `--no-sub` | Exclude sub-replies (included by default) |
| `--rows` | Output as 2D array format (for Feishu writing) |
| `--output` | Output file path (default: stdout) |

Example:

```bash
python3 scripts/bilibili_comments.py BV1ooDyBmE6v \
  --cookie "$BILIBILI_COOKIE" \
  --limit 100 \
  --output /tmp/bili_comments.json
```

### Write to Feishu Spreadsheet

```bash
# 1. Crawl comments (output as row array)
python3 scripts/bilibili_comments.py BV1ooDyBmE6v \
  --cookie "$BILIBILI_COOKIE" --limit 100 --rows \
  --output /tmp/bili_rows.json

# 2. Create Feishu spreadsheet and write
ROWS=$(cat /tmp/bili_rows.json)
lark-cli sheets +create \
  --title "Bilibili Video Comments - BV1ooDyBmE6v" \
  --headers '["#","Username","Level","Comment","Likes","Time","Replies","Is Top-Level"]' \
  --values "$ROWS"
```

## Notes

- Only 3 comments returned without login
- Only 3 sub-replies returned by default
- Built-in 0.5s delay to prevent rate limiting
- `cookie.json` contains sensitive information; exclude it when sharing the skill

---

[中文版](README.md)
