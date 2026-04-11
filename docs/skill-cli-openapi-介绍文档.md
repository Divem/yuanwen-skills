# Skill / CLI / OpenAPI 工具链介绍文档

> 版本：1.0 | 适用项目：种点什么 — 云端菜园认养平台 | 更新日期：2026-04-10

---

## 一、概述

"种点什么"项目在开发和运营过程中，深度整合了一套 **Skill + CLI + OpenAPI** 工具链，用于实现从设计、开发、文档管理到自动化测试的全流程覆盖。

### 工具全景图

```
┌─────────────────────────────────────────────────────────┐
│                   种点什么 · 工具链                       │
├──────────┬──────────┬──────────┬──────────┬─────────────┤
│ Lark-CLI │ Pencil   │ GitHub   │ AutoGLM  │ Feishu      │
│ 飞书CLI  │ CLI      │ CLI (gh) │ CLI      │ OpenAPI     │
│          │ 设计工具  │ 代码协作  │ 手机自动化│ 直接API调用  │
├──────────┼──────────┼──────────┼──────────┼─────────────┤
│ 文档管理  │ UI 设计  │ 仓库管理  │ App 测试 │ 批量文档操作 │
│ 消息通知  │ 原型生成  │ PR/Issue │ 脚本录制  │ 认证鉴权    │
│ 多维表格  │ 图片导出  │ CI/CD    │ 任务执行  │ 内容同步    │
└──────────┴──────────┴──────────┴──────────┴─────────────┘
```

---

## 二、各工具详解

### 2.1 Lark-CLI（飞书命令行工具）

**定位**：项目文档管理和团队协作的核心工具

| 属性 | 说明 |
|------|------|
| 包名 | `@larksuite/lark-cli` |
| 安装 | `npm install -g @larksuite/lark-cli` |
| 文档 | https://open.feishu.cn/document/ |

**核心能力**：

- **文档操作 (docs)** — 创建、搜索、读取飞书文档，是项目知识库的入口
- **即时通讯 (im)** — 发送消息、管理群聊，用于项目通知和协作
- **多维表格 (base)** — 数据管理，适合用户认养记录、农场状态追踪
- **日历 (calendar)** — 农场活动排期、用户预约管理
- **知识库 (wiki)** — 项目文档沉淀、培训材料管理
- **API 直调 (api)** — 当内置命令不足时，直接调用飞书 OpenAPI

**项目中的典型用法**：

```bash
# 搜索项目文档
lark-cli docs +search --query "商业计划书"

# 发送群消息通知
lark-cli im +messages-send --chat-id oc_xxx --text "今日农场照片已更新"

# 直接调用 API（创建文档）
lark-cli api POST /docx/v1/documents --data '{"title":"新章节","folder_token":"xxx"}'
```

---

### 2.2 Pencil CLI（AI 设计工具）

**定位**：基于 AI 的 UI/UX 设计生成器，用于快速产出应用界面原型

| 属性 | 说明 |
|------|------|
| 包名 | `@pencil.dev/cli` |
| 版本 | 0.2.4 |
| AI 模型 | Claude Opus（默认） |
| 文件格式 | `.pen`（专有矢量设计格式） |

**核心能力**：

- **从零创建** — 通过自然语言描述生成完整设计文件
- **迭代修改** — 在现有设计基础上通过提示词修改
- **批量操作** — 通过 JSON 任务文件一次性执行多个设计任务
- **图片导出** — 支持 PNG/JPEG/WEBP/PDF 格式导出

**项目中的典型用法**：

```bash
# 创建应用主页设计
pencil --out 种点什么-主页.pen --prompt "设计一个云端菜园认养App首页，包含菜地列表、今日照片、认养状态"

# 在已有设计上迭代
pencil --in 种点什么-主页.pen --out 种点什么-主页-v2.pen --prompt "添加底部导航栏：首页、我的菜地、农场、个人中心"

# 导出为 PNG
pencil --in 种点什么-主页.pen --out 种点什么-主页.pen --export 种点什么-主页.png --export-scale 2
```

---

### 2.3 GitHub CLI (gh)

**定位**：代码仓库管理和开发协作

| 属性 | 说明 |
|------|------|
| 版本 | 2.88.1 |
| 安装 | `brew install gh` (macOS) |
| 文档 | https://cli.github.com/manual |

**核心能力**：

- **仓库管理** — 创建、克隆、Fork 仓库
- **PR 工作流** — 创建、审查、合并 Pull Request
- **Issue 追踪** — 创建和管理项目 Issue
- **CI/CD** — 查看和管理 GitHub Actions 运行状态
- **API 调用** — 通过 `gh api` 直接调用 GitHub REST/GraphQL API

**项目中的典型用法**：

