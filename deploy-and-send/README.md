# Deploy and Send

构建项目为 zip 包并通过飞书（Feishu/Lark）发送。

## 📋 功能

- 🔨 自动构建项目
- 📦 打包为 zip 文件
- 📤 通过飞书机器人发送
- 💾 失败时自动上传到云盘

## 🚀 使用方法

### 快速开始

```bash
# 在项目根目录执行
bash <path-to-skill>/scripts/build-and-zip.sh

# 或指定参数
bash <path-to-skill>/scripts/build-and-zip.sh ./my-project my-app.zip
```

### 作为 Claude Skill 使用

安装 Skill 后，直接对 Claude 说：

```
"打包并发送"
"构建项目并发给我"
"打包成 demo.zip 发给张三"
"只打包不发"
```

### 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `project-dir` | 当前目录 | 项目根目录 |
| `zip-name` | `dist.zip` | 输出 zip 文件名 |
| `user-id` | `ou_342b...` | 飞书用户 ID（收件人） |
| `build-only` | `false` | 仅构建不发送 |

### 发送文件

```bash
# 通过飞书机器人发送
lark-cli im +messages-send \
  --as bot \
  --user-id "ou_xxxxxxxxxxxxxxxx" \
  --file "dist.zip"
```

## ⚙️ 前置要求

1. **安装 lark-cli**
```bash
npm install -g @larksuite/cli
```

2. **登录飞书账号**
```bash
lark-cli auth login
```

3. **验证权限**
```bash
lark-cli auth status
```

## 🔧 工作流程

```
用户请求
    ↓
解析参数（项目目录、zip名、收件人、是否仅构建）
    ↓
执行构建脚本 → 生成 dist/
    ↓
打包 zip
    ↓
通过飞书发送
    ↓
发送失败 → 上传到云盘
```

## 🐛 常见问题

### 发送失败（文件过大）

飞书消息有大小限制（约 20MB），大文件会自动上传到云盘：

```bash
# 手动上传到云盘
lark-cli drive +upload --file "dist.zip" --name "app-$(date +%Y%m%d).zip"
```

### Token 过期

```bash
# 重新登录
lark-cli auth login
```

### 权限不足

确保机器人有 `im:message:send_as_bot` 权限。

## 📁 文件结构

```
deploy-and-send/
├── SKILL.md              # Claude Skill 定义
├── scripts/
│   └── build-and-zip.sh  # 构建和打包脚本
└── README.md             # 本文件
```

## 💡 使用示例

### 场景 1：日常构建发送

```
用户: "打包发送"
Claude: 使用默认参数构建并发送
```

### 场景 2：指定收件人

```
用户: "发给张三"
Claude: 搜索用户 → 确认 → 构建 → 发送
```

### 场景 3：仅构建

```
用户: "只打包不发"
Claude: 构建并打包，跳过发送步骤
```

### 场景 4：指定输出名

```
用户: "打包成 demo-v2.zip"
Claude: 使用指定文件名打包
```

## 📝 注意事项

1. **路径问题**: `--file` 参数必须使用相对路径
2. **文件大小**: 超过 20MB 的文件会自动上传到云盘
3. **收件人**: 首次使用建议先搜索确认用户 ID
4. **构建脚本**: 根据项目类型可能需要自定义构建命令

## 🔗 相关链接

- [飞书开放平台](https://open.feishu.cn/)
- [lark-cli 文档](https://github.com/larksuite/cli)

---

**所属**: [yuanwen-skills](../README.md)
