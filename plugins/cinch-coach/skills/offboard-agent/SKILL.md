---
name: offboard-agent
description: Retire a named coaching assistant and leave a durable final handoff with completed work, unfinished tasks, and the next owner. Use when the coach says to offboard, retire, or finish with an agent. For a checkpoint or a move to another chat without retirement, use agent-brief instead.
---

# Offboard an agent

Close the named agent's assignment in text and preserve enough context for a successor. This skill does not require an audio service, account administration, or a connected coaching account.

## Resolve the request

Use the agent name and successor supplied by the coach or established in the current chat. Read the existing brief using the file convention in [agent-brief](../agent-brief/SKILL.md), plus any relevant current task artifacts. Ask only if the identity or intended retirement is ambiguous.

If the coach only wants to move an agent to a fresh chat or save context, use agent-brief in `handback` mode and preserve its identity. Do not retire it as a side effect of a handoff.

If offboarding an agent from another session, report only what authorized files and the coach's directions establish. Do not pretend to have that session's unseen history or control its process. A missing prior brief can be reconstructed from available evidence, with gaps labeled.

## Preserve the final state

Use agent-brief in `final` mode to save a complete handoff before reporting retirement:

- Separate outcomes actually verified from drafts, plans, and uncertain external results.
- Keep every unfinished task, blocker, and pending approval visible. State the first action a successor should take; do not mark the overall task complete just because the agent is retiring.
- Name the successor if supplied; otherwise use `unassigned`. Preparing a handoff does not launch or notify that person or agent.
- Record any ongoing job or scheduled task known to belong to the assignment, with its actual observed state and owner. Do not imply it stopped when this chat ends. If it needs attention, make that an explicit handoff item.
- Preserve useful files and links. Keep personal coaching data out of the brief unless the coach explicitly asked to include it, following agent-brief's data rules.

Save the final brief with agent status `retired` and read it back. This file update is the retirement record; it is not a shutdown of another session or a cancellation of background work. If saving fails, leave retirement unconfirmed, provide the handoff text, and state what could not be persisted.

## Close clearly

Tell the coach where the final brief is, what remains open, and the next owner. Provide a restart prompt using the actual path so the successor can read it. If the coach names a successor, make the prompt clear that it is the predecessor's brief and that the successor should keep their own identity.

Offboarding does not delete files, remove plugins, revoke sign-ins, change billing, stop unrelated processes, or alter other agents' records. Those actions require their own explicit request and applicable workflow. Finish with a concise written handoff; no voice selection, voice release, or spoken sign-off is part of this skill.
