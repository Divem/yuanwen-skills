---
name: knowflow-os
description: |
  AI-powered knowledge management and content operation system for creators, brands, and content teams.
  Manages the full content lifecycle: information collection to knowledge archiving to topic generation to
  content production to multi-channel distribution to data review to IP asset accumulation.
  Use when: (1) initializing a content or knowledge management project, (2) organizing and classifying
  scattered information into reusable knowledge assets, (3) generating content topics from existing
  knowledge, (4) producing channel-specific content for Xiaohongshu, WeChat articles, video scripts,
  PPT, or Moments, (5) adapting the same content across multiple channels, (6) managing publishing
  workflows and post-publish analytics, (7) creating review reports and repurpose recommendations.
  Not a traditional CMS. It is an AI-native system where knowledge is grouped by assets, content is
  produced by scenarios, and delivery is managed by channel.
metadata:
  author: wen.yuan
---
# KnowFlow OS

## Overview

KnowFlow OS is an AI-native knowledge management and content operation system.

Core loop:
```
Information Collection -> Knowledge Archiving -> Topic Generation ->
Content Production -> Multi-Channel Distribution -> Data Review -> IP/Brand Asset Accumulation
```

Core principle:
```
Knowledge grouped by assets, content produced by scenarios, delivery managed by channel.
```

## Core Capabilities

1. **Project Initialization**: Create the complete KnowFlow OS directory structure with a single command
2. **Knowledge Import & Classification**: Ingest raw materials (text, images, files, links) and classify them into reusable knowledge assets
3. **Topic Generation**: Extract content topics from knowledge assets, scored by relevance and传播 potential
4. **Channel Content Production**: Generate platform-specific content (Xiaohongshu, WeChat, video scripts, PPT)
5. **Cross-Channel Adaptation**: Rewrite the same content for different channels while preserving core messaging
6. **Publishing & Review**: Manage publish workflows, records, and post-publish analytics

## Workflow Decision Tree

When the user provides new materials or asks for content creation, follow this decision tree:

```
User input
├── New material (text/image/file/link)
│   └── Run: import-and-classify workflow
│       -> Save to 00-inbox/
│       -> Extract content
│       -> Classify asset type
│       -> Generate metadata.yml
│       -> Move to 01-knowledge-base/
│
├── "Generate topics" / "Create topic cards"
│   └── Run: knowledge-to-topic workflow
│       -> Select knowledge assets
│       -> Generate topic angles
│       -> Score topics
│       -> Save topic cards to 03-topic-pool/
│
├── "Write content for [channel]" / "Create [platform] post"
│   └── Run: topic-to-content workflow
│       -> Read topic card
│       -> Load related knowledge assets
│       -> Select scenario and channel template
│       -> Generate content draft
│       -> Save to 04-content-factory/
│
├── "Prepare for publish" / "Review before publishing"
│   └── Run: content-to-publish workflow
│       -> Check completeness
│       -> Run review rules
│       -> Move to 05-publish-center/scheduled/
│
├── "Analyze performance" / "Review this content"
│   └── Run: publish-to-review workflow
│       -> Collect publish data
│       -> Analyze performance
│       -> Generate review report to 06-review/
│
└── "Init KnowFlow OS" / "Setup content system"
    └── Run: init-project workflow
        -> Create full directory structure
        -> Create config files (knowflow.yml, AGENTS.md)
        -> Create templates and workflows
```

## Quick Start: Project Initialization

When the user asks to initialize a KnowFlow OS project:

1. Create the directory structure:
   ```
   project-root/
   ├── 00-inbox/
   ├── 01-knowledge-base/
   │   ├── brand/, products/, courses/, people/, cases/
   │   ├── faq/, operations/, training/, research/, media-assets/
   ├── 02-scenarios/
   │   ├── student-content/, course-training/, external-pr/
   │   ├── sales-conversion/, community-operation/, teacher-branding/
   │   ├── recruitment/, internal-sop/, website-content/
   ├── 03-topic-pool/
   │   ├── pending/, approved/, in-progress/, published/, archived/
   ├── 04-content-factory/
   │   ├── drafts/, pending-review/, approved/, rejected/
   ├── 05-publish-center/
   │   ├── scheduled/, records/
   ├── 06-review/
   │   ├── content-reviews/, channel-reviews/, monthly-reports/
   ├── 07-ip-assets/
   │   ├── brand-identity/, signature-content/, content-series/, reusable-assets/
   ├── metadata/
   ├── templates/
   ├── workflows/
   └── skills/
   ```

2. Create `knowflow.yml` from [assets/templates/knowflow.yml](assets/templates/knowflow.yml)
3. Create `AGENTS.md` (see [references/agents-rules.md](references/agents-rules.md))
4. Copy templates from [assets/templates/](assets/templates/) to `templates/`
5. Create workflow configs in `workflows/` (see [references/workflows-detail.md](references/workflows-detail.md))
6. Create scenario configs in `02-scenarios/` (see [references/project-structure.md](references/project-structure.md))
7. Create README.md

