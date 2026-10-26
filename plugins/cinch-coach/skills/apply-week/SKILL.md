---
name: apply-week
description: Put a published quarter week (the coach's library plan, % of FTP) onto athletes' TrainingPeaks calendars. Use when a coach says "apply week 1 of Foundation to my Intermediate athletes", "put weeks 5 and 6 on Sarah", "who still needs next week?", or "undo last week for Mike". For a week aimed at an athlete's own PRs, use athlete-week instead.
---

# Apply week

After quarter-plan publishes a quarter, the coach's TrainingPeaks library holds six plans a week, for example "Foundation Q4 (Int) - Week 3 - (Strength)". This skill applies those plans to athletes a week at a time. The targets are % of FTP, exactly as the coach wrote them.

## Needs

The CinchOS coaching tools: `list_masters`, `publish_master`, `get_plan_status`, `list_planned_workouts`, `list_races`, `apply_plan_weeks`, `undo_applied_week`.

- Each coach works on their own athletes only. Another coach's athlete comes back as not found.
- Writes need the four plan-write switches on for the coach. A `blocked` answer names the switch: stop and tell the coach; an authorized CinchOS administrator manages access.

## Steps

1. **Who, which week, which tier.**
   - Call `get_plan_status` with no athlete for the coach's roster, or with `athleteId` for one athlete. It shows what CinchOS put on each calendar from two weeks back to eight ahead, and whose next week is still open.
   - Owners see every athlete in `list_my_athletes`, but can only apply to their own: athletes whose `coachEmail` is the coach's sign-in or TrainingPeaks coach address. When the coach says "my athletes", keep only those.
   - Ask the tier (Novice, Intermediate or Advanced) and With or Without strength for each athlete, unless the coach said.
2. **Find the published plan.**
   - Call `list_masters` for the quarter's `planId`.
   - Call `publish_master` with that `planId` and no `confirm`; it only reads. Each rendition lists its week, tier, strength, `tpPlanName`, `state` and `tpPlanId`.
   - Use the rendition whose `state` is `published`. If it isn't published yet, say so: the coach publishes the quarter first (quarter-plan).
3. **Check the week.** The week's Monday is the quarter start date plus 7 days per week.
   - Call `list_planned_workouts` for each athlete for that Monday to Sunday.
   - Call `list_races` for races that week.
4. **Preview.** Call `apply_plan_weeks` with `athleteIds`, `tpPlanId` and `startDate` (that Monday), without `confirm`.
   - Show a short summary per athlete with every warning (not linked to TrainingPeaks, outside TrainingPeaks' window, already applied, a race that week, no FTP) and anything already on the calendar.
   - Ask about each warning. Don't decide for the coach.
   - Athletes on different tiers need one call per tier, because each tier is its own TrainingPeaks plan.
5. **Apply.** On a clear OK for exactly what was shown, call again with the same arguments and `confirm: true`. Report what was written, and anything skipped with the reason.
6. **Undo.** Get the `applicationId` from `get_plan_status` and call `undo_applied_week`: preview first, then `confirm: true`. It removes only workouts CinchOS wrote and leaves anything the athlete completed.

## Rules

- One OK covers the preview it follows. If the coach changes athletes, weeks or tiers, preview again.
- A week that's already applied is skipped unless the coach asks to replace it (`replace: true`).
- Races don't move workouts. The preview flags the race week and the coach decides, often with a custom-week taper.
- A "reconnect TrainingPeaks" result means the coach needs to reconnect TrainingPeaks in CinchOS once to grant the new permissions.
- TrainingPeaks only takes planned workouts from 6 days back to 365 days ahead.
- If an athlete is skipped for any reason, tell the coach who and why.
