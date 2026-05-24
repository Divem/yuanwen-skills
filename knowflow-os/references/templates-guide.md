# KnowFlow OS Templates Guide

## Template Files

All templates are in `assets/templates/` and should be copied to `templates/` during project initialization.

### topic-card.md

**Use when**: Generating new topics from knowledge assets.

**Key fields**:
- 选题编号 (Topic ID): TK-XXX
- 选题标题 (Topic title)
- 关联知识资产 (Linked knowledge assets)
- 业务场景 (Business scenarios)
- 目标受众 (Target audience)
- 受众痛点 (Audience pain points)
- 核心观点 (Core thesis)
- 推荐渠道 (Recommended channels)
- 内容角度 (Content angles, 3-5 variations)
- 状态 (Status): pending / approved / in-progress / published / archived

### xiaohongshu.md

**Use when**: Writing Xiaohongshu (Little Red Book) content.

**Key fields**:
- 标题（多选）(Titles, 3-5 options, max 20 chars)
- 封面文案 (Cover text)
- 配图建议 (Image suggestions, 3-9 images)
- 正文 (Body, 500-1000 words, short paragraphs, emoji-rich)
- 话题标签 (Hashtags, 3-8)
- 发布建议 (Publish timing and notes)
- 审核注意事项 (Review checklist)

**Style guidelines**:
- Casual, conversational tone
- Short paragraphs (2-3 lines max)
- Heavy use of emoji and symbols
- Storytelling format preferred
- Clear value proposition in first 2 lines

### wechat-article.md

**Use when**: Writing WeChat public account articles.

**Key fields**:
- 标题（多选）(Titles, 3-5 options, 20-30 chars recommended)
- 摘要 (Summary, 100-200 chars)
- 封面图建议 (Cover image suggestion)
- 正文 (Body, 1000-3000 words)
- 小标题结构 (Subheadings)
- 结尾引导 (Closing CTA)
- 发布建议 (Publish notes)
- 审核注意事项 (Review checklist)

**Style guidelines**:
- Structured, logical flow
- Subheadings every 300-500 words
- Paragraphs under 5 lines on mobile
- Data and citations to support claims
- Natural CTA at the end

### video-script.md

**Use when**: Writing video scripts (short video / live stream).

**Key fields**:
- 视频标题 (Video title)
- 视频时长 (Duration)
- 目标平台 (Target platform)
- 开头钩子 (Opening hook, 0-5 seconds)
- 内容主体 (Body, scene by scene)
- 结尾引导 (Closing CTA, 5-10 seconds)
- 画面建议 (Visual suggestions)
- BGM 建议 (BGM suggestions)
- 字幕要点 (Subtitle highlights)
- 审核注意事项 (Review checklist)

**Style guidelines**:
- Conversational, spoken language
- Speaking rate: 200-250 words/minute
- Hook must grab attention immediately
- One key point per scene
- Clear, actionable CTA

### ppt-outline.md

**Use when**: Creating presentation outlines.

**Key fields**:
- 主题 (Theme)
- 页数 (Page count)
- 目标受众 (Target audience)
- 页面结构 (Page structure, with titles and logic)
- 视觉风格建议 (Visual style)
- 配色建议 (Color scheme)

**Style guidelines**:
- One core point per slide
- Minimal text, maximum visuals
- Include slide logic and diagram suggestions
- Closing slide with action items

### publish-record.md

**Use when**: Recording published content performance.

**Key fields**:
- 内容标题 (Content title)
- 发布渠道 (Channel)
- 发布时间 (Publish time)
- 发布链接 (Link)
- 使用版本 (Content version used)
- 标题/封面 (Title and cover used)
- 各项数据 (Reads, likes, saves, comments, conversions)
- 用户反馈 (User feedback)
- 复盘结论 (Review conclusions)
- 可二次创作方向 (Repurpose directions)

### review-report.md

**Use when**: Conducting post-publish analytics review.

**Key fields**:
- 复盘对象 (Review subject)
- 时间范围 (Time range)
- 数据表现 (Performance metrics)
- 表现好的地方 (What worked well)
- 表现不好的地方 (What didn't work)
- 用户反馈 (User feedback summary)
- 选题/标题/内容结构/渠道判断 (Topic/title/structure/channel assessment)
- 后续优化建议 (Optimization recommendations)
- 可复用经验 (Reusable insights)
- 下一步行动 (Next actions)

## Customizing Templates

When adapting templates for a specific project:

1. Copy templates from `assets/templates/` to `templates/`
2. Modify based on brand voice and channel requirements
3. Add project-specific fields if needed
4. Update review rules in scenario.yml files

## Template Variables

Templates use `{{variable}}` notation for dynamic content:
- `{{topic_id}}` — Topic identifier
- `{{title}}` — Content title
- `{{channel}}` — Target channel
- `{{scenario}}` — Business scenario
- `{{asset_ids}}` — Linked knowledge asset IDs

Replace these with actual values during content generation.
