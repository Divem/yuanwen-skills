# 抖音搜索抓取器

按关键词搜索抖音视频，提取视频元数据（标题、作者、点赞数、时长、发布时间、链接），可选写入飞书表格。

## 功能特性

- 按关键词搜索抖音视频
- 提取标题、作者、点赞数、时长、发布时间、链接
- 支持导出为 JSON 或飞书表格
- 有头/无头浏览器模式可选

## 前置条件

- Node.js
- Playwright（`npm i playwright`）
- 有效的抖音 cookie（需定期刷新）
- lark-cli（导出飞书时需要）

## Cookie 配置

创建 `cookies.json`：

```json
[
  { "name": "sessionid", "value": "<your_value>", "domain": ".douyin.com", "path": "/" },
  { "name": "sessionid_ss", "value": "<your_value>", "domain": ".douyin.com", "path": "/" },
  { "name": "ttwid", "value": "<your_value>", "domain": ".douyin.com", "path": "/" }
]
```

最低需要：`sessionid`、`sessionid_ss`

## 使用方法

```bash
node scripts/douyin_search.js <关键词> [选项]
```

选项：

| 选项 | 说明 |
|------|------|
| `--target N` | 最大采集视频数（默认 50） |
| `--output PATH` | JSON 输出文件路径 |
| `--feishu` | 同时写入飞书表格 |
| `--cookies PATH` | Cookie 文件路径 |
| `--headless` | 无头模式（默认有头） |

示例：

```bash
node scripts/douyin_search.js openclaw --feishu
node scripts/douyin_search.js "AI编程" --target 30 --output ai_videos.json
node scripts/douyin_search.js 短剧 --headless --feishu
```

## 输出格式

### JSON 字段

- `title` — 视频标题
- `author` — 作者昵称
- `likes` — 点赞数（如 "3.8万"、"183"）
- `duration` — 视频时长（如 "07:40"）
- `time` — 相对发布时间（如 "2周前"）
- `videoId` — 抖音视频 ID
- `url` — 完整视频链接

### 飞书表格

列：视频标题 | 作者 | 点赞数 | 时长 | 发布时间 | 链接

## 注意事项

- 抖音 DOM 选择器使用混淆类名，可能随更新变化
- 脚本内置 2-3.5s 随机延迟防限流
- 默认使用有头模式方便调试

---

[English Version](README.en.md)
