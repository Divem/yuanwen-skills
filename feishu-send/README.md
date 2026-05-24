# 飞书消息发送器

通过飞书机器人发送文件、文本或 Markdown 消息给用户或群聊。

## 功能特性

- 发送文件（支持自动降级到云盘上传）
- 发送文本消息
- 发送 Markdown 消息
- 支持按用户名搜索接收人

## 前置条件

- lark-cli 已安装
- 已登录：`lark-cli auth login`
- 机器人已开通 `im:message:send_as_bot` 权限

## 使用方法

直接对 Claude 说：

```
"发到飞书"
"把文件发给张三"
"发条消息给 xx 群"
"send to feishu"
```

## 发送命令

### 发送文件

```bash
lark-cli im +messages-send --as bot --user-id "ou_xxx" --file "./path/to/file"
```

### 发送文本

```bash
lark-cli im +messages-send --as bot --user-id "ou_xxx" --text "消息内容"
```

### 发送 Markdown

```bash
lark-cli im +messages-send --as bot --user-id "ou_xxx" --markdown "**粗体** 文本"
```

### 发送到群聊

```bash
lark-cli im +messages-send --as bot --chat-id "oc_xxx" --file "./path/to/file"
```

## 查找接收人

按用户名搜索：

```bash
lark-cli contact +search-user --query "张三" --format table
```

搜索群聊：

```bash
lark-cli im +chat-search --query "群名" --format table
```

## 发送失败降级

如果文件发送失败（大小限制或权限），自动降级为云盘上传：

```bash
lark-cli drive +upload --file "./filename" --name "filename-$(date +%Y%m%d-%H%M).zip"
```

## 注意事项

- `--file` 只接受相对路径
- 内容较长时，先写入临时文件再用 `--file` 发送
- 群聊用 `--chat-id`，个人用 `--user-id`，二者互斥

---

[English Version](README.en.md)
