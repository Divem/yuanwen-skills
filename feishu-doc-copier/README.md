# 飞书文档批量复制工具 (Feishu Doc Copier)

批量复制飞书文档（云文档/Wiki）到指定位置，保持原有格式完整不变。

## ✨ 功能特点

- 📋 **批量复制**：支持一次复制多个文档
- 🎨 **格式保持**：完美保留 Markdown 格式、标题层级、列表样式
- 🔗 **简单易用**：基于 lark-cli，无需复杂配置
- 📊 **进度显示**：实时显示复制进度和状态
- 🛡️ **错误处理**：单个文档失败不影响其他文档

## 📦 安装

### 方式一：使用 lark-cli（推荐）

**优点**：简单、格式保持最佳

```bash
# 1. 安装 lark-cli
npm install -g @larksuite/cli

# 2. 登录飞书账号
lark-cli auth login

# 3. 安装本工具
pip install -r requirements.txt
```

### 方式二：纯 Python API（无需安装 lark-cli）

**适用场景**：无法安装 npm/nodejs 的环境

```bash
# 1. 安装 Python 依赖
pip install -r requirements.txt

# 2. 创建飞书应用
# 访问 https://open.feishu.cn/app 创建应用
# 开通权限：docx:document:readonly, docx:document:write

# 3. 配置凭证
cp .env.example .env
# 编辑 .env 文件，填入你的 App ID 和 App Secret
```

### 快速开始

```bash
# 克隆仓库
git clone <repository-url>
cd feishu-doc-copier

# 安装依赖
pip install -r requirements.txt

# 配置（如果不用 lark-cli）
cp .env.example .env
# 编辑 .env 填入凭证

# 测试
python scripts/copy_docs.py --help
```

## 🔀 两种工作模式

本工具支持两种工作模式，自动检测并按优先级选择：

### 模式一：lark-cli 模式（优先级高）

**特点：**
- ✅ 格式保持最完整（标题、列表、代码块等）
- ✅ 支持所有飞书文档特性
- ✅ 实现简单可靠

**要求：**
- 安装 Node.js 和 lark-cli
- 登录飞书账号

**自动检测：** 工具会自动检测系统是否安装了 `lark-cli`

### 模式二：纯 Python API 模式（兜底）

**特点：**
- ✅ 零额外依赖（仅需 Python + requests）
- ✅ 无需安装 Node.js
- ⚠️ 部分复杂格式可能转换不完整

**要求：**
- 创建飞书应用（获取 App ID / App Secret）
- 配置环境变量或 .env 文件

**适用场景：**
- 无法安装 Node.js 的环境
- 服务器/容器环境
- 快速原型开发

### 模式切换

工具会自动选择可用模式：
```
1. 检测 lark-cli → 可用则使用 CLI 模式
2. 检测 API 凭证 → 可用则使用 API 模式
3. 都不可用 → 报错提示配置
```

强制使用特定模式（未来版本支持）：
```bash
# 强制使用 CLI 模式
python scripts/copy_docs.py --mode cli <source> <target>

# 强制使用 API 模式  
python scripts/copy_docs.py --mode api <source> <target>
```

## 🚀 使用方法

### 方式一：Python API（推荐）

```python
from scripts.copy_docs import batch_copy, copy_document

# 批量复制多个文档
doc_mappings = [
    ("source_token_1", "target_token_1", "第一章：快速上手"),
    ("source_token_2", "target_token_2", "第二章：进阶技巧"),
    ("source_token_3", "target_token_3", "第三章：实战案例"),
]

result = batch_copy(doc_mappings)
print(f"成功复制 {result['success']}/{result['total']} 个文档")

# 复制单个文档
ok, msg = copy_document("source_token", "target_token")
print(f"{'✓' if ok else '✗'} {msg}")
```

### 方式二：配置文件

1. 创建配置文件 `config.json`：

```json
{
  "folder_token": "URd6fDrTllhkVodVFj7cNfd9ndw",
  "documents": [
    {
      "name": "第一章：快速上手",
      "source": "UTF0w8yt8iIs2Pks3e6cfazOnYc",
      "target": "Fb13dBVX4oj4yZx1z7VcfEz8nUh"
    },
    {
      "name": "第二章：进阶技巧",
      "source": "WK3DwtPRJiSB34k3zURceqmcnAK",
      "target": "Veu9dbTj4oWu7Ax9CzVcakgxnZg"
    }
  ]
}
```

