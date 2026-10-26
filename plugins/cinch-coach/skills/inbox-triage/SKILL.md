---
name: inbox-triage
description: Triage the coach's email through CinchOS and draft replies in their voice. Use when the coach says "triage my inbox", "what's in my inbox", "draft replies to the athletes and prospects", or when the scheduled inbox-triage routine runs. Drafts only; sends nothing.
---

# Inbox triage

Reads the coach's unread mail through CinchOS, sorts it, and writes reply drafts in the summary. All the reading and writing happens in this Claude session on the coach's plan. CinchOS only hands over mail.

## Cost rule

Use the data tools only: `list_accounts`, `list_unread`, `get_thread`, `get_voice_profile`, `search_knowledge`. The OS tools `classify`, `morning_digest` and `draft_reply` run a model on Rincon's account, so skip them here. Do the sorting and writing yourself.

## Steps

1. Call `get_voice_profile` (cinchos-coaching) with `channel: "inbox"`. Follow its `promptBlock` for every draft.
2. Call `list_unread` (cinchos-inbox) for email from the last day (or since the last run). Use `get_thread` when the preview isn't enough.
3. Sort each email into one group:
   - **Athletes** (current Cinch athletes)
   - **Prospects** (leads, consult questions, "how do I sign up")
   - **Partners and business** (vendors, sponsors, TrainingPeaks, events)
   - **Noise** (newsletters, receipts, notifications)
   Use `lead_search` or `list_my_athletes` (cinchos-coaching) when you're not sure who a sender is.
4. For each athlete, prospect or partner email that needs a reply:
   - Call `search_knowledge` when the question touches coaching content ("how should I pace a gravel century"), so the answer matches what Cinch already teaches.
   - Write the reply in the coach's voice. Short, specific, no filler.
   - Put the reply text in the summary under that email, with its message ref, so the email-drafts skill can send it. CinchOS has no tool yet that saves Claude's own text as a Gmail draft.
5. Leave a summary:
   - **Needs you today:** one line each.
   - **Drafts waiting:** who, and the subject.
   - **Suggest archiving:** the noise, as a count plus the senders.

## Rules

- This skill drafts. It sends nothing and archives nothing. Sending is the email-drafts skill, with the coach's OK.
- Email contents stay in this session. Don't write them to files, notes or other tools.
- Anything about money, refunds, injuries or complaints goes to "Needs you today" with a draft at most. The coach decides.
