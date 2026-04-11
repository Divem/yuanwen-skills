# Lark-CLI 命令参考手册

> 版本：1.0.0 | GitHub：https://github.com/larksuite/cli | API 文档：https://open.feishu.cn/document/

Lark-CLI 是飞书/Lark 的官方命令行工具，让你在终端中直接与飞书的所有核心服务交互。

## 目录

- [安装](#安装)
- [快速上手](#快速上手)
- [通用标志 (Global Flags)](#通用标志-global-flags)
- [身份类型 (--as)](#身份类型---as)
- [输出格式 (--format)](#输出格式---format)
- [认证管理 (auth)](#认证管理-auth)
- [配置管理 (config)](#配置管理-config)
- [健康检查 (doctor)](#健康检查-doctor)
- [即时通讯 (im)](#即时通讯-im)
- [通讯录 (contact)](#通讯录-contact)
- [日历 (calendar)](#日历-calendar)
- [文档 (docs)](#文档-docs)
- [云盘 (drive)](#云盘-drive)
- [多维表格 (base)](#多维表格-base)
- [电子表格 (sheets)](#电子表格-sheets)
- [知识库 (wiki)](#知识库-wiki)
- [任务 (task)](#任务-task)
- [邮件 (mail)](#邮件-mail)
- [视频会议 (vc)](#视频会议-vc)
- [会议纪要 (minutes)](#会议纪要-minutes)
- [事件订阅 (event)](#事件订阅-event)
- [API 请求 (api)](#api-请求-api)
- [Schema 查询 (schema)](#schema-查询-schema)
- [AI Agent 技能集成](#ai-agent-技能集成)

---

## 安装

```bash
npm install -g @larksuite/lark-cli
```

---

## 快速上手

```bash
# 1. 初始化配置（输入 App ID 和 App Secret）
lark-cli config init

# 2. 登录授权（浏览器中完成）
lark-cli auth login

# 3. 检查状态
lark-cli doctor

# 4. 开始使用
lark-cli calendar +agenda
lark-cli docs +search --query "项目计划"
lark-cli im +messages-send --chat-id oc_xxx --text "Hello"
```

---

## 通用标志 (Global Flags)

| 标志 | 说明 | 默认值 |
|------|------|--------|
| `--as <type>` | 身份类型：`user` / `bot` / `auto` | `auto` |
| `--format <fmt>` | 输出格式：`json` / `ndjson` / `table` / `csv` / `pretty` | `json` |
| `--dry-run` | 只打印请求，不执行 | - |
| `--page-all` | 自动分页获取所有结果 | - |
| `--page-size <N>` | 每页大小（0 = 使用 API 默认值） | - |
| `--page-limit <N>` | `--page-all` 最大页数（默认 10，0 = 无限） | - |
| `--page-delay <MS>` | 分页间隔毫秒数（默认 200） | - |
| `-o, --output <path>` | 输出到文件 | - |
| `--params <json>` | URL/查询参数 JSON | - |
| `--data <json>` | 请求体 JSON (POST/PATCH/PUT/DELETE) | - |

---

## 身份类型 (--as)

| 类型 | 说明 |
|------|------|
| `user` | 以用户身份调用（使用用户 token） |
| `bot` | 以应用身份调用（使用 app ticket） |
| `auto` | 自动选择（默认） |

部分命令仅支持特定身份（如 `+messages-send` 仅支持 `bot`）。

---

## 输出格式 (--format)

| 格式 | 说明 |
|------|------|
| `json` | 原始 JSON（默认） |
| `pretty` | 格式化 JSON（带缩进和颜色） |
| `table` | 表格形式展示 |
| `csv` | CSV 格式 |
| `ndjson` | 每行一个 JSON 对象 |

---

## 认证管理 (auth)

```bash
# 查看认证状态
lark-cli auth status

# 设备流授权登录（浏览器中完成）
lark-cli auth login

# 指定权限域登录
lark-cli auth login --domain calendar,task

# 只请求推荐权限（自动审批）
lark-cli auth login --recommend

# 请求特定 scope
lark-cli auth login --scope "calendar:calendar:read calendar:calendar:write"

# 非阻塞模式（用于 AI Agent）
lark-cli auth login --no-wait
# 返回后用 device code 完成授权
lark-cli auth login --device-code <code>

# 列出所有已登录用户
lark-cli auth list

# 检查当前 token 是否有指定 scope
lark-cli auth check --scope "calendar:calendar:read"

# 查询应用已启用的 scope
lark-cli auth scopes

# 刷新 token
lark-cli auth refresh

# 登出（清除 token）
lark-cli auth logout
```

---

## 配置管理 (config)

```bash
# 初始化配置（交互式）
lark-cli config init

# 非交互式初始化
lark-cli config init --app-id "cli_xxx" --app-secret-stdin --brand feishu
echo "my-secret" | lark-cli config init --app-id "cli_xxx" --app-secret-stdin

# 创建新应用并初始化
lark-cli config init --new

# 查看当前配置
lark-cli config show

# 查看或设置默认身份类型
lark-cli config default-as
lark-cli config default-as bot

# 移除配置（清除所有 token 和配置）
lark-cli config remove
```

**可用域 (--domain)：** `base` `calendar` `contact` `docs` `drive` `event` `im` `mail` `minutes` `sheets` `task` `vc` `wiki` `all`

---

## 健康检查 (doctor)

```bash
# 全面检查（配置、认证、网络连通性）
lark-cli doctor

# 仅检查本地状态（跳过网络检查）
lark-cli doctor --offline
```

---

## 即时通讯 (im)

### 发送消息

```bash
# 发送文本消息到群聊
lark-cli im +messages-send --chat-id oc_xxx --text "Hello World"

# 发送 Markdown 消息
lark-cli im +messages-send --chat-id oc_xxx --markdown "**粗体** 和 `代码`"

# 发送图片
lark-cli im +messages-send --chat-id oc_xxx --image /path/to/image.png

# 发送文件
lark-cli im +messages-send --chat-id oc_xxx --file /path/to/document.pdf

# 发送视频（需要封面图）
lark-cli im +messages-send --chat-id oc_xxx --video /path/to/video.mp4 --video-cover /path/to/cover.jpg

# 发送音频
lark-cli im +messages-send --chat-id oc_xxx --audio /path/to/audio.mp3

# 发送自定义 content JSON
lark-cli im +messages-send --chat-id oc_xxx --content '{"text":"hello"}' --msg-type text

# 发送私聊消息
lark-cli im +messages-send --user-id ou_xxx --text "私聊消息"

# 幂等发送（防止重复）
lark-cli im +messages-send --chat-id oc_xxx --text "hello" --idempotency-key "unique-key-123"
```

### 回复消息

```bash
# 回复消息
lark-cli im +messages-reply --message-id om_xxx --text "回复内容"

# 回复 Markdown
lark-cli im +messages-reply --message-id om_xxx --markdown "## 标题\n内容"

# 回复图片
lark-cli im +messages-reply --message-id om_xxx --image /path/to/image.png

# 在话题中回复
lark-cli im +messages-reply --message-id om_xxx --text "话题回复" --reply-in-thread
```

### 聊天管理

```bash
# 创建群聊
lark-cli im +chat-create --name "项目群" --users ou_xxx,ou_yyy --type private

# 创建公开群聊
lark-cli im +chat-create --name "公共群" --type public --set-bot-manager

# 创建群聊并邀请 bot
lark-cli im +chat-create --name "混合群" --users ou_xxx --bots cli_xxx

# 搜索群聊（按群名查找 chat_id）
lark-cli im +chat-search --query "项目群"
lark-cli im +chat-search --query "项目群" --format table

# 按成员筛选群聊
lark-cli im +chat-search --member-ids ou_xxx,ou_yyy

# 更新群名称或描述
lark-cli im +chat-update --chat-id oc_xxx --name "新群名" --description "新描述"

# 查看群列表
lark-cli im chats list
```

### 消息查看

```bash
# 列出群聊消息（默认按时间倒序）
lark-cli im +chat-messages-list --chat-id oc_xxx

# 使用 bot 身份查看
lark-cli im +chat-messages-list --chat-id oc_xxx --as bot

# 按时间范围筛选
lark-cli im +chat-messages-list --chat-id oc_xxx --start "2026-03-01T00:00:00+08:00" --end "2026-03-31T23:59:59+08:00"

# 正序排列
lark-cli im +chat-messages-list --chat-id oc_xxx --sort asc

# 查看 P2P 聊天消息
lark-cli im +chat-messages-list --user-id ou_xxx

# 美化输出
lark-cli im +chat-messages-list --chat-id oc_xxx --format table
```

### 消息搜索

```bash
# 搜索消息
lark-cli im +messages-search --query "关键词"

# 按聊天范围搜索
lark-cli im +messages-search --query "预算" --chat-id oc_xxx

# 按发送者筛选
lark-cli im +messages-search --query "报告" --sender ou_xxx

# 仅搜索 @我的消息
lark-cli im +messages-search --query "审批" --is-at-me

# 按附件类型筛选
lark-cli im +messages-search --query "设计稿" --include-attachment-type image

# 按时间范围搜索
lark-cli im +messages-search --query "项目" --start "2026-03-01T00:00:00+08:00" --end "2026-03-31T23:59:59+08:00"
```

### 消息资源

```bash
# 批量获取消息
lark-cli im +messages-mget --message-ids om_xxx,om_yyy

# 下载消息中的图片/文件
lark-cli im +messages-resources-download --message-id om_xxx --file-key boxcn_xxx

# 查看话题消息
lark-cli im +threads-messages-list omt_xxx

# 置顶消息管理
lark-cli im pins list --chat-id oc_xxx
lark-cli im pins add --chat-id oc_xxx --message-id om_xxx
lark-cli im pins remove --chat-id oc_xxx --message-id om_xxx

# 表情回应
lark-cli im reactions list --message-id om_xxx
lark-cli im reactions add --message-id om_xxx --emoji-type "[大笑]"
```

---

## 通讯录 (contact)

```bash
# 获取当前用户信息
lark-cli contact +get-user

# 获取指定用户信息
lark-cli contact +get-user --user-id ou_xxx

# 使用 union_id 查询
lark-cli contact +get-user --user-id on_xxx --user-id-type union_id

# 搜索用户（按相关性排序）
lark-cli contact +search-user --query "张三"

# 美化输出
lark-cli contact +search-user --query "张三" --format table
```

---

## 日历 (calendar)

### 日程概览

```bash
# 查看今日日程
lark-cli calendar +agenda

# 查看指定日期范围
lark-cli calendar +agenda --start "2026-04-01T00:00:00+08:00" --end "2026-04-30T23:59:59+08:00"

# 查看指定日历
lark-cli calendar +agenda --calendar-id "cal_xxx"

# 美化输出
lark-cli calendar +agenda --format table
```

### 创建日程

```bash
# 创建日程
lark-cli calendar +create \
  --summary "项目评审会议" \
  --start "2026-04-15T14:00:00+08:00" \
  --end "2026-04-15T15:00:00+08:00" \
  --description "讨论 Q2 计划"

# 创建日程并邀请参与者
lark-cli calendar +create \
  --summary "周会" \
  --start "2026-04-14T10:00:00+08:00" \
  --end "2026-04-14T11:00:00+08:00" \
  --attendee-ids "ou_xxx,ou_yyy,oc_xxx"

# 创建重复日程
lark-cli calendar +create \
  --summary "每日站会" \
  --start "2026-04-14T09:30:00+08:00" \
  --end "2026-04-14T09:45:00+08:00" \
  --rrule "FREQ=DAILY;COUNT=10"
```

### 查询空闲/忙碌

```bash
# 查看当前用户空闲/忙碌
lark-cli calendar +freebusy

# 查看指定用户
lark-cli calendar +freebusy --user-id ou_xxx --start "2026-04-14T00:00:00+08:00" --end "2026-04-14T23:59:59+08:00"
```

### 智能推荐会议时间

```bash
# 推荐可用会议时间
lark-cli calendar +suggestion --attendee-ids "ou_xxx,ou_yyy" --duration-minutes 60

# 指定搜索范围
lark-cli calendar +suggestion \
  --attendee-ids "ou_xxx" \
  --start "2026-04-14T09:00:00+08:00" \
  --end "2026-04-14T18:00:00+08:00" \
  --duration-minutes 30
```

### 底层操作

```bash
# 日历操作
lark-cli calendar calendars list
lark-cli calendar calendars get --calendar-id cal_xxx

# 日程事件操作
lark-cli calendar events list
lark-cli calendar events get --event-id evt_xxx
lark-cli calendar events delete --event-id evt_xxx
lark-cli calendar events patch --event-id evt_xxx

# 参与者操作
lark-cli calendar event.attendees list
lark-cli calendar freebusys query
```

---

## 文档 (docs)

### 创建文档

```bash
# 创建空白文档
lark-cli docs +create --title "新文档"

# 使用 Markdown 创建
lark-cli docs +create --title "项目计划" --markdown "# 项目计划\n\n## 目标\n\n- 目标一\n- 目标二"

# 在指定文件夹中创建
lark-cli docs +create --title "子文档" --folder-token fld_xxx

# 在知识库中创建
lark-cli docs +create --title "知识库文档" --wiki-space "wiki_xxx" --wiki-node "node_xxx"

# 在个人知识库中创建
lark-cli docs +create --title "个人文档" --wiki-space my_library
```

### 获取文档内容

```bash
# 通过 URL 获取
lark-cli docs +fetch --doc "https://xxx.feishu.cn/docx/xxx"

# 通过 token 获取
lark-cli docs +fetch --doc "docx_xxx"

# 美化输出
lark-cli docs +fetch --doc "https://xxx.feishu.cn/docx/xxx" --format pretty
```

### 更新文档

```bash
# 追加内容
lark-cli docs +update --doc "docx_xxx" --markdown "\n\n## 新增章节\n内容" --mode append

# 覆盖内容
lark-cli docs +update --doc "docx_xxx" --markdown "# 全新内容" --mode overwrite

# 替换指定范围内容
lark-cli docs +update --doc "docx_xxx" --mode replace_range --selection-by-title "## 旧章节" --markdown "## 新章节"

# 仅更新标题
lark-cli docs +update --doc "docx_xxx" --new-title "新标题"

# 在指定位置前插入
lark-cli docs +update --doc "docx_xxx" --mode insert_before --selection-with-ellipsis "目标文本...目标文本" --markdown "插入的内容"

# 创建空白白板
lark-cli docs +update --doc "docx_xxx" --markdown '<whiteboard type="blank"></whiteboard>' --mode append
```

### 搜索文档

```bash
# 搜索文档
lark-cli docs +search --query "项目计划"

# 带筛选条件搜索
lark-cli docs +search --query "周报" --filter '{"type":"docx"}'

# 美化输出
lark-cli docs +search --query "设计" --format table
```

### 文档媒体

```bash
# 插入图片到文档末尾
lark-cli docs +media-insert --doc "docx_xxx" --file /path/to/image.png --type image

# 插入文件到文档末尾
lark-cli docs +media-insert --doc "docx_xxx" --file /path/to/report.pdf --type file

# 设置图片对齐和标题
lark-cli docs +media-insert --doc "docx_xxx" --file /path/to/image.png --align center --caption "图1: 流程图"

# 下载文档中的图片/白板缩略图
lark-cli docs +media-download --token "img_xxx" --output ./downloaded-image.png

# 下载白板缩略图
lark-cli docs +media-download --token "whiteboard_xxx" --type whiteboard --output ./thumbnail.png

# 更新白板内容
echo '<whiteboard DSL>' | lark-cli docs +whiteboard-update --doc "docx_xxx"
```

---

## 云盘 (drive)

### 文件上传/下载

```bash
# 上传文件到云盘根目录
lark-cli drive +upload --file /path/to/report.pdf

# 上传到指定文件夹
lark-cli drive +upload --file /path/to/image.png --folder-token "fld_xxx"

# 自定义文件名
lark-cli drive +upload --file /path/to/data.csv --name "销售数据-2026.csv"

# 从云盘下载文件
lark-cli drive +download --file-token "file_xxx" --output ./downloaded.pdf

# 覆盖已有文件
lark-cli drive +download --file-token "file_xxx" --output ./file.pdf --overwrite
```

### 评论

```bash
# 添加全文评论
lark-cli drive +add-comment --doc "https://xxx.feishu.cn/docx/xxx" --content "整体写得不错"

# 在文档指定位置添加评论
lark-cli drive +add-comment --doc "docx_xxx" --content "这里需要修改" --selection-with-ellipsis "目标段落...目标段落"

# 通过 block ID 定位
lark-cli drive +add-comment --doc "docx_xxx" --block-id "blk_xxx" --content "这段建议优化"
```

### 底层操作

```bash
# 文件操作
lark-cli drive files list
lark-cli drive files get --file-token "file_xxx"
lark-cli drive files delete --file-token "file_xxx"

# 文件元信息
lark-cli drive metas get --file-token "file_xxx"

# 权限管理
lark-cli drive permission.members list --file-token "file_xxx"

# 评论操作
lark-cli drive file.comments list --file-token "file_xxx"
lark-cli drive file.comment.replys list --comment-id "cmt_xxx"
```

---

## 多维表格 (base)

### 表操作

```bash
# 列出所有表
lark-cli base +table-list --base-token "bascn_xxx"

# 获取表信息
lark-cli base +table-get --base-token "bascn_xxx" --table-id "tbl_xxx"

# 创建表（支持同时创建字段）
lark-cli base +table-create --base-token "bascn_xxx" --table-name "客户表"

# 重命名表
lark-cli base +table-update --base-token "bascn_xxx" --table-id "tbl_xxx" --new-name "新表名"

# 删除表
lark-cli base +table-delete --base-token "bascn_xxx" --table-id "tbl_xxx"
```

### 记录操作

```bash
# 列出记录
lark-cli base +record-list --base-token "bascn_xxx" --table-id "tbl_xxx"

# 指定视图查看
lark-cli base +record-list --base-token "bascn_xxx" --table-id "tbl_xxx" --view-id "viw_xxx"

# 分页查询
lark-cli base +record-list --base-token "bascn_xxx" --table-id "tbl_xxx" --limit 50 --offset 0

# 获取单条记录
lark-cli base +record-get --base-token "bascn_xxx" --table-id "tbl_xxx" --record-id "rec_xxx"

# 创建记录
lark-cli base +record-upsert --base-token "bascn_xxx" --table-id "tbl_xxx" \
  --json '{"fields":{"姓名":"张三","部门":"研发","入职日期":"2026-01-15"}}'

# 更新记录
lark-cli base +record-upsert --base-token "bascn_xxx" --table-id "tbl_xxx" \
  --record-id "rec_xxx" --json '{"fields":{"部门":"产品"}}'

# 删除记录
lark-cli base +record-delete --base-token "bascn_xxx" --table-id "tbl_xxx" --record-id "rec_xxx"

# 查看记录变更历史
lark-cli base +record-history-list --base-token "bascn_xxx" --table-id "tbl_xxx" --record-id "rec_xxx"

# 上传附件到记录
lark-cli base +record-upload-attachment --base-token "bascn_xxx" --table-id "tbl_xxx" \
  --record-id "rec_xxx" --field-name "附件" --file /path/to/attachment.pdf
```

### 数据查询

```bash
# 使用 DSL 查询（支持聚合、过滤、排序）
lark-cli base +data-query --base-token "bascn_xxx" --dsl '{
  "table_id": "tbl_xxx",
  "filter": {"conjunction": "and", "conditions":[{"field_name":"部门","operator":"is","value":["研发"]}]},
  "sort": [{"field_name":"入职日期","desc": true}],
  "field_names": ["姓名", "部门", "入职日期"]
}'
```

### 字段操作

```bash
# 列出字段
lark-cli base +field-list --base-token "bascn_xxx" --table-id "tbl_xxx"

# 创建字段
lark-cli base +field-create --base-token "bascn_xxx" --table-id "tbl_xxx" \
  --field-name "预算" --type "currency"

# 获取字段信息
lark-cli base +field-get --base-token "bascn_xxx" --table-id "tbl_xxx" --field-id "fld_xxx"

# 更新字段
lark-cli base +field-update --base-token "bascn_xxx" --table-id "tbl_xxx" --field-id "fld_xxx" --new-name "新字段名"

# 删除字段
lark-cli base +field-delete --base-token "bascn_xxx" --table-id "tbl_xxx" --field-id "fld_xxx"

# 搜索下拉选项
lark-cli base +field-search-options --base-token "bascn_xxx" --table-id "tbl_xxx" --field-id "fld_xxx" --query "研发"
```

### 视图操作

```bash
# 列出视图
lark-cli base +view-list --base-token "bascn_xxx" --table-id "tbl_xxx"

# 创建视图
lark-cli base +view-create --base-token "bascn_xxx" --table-id "tbl_xxx" --view-name "看板视图"

# 设置排序
lark-cli base +view-set-sort --base-token "bascn_xxx" --table-id "tbl_xxx" --view-id "viw_xxx" \
  --sort-conditions '[{"field_name":"入职日期","desc":true}]'

# 设置过滤
lark-cli base +view-set-filter --base-token "bascn_xxx" --table-id "tbl_xxx" --view-id "viw_xxx" \
  --filter-conditions '{"conjunction":"and","conditions":[{"field_name":"部门","operator":"is","value":["研发"]}]}'

# 重命名视图
lark-cli base +view-rename --base-token "bascn_xxx" --table-id "tbl_xxx" --view-id "viw_xxx" --new-name "新视图名"

# 删除视图
lark-cli base +view-delete --base-token "bascn_xxx" --table-id "tbl_xxx" --view-id "viw_xxx"
```

### 仪表盘 & 工作流 & 表单

```bash
# 仪表盘
lark-cli base +dashboard-list --base-token "bascn_xxx"
lark-cli base +dashboard-create --base-token "bascn_xxx" --name "数据看板"
lark-cli base +dashboard-block-create --base-token "bascn_xxx" --dashboard-id "dash_xxx"

# 表单
lark-cli base +form-list --base-token "bascn_xxx" --table-id "tbl_xxx"
lark-cli base +form-create --base-token "bascn_xxx" --table-id "tbl_xxx"

# 工作流
lark-cli base +workflow-list --base-token "bascn_xxx"
lark-cli base +workflow-create --base-token "bascn_xxx"
lark-cli base +workflow-enable --base-token "bascn_xxx" --workflow-id "wf_xxx"
```

---

## 电子表格 (sheets)

### 创建表格

```bash
# 创建空白电子表格
lark-cli sheets +create --title "销售数据"

# 创建带表头和初始数据的表格
lark-cli sheets +create --title "员工表" \
  --headers '["姓名","部门","入职日期"]' \
  --data '[["张三","研发","2026-01-15"],["李四","产品","2026-02-20"]]'

# 在指定文件夹创建
lark-cli sheets +create --title "Q2预算" --folder-token "fld_xxx"
```

### 读取数据

```bash
# 通过 URL 读取
lark-cli sheets +read --url "https://xxx.feishu.cn/sheets/xxx"

# 读取指定范围
lark-cli sheets +read --spreadsheet-token "shtcn_xxx" --range "A1:D10"

# 指定 sheet 读取
lark-cli sheets +read --spreadsheet-token "shtcn_xxx" --sheet-id "sheet1" --range "A1:Z100"

# 格式化输出
lark-cli sheets +read --url "https://xxx.feishu.cn/sheets/xxx" --format table

# 获取原始值
lark-cli sheets +read --spreadsheet-token "shtcn_xxx" --range "A1:D10" --value-render-option Formula
```

### 写入数据

```bash
# 写入数据
lark-cli sheets +write --spreadsheet-token "shtcn_xxx" --range "A1:C3" \
  --values '[["姓名","部门","薪资"],["张三","研发","20000"],["李四","产品","18000"]]'

# 追加数据
lark-cli sheets +append --spreadsheet-token "shtcn_xxx" --range "A:C" \
  --values '[["王五","设计","19000"]]'
```

### 搜索 & 导出

```bash
# 查找单元格
lark-cli sheets +find --spreadsheet-token "shtcn_xxx" --find "张三"

# 忽略大小写搜索
lark-cli sheets +find --spreadsheet-token "shtcn_xxx" --find "SALES" --ignore-case

# 正则搜索
lark-cli sheets +find --spreadsheet-token "shtcn_xxx" --find "\\d{4}-\\d{2}" --search-by-regex

# 导出为 Excel
lark-cli sheets +export --spreadsheet-token "shtcn_xxx" --file-extension xlsx --output-path ./export.xlsx

# 导出为 CSV
lark-cli sheets +export --spreadsheet-token "shtcn_xxx" --sheet-id "sheet1" --file-extension csv --output-path ./export.csv
```

### 查看信息

```bash
# 查看表格信息（包含所有 sheet 列表）
lark-cli sheets +info --spreadsheet-token "shtcn_xxx"

# 底层操作
lark-cli sheets spreadsheets list
lark-cli sheets spreadsheet.sheets list --spreadsheet-token "shtcn_xxx"
```

---

## 知识库 (wiki)

```bash
# 获取知识空间节点信息
lark-cli wiki spaces get_node --node-token "node_xxx"

# 底层操作
lark-cli wiki spaces list --space-id "wiki_xxx"
```

---

## 任务 (task)

### 创建任务

```bash
# 创建简单任务
lark-cli task +create --summary "完成项目文档"

# 创建带详情的任务
lark-cli task +create \
  --summary "代码审查" \
  --description "审查 PR #123 的代码变更" \
  --due "2026-04-20" \
  --assignee "ou_xxx"

# 使用相对日期
lark-cli task +create --summary "提交周报" --due "+2d"

# 添加到任务清单
lark-cli task +create --summary "子任务" --tasklist-id "tasklist_xxx"
```

### 查看任务

```bash
# 查看我的任务
lark-cli task +get-my-tasks

# 查看已完成任务
lark-cli task +get-my-tasks --complete

# 按截止日期筛选
lark-cli task +get-my-tasks --due-start "2026-04-01" --due-end "2026-04-30"

# 搜索任务
lark-cli task +get-my-tasks --query "文档"

# 获取所有任务（自动分页）
lark-cli task +get-my-tasks --page-all

# 美化输出
lark-cli task +get-my-tasks --format table
```

### 任务管理

```bash
# 完成任务
lark-cli task +complete --task-id "task_xxx"

# 重新打开任务
lark-cli task +reopen --task-id "task_xxx"

# 更新任务
lark-cli task +update --task-id "task_xxx" --summary "新标题" --due "2026-05-01"

# 批量更新
lark-cli task +update --task-id "task_a,task_b" --due "2026-04-30"

# 分配任务
lark-cli task +assign --task-id "task_xxx" --add "ou_xxx,ou_yyy"

# 移除任务执行人
lark-cli task +assign --task-id "task_xxx" --remove "ou_xxx"

# 添加评论
lark-cli task +comment --task-id "task_xxx" --content "进度如何？"

# 管理提醒
lark-cli task +reminder --task-id "task_xxx" --due "2026-04-15T09:00:00+08:00"

# 管理关注者
lark-cli task +followers --task-id "task_xxx" --add "ou_xxx"
```

### 任务清单

```bash
# 创建任务清单并添加任务
lark-cli task +tasklist-create --name "Q2 OKR" --description "第二季度目标"

# 管理清单成员
lark-cli task +tasklist-members --tasklist-id "tl_xxx" --add "ou_xxx"

# 向清单添加任务
lark-cli task +tasklist-task-add --tasklist-id "tl_xxx" --task-id "task_xxx"

# 底层操作
lark-cli task tasklists list
lark-cli task tasks get --task-id "task_xxx"
lark-cli task subtasks list --task-id "task_xxx"
```

---

## 邮件 (mail)

### 撰写 & 发送

```bash
# 撰写邮件（保存为草稿）
lark-cli mail +send \
  --to "alice@example.com" \
  --subject "项目进度汇报" \
  --body "<h1>项目进度</h1><p>本周完成了...</p>"

# 直接发送（需用户确认）
lark-cli mail +send \
  --to "alice@example.com" \
  --subject "项目进度汇报" \
  --body "本周完成了..." \
  --confirm-send

# 带抄送和密送
lark-cli mail +send \
  --to "alice@example.com" \
  --cc "bob@example.com,carol@example.com" \
  --bcc "manager@example.com" \
  --subject "周报" \
  --body "本周工作汇报"

# 带附件
lark-cli mail +send \
  --to "alice@example.com" \
  --subject "设计稿" \
  --body "请查看附件" \
  --attach "/path/to/design.pdf,/path/to/data.xlsx"

# 内联图片
lark-cli mail +send \
  --to "alice@example.com" \
  --subject "报告" \
  --body '<p>见图</p><img src="cid:a1b2c3">' \
  --inline '[{"cid":"a1b2c3","file_path":"/path/to/chart.png"}]'
```

### 回复 & 转发

```bash
# 回复邮件（保存为草稿）
lark-cli mail +reply --message-id "msg_xxx" --body "收到，我会在周五前完成"

# 直接回复
lark-cli mail +reply --message-id "msg_xxx" --body "已完成" --confirm-send

# 回复全部
lark-cli mail +reply-all --message-id "msg_xxx" --body "已处理"

# 转发邮件
lark-cli mail +forward --message-id "msg_xxx" --to "bob@example.com" --body "转发给你看看"
```

### 邮件管理

```bash
# 查看邮件摘要
lark-cli mail +triage

# 搜索邮件
lark-cli mail +triage --query "预算报告"

# 按条件筛选
lark-cli mail +triage --filter '{"folder":"INBOX","from":["boss@example.com"]}'

# 查看筛选字段参考
lark-cli mail +triage --print-filter-schema

# 查看完整邮件
lark-cli mail +message --message-id "msg_xxx"

# 批量查看
lark-cli mail +messages --message-ids "msg_a,msg_b"

# 查看邮件线程
lark-cli mail +thread --thread-id "thread_xxx"

# 编辑草稿
lark-cli mail +draft-edit --message-id "msg_xxx" --body "修改后的内容"
```

### 邮件监控

```bash
# 实时监控新邮件（WebSocket）
lark-cli mail +watch

# 查看输出字段参考
lark-cli mail +watch --print-output-schema
```

---

## 视频会议 (vc)

### 会议纪要

```bash
# 通过会议 ID 查询纪要
lark-cli vc +notes --meeting-ids "meeting_xxx"

# 通过日历事件 ID 查询纪要
lark-cli vc +notes --calendar-event-ids "evt_xxx"

# 批量查询
lark-cli vc +notes --minute-tokens "mt_a,mt_b"

# 下载纪要附件到指定目录
lark-cli vc +notes --meeting-ids "meeting_xxx" --output-dir ./meeting-notes
```

### 搜索会议记录

```bash
# 搜索会议
lark-cli vc +search --query "项目评审"

# 按时间范围搜索
lark-cli vc +search --start "2026-03-01" --end "2026-03-31"

# 按组织者筛选
lark-cli vc +search --organizer-ids "ou_xxx"

# 按参与者筛选
lark-cli vc +search --participant-ids "ou_xxx,ou_yyy"
```

---

## 会议纪要 (minutes)

```bash
# 底层操作
lark-cli minutes minutes list
lark-cli minutes minutes get --minute-id "mt_xxx"
```

---

## 事件订阅 (event)

```bash
# 订阅所有事件（NDJSON 输出）
lark-cli event +subscribe

# 订阅指定事件类型
lark-cli event +subscribe --event-types "im.message.receive_v1,calendar.event.changed_v1"

# 正则过滤事件
lark-cli event +subscribe --filter "^im\\."

# 美化 JSON 输出
lark-cli event +subscribe --json

# 简洁输出
lark-cli event +subscribe --compact

# 按事件路由写入不同目录
lark-cli event +subscribe \
  --route '^im\.message=dir:./im/' \
  --route '^contact\.=dir:./contacts/'

# 静默模式
lark-cli event +subscribe --quiet

# 写入文件目录
lark-cli event +subscribe --output-dir ./events
```

---

## API 请求 (api)

直接调用飞书 Open API，适用于 lark-cli 尚未封装的接口。

```bash
# GET 请求
lark-cli api GET /open-apis/calendar/v4/calendars

# 带查询参数
lark-cli api GET /open-apis/calendar/v4/calendars --params '{"calendar_id":"primary"}'

# POST 请求
lark-cli api POST /open-apis/calendar/v4/calendars \
  --data '{"name":"工作日历"}'

# PATCH 请求
lark-cli api PATCH /open-apis/calendar/v4/calendars/cal_xxx \
  --data '{"name":"新名称"}'

# 自动分页
lark-cli api GET /open-apis/calendar/v4/events --params '{"calendar_id":"primary"}' --page-all

# 指定身份
lark-cli api GET /open-apis/contact/v3/users/me --as user

# 表格输出
lark-cli api GET /open-apis/calendar/v4/events --params '{"calendar_id":"primary"}' --format table

# 下载二进制响应
lark-cli api GET /open-apis/drive/v1/export_tasks/task_xxx/download -o ./output.pdf

# Dry run（仅打印请求）
lark-cli api POST /open-apis/im/v1/messages --data '{"receive_id":"oc_xxx"}' --dry-run
```

---

## Schema 查询 (schema)

查看 API 方法参数、类型和所需 scope。

```bash
# 查看某个 API 的 schema
lark-cli schema calendar.v4.calendar_event.create

# 美化输出
lark-cli schema calendar.v4.calendar_event.create --format pretty
```

---

## AI Agent 技能集成

lark-cli 可与 Claude Code 等 AI Agent 配合使用，通过技能包教会 Agent 飞书 API 的使用模式。

```bash
# 安装所有技能
npx skills add larksuite/cli --all -y

# 安装指定领域技能
npx skills add larksuite/cli -s lark-calendar -y
npx skills add larksuite/cli -s lark-im -y
npx skills add larksuite/cli -s lark-docs -y
npx skills add larksuite/cli -s lark-sheets -y
npx skills add larksuite/cli -s lark-base -y
npx skills add larksuite/cli -s lark-task -y
npx skills add larksuite/cli -s lark-mail -y
npx skills add larksuite/cli -s lark-contact -y
npx skills add larksuite/cli -s lark-drive -y
npx skills add larksuite/cli -s lark-wiki -y
```

更多详情：https://github.com/larksuite/cli#install-ai-agent-skills
