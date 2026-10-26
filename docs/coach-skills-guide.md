# Coach Skills: a practical guide
### What each skill does and how to use it in your coaching work
*Rincon AI · Coaching guide for cinch-coach 0.9.0 · October 26, 2026*

## Start here

This guide explains 22 skills with a purpose and example for each. Begin by giving your coaching assistant a permanent work folder.

1. **Download Claude Desktop.** Get it from [claude.com/download](https://claude.com/download), install it and sign in with your own Claude account. Your plan or organization must include Claude Code access.
2. **Create a blank folder.** In Documents, make a folder called `Coaching Workspace`. This will hold your skills download, saved instructions, agent memory and work.
3. **Start a local session.** Open Claude Desktop's **Code** tab. Choose **Local**, then **Open folder** and select `Coaching Workspace`. Keep Worktree off if shown.

### Ask your agent to set it up

Paste this into the session. Desktop includes the Code agent; it can install the separate command-line tool (CLI) for you if needed.

```text
Set up this folder as my coaching workspace.
Download the complete repository into coach-skills/:
https://github.com/jcavnr-collab/coach-skills
Read coach-skills/docs/agent-setup.md and follow it.
Install the Claude Code CLI if needed, install the skills,
and prepare local memory and agent handoff files.
Keep existing files. Tell me when to open a new session.
```

Follow any installation or folder-access prompts. When setup finishes, choose **New session**, select **Local** and open the **same Coaching Workspace folder**. Continue with the steps on the next page.

## Your coaching workspace

The agent downloads the full repository into a `coach-skills` subfolder. Your personal working files live beside it, so updating the skills preserves your saved context.

| Location in Coaching Workspace | What it holds |
|---|---|
| `coach-skills/` | The complete public skills repository and guide |
| `CLAUDE.md` | Your working instructions and which memory files to read |
| `MEMORY.md` | Saved preferences and decisions you want carried forward |
| `Agents/` | Named assistants' briefs, current work and handoffs |

These are files you can read and back up. Claude also maintains its own automatic memory separately. A fresh chat resumes from the files it reads; it does not inherit the previous conversation.

### Finish setup in the new session

Ask: **"Read CLAUDE.md and MEMORY.md, check that Coach Skills is loaded, then help me run coach-setup."** Ask the agent to guide CinchOS sign-in with your own account. In a terminal session, use `/mcp`. Service access comes from your account.

Keep opening `Coaching Workspace` for future sessions. To continue a named assistant, ask it to read its saved brief in `Agents/`. [Detailed setup and troubleshooting](https://github.com/jcavnr-collab/coach-skills/blob/main/docs/agent-setup.md) are available in the repository.

In the examples below, replace bracketed details with your own.

### coach-setup

**Set your working preferences.** Records your coach identity, planning day, time zone and writing style in local instruction files. Use it at the start, or when your preferences change.

```text
/cinch-coach:coach-setup Help me set up my coaching workspace.
```

### cinchos-guide

**Check access and find the right workflow.** Explains which connected tools can help with your job and identifies missing connections or permissions.

```text
/cinch-coach:cinchos-guide Check my connections and show
which coaching workflows I can use.
```

## Plan the training week

These skills use CinchOS. Calendar changes also need the coach's connected TrainingPeaks account. Give an explicit athlete list and check the dates, tier and existing workouts before applying a week.

### sunday-prep

**See who needs attention before planning.** Summarizes open weeks, upcoming races, missed sessions and waiting comments. It reads the current records. Use it on your chosen planning day.

```text
/cinch-coach:sunday-prep Get me ready for my next planning day.
Show the athletes who need attention.
```

### quarter-plan

**Build a quarter of training.** Creates or revises quarter masters using your programs, then publishes the selected tier and strength versions to your TrainingPeaks library. Applying them to athletes is a separate step.

```text
/cinch-coach:quarter-plan Build [quarter] for [date range]
using [program]. Show the first week's tier and strength options.
```

### apply-week

**Use a published library week.** Places the selected week on athletes' calendars using the library's percent-of-FTP targets. It can preview the plan and check existing calendar workouts first.

```text
/cinch-coach:apply-week Preview week [number] of [quarter]
for [athletes], [tier], [strength choice]. Show the dates.
```

### athlete-week

**Set targets using each athlete's current power PRs.** Previews a quarter week with athlete-specific targets, then sends the selected workouts. Check the PR duration, date, percentage and calculated watts. Resolve flagged gaps before sending.

```text
/cinch-coach:athlete-week Preview week [number] of [quarter]
for [athlete], [tier]. Show the PRs used and target watts.
```

### custom-week

**Make an individual exception.** Builds a taper, travel week or other custom week from your coaching instructions. Shows which scheduled workouts it would replace.

```text
/cinch-coach:custom-week Build a travel week for [athlete]
starting [date], using these sessions: [instructions].
```

After applying workouts, ask which calendar entries landed. Check an uncertain result before repeating the action.

## Stay in touch with athletes

Use these skills to prepare replies and keep track of athletes who need contact. Review the recipients and final text when choosing what to send.

### comments-by-prompt

**Reply to coaching comments from short instructions.** Reads the waiting queue, drafts replies in your writing style and supports sending the selected batch through CinchOS.

```text
/cinch-coach:comments-by-prompt Show my waiting comments.
For [athlete], acknowledge the progress and ask about pacing.
```

### roster-check

**Find athletes who have gone quiet.** Shows athletes overdue for coach contact, their latest activity and suggested check-ins. Edit the messages before choosing which ones to post.

```text
/cinch-coach:roster-check Show athletes due for a check-in
and suggest a short message for each.
```

### inbox-triage

**Review your connected inbox.** Groups mail by what needs attention and drafts replies in the conversation. Useful for a daily review of athlete, prospect and business messages.

```text
/cinch-coach:inbox-triage Review the last day of my inbox.
Show what needs me today and draft replies here.
```

### email-drafts

**Review and send email replies.** Works with replies prepared during inbox triage or drafts already in Gmail. Shows the final recipients, subject and message, then reports the send result. It also supports requested archiving.

```text
/cinch-coach:email-drafts Show the replies from this triage.
Make [reply] shorter and show the final messages together.
```

Inbox skills need your authorized `cinchos-inbox` connection and connected mailbox. A reply written in the chat becomes a saved email draft through the email workflow.

## Prepare consults, lessons and articles

### prospect-invite

**Prepare a personal consult invitation.** Uses an existing prospect invite record, your supplied link and the chosen coach's calendar to prepare the message and four appointment options. Sending also notifies the selected coach.

```text
/cinch-coach:prospect-invite Prepare [prospect]'s invitation
using [link]. [Coach] will take the consult. Show the times.
```

### consult-report

**Draft an athlete report.** Creates a Roadmap Report or To The Moon Assessment using the athlete's records and your requested focus. Finalizing saves it to the athlete's timeline and returns a secure link. Delivering that link is a separate action.

```text
/cinch-coach:consult-report Draft a Roadmap Report for
[athlete], focused on [goal event] and [coaching priority].
```

### skill-author

**Create or revise a coaching lesson.** Turns your teaching notes into a lesson draft with steps, common mistakes and mastery checks. It can save a draft through the coaching connection and return its Skills Studio link. Review and publish the lesson in Studio.

```text
/cinch-coach:skill-author Draft a lesson on [topic] using
[notes]. Check the catalog for related lessons first.
```

### playbook-author

**Organize lessons around a goal.** Uses the lesson catalog to propose an ordered playbook, identify gaps and save an assembly outline in your work folder. Assemble and publish the playbook in Skills Studio.

```text
/cinch-coach:playbook-author Plan a [level] playbook for
[goal]. Show the lesson order and gaps to fill.
```

### blog-author

**Write and manage coaching articles.** Drafts or revises articles, helps choose a byline and audience, adds images and checks readiness. Coaches can submit their own drafts. Owners, office managers and super admins can publish after reviewing the exact preview.

```text
/cinch-coach:blog-author Turn [notes] into a Training Tips
article for [audience]. Show the draft before saving it.
```

Lessons need Skills Studio access; articles need blog access through the coaching connection. A **Coach Skill** is an instruction for Claude; a **lesson** teaches an athlete.

## Keep work across sessions

A named assistant has a role and a saved brief that a later chat can read. Keep briefs in your work folder, outside the downloaded plugin. These four skills use local files.

### onboard-agent

**Start or resume a named assistant.** Establishes its assignment, finds an existing brief when available and records the next action. Use `coach-setup` for your personal preferences and this skill for the assistant's role.

```text
/cinch-coach:onboard-agent Alex. Help me prepare the coaching
week. Keep your working brief in this folder.
```

### agent-brief

**Save progress or prepare a handoff.** Records decisions, completed work, open tasks and the next action in a portable text file. Use `checkpoint` during ongoing work or `handback` when passing it to another chat or person.

```text
/cinch-coach:agent-brief checkpoint
```

### reboot-agent

**Continue the same assistant in a fresh chat.** Saves and checks its brief, then gives you a restart prompt. Open a new chat in the work folder and paste that prompt. Check the new chat's read-back before continuing.

```text
/cinch-coach:reboot-agent Alex
```

### offboard-agent

**Retire an assistant with a final handoff.** Preserves completed work and unfinished tasks, and records the next owner. Account access and scheduled jobs are managed separately.

```text
/cinch-coach:offboard-agent Alex. Save the final handoff
and list unfinished work for the next owner.
```

When changing computers, bring the work folder and supporting files, install the plugin, and sign into the needed services. Ask the new chat to read the saved brief before starting.

## Create useful coaching documents

### excalidraw-process-flow-diagram

**Draw a process you can explain.** Maps athlete onboarding, a weekly review or an office handoff, including owners and decisions. Saves an editable Excalidraw file with PNG and SVG previews.

```text
/cinch-coach:excalidraw-process-flow-diagram Map our athlete
onboarding process. Show each owner and the decision points.
```

### cinch-whitepaper

**Turn notes into a Cinch-branded guide.** Creates a coaching paper or how-to document in Cinch's colors and fonts. Saves editable Markdown, self-contained HTML, a PDF and page previews in your work folder.

```text
/cinch-coach:cinch-whitepaper Turn these notes into a coaching
guide. Save the editable source and PDF in my work folder.
```

Both tools run locally. On first use, the assistant checks the renderer and installs the required browser dependencies. Open the finished diagram or PDF and check its labels, page breaks and wording before sharing.

### Keep your setup working

- **A skill is missing:** check Desktop's plugin controls, or `/plugin` in a terminal session. Enable cinch-coach and open a new session.
- **A connection needs sign-in:** ask the agent to guide authentication, using `/mcp` in a terminal session if needed. A permission error needs the appropriate service access.
- **A new chat needs context:** give it the saved brief's path and ask it to read back the assignment.
- **An update is available:** ask your agent to refresh `coach-skills` from GitHub, update the installed plugin and help you reload. Keep personal files in the parent workspace.

For a first session, finish setup, run `sunday-prep`, and preview one athlete's week. Save an `agent-brief` checkpoint before leaving.
