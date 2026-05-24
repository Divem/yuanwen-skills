# KnowFlow OS Project Structure

## Directory Overview

```
project-root/
├── 00-inbox/                    # Raw material entry point
├── 01-knowledge-base/           # Shared knowledge asset library
│   ├── brand/                   # Brand positioning, story, guidelines
│   ├── products/                # Product introductions, features, pricing
│   ├── courses/                 # Course systems, curricula, methods
│   ├── people/                  # Team profiles, instructor bios
│   ├── cases/                   # Case studies (anonymized)
│   ├── faq/                     # FAQs and standard answers
│   ├── operations/              # Operational data, activity records
│   ├── training/                # Training materials, SOPs
│   ├── research/                # Industry reports, competitive analysis
│   └── media-assets/            # Images, videos, design assets
├── 02-scenarios/                # Business scenario workspaces
│   ├── student-content/         # Student-facing content (social media)
│   ├── course-training/         # Course and training materials
│   ├── external-pr/             # External brand communication
│   ├── sales-conversion/        # Sales support content
│   ├── community-operation/     # Community management content
│   ├── teacher-branding/        # Teacher IP building
│   ├── recruitment/             # Recruitment content
│   ├── internal-sop/            # Internal SOPs
│   └── website-content/         # Website content
├── 03-topic-pool/               # Topic library
│   ├── pending/                 # Pending topics
│   ├── approved/                # Approved topics
│   ├── in-progress/             # In-progress topics
│   ├── published/               # Published topics
│   └── archived/                # Archived topics
├── 04-content-factory/          # Content production area
│   ├── drafts/                  # Content drafts
│   ├── pending-review/          # Pending review
│   ├── approved/                # Approved content
│   └── rejected/                # Rejected content
├── 05-publish-center/           # Publishing center
│   ├── scheduled/               # Scheduled content
│   └── records/                 # Publish records
├── 06-review/                   # Data review
│   ├── content-reviews/         # Content reviews
│   ├── channel-reviews/         # Channel reviews
│   └── monthly-reports/         # Monthly reports
├── 07-ip-assets/                # IP / Brand assets
│   ├── brand-identity/          # Brand identity
│   ├── signature-content/       # Signature/flagship content
│   ├── content-series/          # Content series assets
│   └── reusable-assets/         # Reusable assets
├── metadata/                    # Global indexes
│   ├── content-index.yml
│   ├── asset-index.yml
│   └── scenario-index.yml
├── templates/                   # Content templates
│   ├── topic-card.md
│   ├── xiaohongshu.md
│   ├── wechat-article.md
│   ├── video-script.md
│   ├── ppt-outline.md
│   ├── publish-record.md
│   └── review-report.md
├── workflows/                   # Workflow configs
│   ├── import-and-classify.yml
│   ├── knowledge-to-topic.yml
│   ├── topic-to-content.yml
│   ├── content-to-publish.yml
│   └── publish-to-review.yml
├── skills/                      # Agent skills
│   ├── import-content/
│   ├── classify-knowledge/
│   ├── summarize-content/
│   ├── generate-topic/
│   ├── xiaohongshu-writing/
│   ├── wechat-writing/
│   ├── video-script-writing/
│   ├── ppt-outline/
│   ├── channel-adaptation/
│   └── review-analysis/
├── knowflow.yml                 # Project configuration
├── AGENTS.md                    # Agent rules
└── README.md                    # Project overview
```

## Knowledge Asset Directory Structure

Each knowledge asset directory contains:

```
asset-name/
├── metadata.yml       # Metadata (source, type, tags, dates)
├── raw.md             # Original content or file reference
├── summary.md         # Summary and key points
├── notes.md           # Reusable knowledge notes
└── attachments/       # Attachments (images, PDFs, etc.)
```

## Scenario Directory Structure

Each scenario directory contains:

```
scenario-name/
├── scenario.yml        # Scenario definition (goals, audience, channels, strategy)
├── README.md           # Scenario description
├── topic-registry.yml  # Topic registry for this scenario
└── content-index.yml   # Content index for this scenario
```

## Content File Naming Convention

```
topic-id-channel-version.md
```

Example: `TK-001-xiaohongshu-v1.md`

## Index File Formats

### metadata/content-index.yml

```yaml
contents:
  - id: CT-001
    topic_id: TK-001
    title: Example Title
    channel: xiaohongshu
    status: draft
    path: 04-content-factory/drafts/TK-001-xiaohongshu-v1.md
    created_at: "2026-05-23"
    updated_at: "2026-05-23"
```

### metadata/asset-index.yml

```yaml
assets:
  - id: AS-001
    name: Brand Introduction
    category: brand
    type: brand-story
    path: 01-knowledge-base/brand/brand-intro/
    tags: [brand, intro, positioning]
    status: active
    created_at: "2026-05-23"
    updated_at: "2026-05-23"
    related_topics: [TK-001, TK-002]
```

### metadata/scenario-index.yml

```yaml
scenarios:
  - id: SC-001
    name: Student Content Operation
    slug: student-content
    description: Social media content for students
    path: 02-scenarios/student-content/
    target_audience: Students and prospects
    primary_channels: [xiaohongshu, moments]
    knowledge_asset_categories: [brand, courses, cases]
    status: active
```
