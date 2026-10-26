---
name: cinchos-guide
description: How to use the two CinchOS connections (cinchos-coaching and cinchos-inbox) well. Which tool does which job, the rules every write follows, which tools are legacy, and how to keep answers small. Read it before the first CinchOS call in a session, and whenever a request touches Cinch athletes, TrainingPeaks, plans or quarters, coaching comments, nudges, leads, consults, reports, email, calendar or support.
---

# CinchOS guide

CinchOS is Cinch Cycling's operating system. Claude reaches it through two connections, both signed in as the coach using Claude:

- **cinchos-coaching**: athletes, TrainingPeaks, coaching comments, nudges, leads and onboarding, plans and quarters, Workout Zones, Skills Studio drafts, knowledge and voice.
- **cinchos-inbox**: email, calendar, consult invites and booking, Roadmap and To The Moon reports, Today's Priorities, Community join requests, support requests.

The other skills in this plugin handle whole workflows. This guide is the map behind them.

## Rules every session follows

1. **Preview, then confirm when the tool supports it.** For tools with a `confirm` argument, show the returned preview and call again with `confirm: true` only after a clear yes for exactly what was shown. One yes covers one preview. **Skills Studio draft exception:** `create_skill_draft` and `update_skill_draft` save immediately and do not accept `confirm` or a preview flag. Show the proposed lesson/edit in the conversation and get the coach's OK before that one draft write. Publishing always stays in Skills Studio.
2. **Own athletes only.** Writes for an athlete (zones, weeks, plans, races, thresholds) only work when the athlete's coach is one of the caller's own addresses: their sign-in, or the TrainingPeaks coach account they connected. Anyone else answers "not found".
   - Owners and office managers *see* every athlete in `list_my_athletes`, but the write rule still applies to them.
   - When the coach says "my athletes", filter by `coachEmail`. Use only this coach's confirmed sign-in and connected TrainingPeaks coach addresses from coach-setup. If those are unknown, resolve them before selecting recipients. Never infer the current coach from an owner role or someone else's example.
3. **Safeguards are not obstacles.** Sends pass four gates: an environment switch, a workspace switch, a per-coach allowlist, and your `confirm`.
   - A `blocked`, `forbidden` or "not turned on" answer names what is off. Tell the coach and stop. an authorized CinchOS administrator manages access.
   - Never retry a blocked send another way.
4. **Health and money stay in the conversation.** Heart rate, weight, power, injuries, billing and email contents are not written to files, notes or other tools unless the coach asks for that file.
5. **Big answers.** Some reads are very large (`get_master_week` is about 100,000 characters for one week).
   - Ask for one week, one tier, one athlete at a time.
   - Summarize rather than paste.
   - When the coach wants detail, show one ride.
6. **Model-running tools cost Rincon money.** `classify`, `morning_digest` and `draft_reply` run a model on Rincon's account. When you can do the sorting or writing yourself from `list_unread` and `get_thread`, do it yourself. Use them when the coach asks for them.
7. **Dates.** A quarter runs Monday to Sunday, always. TrainingPeaks only takes planned workouts from 6 days back to 365 days ahead. Use the coach's confirmed time zone; do not assume a location or UTC offset.
8. **Zone names.** CinchOS names the coach's TTM zones MES, PF1, PF2, PF5 (Potency Factor), TF8, TF12, TF20 (Threshold Factor), F2F40, F2F60, F2F90 (Fall-to Factor), Medium and Low Medium; the number is the duration in minutes. Tools return these labels; zone ids in tool arguments (`shortSurge`, `cp`, `highMed`...) didn't change. Use the new names with coaches, not the older ones (Short Surge, Long Surge, VO2, High Threshold, Critical Power, Low Threshold, High Medium). Reports already sent keep the old names.

## Which tool for which job

### Athletes and TrainingPeaks (cinchos-coaching)

| Job | Tools |
|---|---|
| Roster, filter by tier or health | `list_my_athletes` |
| One athlete's profile, or recent emails, comments and billing | `get_athlete`, `get_athlete_timeline` |
| Recent rides, or one ride in detail | `ask_trainingpeaks` (`days`; `workoutId` for intervals and mean-max; `live: false` for synced data, lighter on TrainingPeaks) |
| What's planned on the calendar | `list_planned_workouts` |
| TrainingPeaks zones, or change an FTP or threshold (before a send, never mid-week; `get_athlete_zones` shows the suggested FTP) | `get_zones`, `update_zone_threshold` |
| Races | `list_races`, `save_race` |
| What CinchOS has put on calendars, whose next week is open | `get_plan_status` |

### Quarters and weeks (cinchos-coaching)

| Job | Tools | Skill |
|---|---|---|
| Find programs and quarters | `list_masters` | quarter-plan |
| Read a week | `get_master_week` (one tier per call) | quarter-plan |
| Start a quarter | `start_quarter` | quarter-plan |
| Change a quarter | `copy_master_week`, `edit_master_week`, `set_quarter_strength` | quarter-plan |
| Publish to TrainingPeaks | `publish_master` (also on the Plans page) | quarter-plan |
| Bring a program in, or read its intervals | `consolidate_tp_library`, `import_master_intervals` | quarter-plan |
| Apply a published week (% of FTP) | `publish_master` (no confirm, for the `tpPlanId`), then `apply_plan_weeks` with `tpPlanId` and `startDate` | apply-week |
| A week at an athlete's own PRs | `get_athlete_zones`, `set_athlete_zones`, `preview_athlete_week`, `send_athlete_week` | athlete-week |
| A taper or custom week | `build_custom_week` | custom-week |
| Take a week off a calendar | `get_plan_status` for the `applicationId`, then `undo_applied_week` | any |

