---
name: skill-author
description: Create or revise a Cinch curriculum lesson draft directly in Skills Studio for the coach to review and publish. Use when the coach says "draft a skill on ...", "turn this video into a skill", "edit this Studio draft", or "revise the cornering lesson". Handles existing-draft revisions as well as new lessons.
---

# Skill author

Claude drafts the lesson. The coach reviews it in Skills Studio and publishes it themselves.

## Needs

Use `list_skills`, `get_skill`, `create_skill_draft`, and `update_skill_draft` on
the coaching MCP. Reads need `trainingpeaks:read`; drafts need `coaching:draft`.
The caller must have active Skills Studio workspace access. Tenant and author
come from the connection, never from tool arguments.

These tools use the plugin's existing `cinchos-coaching` connection at
`https://os.cinchcycling.com/api/mcp/coaching`; do not add a separate Skills MCP.
Read the Skills Studio section of [cinchos-guide](../cinchos-guide/SKILL.md).
The draft tools save immediately: they have no `confirm` or preview argument.
Show the proposed content or change to the coach and use their approval for that exact
write. If the session already contains that approval, do not ask for it again.

If the connected deployment has not shipped these tools yet, say so. Draft in
the conversation and, on the coach's OK, save `Skill drafts/<title>.md` in their work
folder. Do not claim it reached Studio. A permission or validation error is not
tool unavailability: show the error and resolve it, rather than claiming success.

## Steps

1. For an existing lesson, locate it with `list_skills` (include drafts) or use
   the coach's supplied ID, then call `get_skill({skillId})`. Establish the requested
   change, current status, and revision before drafting an edit. For a new
   lesson, search published examples and existing drafts to avoid duplicating
   one. Use the returned `levels` and `categories` vocabulary; read relevant
   examples with `get_skill` to match their structure. If none exist, use the coach's
   supplied material and ask only about gaps that prevent a grounded lesson.
2. Call `search_knowledge` (cinchos-coaching, `depth: "deep"`) on the topic. Build the lesson from what Cinch has already taught. Cite where an idea came from in your notes to the coach, not in the lesson.
3. Call `get_voice_profile` with `channel: "general"` for the coach's written tone.
   This is a writing-style profile, not an audio or ElevenLabs dependency.
4. Draft: title, level, short intro, the steps or drills, common mistakes, and how the athlete knows they've got it. Leave the video slot empty unless the coach gives you one.
5. Show the coach the draft. Take edits.
6. On the coach's OK, call `create_skill_draft` (or `update_skill_draft` for an existing
   draft). Read it back with `get_skill` and compare the saved fields with the
   approved content. Give them the returned `studioUrl` and any remaining
   readiness gaps. If read-back fails, distinguish the acknowledged save from
   unverified content and provide the link to check. Never call a publishing
   endpoint, change status, affirm assets, or unpublish on their behalf.

## Tool contract

- `list_skills`: optional `level`, `category`, `status` (`draft` or `published`),
  `search` (up to 120 characters), `limit` (1–100, default 30), `offset`.
  Follow non-null `nextOffset` for more; null or an empty page ends pagination.
- `get_skill`: `{skillId}`. Returns full content, assets/readiness, internal
  reviewer note, `revision`, and `studioUrl`.
- `create_skill_draft`: required `title`, `level`, `category`, `intro`, and
  `bodySections: {steps: string[], commonMistakes: string[], masteryChecks: string[]}`.
  `level` and `category` may be null when not yet chosen; never invent a category.
  Sections are plain text, not HTML. Optional `cues`, `tags`, `reviewerNote`, and
  `existingVideo: {mediaUrl, posterUrl?, durationSeconds?}`. Video/poster must be
  existing HTTPS URLs. No upload or video generation.
- `update_skill_draft`: `{skillId, expectedRevision, ...changedFields}`. Use the
  revision from the latest get/create/update. Omitted fields stay unchanged;
  supplied arrays replace their field. When changing `bodySections`, include
  all three arrays, carrying forward unchanged sections from the current read.
  Pass null to clear nullable intro/reviewerNote/level/category; pass empty
  arrays to clear a section. Reviewer notes stay staff-only and send no
  notification. Never put them in athlete-facing lesson sections.

If an edit is stale, get the current skill and show the coach the difference before
retrying with approval of the reconciled change. If it is published, explain
that MCP edits require a draft; the coach handles published content in Skills Studio.
Do not promise an unpublish control exists or silently create a replacement.
After an uncertain create response, search for the draft and inspect candidates
before retrying, so a lost response does not produce duplicate lessons. If the
result cannot be reconciled, report the uncertainty and stop that write. After
an uncertain update, read the current content and revision before retrying.

## Rules

- Drafts only. The coach's manual Publish action in Skills Studio approves the lesson
  text; the existing generated-media affirmation gate remains unchanged. A draft
  without video can be saved but is not yet publish-ready. Readiness is not
  permission for the agent to publish.
- Coaching claims come from Cinch's own material or the coach. If the knowledge base has nothing on a point, ask the coach instead of filling the gap.
