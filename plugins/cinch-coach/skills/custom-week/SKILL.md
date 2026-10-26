---
name: custom-week
description: Build a taper week or a custom week for one athlete and put it on their TrainingPeaks calendar in place of the plan week. Use when the coach says "Sarah races on the 14th, give her a taper", "Mike's traveling next week, two short rides and a run", or "Jen's sick, push this week's intensity to next week".
---

# Custom week

For one athlete at a time. The week replaces what the plan would have put in that slot, and the Plans page marks it as taper or custom.

For a quarter week aimed at the athlete's own power PRs, use the athlete-week skill instead. This skill is for weeks the coach describes themselves: tapers, travel, illness.

## Needs

The CinchOS coaching tools: `get_plan_status`, `build_custom_week`, `get_zones`, `list_races`, `save_race`. Read the athlete's recent training with `get_athlete_timeline`. Only the coach's own athletes are available.

## Steps

1. Call `get_plan_status` for the athlete to see their plan, the week in question and anything already applied. Check their zones with `get_zones`.
2. For a taper: count back from the race date. Take it from `list_races` or from the coach; TrainingPeaks doesn't let a coach read races back. If the coach gives a race that isn't saved, offer to save it with `save_race` (name, date, priority A, B or C). Ask them for the taper shape (how many days, how much to cut volume, which openers to keep).
3. For a custom week: build from the coach's notes. Keep the plan's intent for the week where you can and say what you dropped.
4. Call `build_custom_week` with `athleteId`, `weekStart` (YYYY-MM-DD; day 1 is that date), `mode` (`"taper"` or `"custom"`) and `workouts` (each with `day`, `workoutType`, `title`, `description`, `durationSeconds`, and `tssPlanned` only when the coach gives one). It previews first. Show the coach the days, total hours compared with the plan week, and any planned workouts it would replace.
5. On their OK for that preview, call it again with the same arguments and `confirm: true`. If a week is already applied in that slot, it needs `replace: true`.
6. If the coach changes an FTP or threshold, `update_zone_threshold` previews the current and new value; confirm with `confirm: true` and TrainingPeaks recalculates the zones. Change FTP before sending a week, never mid-week: TrainingPeaks keeps planned targets as % of FTP, so a new FTP moves every workout already on the calendar. `get_athlete_zones` shows a suggested FTP (the 12-month TF20 PR) and flags one more than 15% off.

## Rules

- One athlete per call. For a group taper, run it once per athlete.
- TrainingPeaks only takes planned workouts from 6 days back to 365 days ahead.
- The tool doesn't check the athlete's availability. Ask the coach if travel or work days matter.
- Leave completed workouts alone.
- Health questions (illness, injury) get flagged to the coach. Build only what they describes.
