# Skills Backup

达尔文的 Claude Code 自定义 Skills 备份仓库。

## 包含的 Skill

| Skill | 说明 |
|-------|------|
| [deploy-and-send](deploy-and-send/) | 构建项目为 zip 并通过飞书发送 |
| [skill-backup](skill-backup/) | 备份、同步和恢复自定义 Skills |

## 使用方式

备份目录 `~/Documents/coder/skills-backup/` 是 Git 仓库，变更后手动推送：

```bash
cd ~/Documents/coder/skills-backup
git add -A && git commit -m "sync: 更新 skill" && git push
```
