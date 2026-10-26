---
name: coach-setup
description: Set a Cinch coach up in Claude on day one. Check the CinchOS connections, interview the coach a few questions at a time, and write their personal CLAUDE.md files so every future session knows who they are, how they work and what never happens without asking. Use when a coach says "set me up", "get Claude ready for me", "interview me", "update my CLAUDE.md", "Claude keeps forgetting how I work", or on their first session.
---

# Coach setup

Every Claude Code session reads two instruction files:

- `~/.claude/CLAUDE.md`, the coach's own file for every session on this Mac;
- `CLAUDE.md` in the folder the session starts in, for that work.

This skill interviews the coach and writes both. Keep it a conversation: a few questions at a time, short, in plain words. It should take 15 to 20 minutes.

Run it again any time to update the files. Read what's there first and change only what the coach changes.

## Step 1: Check the connections

1. Call `list_my_athletes` (cinchos-coaching). If it needs sign-in, help an authorized CinchOS user connect through `/mcp` in Claude Code. If the coach has no CinchOS access, mark service workflows unavailable and continue setting up local agents and diagrams. Never treat unavailable data as an empty roster.
2. Call `list_accounts` (cinchos-inbox) to see which email accounts are connected. Note any that are missing; don't fix them now.
3. Call `get_voice_profile` with `channel: "general"`. If it returns a writing-style profile, use it. If none is available, ask how the coach likes to write. This is text style only; no audio or ElevenLabs setup is needed.

## Step 2: Prefill what CinchOS already knows

So you don't ask what you can look up:

- Count athletes by `coachEmail` from `list_my_athletes`. Work out which addresses are the coach's own: their sign-in, plus the TrainingPeaks coach account. Confirm the addresses with the signed-in coach; do not infer identity from the largest roster or reuse an example address. Store confirmed aliases only in the coach's local work instructions, outside this repository.
- The other coaches and how many athletes each has.
- Their voice profile summary (tone, sign-off), if there is one.

Show this back in one short block and ask: *"Is this right? Anything I'm missing?"*

## Step 3: Interview

Ask in this order, two or three questions per turn. Skip anything already answered. Offer examples so it's easy to answer.

1. **You and the business.** Your role at Cinch. What Cinch sells (programs, coaching levels). Who else works with you (coaches, office manager), and what you hand to them.
2. **Your week.** When you plan training (for example Sunday). When you answer comments and email. Your busiest days. Your time zone.
3. **How you like answers.** Short or detailed? Tables or bullets? How should Claude address you? When should it just do something, and when should it ask?
4. **Never without asking.** Confirm the defaults, and add any others:
   - nothing sends to an athlete, lead or coach without your OK on the exact text;
   - nothing changes in TrainingPeaks without your OK on a preview;
   - no money, refunds or billing changes;
   - health and injury questions come to you;
   - nothing deletes files.
5. **Your files.** Where you keep spreadsheets, documents and race files. Which folder Claude should start in (suggest `Documents/Cinch`). Anything Claude should never open.
6. **Training language.** Words and rules you always use: the ride tiers (Novice, Intermediate, Advanced), the TTM zones (MES, PF1, PF2, PF5, TF8, TF12, TF20, F2F40, F2F60, F2F90, Medium, Low Medium), Level 1 to 6, the usual strength days, quarter naming. Anything Claude tends to get wrong.
7. **Goals for Claude.** The three jobs you most want off your plate.

## Step 4: Draft, show, write

Draft both files and show them in full before writing anything.

**`~/.claude/CLAUDE.md`, the coach's own.** Keep it under about 60 lines:

```markdown
# About me
<name>, <role> at Cinch Cycling. <one line on the business>. Time zone: <tz>.

# How I work
- <weekly rhythm>
- <how I like answers>

# Never without asking me
- <the confirmed list>

# My service identity
- <confirmed sign-in and TrainingPeaks coach addresses; never passwords or tokens>

# People
- <coaches and what each handles, office manager>

# Words I use
- <tiers, zones, levels, naming>
```

**`<work folder>/CLAUDE.md`, the Cinch work folder.** Keep it under about 60 lines:

```markdown
# Cinch work
<Record which of cinchos-coaching and cinchos-inbox were actually verified, or say not connected.> Use the cinchos-guide skill before the first CinchOS call; the coach skills (quarter-plan, apply-week, athlete-week, sunday-prep and the rest) handle whole jobs.

# Always
- Preview first, then send or write only after I say yes to exactly what was shown.
- "My athletes" means athletes coached by <own addresses>. Owners see everyone, but writes only reach my own.
- Quarters run Monday to Sunday.
- Write as me with get_voice_profile.
- Health, power and email contents stay in the conversation, never in files unless I ask.

# Files
- <where spreadsheets, documents and race files live>
- Save new files in <folder>.

# My priorities
- <the three jobs>
```

Rules for the files:

- No athlete names or data, no health data, no passwords, no API keys. These files describe the coach, not the athletes.
- Plain words, short lines, the coach's own phrasing where possible.
- Rules that change with CinchOS (tool names, gates) stay out. They live in the cinchos-guide skill, which updates with the plugin.

Write the files only when the coach says to.

- If a file already exists, show what changes (added, changed, removed) and keep everything else as it is.
- After writing, read both files back and confirm the paths.

## Step 5: Wrap up

Tell the coach:

- which two files were written, and where;
- that every new session reads them, so start a new session to see the effect;
- how to change them later: *"update my CLAUDE.md: ..."*, or run this skill again;
- three things to try next, picked from their goals. For example: *"get me ready for Sunday"*, *"go through my coaching comments"*, *"show me week 1 of this quarter"*.

## Rules

- Ask; don't guess facts about the coach or the business. If the coach skips a question, leave that part out.
- Never write the files without showing the full draft first.
- Keep each file short. A long CLAUDE.md gets ignored. Put detail in the cinchos-guide skill, or in a separate notes file the CLAUDE.md points to.
