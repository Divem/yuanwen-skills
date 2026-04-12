# 达达的技能仓库 (Skills Repo)

Claude Code 自定义 Skills 合集，用于提升工作效率和自动化任务。

## 📦 包含的技能

| 技能 | 说明 | 语言 |
|------|------|------|
| [feishu-doc-copier](feishu-doc-copier/) | 批量复制飞书文档（双模式：CLI + API） | 🇨🇳 中文 |
| [deploy-and-send](deploy-and-send/) | 构建项目为 zip 并通过飞书发送 | 🇺🇸 英文 |
| [skill-backup](skill-backup/) | 备份、同步和恢复自定义 Skills | 🇨🇳 中文 |
| [feishu-send](feishu-send/) | 发送文件/消息到飞书用户或群组 | 🇺🇸 英文 |

## 🚀 快速开始

### 安装单个 Skill

```bash
# 克隆整个仓库
git clone https://github.com/Divem/yuanwen-skills.git
cd yuanwen-skills

# 安装特定 skill（示例：feishu-doc-copier）
cd feishu-doc-copier
pip install -r requirements.txt
```

### 备份和同步

```bash
# 备份 skills 到本仓库
cd ~/Documents/coder/yuanwen-skills

# 查看变更
git status

# 提交并推送
git add .
git commit -m "更新: xxx skill"
git push origin main
```

## 📂 仓库结构

```
yuanwen-skills/
├── README.md                    # 本文件
├── feishu-doc-copier/          # 飞书文档复制
│   ├── README.md               # 详细使用文档
│   ├── SKILL.md                # Claude Skill 定义
│   └── scripts/
├── deploy-and-send/            # 构建并发送
│   ├── README.md
│   └── scripts/
├── skill-backup/               # Skills 备份工具
│   ├── README.md
│   └── SKILL.md
└── feishu-send/                # 飞书消息发送
    ├── README.md
    └── SKILL.md
```

## 🛠️ 开发规范

### Skill 结构标准

每个 Skill 应包含：

```
skill-name/
├── SKILL.md              # Claude 使用的技能定义（必需）
├── README.md             # 给用户的使用说明（必需）
├── scripts/              # 可执行脚本（可选）
├── references/           # 参考文档（可选）
└── assets/               # 资源文件（可选）
```

### 文档语言

- **SKILL.md**: 使用 Claude 能理解的语言（中文或英文）
- **README.md**: 使用中文，方便中文用户阅读

### 提交规范

```bash
# 功能更新
git commit -m "feat(feishu-doc-copier): 添加批量复制功能"

# 修复问题
git commit -m "fix(deploy-and-send): 修复大文件发送失败"

# 文档更新
git commit -m "docs(skill-backup): 更新使用说明"
```

## 🤝 贡献

欢迎提交新的 Skills 或改进现有 Skills！

### 添加新 Skill 流程

1. 在 `~/.claude/skills/` 开发并测试 Skill
2. 复制到本仓库：`cp -r ~/.claude/skills/my-skill ./`
3. 创建 README.md 说明使用方法
4. 提交并推送

## 📄 许可证

所有 Skills 遵循 MIT 许可证，自由使用和修改。

## 👤 作者

**达尔文** - 个人 Skills 合集

---

💡 **提示**: 这是一个个人 Skills 备份仓库，主要用于跨设备同步和分享。