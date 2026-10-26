---
name: sunday-prep
description: Build the coach's Sunday planning list from CinchOS. Use when the coach says "get me ready for Sunday", "who do I need to plan for", "who missed sessions this week", or asks what's waiting before they plan the week. Read-only; changes nothing.
---

# Sunday prep

Use the coach's chosen planning day and time zone. This skill prepares a short list of athletes who need attention before the next training week.

Everything here is read-only. Nothing is written to TrainingPeaks or sent to anyone.

## Steps

1. Call `list_my_athletes` (cinchos-coaching). Owners may see every Cinch athlete. For "my athletes", match `coachEmail` to the coach's confirmed sign-in and TrainingPeaks addresses from coach-setup; resolve missing identity before selecting the roster.
2. Call `list_coaching_queue` for comments still waiting on a reply. Count them per athlete.
3. For each active athlete, call `ask_trainingpeaks` with `days: 7` and `live: false` (synced data, light on TrainingPeaks). Flag athletes with no completed workouts this week, or far fewer than usual.
4. Plans and races: call `get_plan_status` (no athlete) for whose next week is still open and what CinchOS has applied up to eight weeks ahead. Call `list_races` (no athlete) for races in the next 6 weeks. Both cover only the coach's own athletes; say so if they ask about the whole team.
5. Present one list, grouped:
   - **Next week still open** (name, last applied week)
   - **Race coming up** (name, race, date)
   - **Missed sessions** (name, what's missing)
   - **Comments waiting** (name, count)

Keep it to one screen. Names first, details short. End by asking which athlete they want to start with.

## Notes

- Use `get_athlete_timeline` only when the coach asks about one athlete in detail.
- Heart rate, weight and health data stay in this conversation. Don't paste them into files or other tools.