```bash
# 创建 PR
gh pr create --title "feat: 添加每日照片推送功能" --body "实现定时摄影+用户推送"

# 查看 CI 状态
gh run list --limit 5

# 搜索代码
gh search code "FeishuDocCopier" --repo dawinyuan/zhongseed
```

---

### 2.4 Open-AutoGLM CLI（Android 自动化）

**定位**：基于视觉语言模型的 Android 手机自动化测试工具

| 属性 | 说明 |
|------|------|
| 命令 | `cli-anything-open-autoglm` |
| Python | >= 3.10 |
| 连接方式 | ADB (USB / WiFi) |

**核心能力**：

- **设备管理** — 通过 ADB 管理 Android 设备连接
- **自然语言任务** — 用中文描述要执行的操作，AI 自动控制手机完成
- **脚本录制** — 将操作录制为 JSON/Python 脚本，支持回放
- **交互模式 (REPL)** — 持续对话式操作手机

**项目中的典型用法**：

```bash
# 连接设备
cli-anything-open-autoglm device connect 192.168.1.100:5555

# 执行自动化任务
cli-anything-open-autoglm task run "打开种点什么App，进入我的菜地页面，截取当前生长状态"

# 启动交互模式
cli-anything-open-autoglm repl --device emulator-5554
```

---

### 2.5 飞书 OpenAPI（直接 API 调用）

**定位**：当 Lark-CLI 内置命令无法满足需求时，通过 Python + requests 直接调用飞书 OpenAPI

| 属性 | 说明 |
|------|------|
| 基地址 | `https://open.feishu.cn/open-apis` |
| 认证方式 | tenant_access_token（应用级别） |
| 封装类 | `FeishuDocCopier`（项目自研） |

**项目中使用的核心 API 端点**：

| 端点 | 方法 | 用途 |
|------|------|------|
| `/auth/v3/tenant_access_token/internal` | POST | 获取访问令牌 |
| `/docx/v1/documents` | POST | 创建新文档 |
| `/docx/v1/documents/{token}/blocks` | GET | 获取文档内容块 |
| `/docx/v1/documents/{id}/blocks/batch_create` | POST | 批量插入内容块 |
| `/docx/v1/documents/{id}/blocks/{parent}/children` | POST | 在指定位置添加子块 |

**代码示例**（来自 `copy_docs_api.py`）：

```python
class FeishuDocCopier:
    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret
    
    def get_access_token(self):
        url = f"{BASE_URL}/auth/v3/tenant_access_token/internal"
        resp = requests.post(url, json={
            "app_id": self.app_id,
            "app_secret": self.app_secret
        })
        self.access_token = resp.json()["tenant_access_token"]
    
    def create_document(self, title, folder_token):
        url = f"{BASE_URL}/docx/v1/documents"
        resp = requests.post(url, headers=self.get_headers(), json={
            "title": title,
            "folder_token": folder_token
        })
        return resp.json()["data"]["document"]["document_id"]
```

---

## 三、工具间的协作关系

```
    ┌──────────────┐
    │ 需求/设计阶段  │
    └──────┬───────┘
           ▼
    ┌──────────────┐    生成 UI 原型     ┌──────────────┐
    │  Pencil CLI  │ ──────────────────→ │  .pen 文件    │
    └──────────────┘    导出 PNG          │  .png 截图    │
                                         └──────────────┘
           ▼
    ┌──────────────┐    推送代码         ┌──────────────┐
    │  GitHub CLI  │ ──────────────────→ │  远程仓库     │
    │  (gh)        │    管理 PR/Issue    │  CI/CD       │
    └──────────────┘                     └──────────────┘
           ▼
    ┌──────────────┐    管理文档         ┌──────────────┐
    │  Lark-CLI    │ ──────────────────→ │  飞书知识库   │
    │  + OpenAPI   │    发送通知         │  团队群组     │
    └──────────────┘                     └──────────────┘
           ▼
    ┌──────────────┐    自动化测试       ┌──────────────┐
    │  AutoGLM CLI │ ──────────────────→ │  测试报告     │
    │              │    录制脚本         │  操作脚本     │
    └──────────────┘                     └──────────────┘
```

---

## 四、环境要求总览

| 工具 | 运行环境 | 依赖 |
|------|---------|------|
| Lark-CLI | Node.js | npm |
| Pencil CLI | Node.js | npm, Anthropic API Key |
| GitHub CLI | 原生二进制 | Homebrew (macOS) |
| AutoGLM CLI | Python >= 3.10 | ADB, pip |
| 飞书 OpenAPI | Python 3.x | requests 库, App ID/Secret |

---

## 五、安全注意事项

1. **凭证管理** — App ID 和 App Secret 应使用环境变量存储，禁止硬编码到源码中
2. **Token 时效** — tenant_access_token 有效期约 2 小时，需要定期刷新
3. **权限最小化** — 飞书应用只申请实际需要的 API 权限范围
4. **敏感文件** — `.env`、凭证文件不得提交到 Git 仓库
