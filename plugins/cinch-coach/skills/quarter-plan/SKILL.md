---
name: quarter-plan
description: Design and publish a Cinch quarter with the coach. Start the quarter over a Monday-to-Sunday date range from any of their programs (or empty), change any week or workout using any program as a template, set the strength days, and publish six plans a week to their TrainingPeaks library. Use when the coach says "set up Q4 from Foundation", "start the quarter on October 19", "use Climbing week 7 for week 3", "give me 6 accelerations on Sunday", "put the Plyo circuit on Fridays", or "publish the quarter to TrainingPeaks".
---

# Quarter plan

The coach writes each program once, at Advanced. CinchOS derives Novice and Intermediate from it: fewer reps and shorter endurance fill, with the same intensities, days and descriptions.

A quarter always runs from a Monday to a Sunday. It starts from any of the coach's programs, a legacy program or an earlier quarter, or empty, and the coach changes whatever they want. Programs themselves stay as they are in TrainingPeaks; only the quarter changes.

Publishing puts six TrainingPeaks plans per week into the coach's plan library: Novice, Intermediate and Advanced, each with and without strength. Coaches then apply those plans to athletes in TrainingPeaks.

Nothing in this skill changes an athlete's calendar.

## Needs

The CinchOS coaching tools, used in this order:

1. `list_masters`
2. `consolidate_tp_library`
3. `import_master_intervals`
4. `start_quarter`
5. `get_master_week`
6. `copy_master_week`, `edit_master_week` and `set_quarter_strength`
7. `publish_master`

They need quarter masters turned on for the workspace, and the coach as a plan editor. Importing and publishing also need the four plan-write switches on for the coach. If a tool answers "not turned on", "forbidden" or `blocked`, stop and tell the coach which one. an authorized CinchOS administrator manages access.

## Steps

Every write starts with a preview. Show the coach the preview, and call again with `confirm: true` only after a clear yes for exactly what was shown.

1. **Find the program.** Call `list_masters`. Check whether the requested program and its intervals are already available; skip import only when the tool confirms they are ready.
   - If the program is there, note its `planId`.
   - If it isn't, call `consolidate_tp_library` with no arguments to list the programs, then with `program` to preview it. The preview shows how many TrainingPeaks plans become one master and how well the tiers match.
   - On the coach's OK, call with `confirm: true`. Repeat while `status` is `reading`; each call reads a batch of plans. It only reads TrainingPeaks.
   - A program whose tiers ride different workouts stays `legacy`. Tell the coach; it can't be published as a master.
2. **Import its intervals.** TrainingPeaks doesn't hand intervals to a coach's account, so CinchOS reads them through the import athlete's own account. Each plan is put on that athlete's calendar about a year out, read, and removed.
   - Call `import_master_intervals` with the program master's `planId` to preview. Tell the coach how many plans will be read and on whose calendar.
   - On their OK, call with `confirm: true`, and repeat while `status` is `reading`. Each call does a little, and `ridesRemaining` should keep falling.
   - The default reads Advanced only, and that is enough to publish all three tiers. Add `tiers: ["advanced", "intermediate", "novice"]` only if the coach wants their own Novice and Intermediate intervals; the result then shows their real rep ratios.
   - If `status` is `failed` with `clearDates`, read the error to the coach word for word. A temporary plan may be on those dates; they clear them in TrainingPeaks, then you call `undo_applied_week` with the `applicationId`.
3. **Start the quarter.** Ask for anything missing:
   - the quarter (`quarterLabel`, like "Q4 2026");
   - the first day, a Monday (`startDate`), and the last day, a Sunday (`endDate`). A quarter always runs Monday to Sunday. If the coach gives another day, the tool names the nearest Mondays or Sundays: ask them which they meant;
   - where the weeks come from: a program, legacy program or earlier quarter (`planId`) from week `fromWeek` (default 1), or nothing (`program` name only) to start empty.

   Call `start_quarter` without `confirm` and show the weeks with their dates and where each comes from, plus any that start empty. On the coach's OK, call with `confirm: true`. It returns the quarter's `planId`. "exists" means it was already started; use that `planId` and its dates.
