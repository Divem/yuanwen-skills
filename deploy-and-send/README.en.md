# Deploy and Send

Build project, package as zip, and send via Feishu.

## Features

- Auto-build project (runs `build` script)
- Package `dist/` directory as zip
- Send to specified user via Feishu bot
- Auto-fallback to cloud drive upload on failure

## Prerequisites

- `package.json` with `build` script in project root
- lark-cli installed and logged in (`lark-cli auth login`)
- `dist/` directory generated after build

## Usage

Simply tell Claude:

```
"package and send"
"deploy and send"
"send to me"
"only package, don't send"
```

You can also specify parameters:

```
"package xxx project and send to Zhang San"
"package as demo.zip"
```

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| Project directory | Current directory | Path to the project to build |
| Zip filename | `dist.zip` | Output filename |
| Recipient | Default user | Feishu user ID (`ou_...`) |
| Build only | false | Whether to only package without sending |

## Workflow

1. Parse user intent and confirm parameters
2. Run `npm run build` to build the project
3. Package `dist/` as zip
4. Send file via Feishu
5. Fallback to cloud drive upload if sending fails

## Notes

- `--file` parameter must use relative path
- Auto-attempts cloud drive upload on send failure
- Build failure prevents sending step from executing

---

[中文版](README.md)
