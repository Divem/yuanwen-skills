# 抖音评论抓取器

抓取抖音视频评论并通过 lark-cli 写入飞书表格。

## 功能特性

- Playwright 有头浏览器模式，模拟真实用户行为
- 自动展开评论区、滚动加载、去重
- 提取评论昵称、内容、点赞数、时间地区
- 自动写入飞书表格

## 前置条件

- Node.js
- Playwright（`npm install playwright`）
- lark-cli（`npm install -g @larksuite/cli`）
- 抖音登录 cookie

## Cookie 配置

浏览器登录抖音 → F12 → Application → Cookies → `douyin.com`，获取以下 cookie：

| Cookie | 必要性 |
|--------|--------|
| `sessionid` | 推荐 |
| `sessionid_ss` | 推荐 |
| `passport_csrf_token` | 推荐 |
| `uid_tt` | 推荐 |
| `odin_tt` | 推荐 |
| `ttwid` | 必要 |

## 使用方法

### 抓取评论

```bash
node scripts/scrape_comments.js \
  --url "https://www.douyin.com/video/<ID>" \
  --cookies @cookies.json \
  --count 100 \
  --output douyin_comments.json
```

`--cookies` 支持两种格式：
- JSON 数组字符串：`--cookies '[{"name":"sessionid",...}]'`
- 文件路径：`--cookies @cookies.json`

### 上传飞书表格

```bash
node scripts/upload_to_feishu.js \
  --input douyin_comments.json \
  --title "抖音视频评论-20260412"
```

## 注意事项

- 抖音会弹出安全验证，脚本会自动移除，反复触发需手动处理
- 评论懒加载，每次滚动约加载 10-20 条
- 连续 5 轮无新评论则自动停止
- 抖音前端经常更新，如提取失败需检查 DOM 选择器

---

[English Version](README.en.md)
