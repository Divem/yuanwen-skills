# Feishu Message Sender

Send files, text, or Markdown messages to users or groups via Feishu bot.

## Features

- Send files (with automatic fallback to cloud drive upload)
- Send text messages
- Send Markdown messages
- Support searching recipients by username

## Prerequisites

- lark-cli installed
- Logged in: `lark-cli auth login`
- Bot has `im:message:send_as_bot` permission enabled

## Usage

Simply tell Claude:

```
"send to Feishu"
"send file to Zhang San"
"send message to xx group"
"send to feishu"
```

## Send Commands

### Send File

```bash
lark-cli im +messages-send --as bot --user-id "ou_xxx" --file "./path/to/file"
```

### Send Text

```bash
lark-cli im +messages-send --as bot --user-id "ou_xxx" --text "message content"
```

### Send Markdown

```bash
lark-cli im +messages-send --as bot --user-id "ou_xxx" --markdown "**bold** text"
```

### Send to Group

```bash
lark-cli im +messages-send --as bot --chat-id "oc_xxx" --file "./path/to/file"
```

## Find Recipients

Search by username:

```bash
lark-cli contact +search-user --query "Zhang San" --format table
```

Search group:

```bash
lark-cli im +chat-search --query "group name" --format table
```

## Send Failure Fallback

If file sending fails (size limit or permission), automatically fallback to cloud drive upload:

```bash
lark-cli drive +upload --file "./filename" --name "filename-$(date +%Y%m%d-%H%M).zip"
```

## Notes

- `--file` only accepts relative paths
- For long content, write to a temporary file first, then send with `--file`
- Use `--chat-id` for groups, `--user-id` for individuals; the two are mutually exclusive

---

[中文版](README.md)
