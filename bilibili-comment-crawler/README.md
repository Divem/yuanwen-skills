# Bilibili 评论采集器

从 B 站视频采集评论数据，支持分页获取、子回复展开、写入飞书表格。

## 功能特性

- 分页采集：自动翻页获取全部评论（每页 20 条）
- 子回复展开：自动提取一级评论下的子回复
- 飞书导出：支持将结果写入飞书表格
- 数据清洗：自动清理 HTML 标签和换行符

## 前置条件

- Python 3
- curl（API 请求依赖）
- B 站登录 cookie（未登录只能获取 3 条评论）
- lark-cli（写入飞书表格时需要）

## Cookie 配置

### 获取方式

1. Chrome 打开 bilibili.com 并登录
2. F12 → Application → Cookies → `www.bilibili.com`
3. 复制这 4 项：`SESSDATA`、`bili_jct`、`DedeUserID`、`DedeUserID__ckMd5`

### 配置方法（三选一）

**方式 1：配置文件（推荐）**

编辑 `~/.claude/skills/bilibili-comment-crawler/cookie.json`：

```json
{
  "SESSDATA": "xxx",
  "bili_jct": "xxx",
  "DedeUserID": "xxx",
  "DedeUserID__ckMd5": "xxx"
}
```

**方式 2：环境变量**

```bash
export BILIBILI_COOKIE="SESSDATA=xxx; bili_jct=xxx; DedeUserID=xxx; DedeUserID__ckMd5=xxx"
```

**方式 3：命令行参数**

```bash
--cookie "SESSDATA=xxx; ..."
```

## 使用方法

### 采集评论

```bash
python3 scripts/bilibili_comments.py <BV号或URL> [选项]
```

常用选项：

| 选项 | 说明 |
|------|------|
| `--cookie` | Cookie 字符串 |
| `--limit` | 最大评论数（默认 100） |
| `--sort` | 排序方式，`2`=按时间（默认），`1`=按热度 |
| `--no-sub` | 不包含子回复（默认包含） |
| `--rows` | 输出为二维数组格式（用于飞书写入） |
| `--output` | 输出文件路径（默认 stdout） |

示例：

```bash
python3 scripts/bilibili_comments.py BV1ooDyBmE6v \
  --cookie "$BILIBILI_COOKIE" \
  --limit 100 \
  --output /tmp/bili_comments.json
```

### 写入飞书表格

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

## 注意事项

- 未登录仅返回 3 条评论
- 子回复默认返回 3 条
- 脚本内置 0.5s 延迟防限流
- `cookie.json` 包含敏感信息，共享 skill 时应排除此文件
