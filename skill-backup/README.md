# Skill Backup

备份、同步和恢复 Claude Code 自定义 Skills。

## 📋 功能

- 💾 备份 Skills 到指定目录
- 🔄 同步 Skills 变更
- 📤 恢复 Skills 到新环境
- 🧹 智能识别自建 Skills

## 🚀 使用方法

### 快速开始

```bash
# 备份所有自建 Skills
# 默认备份到 ~/Documents/coder/yuanwen-skills/

# 在 Claude 中直接说：
"备份 skills"
"导出我的 skills"
"sync skills"
```

### 手动备份

```bash
# 复制单个 skill
cp -r ~/.claude/skills/my-skill ~/Documents/coder/yuanwen-skills/

# 使用 rsync（推荐）
rsync -av --delete ~/.claude/skills/my-skill/ ~/Documents/coder/yuanwen-skills/my-skill/
```

### 变更检测

```bash
# 检测是否有变更
if diff -rq ~/.claude/skills/my-skill ~/Documents/coder/yuanwen-skills/my-skill > /dev/null 2>&1; then
    echo "无变化，跳过"
else
    echo "有变更，需要备份"
    rm -rf ~/Documents/coder/yuanwen-skills/my-skill
    cp -r ~/.claude/skills/my-skill ~/Documents/coder/yuanwen-skills/
fi
```

## ⚙️ 工作原理

### 识别自建 Skills

```
~/.claude/skills/
├── superpowers:xxx/     ← 系统内置，跳过
├── npm-installed/       ← npm 安装，跳过（有 package.json）
└── my-custom-skill/     ← 自建 Skill，备份 ✓
```

**排除规则**:
- ❌ `superpowers:` 前缀 - 系统内置 Skills
- ❌ 含 `node_modules/` 或 `package.json` - npm 安装的第三方 Skills
- ✅ 其他 - 自建 Skills

### 备份模式

1. **完整备份** (首次)
   ```bash
   cp -r ~/.claude/skills/<skill-name> <backup-dir>/
   ```

2. **增量备份** (后续)
   ```bash
   # 对比文件内容
   diff -rq <source> <target>
   
   # 如有变更，覆盖
   rm -rf <target>
   cp -r <source> <target>
   ```

3. **恢复模式**
   ```bash
   cp -r <backup-dir>/<skill-name> ~/.claude/skills/
   ```

## 📂 推荐目录结构

```
yuanwen-skills/              # 备份仓库
├── README.md                # 仓库说明
├── my-skill-1/             # Skill 1
│   ├── SKILL.md
│   ├── README.md
│   └── scripts/
├── my-skill-2/             # Skill 2
│   ├── SKILL.md
│   └── ...
└── ...
```

## 🔧 使用场景

### 场景 1：日常备份

```
用户: "备份 skills"
Claude: 
  1. 扫描 ~/.claude/skills/
  2. 识别出 5 个自建 Skills
  3. 对比备份目录
  4. 发现 2 个有变更
  5. 更新备份
  6. 提示用户 git push
```

### 场景 2：跨设备同步

**设备 A**: 开发 Skill → 备份到仓库 → git push
**设备 B**: git pull → 恢复到 ~/.claude/skills/

### 场景 3：批量恢复

```
用户: "恢复 skills"
Claude:
  1. 扫描备份目录
  2. 列出可恢复的 Skills
  3. 用户选择
  4. 复制到 ~/.claude/skills/
```

### 场景 4：指定 Skill 备份

```
用户: "备份 feishu-doc-copier"
Claude: 仅处理该 Skill
```

## 🐛 常见问题

### macOS 时间戳问题

**问题**: macOS 修改文件不更新目录 mtime，导致无法通过时间戳判断变更。

**解决方案**: 使用 `diff -rq` 对比文件内容，而非时间戳。

```bash
# 正确做法
diff -rq ~/.claude/skills/my-skill ~/backup/my-skill

# 错误做法（macOS 不准确）
ls -lt ~/.claude/skills/my-skill
```

### 备份目录已存在

**处理逻辑**:
1. 对比内容
2. 相同 → 跳过
3. 不同 → 覆盖并提示

### 恢复时 Skill 已存在

**处理逻辑**:
1. 检查目标是否存在
2. 存在 → 跳过（不覆盖，防误删）
3. 不存在 → 复制

## 💡 最佳实践

### 1. 定期备份

```bash
# 添加到 .zshrc 或定时任务
alias skills-backup='cd ~/Documents/coder/yuanwen-skills && ./backup.sh'
```

### 2. Git 工作流

```bash
# 修改 Skill 后
cd ~/Documents/coder/yuanwen-skills

# 1. 备份
cp -r ~/.claude/skills/my-skill ./

# 2. 提交
git add .
git commit -m "feat(my-skill): 添加新功能"

# 3. 推送
git push origin main
```

### 3. 版本控制

```
my-skill/
├── SKILL.md              # 主要代码和配置
├── README.md             # 使用说明
├── references/           # 文档（可大）
└── scripts/              # 脚本
```

**注意**: `references/` 可以放大的文档，因为 Skill 是按需加载。

## 📝 注意事项

1. **排除系统 Skills**: 不会备份 `superpowers:` 开头的内置 Skills
2. **排除 npm Skills**: 不会备份含 `node_modules/` 的第三方 Skills
3. **谨慎恢复**: 恢复时不覆盖已存在的 Skills，防止误删
4. **Git 提交**: 备份后记得 `git push`，才是真正的备份

## 🔗 相关链接

- [Claude Code Skills 文档](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/tutorials)
- [本仓库](../README.md)

---

**所属**: [yuanwen-skills](../README.md)
