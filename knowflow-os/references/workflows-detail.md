# KnowFlow OS Workflows — Detailed Execution Guide

## Workflow 1: import-and-classify

**Purpose**: Import raw materials and automatically classify them.

**Steps**:

1. **scan_inbox**: Check 00-inbox/ for new materials
2. **detect_file_type**: Identify the material type (text, image, PDF, link, audio, video, chat)
3. **extract_text**: Extract full text content (OCR for images, parsing for documents, scraping for links)
4. **summarize_content**: Generate a concise summary of the content
5. **classify_asset_type**: Determine which knowledge asset category fits best:
   - brand, products, courses, people, cases, faq, operations, training, research, media-assets
6. **generate_metadata**: Create metadata.yml with:
   - id, name, category, type, tags, source, status, created_at, updated_at, related_topics
7. **recommend_storage_path**: Suggest the archive location in 01-knowledge-base/
8. **create_asset_folder**: Create the asset directory with metadata.yml, raw.md, summary.md, notes.md
9. **move_to_knowledge_base**: Move processed files to the recommended path
10. **update_content_index**: Add the new asset to metadata/asset-index.yml

**Key Rules**:
- Never delete or overwrite raw files
- All materials must enter through 00-inbox/
- When uncertain, place in `01-knowledge-base/uncategorized/` with explanation

---

## Workflow 2: knowledge-to-topic

**Purpose**: Generate content topics from knowledge assets.

**Steps**:

1. **select_knowledge_assets**: Choose relevant assets from 01-knowledge-base/
2. **extract_key_points**: Identify the most valuable and传播-worthy knowledge points
3. **identify_audience**: Define the target audience for potential topics
4. **identify_pain_points**: Map audience pain points to knowledge points
5. **generate_topic_angles**: Create multiple topic angles:
   - Pain point type
   -干货 type
   - Story type
   - Opinion type
   - Interactive type
6. **score_topics**: Rate each topic on:
   - Relevance to knowledge assets (1-5)
   - Audience demand match (1-5)
   -传播 potential (1-5)
   - Operability (1-5)
7. **save_topic_cards**: Generate topic cards using templates/topic-card.md and save to 03-topic-pool/pending/

**Key Rules**:
- Every topic must link to at least one knowledge asset
- Every topic must link to at least one scenario
- Topics should be specific and actionable, not vague

---

## Workflow 3: topic-to-content

**Purpose**: Generate channel-specific content from topics.

**Steps**:

1. **read_topic_card**: Load the topic from 03-topic-pool/
2. **load_related_knowledge_assets**: Read all linked assets from 01-knowledge-base/
3. **select_scenario**: Determine which business scenario applies
4. **select_channel_template**: Choose the appropriate template from templates/
5. **generate_content_draft**: Write the content following the template structure
6. **generate_title_options**: Create 3-5 title alternatives
7. **generate_cover_copy**: Write cover/cover image text for visual channels
8. **generate_publish_suggestions**: Add timing, channel, and注意事项 recommendations
9. **save_to_content_factory**: Save the draft to 04-content-factory/drafts/

**Key Rules**:
- Different channels require different content versions
- Content must cite which knowledge assets were used
- Include review notes and compliance checks
- Apply scenario-specific tone and style from scenario.yml

---

## Workflow 4: content-to-publish

**Purpose**: Prepare content for publishing.

**Steps**:

1. **check_content_completeness**: Verify all required sections are present
2. **run_review_rules**: Check against scenario-specific review rules:
   - No exaggerated claims
   - Cases anonymized
   - Sources cited
   - Channel format correct
3. **create_channel_version**: Finalize the channel-specific version
4. **move_to_scheduled**: Move to 05-publish-center/scheduled/
5. **create_publish_checklist**: Generate a pre-publish checklist

---

## Workflow 5: publish-to-review

**Purpose**: Post-publish analytics and review.

**Steps**:

1. **collect_publish_data**: Gather metrics (reads, likes, saves, comments, shares, conversions)
2. **analyze_performance**: Compare with historical data and similar content
3. **summarize_feedback**: Analyze comments and user feedback
4. **update_topic_status**: Move topic from in-progress to published in 03-topic-pool/
5. **recommend_repurpose_actions**: Suggest二次创作 directions
6. **save_review_report**: Generate review report using templates/review-report.md to 06-review/

**Key Rules**:
- Complete review within 7 days of publishing
- Review must include both quantitative data and qualitative feedback
- Conclusions must lead to actionable improvements
- Reusable insights should update related knowledge assets

---

## Workflow Triggers

| User Request | Triggered Workflow |
|-------------|-------------------|
| "Upload this file/image/link" | import-and-classify |
| "Organize these materials" | import-and-classify |
| "Generate topics from X" | knowledge-to-topic |
| "What should I write about?" | knowledge-to-topic |
| "Write a Xiaohongshu post about X" | topic-to-content |
| "Create a video script for X" | topic-to-content |
| "Prepare this for publishing" | content-to-publish |
| "Review this published content" | publish-to-review |
| "Analyze the performance of X" | publish-to-review |
| "Init KnowFlow OS" | init-project (all workflows) |
