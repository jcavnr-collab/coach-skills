---
name: roster-check
description: Find Cinch athletes who are slipping and help the coach re-engage them. Use when the coach asks "who's slipping", "who haven't I talked to", "who's gone quiet", or wants to send re-engagement nudges.
---

# Roster check

Shows the coach who has gone quiet and offers a ready nudge for each one.

## Steps

1. Call `list_engagement_nudges` (cinchos-coaching). It returns athletes with no coach contact in 7 days, longest quiet first, each with a drafted comment on their latest ride.
2. Show the coach a numbered list: athlete, days quiet, latest ride in a few words, and the drafted nudge.
3. Take their edits in plain language ("make 3 shorter", "skip Mike", "ask Sarah about her knee"). Rewrite the text yourself in the coach's voice. Call `get_voice_profile` with `channel: "coaching"` once at the start and follow its `promptBlock`.
4. If the coach wants a fresh draft from the OS instead, call `regenerate_engagement_nudge`.
5. Show the final text of every nudge they want to send, all together. Send only after they say to send them.
6. Send each with `send_engagement_nudge` (`confirm: true`, and `bodyOverride` set to the final text when you changed it). Report what posted and what failed.

## Rules

- Show the exact text before anything posts. One "send them" from the coach covers the batch they just saw, nothing else.
- If a send fails because a safeguard is off (kill switch, allowlist), report it plainly and stop. Don't retry around it.