2. 读取配置并复制：

```python
import json
from scripts.copy_docs import batch_copy

with open("config.json") as f:
    config = json.load(f)

doc_mappings = [
    (doc["source"], doc["target"], doc["name"])
    for doc in config["documents"]
]

batch_copy(doc_mappings)
```

### 方式三：命令行

```bash
# 复制单个文档
python scripts/copy_docs.py <source_token> <target_token>

# 示例
python scripts/copy_docs.py UTF0w8yt8iIs2Pks3e6cfazOnYc Fb13dBVX4oj4yZx1z7VcfEz8nUh
```

## 📋 完整示例

### 示例：复制整套教程

```python
#!/usr/bin/env python3
"""
复制 Claude Code 教程到个人空间
"""

from scripts.copy_docs import batch_copy

# 定义文档映射（源文档 → 目标文档）
CHAPTERS = [
    ("UTF0w8yt8iIs2Pks3e6cfazOnYc", "Fb13dBVX4oj4yZx1z7VcfEz8nUh", "第一章：快速上手"),
    ("WK3DwtPRJiSB34k3zURceqmcnAK", "Veu9dbTj4oWu7Ax9CzVcakgxnZg", "第二章：接入国内大模型"),
    ("I0ekw6ODHiDrNNkxvJIcPqAgnKf", "MikXdQMs1oHIxNx6YDYcjwihnGh", "第三章：入门基础操作"),
    ("GiigwIdtyiaQeKkzxLvcGFbKnwf", "NcWidexnhotRL4xzumkcf5rJn5p", "第四章：文本处理与创作"),
]

# 执行批量复制
result = batch_copy(CHAPTERS)

# 输出结果
print("\n复制结果汇总：")
for doc in result['results']:
    status = "✅" if doc['success'] else "❌"
    print(f"{status} {doc['name']}: {doc['message']}")
```

## 🔑 如何获取文档 Token 和 API 凭证

### 获取文档 Token

从飞书文档 URL 中提取：
- 云文档：`https://your-domain.feishu.cn/docx/DOC_TOKEN` → `DOC_TOKEN`
- Wiki：`https://your-domain.feishu.cn/wiki/TOKEN` → `TOKEN`

**示例：**
```
URL: https://example.feishu.cn/docx/UTF0w8yt8iIs2Pks3e6cfazOnYc
Token: UTF0w8yt8iIs2Pks3e6cfazOnYc
```

### 获取 API 凭证（仅 API 模式需要）

