# Douyin Search

使用 Playwright 搜索抖音视频并提取元数据，支持一键导出到飞书表格。

## 功能

- 按关键词搜索抖音视频
- 自动滚动加载，提取视频元数据（标题、作者、点赞数、时长、发布时间、链接）
- 去重处理，每 2-3.5 秒随机延迟防限流
- 可选择性写入飞书表格

## 前置要求

- **Node.js**
- **Playwright** (`npm install playwright`)
- **lark-cli** (`npm install -g @larksuite/cli`，上传飞书时需要)
- **抖音登录 Cookie**

### Cookie 获取

1. Chrome 打开 douyin.com 并登录
2. F12 → Application → Cookies → `.douyin.com`
3. 创建 `douyin_cookies.json` 文件：

```json
[
  { "name": "sessionid", "value": "xxx", "domain": ".douyin.com", "path": "/" },
  { "name": "sessionid_ss", "value": "xxx", "domain": ".douyin.com", "path": "/" },
  { "name": "ttwid", "value": "xxx", "domain": ".douyin.com", "path": "/" }
]
```

必需：`sessionid`, `sessionid_ss`。可选：`ttwid`, `passport_csrf_token`, `sid_guard`。

## 使用方法

### 基本搜索

```bash
node scripts/douyin_search.js openclaw
```

### 参数说明

| 参数 | 必需 | 说明 |
|------|------|------|
| `keyword` | 是 | 搜索关键词 |
| `--target N` | 否 | 最大采集视频数（默认50） |
| `--output PATH` | 否 | JSON 输出路径（默认 `douyin_search_<keyword>.json`） |
| `--cookies PATH` | 否 | Cookie 文件路径（默认查找 `douyin_cookies.json`） |
| `--feishu` | 否 | 同时写入飞书表格 |
| `--headless` | 否 | 使用无头模式（默认有头，便于调试） |

### 完整示例

```bash
# 搜索并导出到飞书
node scripts/douyin_search.js "AI编程" --target 30 --feishu

# 指定 Cookie 文件和输出路径
node scripts/douyin_search.js 短剧 --cookies ./my_cookies.json --output short_videos.json --headless
```

### 作为 Claude Skill 使用

安装 Skill 后，直接对 Claude 说：

```
"搜索抖音关于 openclaw 的视频"
"抓取抖音上 AI编程 相关的视频"
"抖音搜索 短剧 并导出到飞书"
```

## 输出格式

### JSON 文件

```json
[
  {
    "title": "视频标题",
    "author": "作者昵称",
    "likes": "3.8万",
    "duration": "07:40",
    "time": "2周前",
    "videoId": "7482xxxxxxxx",
    "url": "https://www.douyin.com/video/7482xxxxxxxx"
  }
]
```

字段说明：
- `title` — 视频标题/描述
- `author` — 创作者昵称
- `likes` — 点赞数（原始字符串，如 "3.8万", "183"）
- `duration` — 视频时长（如 "07:40"）
- `time` — 相对发布时间（如 "2周前", "12小时前"）
- `videoId` — 抖音视频 ID
- `url` — 完整视频链接

### 飞书表格

列名：视频标题 | 作者 | 点赞数 | 时长 | 发布时间 | 链接  
标题格式：`抖音搜索 - <keyword> (YYYY/M/D)`

## 工作原理

1. 使用 Playwright 有头模式打开抖音搜索页
2. 注入登录 Cookie 获取完整搜索结果
3. 自动滚动页面加载更多视频（每滚动 1000px，延迟 2-3.5 秒）
4. 提取视频卡片数据，去重处理
5. 达到目标数量或连续 5 轮无新数据则停止
6. 保存 JSON，可选写入飞书表格

## 注意事项

- **DOM 选择器**：使用 `.VDYK8Xd7`, `.z2lFLtJ0`, `.ckopQfVu`, `.dW_QmDH1` 等混淆类名，抖音更新可能导致选择器失效。如返回空结果，需检查页面结构并更新脚本中的选择器。
- **有头模式**：默认有头模式便于调试和观察，生产环境可加 `--headless` 使用无头模式。
- **Cookie 有效期**：Cookie 会过期，需定期重新获取。
- **防限流**：内置 2-3.5 秒随机延迟，避免触发反爬机制。

## 文件结构

```
douyin-search/
├── SKILL.md                  # Claude Skill 定义
├── README.md                 # 本文件
└── scripts/
    └── douyin_search.js      # 搜索脚本
```

---

**所属**: [yuanwen-skills](../README.md)
