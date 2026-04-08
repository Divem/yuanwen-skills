---
name: deploy-and-send
description: Build project into a zip and send via Feishu (lark-cli). Use when the user says "deploy", "build and send", "打包发送", "部署并发送", "发给我", "构建并推送", or wants to share the latest build artifact.
---

# Deploy and Send

Build project, zip `dist/`, send via Feishu.

## Defaults

Silently use these values — do NOT ask unless the user requests a change:

| Parameter | Default |
|-----------|---------|
| `project-dir` | current working directory |
| `zip-name` | `dist.zip` |
| `user-id` | `ou_342b526d834b2519ffcb8de48e9addc1` |
| `build-only` | false (build + send) |

## Workflow

1. Parse user intent for parameter overrides (e.g. "发给我" → use default; "发给张三" → ask for user-id; "只打包" → build-only=true). Use AskUserQuestion only when the user's intent is ambiguous or refers to a different value.
2. Build and zip:
   ```bash
   bash <skill-path>/scripts/build-and-zip.sh <project-dir> <zip-name>
   ```
3. If `build-only` is false, send via Feishu:
   ```bash
   lark-cli im +messages-send --as bot --user-id <user-id> --file <zip-name>
   ```
4. If send fails (size limit or permission), fallback to Drive upload:
   ```bash
   lark-cli drive +upload --file <zip-name> --name "<name>-$(date +%Y%m%d-%H%M).zip"
   ```

## Parameter Override Guide

When the user's request implies a non-default value, ask for the specific info:

- **Different recipient** ("发给张三"): ask for open_id or search via `lark-cli contact +search-user`
- **Different zip name** ("打包成 demo.zip"): use the specified name
- **Build only** ("只打包不发" / "只构建"): set build-only=true, skip send
- **Different project** ("打包 xxx 项目"): use the specified project dir

## Error Handling

- Token expired (`lark-cli auth status`): run `lark-cli auth login`
- Build fails: report error, do not send
- Send permission error: suggest checking `im:message:send_as_bot` scope