1. **创建飞书应用**
   - 访问 [飞书开放平台](https://open.feishu.cn/app)
   - 点击「创建企业自建应用」
   - 填写应用名称和描述

2. **开通权限**
   - 进入应用详情 → 权限管理
   - 搜索并添加以下权限：
     - `docx:document:readonly` - 读取文档
     - `docx:document:write` - 写入文档

3. **获取凭证**
   - 应用详情 → 凭证与基础信息
   - 复制 `App ID` 和 `App Secret`

4. **配置凭证**
   ```bash
   cp .env.example .env
   # 编辑 .env 文件
   FEISHU_APP_ID=cli_xxxxxxxxxxxxxxxx
   FEISHU_APP_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

5. **发布应用（重要）**
   - 应用详情 → 版本管理与发布
   - 点击「创建版本」→「申请发布」
   - 管理员审批通过后即可使用

### 创建目标文档

如果目标文档不存在，先创建：

```bash
lark-cli api POST /open-apis/docx/v1/documents \
  --data '{"title": "文档标题", "folder_token": "YOUR_FOLDER_TOKEN"}'
```

**返回示例：**
```json
{
  "code": 0,
  "data": {
    "document": {
      "document_id": "Fb13dBVX4oj4yZx1z7VcfEz8nUh"
    }
  }
}
```

## ⚠️ 注意事项

1. **权限要求**
   - 源文档：需要读取权限
   - 目标位置：需要写入权限

2. **格式兼容性**
   - ✅ 标题层级（# ## ###）
   - ✅ 有序/无序列表
   - ✅ 代码块
   - ✅ 引用块
   - ⚠️ 图片：保留引用，但需确保目标空间可访问
   - ⚠️ 内部链接：保留，但跨文档链接需手动更新

3. **内容限制**
   - 单个文档大小限制：约 50MB
   - 批量复制建议：一次不超过 50 个文档

## 🐛 故障排除

### 问题 1：没有可用的复制模式

**症状：** `无法使用任何复制模式`

**解决方案：**
```bash
# 方案 A：安装 lark-cli
npm install -g @larksuite/cli

# 方案 B：配置 API 凭证
cp .env.example .env
# 编辑 .env，填入 App ID 和 App Secret
```

### 问题 2：API 模式格式不完整

**症状：** 使用 API 模式复制后，部分格式丢失

**原因：** 飞书 API 返回的是结构化 block 数据，转换为 Markdown 可能不完全

**解决方案：**
```bash
# 优先使用 lark-cli 模式（格式保持最佳）
npm install -g @larksuite/cli
lark-cli auth login

# 然后重新复制
python scripts/copy_docs.py <source> <target>
```

### 问题 3：获取内容失败

**症状：** `获取源文档失败`

**解决方案：**
```bash
# 1. 检查是否已登录
lark-cli auth status

# 2. 如果没有登录，重新登录
lark-cli auth login

# 3. 检查文档是否共享给你
# 在飞书中打开文档，确认有访问权限
```

### 问题 2：更新失败

**症状：** `更新目标文档失败`

**解决方案：**
```bash
# 1. 检查目标文档是否存在
lark-cli api GET /open-apis/docx/v1/documents/TARGET_TOKEN

# 2. 检查文件夹权限
# 确保你对目标文件夹有写入权限

# 3. 重新创建目标文档
lark-cli api POST /open-apis/docx/v1/documents \
  --data '{"title": "新文档", "folder_token": "FOLDER_TOKEN"}'
```

### 问题 3：格式丢失

**症状：** 标题、列表等格式不正确

**原因：** 使用了管道传递内容导致格式丢失

**正确做法：**
```python
# ✅ 正确：使用 Python 变量传递
content = fetch_doc(source_token)
update_doc(target_token, content)

# ❌ 错误：使用管道会导致格式丢失
echo "$content" | lark-cli docs +update ...
```

## 📊 工作原理

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  源文档      │     │  lark-cli    │     │  目标文档    │
│  (飞书)     │────▶│  +fetch      │────▶│  (飞书)     │
└─────────────┘     └──────────────┘     └─────────────┘
                            │
                            ▼
                    ┌──────────────┐
                    │  JSON 响应   │
                    │  markdown    │
                    └──────────────┘
                            │
                            ▼
                    ┌──────────────┐
                    │  lark-cli    │
                    │  +update     │
                    └──────────────┘
```

1. **获取**：`lark-cli docs +fetch --doc <token> --format json`
2. **提取**：解析 JSON，提取 `data.markdown`
3. **更新**：`lark-cli docs +update --mode overwrite`

## 📝 API 参考

### `copy_document(source_token, target_token)`

复制单个文档。

**参数：**
- `source_token` (str): 源文档 token
- `target_token` (str): 目标文档 token

**返回：**
- `(bool, str)`: (成功标志, 消息)

**示例：**
```python
ok, msg = copy_document("UTF0w...", "Fb13d...")
# 输出: (True, "复制成功 (19250 字符)")
```

### `batch_copy(doc_mappings, verbose=True)`

批量复制多个文档。

**参数：**
- `doc_mappings` (List[Tuple[str, str, str]]): [(source, target, name), ...]
- `verbose` (bool): 是否打印详细信息，默认 True

**返回：**
- `dict`: {"total": int, "success": int, "failed": int, "results": List[dict]}

**示例：**
```python
mappings = [
    ("src1", "tgt1", "文档1"),
    ("src2", "tgt2", "文档2"),
]
result = batch_copy(mappings)
# 输出: {"total": 2, "success": 2, "failed": 0, "results": [...]}
```

## 📄 许可证

MIT License - 自由使用和修改

## 🤝 贡献

欢迎提交 Issue 和 PR！

## 💡 使用建议

1. **首次使用**：先复制 1-2 个文档测试
2. **批量复制**：建议分批进行，每批不超过 20 个
3. **重要文档**：复制后抽样检查格式
4. **定期备份**：对于重要文档，定期执行备份复制

---

**Made with ❤️ for Feishu/Lark users**
