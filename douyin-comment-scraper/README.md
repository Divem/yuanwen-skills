# Douyin Comment Scraper

抓取抖音视频评论并通过 lark-cli 写入飞书表格。基于 Playwright 有头浏览器模式，模拟真实用户操作采集评论数据。

## 功能

- 从抖音视频链接提取评论（昵称、内容、点赞数、时间地区）
- 自动滚动加载、去重
- 自动移除遮挡弹窗（新手引导、登录验证）
- 每 20 条自动保存，防止数据丢失
- 一键上传飞书表格

## 前置要求

- **Node.js**
- **Playwright** (`npm install playwright`)
- **lark-cli** (`npm install -g @larksuite/cli`，上传飞书时需要)
- **抖音登录 Cookie**

### Cookie 获取

1. Chrome 打开 douyin.com 并登录
2. F12 → Application → Cookies → `.douyin.com`
3. 需要的 Cookie 项：

| Cookie | 必要性 |
|--------|--------|
| `ttwid` | 必要 |
| `sessionid` | 推荐 |
| `sessionid_ss` | 推荐 |
| `passport_csrf_token` | 推荐 |
| `uid_tt` | 推荐 |
| `odin_tt` | 推荐 |
| `sid_guard` | 可选 |

## 使用方法

### 1. 抓取评论

```bash
node scripts/scrape_comments.js \
  --url "https://www.douyin.com/video/7492xxxxxxxx" \
  --cookies @cookies.json \
  --count 100 \
  --output douyin_comments.json
```

#### 参数说明

| 参数 | 必需 | 说明 |
|------|------|------|
| `--url, -u` | 是 | 抖音视频链接（支持 `/video/<id>` 或 `modal_id=<id>` 格式） |
| `--cookies, -c` | 否 | Cookie JSON 数组字符串，或 `@path` 从文件读取 |
| `--count` | 否 | 抓取评论数量（默认100） |
| `--output, -o` | 否 | 输出文件路径（默认 `douyin_comments.json`） |

#### Cookie JSON 格式

```json
[
  {"name": "sessionid", "value": "xxx", "domain": ".douyin.com", "path": "/"},
  {"name": "ttwid", "value": "xxx", "domain": ".douyin.com", "path": "/"}
]
```

### 2. 上传飞书表格

```bash
node scripts/upload_to_feishu.js \
  --input douyin_comments.json \
  --title "抖音视频评论-20260412"
```

#### 参数说明

| 参数 | 必需 | 说明 |
|------|------|------|
| `--input, -i` | 是 | 评论 JSON 文件路径 |
| `--title` | 否 | 飞书表格标题（默认 `抖音视频评论-日期`） |
| `--folder-token` | 否 | 飞书云盘文件夹 token |

### 作为 Claude Skill 使用

安装 Skill 后，直接对 Claude 说：

```
"抓取这个抖音视频的评论 https://www.douyin.com/video/7492xxx"
"导出抖音评论到飞书表格"
"获取这个视频的评论区内容"
```

## 输出格式

```json
[
  {
    "nickname": "用户昵称",
    "content": "评论内容（最多500字）",
    "likes": "42",
    "time": "3天前 · 北京"
  }
]
```

## 工作原理

1. 用 Playwright 有头模式打开抖音精选页
2. 注入用户 Cookie 模拟登录状态
3. 移除遮挡弹窗（新手引导、安全验证等）
4. 点击评论图标，等待评论列表渲染
5. 自动滚动评论区，提取每条评论数据
6. 去重、每 20 条自动保存 JSON
7. 达到目标数量或连续 5 轮无新评论后停止

## 常见问题

### 验证码/安全验证

抖音会弹出 `uc-second-verify` 验证框，脚本会自动移除。如果反复触发，需要手动处理或更换 Cookie。

### 评论数量不足

抖音评论懒加载，每次滚动加载约 10-20 条。脚本自动处理翻页，连续 5 轮无新评论则停止。

### 选择器失效

抖音前端经常更新，如果提取不到数据，需要用 Playwright debug 模式截图并检查 DOM 更新选择器。

### DOM 选择器参考

| 数据 | 选择器 |
|------|--------|
| 评论列表容器 | `[data-e2e="comment-list"]` |
| 单条评论 | `[data-e2e="comment-item"]` |
| 昵称 | `.BT7MlqJC a` |
| 评论内容 | `.C7LroK_h` |
| 时间·地区 | `.fJhvAqos span` |
| 点赞数 | `.vXZJEXVc p` |
| 评论图标 | `[data-e2e="feed-comment-icon"]` |

## 文件结构

```
douyin-comment-scraper/
├── SKILL.md                          # Claude Skill 定义
├── README.md                         # 本文件
├── scripts/
│   ├── scrape_comments.js            # 评论抓取脚本
│   └── upload_to_feishu.js           # 飞书表格上传脚本
└── douyin-comment-scraper.skill      # Skill 打包文件
```

---

**所属**: [yuanwen-skills](../README.md)
