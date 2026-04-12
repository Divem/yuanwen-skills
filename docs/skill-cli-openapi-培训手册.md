# Skill / CLI / OpenAPI 培训手册

> 适用项目：种点什么 — 云端菜园认养平台 | 更新日期：2026-04-10
> 预计学习时间：3-4 小时（含实操练习）

---

## 培训目标

完成本手册学习后，你将能够：

- ✅ 独立安装和配置所有 CLI 工具
- ✅ 使用 Lark-CLI 进行飞书文档和消息管理
- ✅ 使用 Pencil CLI 生成和修改 UI 设计
- ✅ 使用 GitHub CLI 完成日常开发协作
- ✅ 使用 AutoGLM CLI 进行 Android 自动化测试
- ✅ 通过 Python 直接调用飞书 OpenAPI 实现批量操作

---

## 模块一：环境搭建（30 分钟）

### 1.1 前置条件检查

```bash
# 检查 Node.js（Lark-CLI 和 Pencil CLI 需要）
node --version    # 需要 >= 18.x

# 检查 Python（AutoGLM 和 OpenAPI 脚本需要）
python3 --version  # 需要 >= 3.10

# 检查 Homebrew（macOS 安装 GitHub CLI 需要）
brew --version

# 检查 ADB（AutoGLM 需要）
adb version
```

### 1.2 一键安装所有工具

```bash
# 1. Lark-CLI
npm install -g @larksuite/lark-cli

# 2. Pencil CLI
npm install -g @pencil.dev/cli

# 3. GitHub CLI
brew install gh

# 4. Python 依赖（用于 OpenAPI 直接调用）
pip install requests

# 5. AutoGLM CLI（如需 Android 自动化）
git clone https://github.com/zai-org/Open-AutoGLM.git
cd Open-AutoGLM && pip install -e .
cd agent-harness && pip install -e .
```

### 1.3 认证配置

#### Lark-CLI 认证

```bash
# 初始化配置（需要飞书开放平台的 App ID 和 App Secret）
lark-cli config init

# 浏览器登录
lark-cli auth login

# 验证
lark-cli doctor
```

