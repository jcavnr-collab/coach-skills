---
name: comments-by-prompt
description: Answer the coach's TrainingPeaks coaching comments from short instructions and send them as a batch. Use when the coach says "go through my queue", "reply to my comments", "tell Sarah ...", or "send the batch".
---

# Coaching comments by prompt

The coach gives a short instruction per athlete. Claude writes each reply in their voice, shows the whole batch, takes edits, and posts everything on one confirmation.

## Steps

1. Call `get_voice_profile` with `channel: "coaching"` and follow its `promptBlock` for every reply.
2. Call `list_coaching_queue` (cinchos-coaching). Each item has the athlete's comment and the OS draft, if one exists.
3. Match the coach's instructions to queue items by athlete name. If a name matches more than one item or none, ask.
4. For each item:
   - **the coach gave an instruction:** pull context with `get_athlete_timeline` (and `ask_trainingpeaks` with the workout id when the comment is about one session), then write the reply yourself from their instruction.
   - **No instruction:** keep the OS draft as written. If there's no draft, call `draft_coaching_reply`.
5. Show the batch as a numbered list: athlete, their comment in one line, the reply in full.
6. Take edits in plain language ("make 2 warmer", "drop the bit about cadence") and show the changed replies again.
7. When the coach says to send, call `edit_coaching_draft` for each reply you wrote or changed. Then send all the draft ids in one `send_coaching_replies_bulk` call with `confirm: true`.
8. Report what posted and what failed.

## Rules

- Show the exact text of every reply before anything posts. "Send them" covers only the batch the coach just saw.
- Replies go to athletes. Keep them in the coach's voice, short, and specific to the ride.
- If a safeguard blocks a send, report it and stop.
