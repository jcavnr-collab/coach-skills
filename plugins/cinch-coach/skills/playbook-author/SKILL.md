---
name: playbook-author
description: Plan a Cinch playbook using the live Skills Studio lesson catalog and save an ordered handoff for the coach to assemble in Studio. Use when the coach says "build a playbook for ...", "add the cornering skill to the Level 3 playbook", or "what should go in a gravel playbook". Lesson lookup is connected; playbook writes remain manual.
---

# Playbook author

A playbook is an ordered set of curriculum skills for one goal or level. Claude drafts it; the coach publishes it in Skills Studio.

## Needs

Use `list_skills` and `get_skill` on the existing `cinchos-coaching` connection
to discover and read lessons. Reads need `trainingpeaks:read` and active Skills
Studio workspace access; follow [cinchos-guide](../cinchos-guide/SKILL.md).

The current MCP has no `list_playbooks`, `create_playbook_draft`, or
`add_skill_to_playbook` tool. Do not call those names or claim a playbook was
saved to Studio. Draft its structure in the conversation and, on the coach's OK, save
a Markdown handoff in their work folder. If a later deployment advertises playbook
tools, inspect their actual schemas and permissions before using them.

If lesson tools are absent, explain that limitation and use material the coach
provides. A permission error needs resolution; it is not proof that the catalog
is empty. Do not claim a complete inventory from a failed or partial read.

## Steps

1. Establish the goal and level from the coach's request. For an existing playbook,
   use a provided outline or ask for its current structure, since the MCP
   cannot read playbooks yet. Discover lessons with `list_skills`, using the
   tenant's returned level/category vocabulary and relevant filters. Follow
   non-null `nextOffset` values until the relevant results are complete; null
   or an empty page ends pagination. Read candidate lessons with `get_skill`.
2. Propose a title, short intro, outcomes, and ordered skills with one line on
   why each belongs. Use `get_voice_profile` for the coach's written tone, and
   `search_knowledge` or the coach's supplied material to ground new coaching claims.
3. Include each lesson's ID, title, current status, and returned Studio link.
   Identify gaps and draft dependencies separately. Use skill-author to create
   a missing lesson only when the coach requests or approves that work.
4. After the coach approves the outline, save it as `Skill drafts/<safe-title>.md`
   inside their work folder, preserving unrelated file content. Read it back.
5. Give the coach the file and explain that the playbook still needs assembly and
   publication in Skills Studio. State which lessons are published and which
   need completion; do not describe a local outline as a saved Studio playbook.

## Rules

- Drafts only. The coach publishes.
- Published skills only inside a playbook the coach is about to publish. Flag any draft skills it depends on.