## Detailed Workflows

For step-by-step workflow execution, see [references/workflows-detail.md](references/workflows-detail.md).

### Workflow 1: import-and-classify

Process: `scan_inbox -> detect_type -> extract_text -> summarize -> classify -> generate_metadata -> create_folder -> move -> update_index`

Key rules:
- Never delete or overwrite raw files
- All materials must go through 00-inbox/ first
- Generate metadata.yml for every asset
- Create raw.md, summary.md, notes.md for each asset

### Workflow 2: knowledge-to-topic

Process: `select_assets -> extract_points -> identify_audience -> identify_pain_points -> generate_angles -> score -> save_cards`

Key rules:
- Every topic must link to at least one knowledge asset
- Every topic must link to at least one scenario
- Topics should be specific and actionable

### Workflow 3: topic-to-content

Process: `read_topic -> load_assets -> select_scenario -> select_template -> generate_draft -> generate_titles -> generate_cover -> generate_suggestions -> save`

Key rules:
- Different channels require different content versions
- Content must cite which knowledge assets were used
- Include review notes and compliance checks

### Workflow 4: content-to-publish

Process: `check_completeness -> run_review -> create_version -> move_to_scheduled -> create_checklist`

### Workflow 5: publish-to-review

Process: `collect_data -> analyze -> summarize_feedback -> update_status -> recommend_repurpose -> save_report`

Key rules:
- Complete review within 7 days of publishing
- Review must include data and user feedback
- Conclusions must lead to actionable improvements

## Asset Categories

Knowledge assets are organized into 10 categories:

| Category | Description |
|----------|-------------|
| brand | Brand positioning, brand story, visual guidelines |
| products | Product introductions, feature descriptions, pricing |
| courses | Course systems, curricula, teaching methods |
| people | Team introductions, instructor profiles, stories |
| cases | Student/client case studies (anonymized by default) |
| faq | Frequently asked questions, standard answers |
| operations | Operational data, activity records |
| training | Training materials, SOPs, internal knowledge |
| research | Industry reports, competitive analysis, research |
| media-assets | Images, videos, design assets |

## Content Channels

Supported channels and their characteristics:

| Channel | Format | Style | Key Requirements |
|---------|--------|-------|------------------|
| xiaohongshu | 500-1000 words | Casual, emoji-rich | 3-9 images, 3-8 hashtags |
| wechat-article | 1000-3000 words | Structured, in-depth | Summary, cover image |
| moments | 100-300 words | Light, interactive | 1-9 images |
| video-script | Time-based | Conversational | Hook + story + CTA |
| ppt | Slide-based | Visual, point-based | One point per slide |
| brochure | Page-based | Professional | Brand consistent |
| website | SEO-friendly | Formal, concise | Keywords optimized |
| feishu-doc | Document-based | Collaborative | Structured |

## Templates

All content templates are in [assets/templates/](assets-templates):

- `topic-card.md` — Topic card template
- `xiaohongshu.md` — Xiaohongshu content template
- `wechat-article.md` — WeChat article template
- `video-script.md` — Video script template
- `ppt-outline.md` — PPT outline template
- `publish-record.md` — Publishing record template
- `review-report.md` — Review report template

## Examples

A complete yoga studio example is available at [assets/examples/yoga-studio/](assets-examples-yoga-studio) demonstrating how the same knowledge assets are reused across multiple scenarios.

## Core Rules (Summary)

For the complete agent rules, see [references/agents-rules.md](references/agents-rules.md).

Key principles:
1. Raw materials are never deleted or overwritten
2. All materials enter through 00-inbox/
3. Knowledge assets live in 01-knowledge-base/
4. Scenarios in 02-scenarios/, topics in 03-topic-pool/
5. Content drafts in 04-content-factory/, publish records in 05-publish-center/records/
6. Reviews in 06-review/, IP assets in 07-ip-assets/
7. Shared knowledge assets stored once, referenced by scenarios
8. Different channels get different content versions
9. User cases are anonymized by default
10. No exaggerated or unverifiable claims
11. Cite knowledge assets used in content generation
12. Uncertain classification goes to a "pending confirmation" folder

## Resources

### references/
- [references/agents-rules.md](references/agents-rules.md) — Complete agent rules and default processing flows
- [references/project-structure.md](references/project-structure.md) — Directory structure and file organization
- [references/workflows-detail.md](references/workflows-detail.md) — Step-by-step workflow execution guide
- [references/templates-guide.md](references/templates-guide.md) — Template usage and customization guide

### assets/
- [assets/templates/](assets/templates/) — Ready-to-use content templates and config files
- [assets/examples/yoga-studio/](assets/examples/yoga-studio/) — Complete example project
