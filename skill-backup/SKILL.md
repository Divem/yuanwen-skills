---
name: skill-backup
description: 备份自定义 Skills 到指定目录。当用户说"备份 skill"、"备份技能"、"导出 skill"时触发。
---

# Skill Backup

备份 Claude Code 自定义 skills 到指定目录。

## 工作流

1. **扫描源目录** `~/.claude/skills/`，列出所有自定义 skill 名称（排除 `superpowers:` 前缀的内置 skill）
2. **向用户确认**以下信息：
   - 备份哪些 skill（默认全部）
   - 目标目录路径（默认 `~/Documents/coder/skills_backup`）
3. 用户确认后，执行备份：将每个 skill 的完整目录（包含 SKILL.md、scripts/、references/、assets/ 等）复制到目标目录
4. 输出备份结果摘要

## 备份命令

```bash
cp -r ~/.claude/skills/<skill-name> <target-dir>/
```

## 注意事项

- 如果目标已存在同名 skill，跳过并提示用户（不覆盖）
- 备份完成后列出成功/跳过的 skill 清单
