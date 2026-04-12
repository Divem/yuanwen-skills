# Bilibili Comment Crawler

从B站视频采集评论数据，支持分页获取、子回复展开、写入飞书表格。

## 功能

- 采集B站视频全部评论（支持BV号或完整URL）
- 自动分页、展开子回复
- 清理HTML标签，输出干净的文本
- 支持按时间/热度排序
- 输出JSON或二维数组（可直接写入飞书表格）

## 前置要求

- **Python 3**
- **curl**（API请求依赖）
- **B站登录Cookie**（未登录仅返回3条评论）
- **lark-cli**（可选，写入飞书表格时需要）

### Cookie 获取

1. Chrome 打开 bilibili.com 并登录
2. F12 → Application → Cookies → `www.bilibili.com`
3. 复制4项: `SESSDATA`, `bili_jct`, `DedeUserID`, `DedeUserID__ckMd5`
4. 拼接: `SESSDATA=xxx; bili_jct=xxx; DedeUserID=xxx; DedeUserID__ckMd5=xxx`

也可设置环境变量 `BILIBILI_COOKIE` 避免每次传入。

## 使用方法

### 基本采集

```bash
python3 scripts/bilibili_comments.py BV1ooDyBmE6v \
  --cookie "$BILIBILI_COOKIE" \
  --limit 100 \
  --output /tmp/comments.json
```

### 参数说明

| 参数 | 必需 | 说明 |
|------|------|------|
| `bv_id` | 是 | BV号或完整URL |
| `--cookie` | 是 | Cookie字符串（或设置 `BILIBILI_COOKIE` 环境变量） |
| `--limit` | 否 | 最大评论数（默认100） |
| `--sort` | 否 | `2`=按时间（默认），`1`=按热度 |
| `--no-sub` | 否 | 不包含子回复 |
| `--rows` | 否 | 输出二维数组格式（用于lark-cli写入） |
| `--output` | 否 | 输出文件路径（默认stdout） |

### 采集 + 写入飞书表格

```bash
# 1. 采集评论
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

### 作为 Claude Skill 使用

安装 Skill 后，直接对 Claude 说：

```
"采集B站评论 BV1ooDyBmE6v"
"获取这个B站视频的评论 https://www.bilibili.com/video/BV1ooDyBmE6v"
"爬取bilibili评论并写入飞书表格"
```

## 输出格式

### JSON 模式（默认）

```json
[
  {
    "rpid": "1234567890",
    "uname": "用户名",
    "level": 6,
    "message": "评论内容",
    "like": 42,
    "ctime": "2025/04/12 10:30:00",
    "rcount": 3,
    "is_root": true
  }
]
```

### 二维数组模式（`--rows`）

```json
[
  ["1", "用户名", "6", "评论内容", "42", "2025/04/12 10:30:00", "3", "yes"]
]
```

## API 限制

- 未登录: 仅返回3条评论
- 已登录: 可获取全部评论（每页20条，自动翻页）
- 子回复: 每条一级评论默认返回3条子回复
- 内置 0.5s 请求间隔防限流

## 文件结构

```
bilibili-comment-crawler/
├── SKILL.md                      # Claude Skill 定义
├── README.md                     # 本文件
└── scripts/
    └── bilibili_comments.py      # 采集脚本
```

---

**所属**: [yuanwen-skills](../README.md)
