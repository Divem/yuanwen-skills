# 达尔文的技能仓库 (Skills Repo)

Claude Code 自定义 Skills 合集，用于提升工作效率和自动化任务。

## 📦 包含的技能

### 飞书集成

| 技能 | 说明 | 语言 |
|------|------|------|
| [feishu-send](feishu-send/) | 发送文件/消息到飞书用户或群组 | 🇨🇳 中文 |
| [feishu-doc-copier](feishu-doc-copier/) | 批量复制飞书文档（双模式：CLI + API） | 🇨🇳 中文 |
| [feishu-doc-download](feishu-doc-download/) | 下载飞书文档并转为本地 Markdown 文件 | 🇨🇳 中文 |
| [feishu-sync](feishu-sync/) | 双向同步本地目录与飞书云文档 | 🇨🇳 中文 |
| [deploy-and-send](deploy-and-send/) | 构建项目为 zip 并通过飞书发送 | 🇨🇳 中文 |

### 内容采集

| 技能 | 说明 | 语言 |
|------|------|------|
| [bilibili-comment-crawler](bilibili-comment-crawler/) | 批量采集B站视频评论并写入飞书表格 | 🇨🇳 中文 |
| [douyin-comment-scraper](douyin-comment-scraper/) | 抓取抖音视频评论并导出到飞书 | 🇨🇳 中文 |
| [douyin-search](douyin-search/) | 搜索抖音视频并提取元数据 | 🇨🇳 中文 |

### 内容运营

| 技能 | 说明 | 语言 |
|------|------|------|
| [knowflow-os](knowflow-os/) | AI 知识管理与内容运营系统 | 🇨🇳 中文 |

### 工具

| 技能 | 说明 | 语言 |
|------|------|------|
| [skill-backup](skill-backup/) | 备份、同步和恢复自定义 Skills | 🇨🇳 中文 |
| [skill-landing-generator](skill-landing-generator/) | 为 Skill 生成统一风格的落地页和手册页 HTML | 🇨🇳 中文 |
| [docs-organizer](docs-organizer/) | 文档目录管理（初始化 / 诊断审计） | 🇨🇳 中文 |

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
├── AGENTS.md                    # AI 代理指引
├── bilibili-comment-crawler/   # B站评论采集
│   ├── SKILL.md
│   └── scripts/
├── deploy-and-send/            # 构建并发送
│   ├── SKILL.md
│   └── scripts/
├── docs-organizer/             # 文档目录管理
│   ├── SKILL.md
│   ├── README.md
│   ├── references/
│   └── scripts/
├── douyin-comment-scraper/     # 抖音评论抓取
│   ├── SKILL.md
│   └── scripts/
├── douyin-search/              # 抖音视频搜索
│   ├── SKILL.md
│   └── scripts/
├── feishu-doc-copier/          # 飞书文档复制
│   ├── SKILL.md
│   ├── README.md
│   ├── references/
│   └── scripts/
├── feishu-doc-download/        # 飞书文档下载
│   └── SKILL.md
├── feishu-send/                # 飞书消息发送
│   └── SKILL.md
├── feishu-sync/                # 飞书双向同步
│   ├── SKILL.md
│   ├── README.md
│   └── scripts/
├── knowflow-os/                # AI 知识管理与内容运营系统
│   ├── SKILL.md
│   ├── README.md
│   ├── assets/
│   └── references/
├── skill-backup/               # Skills 备份工具
│   ├── SKILL.md
│   └── README.md
└── skill-landing-generator/    # Skill 落地页生成器
    ├── SKILL.md
    ├── README.md
    ├── assets/
    └── references/
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