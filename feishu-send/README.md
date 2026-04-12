# Feishu Send

发送文件、文本或 Markdown 消息到飞书（Feishu/Lark）用户或群组。

## 📋 功能

- 📁 发送文件（支持各种格式）
- 💬 发送纯文本消息
- 📝 发送 Markdown 格式消息
- 🔍 智能搜索用户和群组
- 💾 大文件自动上传云盘

## 🚀 使用方法

### 快速开始

```bash
# 发送文件（必须使用相对路径）
lark-cli im +messages-send \
  --as bot \
  --user-id "ou_xxxxxxxxxxxxxxxx" \
  --file "./path/to/file.pdf"

# 发送文本消息
lark-cli im +messages-send \
  --as bot \
  --user-id "ou_xxxxxxxxxxxxxxxx" \
  --text "你好，这是测试消息"

# 发送 Markdown
lark-cli im +messages-send \
  --as bot \
  --chat-id "oc_xxxxxxxxxxxxxxxx" \
  --markdown "**粗体** 和 *斜体* 文本"
```

### 作为 Claude Skill 使用

安装 Skill 后，直接对 Claude 说：

```
"把这份报告发到飞书"
"发消息给张三"
"发送文件 ./data.xlsx 给项目经理"
"发到开发群"
"发送 Markdown 消息给 xxx"
```

## ⚙️ 前置要求

1. **安装 lark-cli**
```bash
npm install -g @larksuite/cli
```

2. **登录并验证**
```bash
lark-cli auth login
lark-cli auth status
```

3. **权限配置**
   - 机器人必须有 `im:message:send_as_bot` 权限
   - 在飞书应用后台 → 权限管理 → 添加权限

## 🔧 工作流程

### 步骤 1：确定收件人

**方式 A：用户指定名称**
```bash
# 搜索用户
lark-cli contact +search-user --query "张三" --format table

# 搜索群组
lark-cli im +chat-search --query "项目群" --format table
```

**方式 B：用户直接提供 ID**
```bash
# 直接使用
--user-id "ou_xxxxxxxxxxxxxxxx"      # 个人
--chat-id "oc_xxxxxxxxxxxxxxxx"      # 群组
```

### 步骤 2：确定内容类型

| 用户说 | 参数 | 示例 |
|--------|------|------|
| "文件" / "把xx发过去" | `--file` | `--file "./report.pdf"` |
| "消息" / "文字" | `--text` | `--text "晚上好"` |
| "Markdown" | `--markdown` | `--markdown "**重要**"` |

### 步骤 3：执行发送

```bash
# 个人
lark-cli im +messages-send --as bot --user-id "ou_xxx" --file "./doc.pdf"

# 群组
lark-cli im +messages-send --as bot --chat-id "oc_xxx" --text "大家好"
```

## 📋 参数说明

| 参数 | 必需 | 说明 |
|------|------|------|
| `file` / `text` / `markdown` | ✓ | 内容（三选一） |
| `user-id` / `chat-id` | ✓ | 收件人 ID（二选一） |
| `as` | ✓ | 发送身份，固定为 `bot` |

**重要**: `--user-id` 和 `--chat-id` 互斥，只能选一个。

## 🐛 故障排除

### 错误：File not found

**原因**: `--file` 必须使用相对路径

**解决**:
```bash
# ✅ 正确（相对路径）
--file "./documents/report.pdf"

# ❌ 错误（绝对路径）
--file "/Users/name/documents/report.pdf"
```

### 错误：File too large

**原因**: 飞书消息有大小限制（约 20MB）

**解决**: 自动上传到云盘
```bash
lark-cli drive +upload \
  --file "./large-file.zip" \
  --name "large-file-$(date +%Y%m%d-%H%M%S).zip"
```

### 错误：Permission denied

**原因**: 机器人没有发送权限

**解决**:
1. 访问 [飞书开放平台](https://open.feishu.cn/)
2. 进入应用 → 权限管理
3. 添加 `im:message:send_as_bot` 权限
4. 重新发布应用

### 错误：Token expired

**解决**:
```bash
lark-cli auth login
```

### 错误：User not found

**解决**: 尝试不同的搜索关键词
```bash
lark-cli contact +search-user --query "张三"    # 姓名
lark-cli contact +search-user --query "zhangsan" # 拼音
lark-cli contact +search-user --query "zhang.san@company.com" # 邮箱
```

## 💡 使用示例

### 场景 1：发送日常报告

```
用户: "把 today's-report.pdf 发到飞书"
Claude:
  1. 检测文件存在
  2. 使用默认收件人或询问
  3. 发送文件
```

### 场景 2：通知团队成员

```
用户: "发消息给项目群：今晚8点开会"
Claude:
  1. 搜索 "项目群"
  2. 确认群组（多个结果时询问）
  3. 发送文本消息
```

### 场景 3：发送格式化通知

```
用户: "发送 Markdown 消息给老板：周报已更新"
Claude:
  1. 生成 Markdown:
     "**周报已更新** 📊\n\n请查看附件..."
  2. 搜索 "老板"
  3. 确认并发送
```

### 场景 4：批量发送

```
用户: "把季度总结.pdf 发给张三、李四、王五"
Claude:
  1. 逐个搜索用户
  2. 确认收件人列表
  3. 循环发送给每个人
```

## 📝 注意事项

1. **路径问题**
   - `--file` 只接受相对路径
   - 长内容建议先写入临时文件再发送

2. **大小限制**
   - 消息：约 20MB
   - 超大文件自动转云盘上传

3. **ID 类型**
   - 个人：`ou_` 开头
   - 群组：`oc_` 开头
   - 不要混用 `--user-id` 和 `--chat-id`

4. **搜索策略**
   - 优先精确匹配
   - 多个结果时询问用户选择
   - 支持姓名、拼音、邮箱搜索

## 📁 文件结构

```
feishu-send/
├── SKILL.md              # Claude Skill 定义
└── README.md             # 本文件
```

## 🔗 相关链接

- [飞书开放平台](https://open.feishu.cn/)
- [lark-cli GitHub](https://github.com/larksuite/cli)
- [本仓库](../README.md)

---

**所属**: [yuanwen-skills](../README.md)
