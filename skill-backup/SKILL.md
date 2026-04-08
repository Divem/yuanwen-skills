---
name: skill-backup
description: 备份、同步和恢复自定义 Skills。当用户说"备份 skill"、"备份技能"、"导出 skill"、"sync skills"、"归档 skill"、"恢复 skill"时触发。支持备份全部自建 skill 或指定 skill。
---

# Skill Backup

备份、同步和恢复 Claude Code 自定义 skills。

## 工作流

### 备份模式（默认）

1. **扫描源目录** `~/.claude/skills/`，识别自建 skill：
   - 排除 `superpowers:` 前缀的内置 skill
   - 排除 npm 安装的第三方 skill（目录下含 `node_modules` 或 `package.json`）
   - 如果用户指定了具体 skill 名称，只处理匹配的
2. **向用户确认**以下信息：
   - 备份哪些 skill（列出识别到的自建 skill，默认全部）
   - 目标目录路径（默认 `~/Documents/coder/skills_backup`）
3. 用户确认后，逐个检查并备份：
   - 目标不存在 → 复制
   - 目标已存在且源更新过 → 覆盖并提示
   - 目标已存在且无变化 → 跳过
4. 输出备份结果：成功 / 跳过 / 失败数量及清单

### 恢复模式

1. 扫描备份目录，列出可恢复的 skill
2. 向用户确认要恢复哪些
3. 复制到 `~/.claude/skills/`（已存在则跳过，不覆盖）

## 判断用户意图

- 说"备份/sync/归档/导出 skill" → 备份模式
- 说"恢复/还原 skill" → 恢复模式
- 说"备份 xxx skill" → 备份模式，仅处理指定 skill

## 变更检测逻辑

用 `diff -rq` 对比源和目标的文件内容，而非目录时间戳（macOS 修改文件不更新目录 mtime）：

```bash
# 检测是否有变化
if diff -rq ~/.claude/skills/<skill-name> <target-dir>/<skill-name> > /dev/null 2>&1; then
  echo "SKIP: 无变化"
else
  rm -rf <target-dir>/<skill-name>
  cp -r ~/.claude/skills/<skill-name> <target-dir>/
  echo "OK: 已更新"
fi
```

## 备份命令

```bash
# 全量备份（目标不存在时）
cp -r ~/.claude/skills/<skill-name> <target-dir>/
```