> 📌 **获取 App ID/Secret**：前往 [飞书开放平台](https://open.feishu.cn/) → 创建企业自建应用 → 凭证与基础信息

#### GitHub CLI 认证

```bash
# 交互式登录（浏览器完成授权）
gh auth login

# 验证
gh auth status
```

#### Pencil CLI 认证

```bash
# 交互式登录
pencil login

# 验证
pencil status
```

### 1.4 验证安装

```bash
# 逐一验证
lark-cli --version
pencil version
gh --version
cli-anything-open-autoglm --version  # 如已安装
```

**🎯 检查点**：以上命令全部返回版本号即表示环境搭建完成。

---

## 模块二：Lark-CLI 实战（45 分钟）

### 2.1 基础概念

Lark-CLI 的命令结构为：

```
lark-cli <服务> <+操作> [--参数]
```

- **服务**：`docs`、`im`、`base`、`calendar` 等
- **操作**：前缀 `+`，如 `+search`、`+messages-send`
- **参数**：`--format json`、`--page-all` 等

### 2.2 文档操作

#### 练习 1：搜索和读取文档

```bash
# 搜索包含关键词的文档
lark-cli docs +search --query "商业计划书"

# 获取文档信息（需要 document_token）
lark-cli docs +get --document-id "BlUiwJZZuiZnNOk8YItcvaldn9C"

# 以表格形式输出
lark-cli docs +search --query "种点什么" --format table
```

#### 练习 2：使用 API 子命令进行高级操作

```bash
# 获取文档所有内容块
lark-cli api GET /docx/v1/documents/BlUiwJZZuiZnNOk8YItcvaldn9C/blocks --page-all

# 创建新文档
lark-cli api POST /docx/v1/documents \
  --data '{"title":"测试文档","folder_token":"URd6fDrTllhkVodVFj7cNfd9ndw"}'

# Dry-run 模式（只看请求不执行）
lark-cli api POST /docx/v1/documents \
  --data '{"title":"测试"}' \
  --dry-run
```

### 2.3 即时通讯

#### 练习 3：发送消息

```bash
# 发送文本消息到群组
lark-cli im +messages-send --chat-id oc_xxx --text "测试消息"

# 发送富文本消息（JSON 格式）
lark-cli im +messages-send --chat-id oc_xxx \
  --msg-type "post" \
  --data '{"zh_cn":{"title":"今日更新","content":[[{"tag":"text","text":"菜地照片已上传"}]]}}'
```

### 2.4 通用技巧

```bash
# 自动分页获取所有结果
lark-cli base +records-list --app-token xxx --table-id yyy --page-all

# 输出为 CSV（方便导入 Excel）
lark-cli base +records-list --app-token xxx --table-id yyy --format csv -o data.csv

# JSON 输出 + jq 筛选
lark-cli docs +search --query "计划" | jq '.data.docs_entities[].title'
```

**🎯 检查点**：能够通过命令行搜索文档、发送消息、使用 API 子命令。

---

## 模块三：Pencil CLI 实战（30 分钟）

### 3.1 设计生成

#### 练习 4：创建一个简单页面

```bash
# 生成登录页设计
pencil --out login.pen --prompt "设计一个简洁的移动端登录页面，包含：Logo区域、手机号输入框、验证码输入框、登录按钮、微信登录选项"
```

#### 练习 5：迭代修改设计

```bash
# 在已有设计上添加元素
pencil --in login.pen --out login-v2.pen \
  --prompt "在页面底部添加用户协议和隐私政策的链接文字"

# 修改配色方案
pencil --in login-v2.pen --out login-v3.pen \
  --prompt "将主色调改为绿色 #4CAF50，体现农业主题"
```

### 3.2 批量操作

#### 练习 6：通过任务文件批量生成

创建 `tasks.json`：

```json
[
  { "prompt": "设计App首页：顶部搜索栏、轮播图展示农场实景、菜地认养卡片列表" },
  { "prompt": "在首页底部添加导航栏：首页、我的菜地、农场探访、个人中心" },
  { "prompt": "添加一个浮动的'立即认养'按钮在右下角" }
]
```

```bash
pencil --tasks tasks.json --out homepage.pen
```

### 3.3 导出图片

```bash
# 导出为 2 倍分辨率 PNG
pencil --in homepage.pen --out homepage.pen --export homepage.png --export-scale 2

# 导出为 PDF
pencil --in homepage.pen --out homepage.pen --export homepage.pdf --export-type pdf
```

**🎯 检查点**：能够用自然语言创建设计、迭代修改、批量操作并导出图片。

---

## 模块四：GitHub CLI 实战（30 分钟）

### 4.1 日常开发流程

#### 练习 7：完整的 PR 工作流

```bash
# 1. 创建并切换到功能分支
git checkout -b feat/daily-photo-push

# 2. 编写代码后提交
git add .
git commit -m "feat: 添加每日照片推送功能"

# 3. 推送分支并创建 PR
gh pr create \
  --title "feat: 添加每日照片推送功能" \
  --body "## 变更说明
- 新增定时摄影模块
- 实现用户推送通知
  
## 测试计划
- [ ] 单元测试通过
- [ ] 集成测试通过"

# 4. 查看 PR 状态
gh pr status

# 5. 查看 CI 检查结果
gh pr checks
```

### 4.2 Issue 管理

#### 练习 8：创建和管理 Issue

```bash
# 创建 Issue
gh issue create \
  --title "bug: iOS 端照片加载缓慢" \
  --body "复现步骤：1. 打开我的菜地 2. 等待照片加载 3. 超过 5 秒" \
  --label "bug"

# 列出所有未关闭的 bug
gh issue list --label "bug" --state open

# 关闭 Issue
gh issue close 42 --comment "已在 PR #55 中修复"
```

### 4.3 常用快捷操作

```bash
# 在浏览器中打开当前仓库
gh repo view --web

# 查看最近 5 次 Actions 运行
gh run list --limit 5

# 下载最新 Release
gh release download --latest
```

**🎯 检查点**：能够通过命令行创建 PR、管理 Issue、查看 CI 状态。

---

## 模块五：飞书 OpenAPI 直接调用（45 分钟）

### 5.1 何时使用 OpenAPI 而非 Lark-CLI

| 场景 | 推荐工具 |
|------|---------|
| 简单查询、一次性操作 | Lark-CLI |
| 批量操作（>50 条记录） | OpenAPI + Python |
| 需要复杂逻辑判断 | OpenAPI + Python |
| 需要错误重试和日志 | OpenAPI + Python |
| CI/CD 自动化流程 | OpenAPI + Python |

### 5.2 认证流程

#### 练习 9：获取 Access Token

```python
import requests

BASE_URL = "https://open.feishu.cn/open-apis"

def get_tenant_token(app_id, app_secret):
    """获取租户级访问令牌"""
    url = f"{BASE_URL}/auth/v3/tenant_access_token/internal"
    resp = requests.post(url, json={
        "app_id": app_id,
        "app_secret": app_secret
    })
    data = resp.json()
    
    if data.get("code") == 0:
        print(f"✓ Token 获取成功，有效期 {data['expire']} 秒")
        return data["tenant_access_token"]
    else:
        raise Exception(f"认证失败: {data.get('msg')}")

# 使用环境变量（推荐！）
import os
token = get_tenant_token(
    os.environ["FEISHU_APP_ID"],
    os.environ["FEISHU_APP_SECRET"]
)
```

> ⚠️ **安全提醒**：永远不要把 App Secret 硬编码到代码中，使用环境变量：
> ```bash
> export FEISHU_APP_ID="cli_a9xxxxxxxxxx"
> export FEISHU_APP_SECRET="hOYkxxxxxxxxxxxxxxxx"
> ```

### 5.3 文档操作

#### 练习 10：创建文档并写入内容

```python
import requests
import os

BASE_URL = "https://open.feishu.cn/open-apis"

class FeishuClient:
    def __init__(self):
        self.token = None
    
    def auth(self):
        """认证"""
        resp = requests.post(
            f"{BASE_URL}/auth/v3/tenant_access_token/internal",
            json={
                "app_id": os.environ["FEISHU_APP_ID"],
                "app_secret": os.environ["FEISHU_APP_SECRET"]
            }
        )
        self.token = resp.json()["tenant_access_token"]
    
    @property
    def headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
    
    def create_doc(self, title, folder_token):
        """创建文档"""
        resp = requests.post(
            f"{BASE_URL}/docx/v1/documents",
            headers=self.headers,
            json={"title": title, "folder_token": folder_token}
        )
        data = resp.json()
        doc_id = data["data"]["document"]["document_id"]
        print(f"✓ 文档已创建: {doc_id}")
        return doc_id
    
    def add_content(self, doc_id, blocks):
        """向文档添加内容块"""
        # 获取文档根块 ID
        resp = requests.get(
            f"{BASE_URL}/docx/v1/documents/{doc_id}/blocks",
            headers=self.headers,
            params={"page_size": 1}
        )
        root_id = resp.json()["data"]["items"][0]["block_id"]
        
        # 批量添加内容
        resp = requests.post(
            f"{BASE_URL}/docx/v1/documents/{doc_id}/blocks/{root_id}/children",
            headers=self.headers,
            json={"children": blocks}
        )
        print(f"✓ 已添加 {len(blocks)} 个内容块")
        return resp.json()

# 使用示例
client = FeishuClient()
client.auth()

doc_id = client.create_doc("农场周报 - 第 15 周", "URd6fDrTllhkVodVFj7cNfd9ndw")

client.add_content(doc_id, [
    {
        "block_type": 3,  # heading1
        "heading1": {
            "elements": [{"text_run": {"content": "本周菜地生长情况"}}]
        }
    },
    {
        "block_type": 2,  # text
        "text": {
            "elements": [{"text_run": {"content": "番茄区域长势良好，预计下周可以采摘。"}}]
        }
    }
])
```

### 5.4 批量文档复制

#### 练习 11：批量复制课程章节（项目实际场景）

```python
"""
场景：将教程源文档的内容批量复制到目标文档
核心逻辑：读取源文档块 → 转换格式 → 写入目标文档
"""

# 支持的块类型映射
BLOCK_TYPE_MAP = {
    2: "text",        # 文本
    3: "heading1",    # 一级标题
    4: "heading2",    # 二级标题
    5: "heading3",    # 三级标题
    12: "ordered",    # 有序列表
    13: "bullet",     # 无序列表
    14: "code",       # 代码块
    15: "quote",      # 引用
    22: "divider",    # 分割线
}

def copy_doc_content(client, source_token, target_doc_id, batch_size=50):
    """复制文档内容（分批处理避免限流）"""
    # 1. 读取源文档所有块
    blocks = []
    page_token = None
    while True:
        params = {"page_size": 500}
        if page_token:
            params["page_token"] = page_token
        
        resp = requests.get(
            f"{BASE_URL}/docx/v1/documents/{source_token}/blocks",
            headers=client.headers,
            params=params
        )
        data = resp.json()["data"]
        blocks.extend(data["items"])
        
        if not data.get("has_more"):
            break
        page_token = data["page_token"]
    
    print(f"  源文档共 {len(blocks)} 个块")
    
    # 2. 转换并分批写入（跳过第一个 page 块）
    converted = []
    for block in blocks[1:]:  # 跳过 page 块
        block_type = block.get("block_type")
        if block_type in BLOCK_TYPE_MAP:
            converted.append(convert_block(block))
    
    # 3. 分批写入（每批最多 50 个）
    for i in range(0, len(converted), batch_size):
        batch = converted[i:i + batch_size]
        client.add_content(target_doc_id, batch)
        print(f"  已写入 {min(i + batch_size, len(converted))}/{len(converted)}")
        time.sleep(0.5)  # 避免限流
```

### 5.5 常见 API 错误处理

| 错误码 | 含义 | 解决方案 |
|--------|------|---------|
| 99991668 | Token 过期 | 重新调用 `get_access_token()` |
| 99991400 | 参数错误 | 检查请求体 JSON 格式 |
| 99991403 | 权限不足 | 在飞书开放平台添加对应权限 |
| 99991672 | 请求频率超限 | 添加 `time.sleep()` 延迟 |

**🎯 检查点**：能够用 Python 获取 Token、创建文档、批量写入内容块、处理常见错误。

---

## 模块六：AutoGLM CLI 实战（30 分钟）

### 6.1 设备连接

#### 练习 12：连接 Android 设备

```bash
# 列出已连接设备
cli-anything-open-autoglm device list

# USB 连接（自动检测）
cli-anything-open-autoglm device list

# WiFi 连接
cli-anything-open-autoglm device tcpip 5555 --serial <设备序列号>
cli-anything-open-autoglm device connect 192.168.1.100:5555
```

### 6.2 任务执行

#### 练习 13：自然语言控制手机

```bash
# 简单任务
cli-anything-open-autoglm task run "打开设置，查看 WiFi 名称"

# 复杂任务
cli-anything-open-autoglm task run "打开微信，搜索'种点什么'公众号，关注它"

# 查看任务历史
cli-anything-open-autoglm task history

# 快速执行（不进入交互模式）
cli-anything-open-autoglm exec "截取当前屏幕"
```

### 6.3 脚本录制与回放

#### 练习 14：录制可复用脚本

```bash
# 进入 REPL 交互模式
cli-anything-open-autoglm repl

# REPL 内部命令：
> /record start my_test      # 开始录制
> 打开种点什么App             # 执行操作
> 点击我的菜地               # 执行操作
> /record stop               # 停止录制

# 导出为脚本
cli-anything-open-autoglm script export my_test --format json -o my_test.json

# 回放脚本
cli-anything-open-autoglm task run --script my_test.json
```

**🎯 检查点**：能够连接设备、用自然语言控制手机、录制和回放脚本。

---

## 模块七：综合实战（30 分钟）

### 练习 15：端到端工作流

模拟一个完整的工作流程，串联所有工具：

```bash
# 第一步：用 Pencil 设计新功能的 UI
pencil --out 新功能-认养日历.pen \
  --prompt "设计一个认养日历页面，展示每日菜地照片，可左右滑动切换日期"

# 第二步：导出设计图用于评审
pencil --in 新功能-认养日历.pen --out 新功能-认养日历.pen \
  --export 新功能-认养日历.png --export-scale 2

# 第三步：创建 GitHub Issue 追踪需求
gh issue create \
  --title "feat: 认养日历功能" \
  --body "设计稿见附件。需实现日历视图 + 每日照片展示。"

# 第四步：开发完成后创建 PR
gh pr create --title "feat: 实现认养日历功能" --body "Closes #123"

# 第五步：用 Lark-CLI 在团队群通知
lark-cli im +messages-send --chat-id oc_xxx \
  --text "🌱 认养日历功能已提交 PR，请 review"

# 第六步（可选）：用 AutoGLM 在真机上自动化测试
cli-anything-open-autoglm task run \
  "打开种点什么App，进入认养日历页面，左滑三次查看历史照片"
```

---

## 附录 A：常用命令速查表

### Lark-CLI

| 场景 | 命令 |
|------|------|
| 搜索文档 | `lark-cli docs +search --query "关键词"` |
| 发送消息 | `lark-cli im +messages-send --chat-id oc_xxx --text "内容"` |
| 查看日程 | `lark-cli calendar +agenda` |
| 调用任意 API | `lark-cli api <METHOD> <PATH> [--data JSON]` |
| Dry-run | 任何命令加 `--dry-run` |
| 全量分页 | 任何列表命令加 `--page-all` |

### Pencil CLI

| 场景 | 命令 |
|------|------|
| 新建设计 | `pencil --out file.pen --prompt "描述"` |
| 修改设计 | `pencil --in a.pen --out b.pen --prompt "修改描述"` |
| 批量操作 | `pencil --tasks tasks.json --out file.pen` |
| 导出图片 | `pencil --in file.pen --out file.pen --export img.png` |
| 高清导出 | 加 `--export-scale 2` |

### GitHub CLI

| 场景 | 命令 |
|------|------|
| 创建 PR | `gh pr create --title "标题" --body "描述"` |
| PR 状态 | `gh pr status` |
| 创建 Issue | `gh issue create --title "标题"` |
| 查看 CI | `gh run list --limit 5` |
| 打开网页 | `gh repo view --web` |

### 飞书 OpenAPI

| 场景 | 端点 |
|------|------|
| 获取 Token | `POST /auth/v3/tenant_access_token/internal` |
| 创建文档 | `POST /docx/v1/documents` |
| 读取文档块 | `GET /docx/v1/documents/{token}/blocks` |
| 写入内容 | `POST /docx/v1/documents/{id}/blocks/{parent}/children` |

---

## 附录 B：故障排查

### Lark-CLI 常见问题

| 问题 | 排查步骤 |
|------|---------|
| `Unauthorized` | 执行 `lark-cli auth login` 重新登录 |
| `Permission denied` | 检查飞书应用权限配置 |
| 分页数据不全 | 加 `--page-all --page-limit 0` |

### Pencil CLI 常见问题

| 问题 | 排查步骤 |
|------|---------|
| 认证失败 | 执行 `pencil login` 重新登录 |
| 生成结果不理想 | 优化 prompt，加入更具体的描述 |
| 导出失败 | 检查 `--export-type` 参数 |

### OpenAPI 常见问题

| 问题 | 排查步骤 |
|------|---------|
| Token 过期 | 检查 `expire` 字段，重新获取 |
| 写入内容为空 | 检查 `block_type` 和字段名是否匹配 |
| 频率限制 | 在请求间加 `time.sleep(0.5)` |

---

## 附录 C：进阶学习资源

| 工具 | 资源 |
|------|------|
| Lark-CLI | [飞书开放平台文档](https://open.feishu.cn/document/) |
| Pencil CLI | 内置 `pencil --help` |
| GitHub CLI | [官方手册](https://cli.github.com/manual) |
| AutoGLM | [GitHub 仓库](https://github.com/zai-org/Open-AutoGLM) |
| 飞书 OpenAPI | [API Explorer](https://open.feishu.cn/api-explorer/) — 在线调试所有 API |
