---
name: consult-report
description: Draft and finalize a Roadmap Report or To The Moon Assessment for a Cinch athlete. Use when the coach says "draft Jamie's roadmap report", "do the TTM assessment for Sarah", or asks for a rider report with a focus.
---

# Consult report

## Which report

- **Roadmap Report:** current level, target level, zone progress, season timeline, and a context statement tied to the goal race. Tools: `draft_roadmap_report`, `finalize_roadmap_report`.
- **To The Moon Assessment:** compares against the athlete's intake. Leaves out TSS, IF and NP language and specific workouts. Tools: `draft_to_the_moon_assessment`, `finalize_to_the_moon_assessment`.

If the coach doesn't say which, ask.

## Steps

1. Look the person up by name or email (both tools accept `athleteId`, `email` or `name`). These tools find athletes today. If the person is still a lead and isn't found, tell the coach: the report can go inside the consult invite (prospect-invite skill), or wait for lead support in the OS.
2. Call the draft tool. Pass the coach's focus as `steeringNotes` for the Roadmap Report ("lean on climbing").
3. Show the draft section by section. Take edits and apply them to the draft object.
4. Finalize only when the coach approves. Call the finalize tool with the edited `draft`, `origin: "https://os.cinchcycling.com"` and `confirm: true`. It saves to the athlete's timeline and returns a secure link.
5. Give the coach the link. Sending it to the athlete is their call; offer to draft the note.
