---
name: athlete-week
description: Send one or more athletes a quarter week with their own power PRs as the targets, onto their TrainingPeaks calendars. Use when the coach says "send Alex week 1 at their PRs", "give my athletes next week of Foundation", "preview week 3 for Sarah, Intermediate", "set Mike's zones to this year", "make their 15-second reps 800 W", "is their FTP right?", or "undo Sarah's week 2".
---

# Athlete week

The library plan (from quarter-plan) gives every athlete the same % of FTP. This skill sends one athlete a quarter week where each interval aims at that athlete's own best power for its zone. Coaches send it; athletes never set their own zones.

## Needs

The CinchOS coaching tools: `list_my_athletes`, `list_masters`, `get_athlete_zones`, `set_athlete_zones`, `list_planned_workouts`, `preview_athlete_week`, `send_athlete_week`, `update_zone_threshold`, `undo_applied_week`, `get_plan_status`. They work only for the coach's own athletes. Sending needs the four plan-write switches on for the coach. A `blocked` answer names the switch: stop and tell the coach, an authorized CinchOS administrator manages access.

## How targets are worked out

- **% of zone steps (the usual way now).** A step the coach wrote as a percent of a zone, like "Force (93% F2F90)", carries that as data (a `ZoneRef`). It aims at the athlete's PR for that zone times the coach's percent: F2F90 PR 235 W x 93% = 219 W. It goes to TrainingPeaks as % of the athlete's FTP there, so TrainingPeaks shows 219 W. Warm-ups, recoveries and endurance work the same way when the coach wrote them as % of a zone.
- If the athlete has no PR for that zone, the step keeps the master's % of FTP and the preview names the athlete and the zone. Offer to type a PR (`set_athlete_zones` `zoneWatts`) or pick another window.
- The athlete's saved target percent doesn't change % of zone steps; the coach's percent is the target. The preview says so when one is set.
- **Older steps without a zone** (masters built before % of zone): the coach's % of FTP picks the zone, and the interval aims at the athlete's PR for it:

  | % of FTP | Zone | PR used |
  |---|---|---|
  | 83 to 95 | F2F40 | 40-minute |
  | 95 to 101 | TF20 | 20-minute |
  | 101 to 107 | TF8 | 8-minute |
  | 107 to 112 | PF5 | 5-minute |
  | 112 to 118 | PF2 | 2-minute |
  | 118 to 132 | PF1 | 1-minute |
  | 132 and up | MES | 5-second |

  Warm-ups, cool-downs, recoveries and anything under 83% stay as the coach wrote them.

- CinchOS uses these zone names: PF is the Potency Factor, TF the Threshold Factor, F2F the Fall-to Factor, and the number is the PR's duration in minutes. CinchOS shows these names everywhere; use them, not the older ones (Short Surge, Long Surge, VO2, High Threshold, Threshold, Low Threshold, High Medium).
- The PRs come from the athlete's Workout Zones: the window (trailing 12 months by default, this year or last year), a target percent, and any zone a coach typed over.
- CinchOS holds power history from January 2025. "Career PRs" means the best since then.

## Steps

1. **Who, which week, which tier.**
   - Find the athletes with `list_my_athletes` and the quarter with `list_masters`. Owners may see the whole roster. For "my athletes", match `coachEmail` to the signed-in coach's confirmed addresses from coach-setup. If identity is uncertain, resolve it before building a recipient list. Other coaches' athletes answer "not found" and can't be sent.
   - Ask the tier for each athlete (Novice, Intermediate or Advanced) unless the coach said. CinchOS doesn't store a tier per athlete yet.
   - Confirm whether strength belongs in this athlete's week. Use their saved, approved preference when available; do not enable it by default.
   - "Next week" is the quarter week that starts next Monday. Work out the week number from the quarter's start date.
2. **Zones.** For a new athlete, or when the coach mentions PRs, call `get_athlete_zones` and show the zone watts in one short table.
   - Changes go through `set_athlete_zones`: `basis`, `targetPct`, `zonePct`, or `zoneWatts` to type over a zone (null restores it). Preview, then `confirm: true` on the coach's OK.
   - A typed zone applies to every later week for that athlete. Say so when you set one.
3. **FTP check, before any send.** `get_athlete_zones` and `preview_athlete_week` both show a suggested FTP: the athlete's TF20 (20-minute) PR over the trailing 12 months. `ftpCheck.flagged` means the FTP is more than 15% off it.
   - Tell the coach the FTP, the suggested FTP and how far apart they are. Don't change it on your own.
   - If they want it changed, call `update_zone_threshold` (`kind: "power"`, the new `threshold`) to preview, then `confirm: true` on their OK. Do it **before** sending the week, never mid-week: TrainingPeaks keeps planned targets as % of FTP, so a new FTP moves the watts of every workout already on the calendar, including a week sent at % of zone.
   - The % of zone watts are right whatever the FTP is; the FTP matters for anything still % of FTP and for later changes.
4. **Calendar.** Call `list_planned_workouts` for that week. If anything is already planned, tell the coach. Sending adds the quarter week, so the athlete would get both unless the earlier week came from CinchOS and the coach asks to replace it.
5. **Preview.** Call `preview_athlete_week` (athlete, quarter `planId`, `weekNumber`, `tier`, `withStrength`).
   - Show each ride with its intervals as one compact table: interval, reps, zone and percent (93% F2F90), the PR and its date, the athlete's watts, and the % of FTP that will be sent.
   - Point out targets far above the library: anything over 150% of FTP, usually short reps in PF1 or MES.
   - Also point out a warning that the FTP came from CinchOS, and any rides still waiting for intervals (they block the send).
6. **Send.** Only after the coach says to send exactly what they saw, call `send_athlete_week` with the same arguments and `confirm: true`.
   - Read the result's warnings. "TrainingPeaks didn't give this athlete's FTP" means the targets went as % of CinchOS's FTP. Ask the coach to check the athlete's FTP in TrainingPeaks.
7. **Check.** Call `list_planned_workouts` again and confirm the workouts landed once each. Report the count and the hardest day's TSS.
8. **Resend or undo.**
   - After a zone change, resend with `replace: true`. A send that stopped partway is also finished with `replace: true`.
   - To take a week off, find its `applicationId` with `get_plan_status` and call `undo_applied_week` (preview, then `confirm: true`). It leaves completed workouts alone.

## Several athletes

- Run steps 2 to 5 for each athlete, then show one summary table: athlete, tier, FTP and suggested FTP (flag over 15%), rides, the highest target, warnings, what's already on the calendar.
- Settle any FTP changes for the whole group before the first send.
- One "send them" covers exactly the athletes in that table.
- Send one athlete at a time and report each result. Stop and report on the first `blocked`.

## Rules

- One OK covers the preview it follows. A new tier, week, zone or FTP change needs a new preview.
- FTP changes happen before a send, never in the middle of a week that is already on the calendar.
- Health and power data stay in this conversation. Don't write them to files unless the coach asks for a file.
- Sends write to athletes' TrainingPeaks calendars. Never send on a guess about the athlete, week or tier; ask.
