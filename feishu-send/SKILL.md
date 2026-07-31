---
name: feishu-send
author: wen.yuan
---

# Feishu Send Skill

Send files, text, or markdown messages to Feishu (Lark) users or groups via bot.

**Trigger**: "发到飞书", "发送文件", "发给xxx", "send to feishu", "发消息给xxx"

## Prerequisites

1. Install lark-cli (follow your team's internal guide)
2. Login: `lark-cli auth login`
3. Verify auth: `lark-cli auth status`
4. Bot must have `im:message:send_as_bot` scope enabled

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| file or text | yes | File path or message content |
| target | yes* | User ID (`ou_...`) or Chat ID (`oc_...`). *If not provided, search interactively |

No hardcoded default recipient. Always confirm or search for the target.

## Workflow

### Step 1: Determine Target

- If user specifies a name ("发给张三"): search by name
  ```bash
  lark-cli contact +search-user --query "张三" --format table
  ```
- If user specifies a group ("发到xx群"): search group
  ```bash
  lark-cli im +chat-search --query "群名" --format table
  ```
- If user provides ID directly (`ou_...` / `oc_...`): use it
- If ambiguous (multiple results): ask user to pick

### Step 2: Determine Content Type

| User says | Flag to use |
|-----------|-------------|
| File path / "把xx文件发过去" | `--file` |
| Plain text / "发条消息" | `--text` |
| Markdown content | `--markdown` |

### Step 3: Send

```bash
# Send file (MUST use relative path)
lark-cli im +messages-send --as bot --user-id "ou_xxx" --file "./path/to/file"

# Send text
lark-cli im +messages-send --as bot --user-id "ou_xxx" --text "message"

# Send markdown
lark-cli im +messages-send --as bot --user-id "ou_xxx" --markdown "**bold** text"

# Send to group (use --chat-id instead)
lark-cli im +messages-send --as bot --chat-id "oc_xxx" --file "./path/to/file"
```

### Step 4: Fallback

If file send fails (size limit, permission), fallback to Drive upload:
```bash
lark-cli drive +upload --file "./filename" --name "filename-$(date +%Y%m%d-%H%M%S).ext"
```

## Error Handling

| Error | Action |
|-------|--------|
| Token expired | Run `lark-cli auth login` |
| Permission denied | Check `im:message:send_as_bot` scope |
| File not found | Verify path, suggest alternatives |
| File too large | Fallback to drive upload |
| User not found | Try alternative search terms |
| `--file` absolute path error | Convert to relative path, or use `workdir` |

## Tips

- `--file` only accepts **relative paths** from current directory
- For long content, write to a temp file first, then send with `--file`
- Use `--chat-id` for groups, `--user-id` for individuals (mutually exclusive)