4. **Check a week.** Call `get_master_week` for the quarter at `novice` and `advanced` for one or two weeks. One week can be about 100,000 characters, so ask for one week and one tier per call, and summarize rather than paste it. Show the coach the hours and a key ride per tier, so they see what each tier gets before anything goes to TrainingPeaks. Workout ids for edits come from here.
5. **Design the weeks.** the coach can change anything in the quarter. Each tool previews first: show the changes and the week's hours, TSS and rides per tier before and after, then confirm on their OK.
   - **A whole week from another program:** `copy_master_week` (quarter `planId`, `weekNumber`, `fromPlanId`, `fromWeek`).
   - **Workouts:** `edit_master_week` with `ops`, applied in order:
     - `add`: a new workout, or a copy of any program's workout by `fromWorkoutId`;
     - `remove`;
     - `move` to another day;
     - `replace` with a copy or a new workout;
     - `update`: title, description, type, TSS or intervals.

     Write each step as the coach says it, a percent of a zone: keep their name ("Force (93% F2F90)"), the `IntensityTarget` as % of FTP for the library plan, and add `ZoneRef: { zone: "F2F90", pct: 93 }` (zone codes MES, PF1, PF2, PF5, TF8, TF12, TF20, F2F40, F2F60, F2F90; CinchOS stores them as zone ids). Athlete weeks (athlete-week) then aim that step at each athlete's PR for the zone times the percent. The library plan stays % of FTP.

     To make a ride longer or shorter, change its intervals; its length follows. `structure: []` makes a ride with no intervals (a free ride). Novice and Intermediate follow the coach's edited ride.
   - **Strength:** `set_quarter_strength` with a session for each strength day (use the coach's chosen days, not a default schedule), from the sessions in their TrainingPeaks library; the preview lists them. Every week, or the `weeks` they names, gets them, so each week publishes six plans. `days: []` removes strength.
   - If an edit answers that the week changed, preview it again. If it answers that a publish stopped partway, finish that publish first (step 6).
6. **Publish.** Call `publish_master` with the quarter's `planId` to preview.
   - Show the coach the count, two or three of the TrainingPeaks names (like "Foundation Q4 (Int) - Week 3 - (Strength)"), and any errors.
   - "No intervals yet" means step 2 isn't done for those rides.
   - On their OK, call with `confirm: true`, and repeat while `status` is `publishing`; each call publishes a few plans. Stop on `failed` or `blocked` and read the error to the coach.
   - Calling again resumes at the next plan. Nothing is published twice.
7. **Finish.** Tell the coach how many plans are in their TrainingPeaks library and that coaches can apply them now. They can also open the quarter in CinchOS under Plans and press **Publish to TrainingPeaks** to see the same sheet.

## Rules

- One OK covers the preview it follows. If the coach changes the program, the weeks, the tiers or an edit, preview again.
- A quarter runs Monday to Sunday. Never guess a date the coach didn't give; ask.
- Only quarters change. A program stays as it is in TrainingPeaks, so it's always there as a template.
- Publishing creates plans in the coach's library only. It never applies a plan or changes an athlete's calendar. Coaches apply them with the apply-week skill, or send a week at an athlete's own PRs with athlete-week.
- Make changes before publishing. A week edited after it is published shows as `changed` and stays in TrainingPeaks as published; weeks sent with athlete-week always use the latest version.
- Importing intervals puts temporary plans on the import athlete's calendar a year out and removes each one. Say so when asking for the OK.
- The original TrainingPeaks plans are never changed or deleted.
- Report failures as they are, with the dates or plan named in the error. Don't retry a `failed` import yourself.