**Legacy, don't use for quarters:** `list_plans`, `get_plan`, `create_plan`, `update_plan_week`, `publish_plan`, `clone_plan`, `import_tp_library`, `import_tp_plan`. They belong to the plan library from before quarter masters. `list_tp_plans` is still useful to see what's in a coach's TrainingPeaks library.

### Coaching comments and nudges (cinchos-coaching)

| Job | Tools | Skill |
|---|---|---|
| Comments waiting for a reply | `list_coaching_queue` | comments-by-prompt |
| Draft, edit, send replies | `draft_coaching_reply`, `edit_coaching_draft`, `send_coaching_replies_bulk` (or `send_coaching_reply` for one) | comments-by-prompt |
| Quiet athletes and nudges | `list_engagement_nudges`, `regenerate_engagement_nudge`, `send_engagement_nudge` | roster-check |

### Voice and knowledge (cinchos-coaching)

- `get_voice_profile` with `channel` `coaching`, `inbox` or `general`. Follow its `promptBlock` whenever writing as the coach.
- `search_knowledge` answers from everything Cinch has written: TTM, training notes, past comments. Ground coaching claims in it. If it has nothing, ask the coach.

### Skills Studio (cinchos-coaching)

Use the `skill-author` workflow for lesson drafts. These are tenant-wide library
items, not athlete-specific writes, and require the caller's existing active
Skills Studio workspace access.

| Job | Tools |
|---|---|
| Find visible drafts/published skills and tenant level/category vocabulary | `list_skills` |
| Read a lesson, its revision, assets and publish readiness | `get_skill` |
| Save an approved lesson as a draft | `create_skill_draft` |
| Edit an existing draft with its latest revision | `update_skill_draft` |

Return the tool's `studioUrl`. No MCP tool publishes, unpublishes, affirms media,
or uploads video. MCP edits require draft status; the coach handles published
content in Studio. Do not promise an unpublish control exists. For stale edits, read the current version and show
the differences before retrying. Never add unsupported `confirm` arguments.

### Leads and onboarding (cinchos-coaching)

`list_my_leads`, `get_lead`, `lead_search`, `lead_onboarding_status`, `lead_set_post_consult`, `lead_preview_onboarding_packet`, `lead_send_onboarding_packet` (preview first; the send emails the lead).

### Email and calendar (cinchos-inbox)

| Job | Tools | Skill |
|---|---|---|
| What's unread, read a thread, search | `list_accounts`, `list_unread`, `get_thread`, `search` | inbox-triage |
| Drafts and sending | `draft_reply` (makes a Gmail draft on a message), `get_draft`, `send_draft` (`finalBody` for the approved text), `compose_and_send` (new email), `forward_to`, `schedule_send` | email-drafts |
| Tidy up | `archive_message`, `bulk_archive`, `mark_read`, `bulk_mark_read`, `snooze`, `unsubscribe` | email-drafts |
| Templates and rules | `list_templates`, `save_template`, `apply_template`, `list_rules`, `save_rule`, `delete_rule`, `apply_rules` | |
| To-dos from a thread | `extract_action_items` | |
| Calendar | `list_agenda`, `check_availability`, `propose_times`, `send_invite` | |

### Consults, reports and the day (cinchos-inbox)

| Job | Tools | Skill |
|---|---|---|
| Personal consult invites | `list_personal_consult_invites`, `get_personal_consult_invite`, `save_personal_consult_invite_draft`, `prepare_personal_consult_invite_times`, `select_personal_consult_invite_times`, `preview_personal_consult_invite`, `send_personal_consult_invite` | prospect-invite |
| Move a booked consult | `reassign_consult` (the rider gets an email) | |
| Roadmap and To The Moon reports | `draft_roadmap_report`, `finalize_roadmap_report`, `draft_to_the_moon_assessment`, `finalize_to_the_moon_assessment` | consult-report |
| Today's Priorities | `list_today_queue`, `summarize_today_queue`, `get_queue_item`, `snooze_queue_item`, `dismiss_queue_item` | |
| Community join requests | `admit_join_request`, `decline_join_request` (the person gets an email), `undo_join_decision` | |
| Support requests | `list_support_requests`, `get_support_request`, `create_support_request`, `reply_to_support_request` | |

## Not built yet

- No tool saves Claude's own text straight into a Gmail draft. To send a reply Claude wrote, make the draft with `draft_reply`, then send it with `send_draft` and `finalBody` set to the approved text.
- Playbook authoring tools are not built yet. `playbook-author` uses the live
  lesson catalog, then saves a local assembly handoff. For skill drafts, use the four
  Skills Studio tools above when the connected deployment advertises them. If
  unavailable, follow skill-author's explicitly labeled conversation/file fallback.

## When something fails

- **"not found"** for an athlete: not one of the caller's own athletes, or a typo. Check `list_my_athletes`.
- **"reconnect TrainingPeaks"**: the coach reconnects TrainingPeaks once in CinchOS (Settings › Integrations).
- **The connection asks to sign in**, or tools disappear: reconnect the CinchOS connector in Claude's settings.
- **A tool's answer contradicts this guide**: trust the tool. CinchOS changes faster than this file. Report the mismatch to the plugin maintainer.
