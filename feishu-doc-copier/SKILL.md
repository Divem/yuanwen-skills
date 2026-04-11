---
name: feishu-doc-copier
description: 批量复制飞书文档（包括云文档和 Wiki）到指定位置，保持原有格式不变。适用于：1) 复制整套教程/文档到个人空间 2) 备份重要文档 3) 创建文档副本用于协作 4) 跨空间/跨组织迁移文档。支持批量操作，保持 Markdown 格式、标题层级、列表样式等完整不变。
---

# 飞书文档批量复制工具

使用 lark-cli 的 `docs +fetch` 和 `docs +update` 命令，批量复制飞书文档。

## 前置要求

1. 安装 lark-cli：`npm install -g @larksuite/cli`
2. 完成身份验证：`lark-cli auth login`

## 使用方式

### 方式一：使用脚本批量复制

```python
# 导入复制函数
from scripts.copy_docs import batch_copy

# 定义文档映射 [(source_token, target_token, name), ...]
doc_mappings = [
    ("UTF0w8yt8iIs2Pks3e6cfazOnYc", "Fb13dBVX4oj4yZx1z7VcfEz8nUh", "第一章"),
    ("WK3DwtPRJiSB34k3zURceqmcnAK", "Veu9dbTj4oWu7Ax9CzVcakgxnZg", "第二章"),
]

# 执行批量复制
result = batch_copy(doc_mappings)
```

### 方式二：从配置文件复制

```python
import json
from scripts.copy_docs import batch_copy

# 读取配置
with open("references/config.json") as f:
    config = json.load(f)

# 转换为映射列表
doc_mappings = [
    (doc["source"], doc["target"], doc["name"])
    for doc in config["documents"]
]

# 执行复制
batch_copy(doc_mappings)
```

### 方式三：命令行复制单个文档

```bash
# 复制单个文档
python scripts/copy_docs.py <source_token> <target_token>
```

## 获取文档 Token

从飞书文档 URL 中提取：
- `https://your-domain.feishu.cn/docx/DOC_TOKEN` → `DOC_TOKEN`
- `https://your-domain.feishu.cn/wiki/TOKEN` → `TOKEN`

## 创建目标文档

如果目标文档不存在，需要先创建：

```bash
lark-cli api POST /open-apis/docx/v1/documents \
  --data '{"title": "文档标题", "folder_token": "FOLDER_TOKEN"}'
```

## 注意事项

1. **格式保持**：复制后的文档会保持原有 Markdown 格式、标题层级、列表样式
2. **权限要求**：需要源文档的读取权限和目标位置的写入权限
3. **图片处理**：文档中的图片会保留引用，但需要确保图片在目标空间可访问
4. **链接保留**：文档内的相对链接会保留，跨文档链接需要手动更新

## 工作原理

1. **获取内容**：使用 `lark-cli docs +fetch --doc <token> --format json` 获取文档 Markdown 内容
2. **提取内容**：从 JSON 响应中解析 `data.markdown` 字段
3. **更新文档**：使用 `lark-cli docs +update --mode overwrite` 将内容写入目标文档

## 故障排除

### 获取内容失败
- 检查文档是否共享给你
- 确认文档 token 正确
- 检查网络连接

### 更新失败
- 确认目标文档存在
- 检查是否有写入权限
- 确认 lark-cli 已登录

### 格式丢失
- 确保使用 `--format json` 获取内容
- 确保正确解析 `data.markdown` 字段
- 避免使用管道传递内容（会导致格式丢失）
