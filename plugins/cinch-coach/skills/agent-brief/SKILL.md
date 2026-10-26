---
name: agent-brief
description: Save a named coaching assistant's working context so the same agent or a successor can continue in another chat. Use for checkpoints, handoffs, context-window resets, switching accounts or computers, and final briefs. Preserve decisions, evidence, unfinished work, and a concrete next action in a portable text file.
---

# Save an agent brief

Write the minimum context a fresh assistant needs to continue correctly. A brief is a working handoff, not a transcript or a claim of automatic memory. The workflow uses text and local files only.

## File convention

- Use the coach's established work folder and any existing agent-brief location. Otherwise save one file at `<work folder>/Agents/<agent-slug>.md`, for example `Agents/alex.md`. Derive a simple lowercase, hyphenated filename from the agent's name; do not treat a supplied name as a path.
- Keep this state outside the installed plugin/cache and the shared marketplace repository. An explicit existing brief path takes precedence unless it is inside those locations; explain the issue and use the coach's work folder instead.
- Read an existing brief completely before updating it. Update its working sections while preserving unrelated notes, still-relevant decisions, and open work. Refresh the brief instead of appending a new transcript after every session.
- Use actual paths and links for artifacts. If the coach changes machines or accounts, provide the brief and its necessary supporting files for them to transfer; note which paths will need remapping and which accounts still need sign-in. A copied brief does not transfer access.
- When file access is unavailable, provide the complete brief as an attachment or copyable Markdown, clearly marked as not saved to the coach's local folder.

## Choose the handoff mode

Infer the mode from the request; default to `checkpoint`.

| Mode | Meaning |
|---|---|
| checkpoint | Save progress and continue the current assignment. Do not retire the agent. |
| handback | Prepare for another chat or a named successor. Record the intended recipient and who is expected to act next. |
| final | Record the agent's closing state. Leave unfinished tasks explicitly open; use offboard-agent when the coach asks to retire the agent. |

Use a checkpoint at a useful task boundary or when requested. Do not end an active assignment just because a brief was saved. A handback prepares context; it does not send messages, start another agent, or close the current chat.

## Write the brief

Resolve the agent's name and assignment from the session or existing brief. If still unknown, ask rather than inventing an identity. Prefer a few hundred words, expanding only for decisions and evidence needed to resume. Omit empty optional sections.

Use this shape, adapted to the work:

```markdown
# Agent: [name]

Updated: [actual date and known time zone]
Agent status: [active / paused / retired]
Brief mode: [checkpoint / handback / final]
Coach and role: [known identity and responsibility]
Work folder: [actual path]
Next owner: [same agent / named successor / unassigned]

## Assignment and boundaries
[What the coach requested; relevant limits and durable preferences.]

## Current state
- Verified complete: [outcome and evidence link/path, with date if relevant]
- Open: [remaining work and any blocker]
- Unverified: [prior or reconstructed claims that still need checking]

## Decisions to preserve
[Settled choices, corrections, and rejected attempts that prevent rework.]

## Pending actions and permissions
[Any unsent draft or unapplied change; its exact artifact; what the coach
approved and when, or what remains unapproved. Record an uncertain external
result so the next agent checks it before retrying.]

## Continue here
1. [The first concrete action, with its input and expected result.]
2. [Any essential following step.]

## Sources and files
[Only the links, file paths, and identifiers needed to continue.]

## Restart prompt
[A short instruction naming this agent, this brief's actual path, and the
next task. Mention missing supporting files or access if applicable.]
```

Keep agent status separate from task status: an active agent may finish a task, and a retired agent may leave work unfinished. Preserve the existing status unless the current request changes it; a context checkpoint is not a request to pause or retire. For a previously unnamed status, use `active` for the current working agent.

Record evidence at the stage actually observed: a draft is not sent, an uploaded skill is not a verified installation, and a plan is not an applied workout. Retain the coach's explicit approval and its exact scope; do not turn an old “yes” into permission for changed text, recipients, or actions. Resolve uncertain external results before repeating a send or write.

These briefs describe the work, not the athletes. Keep credentials, tokens, raw email/transcript contents, athlete names, health information, and power data out by default. Refer to authorized source records instead; include personal details only when the coach explicitly requests them in this file. Never copy credentials into a brief.

## Verify and hand back

Respect the coach's existing file-write preferences and session authorization. If the file changed since it was read, reconcile the new content before saving rather than overwriting another agent's work. Read the saved result back, confirm the path, and check that its next action and supporting references are usable. Mark missing or inaccessible references explicitly.

Return a short status and the restart prompt. Claim local persistence only after a successful write and read-back. For an outgoing handoff, report what is ready, what remains open, and who is expected to continue; do not claim that a successor has received or accepted it without evidence.
