# 飞书文档下载器

将飞书文档通过 Open API 下载，解析 blocks 结构，生成带格式的本地 Markdown 文件。

## 功能特性

- 保留标题、列表、加粗、代码块、引用、表格等格式
- 使用 blocks API（非 `raw_content` 纯文本接口）
- 支持文档和图片下载
- 支持知识库文档（wiki）

## 前置条件

- Python 3
- 飞书应用凭证（`app_id`、`app_secret`）

### 所需 API 权限

- `docx:document:readonly` — 读取文档内容
- `wiki:node:read` — 知识库文档

## 使用方法

直接对 Claude 说：

```
"下载这个飞书文档"
"把飞书文档保存到本地"
"导出飞书文档为 Markdown"
```

并提供飞书文档 URL。

## 关键注意事项

1. **不要用 `raw_content` 接口**：它只返回纯文本，无任何格式
2. **不要依赖 feishu CLI**：`feishu auth device-flow` 经常超时或报错
3. **直接用 tenant_access_token + blocks API**：稳定可靠

## Block 类型支持

| 类型 | Markdown 输出 |
|------|--------------|
| 标题 1-9 | `#` 到 `#########` |
| 普通文本 | 段落 |
| 无序列表 | `- item` |
| 有序列表 | `1. item` |
| 代码块 | ` ```lang ... ``` ` |
| 引用 | `> text` |
| 待办 | `- [ ] text` / `- [x] text` |
| 分割线 | `---` |
| 图片 | `![image](url)` |
| 表格 | Markdown 表格 |

## 故障排除

| 问题 | 原因 | 解决 |
|------|------|------|
| Auth error | app_id/app_secret 错误 | 检查凭证文件 |
| 文档访问被拒 | 应用无权限 | 开通 `docx:document:readonly`，将文档分享给应用 |
| 内容为空 | 文档为空或权限不足 | 检查 blocks 返回是否为空 |
| 格式丢失 | 用了 `raw_content` 接口 | 改用 blocks API |
