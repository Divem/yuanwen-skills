---
name: feishu-doc-download
author: wen.yuan
description: 下载飞书文档并转为格式化的本地 Markdown 文件。使用 blocks API 保留标题、列表、加粗、代码块、引用、表格等格式。当用户想下载/保存飞书文档时使用。
metadata: {"emoji":"📥","requires":{"bins":["python3"]}}
---
# 飞书文档下载转 Markdown

将飞书文档通过 Open API 下载，解析 blocks 结构，生成带格式的本地 Markdown 文件。

## 何时使用

- 用户分享飞书文档 URL，要求保存到本地
- 用户想读取飞书文档内容
- 需要批量下载飞书文档

## 前置条件

### 飞书应用凭证

凭证位置：`~/.claude/skills/feishu-doc-reader/reference/feishu_config.json`

```python
import os, json
with open(os.path.expanduser("~/.claude/skills/feishu-doc-reader/reference/feishu_config.json")) as f:
    cfg = json.load(f)
app_id = cfg["app_id"]
app_secret = cfg["app_secret"]
```

### 所需 API 权限

- `docx:document:readonly` - 读取文档内容
- `wiki:node:read` - 如文档在知识库中

## 关键注意事项

1. **不要用 `raw_content` 接口**：它只返回纯文本，无任何格式
2. **不要依赖 feishu CLI**：`feishu auth device-flow` 经常超时或报 `application:application:self_manage` 权限错误
3. **直接用 tenant_access_token + blocks API**：稳定可靠

## 完整流程（execute_code 一次性执行）

以下是一个完整的 Python 脚本，用 `execute_code` 工具执行：

```python
import json, urllib.request, ssl, os, re
from hermes_tools import write_file

# ====== 配置 ======
DOC_TOKEN = "从URL中提取的文档token"
OUTPUT_DIR = "/用户指定的输出目录"

# ====== 读取凭证 ======
with open(os.path.expanduser("~/.claude/skills/feishu-doc-reader/reference/feishu_config.json")) as f:
    cfg = json.load(f)
app_id, app_secret = cfg["app_id"], cfg["app_secret"]

# ====== Step 1: 获取 Tenant Access Token ======
ctx = ssl.create_default_context()
auth_data = json.dumps({"app_id": app_id, "app_secret": app_secret}).encode()
req = urllib.request.Request(
    "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
    data=auth_data, headers={"Content-Type": "application/json"}
)
resp = urllib.request.urlopen(req, timeout=15, context=ctx)
token = json.loads(resp.read())["tenant_access_token"]
headers = {"Authorization": f"Bearer {token}"}

# ====== Step 2: 获取文档标题 ======
req_t = urllib.request.Request(
    f"https://open.feishu.cn/open-apis/docx/v1/documents/{DOC_TOKEN}", headers=headers
)
title = json.loads(urllib.request.urlopen(req_t, timeout=15, context=ctx).read())["data"]["document"]["title"]

# ====== Step 3: 获取所有 Blocks（分页） ======
all_blocks = []
page_token = None
while True:
    path = f"/open-apis/docx/v1/documents/{DOC_TOKEN}/blocks?page_size=500"
    if page_token:
        path += f"&page_token={page_token}"
    req_b = urllib.request.Request("https://open.feishu.cn" + path, headers=headers)
    bd = json.loads(urllib.request.urlopen(req_b, timeout=30, context=ctx).read())
    if bd.get("code") != 0:
        break
    all_blocks.extend(bd["data"]["items"])
    page_token = bd.get("data", {}).get("page_token")
    if not page_token:
        break

# ====== Step 4: 解析 Blocks 为 Markdown ======

def extract_text(elements):
    """从 text_run elements 提取富文本"""
    if not elements:
        return ""
    parts = []
    for el in elements:
        tr = el.get("text_run")
        if not tr:
            continue
        content = tr.get("content", "")
        style = tr.get("text_element_style", {})
        if style.get("bold"):
            content = f"**{content}**"
        if style.get("italic"):
            content = f"*{content}*"
        if style.get("strikethrough"):
            content = f"~~{content}~~"
        if style.get("inline_code"):
            content = f"`{content}`"
        link = style.get("link")
        if link:
            parts.append(f"[{content}]({link.get('url', '')})")
        else:
            parts.append(content)
    return "".join(parts)

def get_text(block):
    """从 block 中提取文本"""
    for key in ["text","heading1","heading2","heading3","heading4","heading5",
                "heading6","heading7","heading8","heading9","bullet","ordered",
                "todo","quote","callout"]:
        d = block.get(key)
        if d:
            return extract_text(d.get("elements", []))
    return ""

# 构建 parent → children 映射
children_map = {}
for b in all_blocks:
    pid = b.get("parent_id")
    if pid:
        children_map.setdefault(pid, []).append(b)

def render(block):
    """递归渲染 block 为 Markdown"""
    bt = block.get("block_type")
    bid = block["block_id"]
    md = ""

    if bt in range(3, 12):  # heading1-9
        level = bt - 2
        text = get_text(block).strip()
        if text:
            md += f"{'#' * level} {text}\n\n"

    elif bt == 2:  # text
        text = get_text(block).strip()
        if text:
            md += f"{text}\n\n"

    elif bt == 12:  # bullet
        text = get_text(block).strip()
        if text:
            md += f"- {text}\n\n"

    elif bt == 13:  # ordered
        text = get_text(block).strip()
        if text:
            md += f"1. {text}\n\n"

    elif bt == 15:  # quote
        text = get_text(block).strip()
        if text:
            md += f"> {text}\n\n"

    elif bt == 14:  # code block
        code_data = block.get("code", {})
        lang = code_data.get("language", "")
        code_text = ""
        for el in code_data.get("elements", []):
            tr = el.get("text_run")
            if tr:
                code_text += tr.get("content", "")
        md += f"```{lang}\n{code_text.rstrip()}\n```\n\n"

    elif bt == 21:  # divider
        md += "---\n\n"

    elif bt == 26:  # image
        img_data = block.get("image", {})
        img_token = img_data.get("token", "")
        md += f"![image](https://open.feishu.cn/open-apis/docx/v1/documents/{DOC_TOKEN}/blocks/{bid}/image/{img_token})\n\n"

    elif bt == 30:  # table
        table_data = block.get("table", {})
        rows = table_data.get("rows", 0)
        cols = table_data.get("columns", 0)
        kids = children_map.get(bid, [])
        cells = {}
        for kid in kids:
            if kid.get("block_type") == 31:  # table_cell
                cell_data = kid.get("table_cell", {})
                c = cell_data.get("column_start", 0)
                r = cell_data.get("row_start", 0)
                cell_kids = children_map.get(kid["block_id"], [])
                cell_text = "".join(get_text(ck).strip() for ck in cell_kids)
                cells[(r, c)] = cell_text
        if rows > 0 and cols > 0:
            for r in range(rows):
                row_texts = [cells.get((r, c), "") for c in range(cols)]
                md += "| " + " | ".join(row_texts) + " |\n"
                if r == 0:
                    md += "| " + " | ".join(["---"] * cols) + " |\n"
            md += "\n"

    elif bt == 16:  # todo
        todo_data = block.get("todo", {})
        checked = "x" if todo_data.get("style") == "checked" else " "
        text = extract_text(todo_data.get("elements", [])).strip()
        md += f"- [{checked}] {text}\n\n"

    elif bt not in [1, 23, 24, 31]:  # skip page, grid, grid_column, table_cell
        text = get_text(block).strip()
        if text:
            md += f"{text}\n\n"

    # 递归渲染子节点
    for kid in children_map.get(bid, []):
        md += render(kid)

    return md

# ====== Step 5: 渲染并保存 ======
root_children = children_map.get(DOC_TOKEN, [])
full_md = f"# {title}\n\n"
for child in root_children:
    full_md += render(child)

# 清理多余空行
full_md = re.sub(r'\n{3,}', '\n\n', full_md).strip() + "\n"

# 保存
filename = re.sub(r'[/\\:*?"<>|]', '_', title) + ".md"
write_file(os.path.join(OUTPUT_DIR, filename), full_md)
```

