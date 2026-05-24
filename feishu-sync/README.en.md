# feishu-sync

Bidirectional manual sync tool between local directories and Feishu cloud documents.

Supports four operations: `init` (first-time full push to establish mapping), `push` (local → Feishu), `pull` (Feishu → local), `status` (view differences).

## Features

- **Bidirectional sync**: Local files ↔ Feishu documents / cloud drive files
- **Incremental updates**: Detect changes based on file hash, only sync files with differences
- **Markdown optimization**: `.md` files are converted to Feishu documents (supporting rich text editing), other files are uploaded via cloud drive
- **Diff comparison**: `status` command shows bidirectional differences between local and Feishu
- **New file detection**: `pull`/`status` can detect newly added documents on the Feishu side
- **Conflict alerts**: Detects bidirectional modifications and guides manual merging

## Prerequisites

1. Install and authenticate [lark-cli](https://github.com/nicepkg/lark-cli)
2. Ensure the following scopes are authorized:
   - `drive:drive`: File read/write
   - `search:docs:read`: Detect new Feishu documents (required for `pull`/`status`)

```bash
lark-cli auth login --scope drive:drive
lark-cli auth login --scope search:docs:read
```

## Usage

```bash
/feishu-sync init --dir <local-directory> --folder <Feishu-URL-or-token>
/feishu-sync push [--dir <local-directory>]
/feishu-sync pull [--dir <local-directory>]
/feishu-sync status [--dir <local-directory>]
```

You can also call the script directly:

```bash
python ~/.claude/skills/feishu-sync/scripts/sync.py <subcommand> [options]
```

## Common Workflow

1. **First-time sync**: `init` scans local directory, creates corresponding structure in Feishu, and uploads all files
2. **Daily push**: After local modifications, run `push` to incrementally update to Feishu
3. **Daily pull**: After Feishu modifications, run `pull` to sync to local (including new Feishu files)
4. **View differences**: `status` to view current sync status

## Notes

- Mapping relationships are stored in `.feishu-sync.json`, recommend adding to `.gitignore`
- Feishu side recommends using an empty folder for initialization to avoid naming conflicts
- Markdown round-trip may have format loss
- File size limit: 20MB
- Feishu drive/v1/files API `folder_token` parameter does not take effect; new file detection is implemented via `docs +search` + timestamp filtering

---

[中文版](README.md)
