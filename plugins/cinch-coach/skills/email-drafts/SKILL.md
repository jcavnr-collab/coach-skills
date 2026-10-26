---
name: email-drafts
description: Review, edit and send the coach's email drafts through CinchOS. Use when the coach says "send the Jamie and Mike drafts", "make Mike's reply warmer", "show me my drafts", or "archive the noise".
---

# Email drafts

Works on the replies the inbox-triage skill wrote in its summary, and on drafts already in the coach's Gmail.

## Steps

1. Find the drafts the coach means. Use the latest triage summary in this session, or ask which ones.
2. For a reply from the triage summary, use its text. For a draft already in Gmail, call `get_draft`. Show the full text.
3. Take edits in plain language. Rewrite in the coach's voice (`get_voice_profile`, `channel: "inbox"`).
4. Show the final text of every email they want to send, together: to, subject, body.
5. Send only after the coach says to.
   - A reply from the triage summary needs a Gmail draft first: call `draft_reply` on the message ref (it makes the draft and costs one model run on Rincon's account).
   - Then call `send_draft` with that draft id, `confirm: true` and `finalBody` set to the final text. The OS learns their voice from the difference.
6. Report what sent and what failed.

## Archiving

When the coach OKs archiving the noise from a triage summary, call `bulk_archive` with those refs and `confirm: true`. Archived mail stays in All Mail.

## Rules

- "Send them" covers only the emails the coach just saw.
- If a send is blocked by a safeguard, report it and stop. The coach can still send from Gmail.
