---
name: prospect-invite
description: Turn the coach's Loom for a prospective athlete into a personal consult invite, with consult times from the chosen coach's calendar. Use when the coach shares a Loom link for a prospect, says "send Jamie the consult invite", or names which coach takes a consult.
---

# Prospect invite

The coach records the Loom. Prepare the invite and show its exact recipients, text and times before the approved send.

Example: "Here's the Loom for Casey Example: <link>. Gravel rider from the website. the selected coach takes the consult. Send it."

## Steps

1. Call `list_personal_consult_invites` (cinchos-inbox) and find the prospect by name. If more than one matches, or none, ask the coach.
2. Call `get_personal_consult_invite` with the task id for the current draft, the sender account and the version.
3. Optional: `research_personal_consult_rider` looks up a verified race-results page. It costs a paid lookup, so ask the coach first unless they asked for research.
4. Pick the consult coach the coach named. If they didn't name one, use the default from the invite settings and say who it is.
5. Call `get_voice_profile` (cinchos-coaching, `channel: "inbox"`) and write the subject and body in the coach's voice, with the Loom link.
6. Call `prepare_personal_consult_invite_times` for that coach, then `select_personal_consult_invite_times` with exactly four slot ids. Spread them across days and times of day unless the coach says otherwise.
7. Call `save_personal_consult_invite_draft`, then `preview_personal_consult_invite`. Show the coach the preview: to, cc, subject, body, the four times, and the coach.
8. Send only when the coach says to. Call `send_personal_consult_invite` with `confirm: true`. The OS texts the consult coach after the email goes.
9. If the email went but the coach text failed, offer `retry_personal_consult_coach_text`.

## Rules

- The rider report goes inside the invite flow. For a separate report, use the consult-report skill.
- Moving a booked consult to another coach is `reassign_consult`. Ask the coach before calling it; the rider gets an email.
- If a save returns a version conflict, re-read the invite and redo the step. Someone changed it in the OS.
