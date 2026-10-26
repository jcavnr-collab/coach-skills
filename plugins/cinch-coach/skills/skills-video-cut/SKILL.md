---
name: skills-video-cut
description: Rough-cut a Cinch skills video in Descript in the house style. Use when the coach says "cut the new cornering video", "clean up this footage", or "add captions to the skills video". Needs the Descript connector.
---

# Skills video cut

Uses the Descript connector (connect it once in Claude under Settings, Connectors, Descript). Claude makes the rough cut; the coach does fine edits in Descript by deleting words from the transcript.

## House style (confirm with the coach and the videographer)

- Cut filler words and pauses over 1.5 seconds.
- Start at the first useful sentence. No "okay, so".
- Studio Sound on.
- Captions on, Cinch caption style.
- Lower third with the skill name in the first 5 seconds.
- Cinch logo end card.

## Steps

1. Find the footage. The videographer drops raw files in the shared Google Drive folder; import with the Drive import, or by URL.
2. Create or open the Descript project named after the skill.
3. Ask Underlord (`prompt_project_agent`) for the house style above in one instruction, plus anything the coach asked for ("cut everything before I say 'the drill'").
4. Tell the coach the project is ready to review in Descript, with a short list of what was cut.
5. When they're happy, publish a share link and export the transcript as Markdown for the skill page (`export_transcript`). Hand both to the skill-author skill if a skill draft is next.

## Notes

- Imports use media minutes and Underlord uses AI credits on the coach's Descript plan.
- No YouTube links as sources.
- Finished video comes out through publish, as a share link.
