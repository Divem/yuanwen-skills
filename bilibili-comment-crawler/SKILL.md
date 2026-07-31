---
name: bilibili-comment-crawler
author: wen.yuan
description: |
  从B站视频采集评论数据，支持分页获取、子回复展开、写入飞书表格。
  当用户提到"采集B站评论"、"获取B站评论"、"爬取bilibili评论"、"B站评论导出"、
  "bilibili comments"时触发。支持传入BV号或完整URL，需要B站登录cookie。
---
# Bilibili Comment Crawler

从B站视频采集评论，支持分页、子回复、写入飞书表格。

## 前置条件

- **Cookie**: 需要 B站登录 cookie（未登录只能获取3条评论）
- **lark-cli**: 写入飞书表格时需要（`lark-cli auth status` 确认可用）
- **Python 3**: 运行采集脚本
- **curl**: API 请求依赖

## Cookie 配置

脚本按以下优先级读取 cookie：`--cookie 参数` > `BILIBILI_COOKIE 环境变量` > `cookie.json 配置文件`

### 配置文件（推荐）

编辑 `~/.claude/skills/bilibili-comment-crawler/cookie.json`：

```json
{
  "SESSDATA": "xxx",
  "bili_jct": "xxx",
  "DedeUserID": "xxx",
  "DedeUserID__ckMd5": "xxx"
}
```

> 注意：`cookie.json` 包含敏感信息，共享 skill 时应排除此文件。

### Cookie 获取方式

1. Chrome 打开 bilibili.com 并登录
2. F12 → Application → Cookies → `www.bilibili.com`
3. 复制这4项: `SESSDATA`, `bili_jct`, `DedeUserID`, `DedeUserID__ckMd5`
4. 拼接格式: `SESSDATA=xxx; bili_jct=xxx; DedeUserID=xxx; DedeUserID__ckMd5=xxx`

也可设置环境变量 `BILIBILI_COOKIE` 避免每次传入。

## 采集流程

### Step 1: 运行采集脚本

```bash
python3 scripts/bilibili_comments.py <BV_ID或URL> \
  --cookie "SESSDATA=xxx; bili_jct=xxx; DedeUserID=xxx; DedeUserID__ckMd5=xxx" \
  --limit 100 \
  --output /tmp/bilibili_comments.json
```

参数说明:
- `--cookie`: B站 cookie 字符串（也可用 `BILIBILI_COOKIE` 环境变量）
- `--limit`: 最大评论数（默认100）
- `--sort`: 排序方式，`2`=按时间（默认），`1`=按热度
- `--no-sub`: 不包含子回复（默认包含）
- `--rows`: 输出为二维数组格式（用于 lark-cli 写入）
- `--output`: 输出文件路径（默认 stdout）

脚本会自动:
1. 通过 BV 号解析出 aid
2. 分页请求评论 API（每页20条，自动翻页）
3. 展开一级评论的子回复
4. 清理 HTML 标签和换行符

### Step 2: 写入飞书表格

采集后用 lark-cli 创建表格并写入:

```bash
# 创建表格（首次）
lark-cli sheets +create \
  --title "B站视频评论 - <BV_ID>" \
  --headers '["序号","用户名","等级","评论内容","点赞数","发布时间","回复数","是否一级评论"]' \
  --values "$(python3 scripts/bilibili_comments.py <BV_ID> --cookie '...' --limit 100 --rows)"
```

追加到已有表格（记住 spreadsheet_token 和 sheet_id）:

```bash
# 获取已有表格信息
lark-cli sheets +info --url "https://...feishu.cn/sheets/<TOKEN>"

# 追加数据（每批最多50行）
python3 scripts/bilibili_comments.py <BV_ID> --cookie '...' --limit 100 --rows --output /tmp/rows.json

# 然后用 lark-cli sheets +append 逐批写入
# range 格式: <sheetId>!A<startRow>:H<endRow>
# values: 2D JSON array
```

**lark-cli +append 注意事项:**
- `--range` 必须指定完整的列范围（如 `A2:H51`），列数要和数据列数匹配
- 建议每批 50 行，避免 API 超时
- sheet_id 和 spreadsheet_token 通过 `+info` 获取

## 一步到位示例

完整采集+写入飞书的命令序列:

```bash
# 1. 采集评论（输出为行数组）
python3 scripts/bilibili_comments.py BV1ooDyBmE6v \
  --cookie "$BILIBILI_COOKIE" --limit 100 --rows \
  --output /tmp/bili_rows.json

# 2. 创建飞书表格并写入
ROWS=$(cat /tmp/bili_rows.json)
lark-cli sheets +create \
  --title "B站视频评论 - BV1ooDyBmE6v" \
  --headers '["序号","用户名","等级","评论内容","点赞数","发布时间","回复数","是否一级评论"]' \
  --values "$ROWS"
```

## API 限制

- 未登录: 仅返回3条评论
- 已登录: 可获取全部评论（分页，每页20条）
- 子回复: 每条一级评论默认返回3条子回复
- 请求间隔: 脚本内置 0.5s 延迟防限流
