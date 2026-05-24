# KnowFlow OS

AI-native knowledge management and content operations system for creators, brands, and content teams.

## Core Loop

```
Information Collection → Knowledge Archiving → Topic Generation → Content Production → Multi-channel Distribution → Data Review → IP/Brand Asset Accumulation
```

Core principle: Knowledge is categorized by asset; content is produced by scenario; distribution is managed by channel.

## Features

- **Project initialization**: One-click creation of complete KnowFlow OS directory structure
- **Knowledge import and classification**: Classify scattered materials into reusable knowledge assets
- **Topic generation**: Extract content topics from knowledge assets, assess relevance and virality potential
- **Channel content production**: Generate platform-specific content for XiaoHongShu, WeChat Official Account, video scripts, PPT, etc.
- **Cross-channel adaptation**: Rewrite the same content for different channel versions
- **Publishing and review**: Manage publishing workflow, record and analyze data

## Directory Structure

```
project-root/
├── 00-inbox/              # Inbox: entry point for all new materials
├── 01-knowledge-base/     # Knowledge base: categorized knowledge assets
│   ├── brand/             # Brand positioning
│   ├── products/          # Product introductions
│   ├── courses/           # Course system
│   ├── people/            # Team / people
│   ├── cases/             # Cases (default anonymous)
│   ├── faq/               # Frequently asked questions
│   ├── operations/        # Operations data
│   ├── training/          # Training materials
│   ├── research/          # Industry research
│   └── media-assets/      # Image and video assets
├── 02-scenarios/          # Scenarios: content production scenario configs
├── 03-topic-pool/         # Topic pool: pending/approved/in-progress/published/archived
├── 04-content-factory/    # Content factory: draft/reviewing/approved/rejected
├── 05-publish-center/     # Publish center: schedule/record
├── 06-review/             # Review: content review/channel review/monthly report
└── 07-ip-assets/          # IP assets: brand identity/signature content/content series
```

## Usage

Simply tell Claude:

```
"Initialize KnowFlow OS"
"Import these materials into knowledge base"
"Generate topics based on these knowledge assets"
"Write a XiaoHongShu post"
"Adapt this content for WeChat Official Account"
"Prepare for publishing"
"Review the data for this content"
```

## Supported Content Channels

| Channel | Format | Style |
|---------|--------|-------|
| XiaoHongShu | 500-1000 words | Casual, emoji-rich |
| WeChat Official Account | 1000-3000 words | Structured, in-depth |
| Moments | 100-300 words | Casual, interactive |
| Video script | Duration-driven | Conversational, with hooks |
| PPT | Slides | Visual, bullet-point style |

## Core Rules

1. Raw materials are never deleted or overwritten
2. All materials must go through the `00-inbox/` entry
3. Knowledge assets are stored in `01-knowledge-base/`, scenarios in `02-scenarios/`
4. The same knowledge asset can be reused by multiple scenarios
5. Different channels must generate different content versions
6. Cases are anonymized by default
7. Content generation must cite which knowledge assets are referenced

## Advanced Tips

### Feishu Sync + Comment Collaboration

Combine with [feishu-sync](../feishu-sync/) to sync the entire KnowFlow OS directory to Feishu:

1. **Sync to Feishu**: After `init`, push local edits to Feishu documents via `push`
2. **Read and edit in Feishu**: Use Feishu mobile app to read knowledge assets, annotate topic cards
3. **Comment-driven optimization**: Add comments in Feishu documents (e.g., "this paragraph is too verbose", "add some data"), AI reads comments and auto-optimizes content
4. **Pull updates**: After Feishu edits, sync back to local via `pull`

This enables an async collaboration flow of "view Feishu document → write comment → AI auto-edits content".

### GitHub Full-space Backup

The entire KnowFlow OS is a Git repository:

- Switch computers: `git clone` to restore the full workspace
- Knowledge assets, topic pools, content drafts are all version-controlled
- Can be paired with GitHub Actions for automatic backup or publishing

### Agent-agnostic, Flexible Switching

KnowFlow OS is a file-system-based content management harness, not tied to any specific AI:

- **Claude Code** → Deep editing, batch processing
- **Cursor / Copilot** → Code-like content generation
- **Claude.ai / ChatGPT** → Quick brainstorming, idea recording
- **Codex** → Generate images and auto-publish

Different agents use the same directory structure to collaborate without interference.

### Codex Image Generation + Auto-publish to XiaoHongShu

If using Codex, you can connect the "image generation → auto-publish" pipeline:

1. Generate XiaoHongShu copy in `04-content-factory/`
2. Use Codex to generate images (based on copy content or brand style)
3. Save images to `media-assets/`
4. Call feishu-send or directly connect to XiaoHongShu API for auto-publishing

Achieve a fully automated pipeline from "one-sentence topic → finished content".

---

[中文版](README.md)
