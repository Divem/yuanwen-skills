# Skill Backup

Backup, sync, and restore Claude Code custom Skills.

## Features

- Backup Skills to specified directory
- Sync Skill changes
- Restore Skills to new environment
- Smart identification of self-built Skills

## Usage

### Quick Start

```bash
# Backup all self-built Skills
# Default backup to ~/Documents/coder/yuanwen-skills/

# In Claude, simply say:
"backup skills"
"export my skills"
"sync skills"
```

### Manual Backup

```bash
# Copy a single skill
cp -r ~/.claude/skills/my-skill ~/Documents/coder/yuanwen-skills/

# Use rsync (recommended)
rsync -av --delete ~/.claude/skills/my-skill/ ~/Documents/coder/yuanwen-skills/my-skill/
```

### Change Detection

```bash
# Detect changes
if diff -rq ~/.claude/skills/my-skill ~/Documents/coder/yuanwen-skills/my-skill > /dev/null 2>&1; then
    echo "No changes, skip"
else
    echo "Changes detected, need backup"
    rm -rf ~/Documents/coder/yuanwen-skills/my-skill
    cp -r ~/.claude/skills/my-skill ~/Documents/coder/yuanwen-skills/
fi
```

## How It Works

### Identify Self-built Skills

```
~/.claude/skills/
├── superpowers:xxx/     ← System built-in, skip
├── npm-installed/       ← npm installed, skip (has package.json)
└── my-custom-skill/     ← Self-built Skill, backup ✓
```

**Exclusion rules**:
- ❌ `superpowers:` prefix - System built-in Skills
- ❌ Contains `node_modules/` or `package.json` - Third-party npm Skills
- ✅ Others - Self-built Skills

### Backup Modes

1. **Full backup** (first time)
   ```bash
   cp -r ~/.claude/skills/<skill-name> <backup-dir>/
   ```

2. **Incremental backup** (subsequent)
   ```bash
   # Compare file contents
   diff -rq <source> <target>
   
   # If changed, overwrite
   rm -rf <target>
   cp -r <source> <target>
   ```

3. **Restore mode**
   ```bash
   cp -r <backup-dir>/<skill-name> ~/.claude/skills/
   ```

## Recommended Directory Structure

```
yuanwen-skills/              # Backup repository
├── README.md                # Repository description
├── my-skill-1/             # Skill 1
│   ├── SKILL.md
│   ├── README.md
│   └── scripts/
├── my-skill-2/             # Skill 2
│   ├── SKILL.md
│   └── ...
└── ...
```

## Use Cases

### Case 1: Daily Backup

```
User: "backup skills"
Claude: 
  1. Scan ~/.claude/skills/
  2. Identify 5 self-built Skills
  3. Compare with backup directory
  4. Found 2 with changes
  5. Update backup
  6. Prompt user to git push
```

### Case 2: Cross-device Sync

**Device A**: Develop Skill → Backup to repository → git push
**Device B**: git pull → Restore to ~/.claude/skills/

### Case 3: Batch Restore

```
User: "restore skills"
Claude:
  1. Scan backup directory
  2. List recoverable Skills
  3. User selects
  4. Copy to ~/.claude/skills/
```

### Case 4: Specific Skill Backup

```
User: "backup feishu-doc-copier"
Claude: Only process this Skill
```

## FAQ

### macOS Timestamp Issue

**Problem**: macOS does not update directory mtime when modifying files, making timestamp-based change detection impossible.

**Solution**: Use `diff -rq` to compare file contents instead of timestamps.

```bash
# Correct approach
diff -rq ~/.claude/skills/my-skill ~/backup/my-skill

# Wrong approach (inaccurate on macOS)
ls -lt ~/.claude/skills/my-skill
```

### Backup Directory Already Exists

**Logic**:
1. Compare contents
2. Same → Skip
3. Different → Overwrite and notify

### Skill Already Exists During Restore

**Logic**:
1. Check if target exists
2. Exists → Skip (do not overwrite, prevent accidental deletion)
3. Does not exist → Copy

## Best Practices

### 1. Regular Backup

```bash
# Add to .zshrc or cron
alias skills-backup='cd ~/Documents/coder/yuanwen-skills && ./backup.sh'
```

### 2. Git Workflow

```bash
# After modifying a Skill
cd ~/Documents/coder/yuanwen-skills

# 1. Backup
cp -r ~/.claude/skills/my-skill ./

# 2. Commit
git add .
git commit -m "feat(my-skill): add new feature"

# 3. Push
git push origin main
```

### 3. Version Control

```
my-skill/
├── SKILL.md              # Main code and config
├── README.md             # Usage instructions
├── references/           # Documentation (can be large)
└── scripts/              # Scripts
```

**Note**: `references/` can contain large documents because Skills load on demand.

## Notes

1. **Exclude system Skills**: Will not backup Skills starting with `superpowers:`
2. **Exclude npm Skills**: Will not backup third-party Skills containing `node_modules/`
3. **Restore with caution**: Does not overwrite existing Skills during restore to prevent accidental deletion
4. **Git commit**: Remember to `git push` after backup for true backup

## Related Links

- [Claude Code Skills Documentation](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/tutorials)
- [This Repository](../README.md)

---

**Part of**: [yuanwen-skills](../README.md)

[中文版](README.md)