## Block 类型参考

| block_type | 类型 | Markdown 输出 |
|---|---|---|
| 1 | page | 跳过（根节点） |
| 2 | text | 普通段落 |
| 3-11 | heading1-9 | `#` 到 `#########` |
| 12 | bullet | `- item` |
| 13 | ordered | `1. item` |
| 14 | code | ` ```lang ... ``` ` |
| 15 | quote | `> text` |
| 16 | todo | `- [ ] text` / `- [x] text` |
| 21 | divider | `---` |
| 26 | image | `![image](url)` |
| 30 | table | Markdown 表格 |
| 31 | table_cell | 表格单元格（table 子节点，不单独渲染） |
| 23 | grid | 跳过 |
| 24 | grid_column | 跳过 |

## 故障排除

| 问题 | 原因 | 解决 |
|------|------|------|
| Auth error (code != 0) | app_id/app_secret 错误 | 检查凭证文件 |
| 文档访问被拒 | 应用无权限或文档未分享给应用 | 开通 `docx:document:readonly` 权限，文档分享给应用 |
| 内容为空 | 文档确实为空或权限不足 | 检查 blocks 返回是否为空 |
| 格式丢失 | 用了 `raw_content` 接口 | 改用 blocks API |
| feishu CLI 报 self_manage 权限错误 | CLI 需要 OAuth | 直接用 API，不依赖 CLI |

## 知识库文档

如果 URL 是 `https://xxx.feishu.cn/wiki/TOKEN`，需要先获取实际的 docx token：

```
GET https://open.feishu.cn/open-apis/wiki/v2/spaces/get_node?token=WIKI_TOKEN
Authorization: Bearer {token}
```

返回的 `data.node.obj_token` 就是 docx token，然后用上面的流程处理。

## 飞书 CLI 配置（可选）

如果也想让 CLI 工作，创建 `~/.feishu-cli/config.json`：

```json
{
  "channels": {
    "feishu": {
      "appId": "YOUR_APP_ID",
      "appSecret": "YOUR_APP_SECRET",
      "domain": "feishu"
    }
  }
}
```

但 CLI 的 OAuth device-flow 不稳定，推荐直接用 API。
