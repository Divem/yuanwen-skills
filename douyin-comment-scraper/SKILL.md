---
name: douyin-comment-scraper
author: wen.yuan
description: >
  抓取抖音视频评论并通过 lark-cli 写入飞书表格。当用户提供抖音视频链接并要求抓取/导出评论、
  获取视频评论区内容、或提到"抖音评论"、"douyin comments"时触发。
  支持有头 Playwright 浏览器模式，需要用户提供登录 cookie。
---
# 抖音视频评论抓取

## 前置条件

- Node.js + Playwright (`npm install playwright`)
- lark-cli 全局安装 (`npm install -g @larksuite/cli`)
- 用户提供的抖音登录 cookie

## 工作流

### 1. 获取 Cookie

向用户请求以下 cookie（任选可获取的）：

| Cookie | 必要性 |
|--------|--------|
| `sessionid` | 推荐 |
| `sessionid_ss` | 推荐 |
| `passport_csrf_token` | 推荐 |
| `sid_guard` | 可选 |
| `uid_tt` | 推荐 |
| `odin_tt` | 推荐 |
| `ttwid` | 必要（可能多个） |

获取方式：浏览器登录抖音 → F12 → Application → Cookies → `douyin.com`

### 2. 从视频链接提取 videoId

从 URL 中匹配 `modal_id=<id>` 或 `/video/<id>` 提取数字 ID。

### 3. 运行抓取脚本

```bash
node <skill-path>/scripts/scrape_comments.js \
  --url "https://www.douyin.com/video/<ID>" \
  --cookies '[{"name":"sessionid","value":"xxx","domain":".douyin.com","path":"/"}, ...]' \
  --count 100 \
  --output douyin_comments.json
```

`--cookies` 也支持 `@path` 从文件读取：`--cookies @cookies.json`

脚本流程：
1. 用 Playwright 有头模式打开 `douyin.com/jingxuan?modal_id=<ID>`
2. 等待页面加载，移除遮挡弹窗（新手引导、登录验证）
3. 点击评论图标，等待评论列表渲染
4. 自动滚动评论区提取评论（昵称、内容、点赞、时间地区）
5. 去重，每 20 条自动保存 JSON，达到目标数量后退出

### 4. 上传飞书表格

```bash
node <skill-path>/scripts/upload_to_feishu.js \
  --input douyin_comments.json \
  --title "抖音视频评论-20260412"
```

自动创建飞书表格并分批写入数据。输出飞书表格 URL。

## DOM 选择器参考

抖音精选页评论区关键选择器：

| 数据 | 选择器 |
|------|--------|
| 评论列表容器 | `[data-e2e="comment-list"]` |
| 单条评论 | `[data-e2e="comment-item"]` |
| 昵称 | `.BT7MlqJC a` |
| 评论内容 | `.C7LroK_h` |
| 时间·地区 | `.fJhvAqos span` |
| 点赞数 | `.vXZJEXVc p` |
| 评论图标（点击打开） | `[data-e2e="feed-comment-icon"]` |

## 常见问题

- **验证码/安全验证**：抖音会弹出 `uc-second-verify` 验证框。脚本会自动移除，但如果反复触发需要用户手动处理或更换 cookie。
- **评论数量不足**：抖音评论懒加载，每次滚动加载约 10-20 条。脚本自动处理，连续 5 轮无新评论则停止。
- **选择器失效**：抖音前端经常更新。如果提取不到数据，用 Playwright debug 模式截图并检查 DOM 更新选择器。
