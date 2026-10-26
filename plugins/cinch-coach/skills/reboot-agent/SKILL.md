---
name: reboot-agent
description: Move a named coaching assistant into a fresh chat while keeping its identity and assignment. Use when the coach says "reboot Alex", "refresh this agent", or wants to reset a long or confused session. Save and verify the handoff first, then resume from it and check the new chat's understanding. This does not retire the agent.
---

# Reboot an agent

Carry the same agent into a fresh chat with its working context intact. Use text and local files only. A reboot is requested by the coach; do not force one just because a session is long or has compacted.

This skill has two phases: **prepare** in the old chat and **resume** in the new one. Default to prepare. An explicit `resume` request runs the second phase, so the fresh chat does not create another restart loop.

## Prepare the restart

1. Resolve the name, assignment, and work folder from the current chat or saved brief. Use the file convention in [agent-brief](../agent-brief/SKILL.md). If the target is a different chat, distinguish its saved context from activity you cannot see; do not claim to have contacted or stopped that agent.
2. Save a checkpoint with agent-brief. Preserve the same identity, assignment, decisions, open work, and exact next action. Include pending external actions and any known ongoing job, with its observed state and owner. If debugging is in progress, capture the failure, evidence, attempted fixes, and next diagnostic step. Mark unknowns rather than treating a job or send as finished.
3. Read the saved brief back. Check that a fresh agent can identify its responsibility, locate the necessary files, and take one concrete next step. Repair gaps from available evidence before proposing the restart. If the old chat is unavailable, use [onboard-agent](../onboard-agent/SKILL.md)'s reconstruction path and label the recovered context and remaining gaps.
4. Put a restart prompt in the brief and give the coach the same prompt with the actual name and full path, for example:

   ```text
   /cinch-coach:reboot-agent resume Alex from /actual/work/folder/Agents/alex.md
   ```

5. Tell the coach to open a fresh Claude Code chat in the same work folder and paste that prompt. Keep the old chat available until the new chat's read-back is correct. Report **restart prepared**, not **reboot completed**: saving a checkpoint has not reset any session.

If a local write or verification fails, preserve the old chat and explain what is missing. When local files are unavailable, provide the brief as an attachment or copyable text for the coach to save and supply to the new chat; do not claim local persistence. Do not clear or delete a conversation, terminate a process, or invoke a session-control tool as part of this portable workflow.

## Resume in the fresh chat

1. Read the entire supplied brief and applicable local instructions. If the file or required supporting context is inaccessible, say exactly what is missing. Do not reconstruct a confident history from the restart prompt alone.
2. Use onboard-agent's returning-agent path to retain the same identity and resume the assignment. Check only current facts needed for the next action; record unavailable checks as unverified. In particular, reconcile an uncertain send or save before repeating it, and verify required connections rather than assuming sign-in transferred.
3. Give a concise read-back: **who I am, what I own, the current state, and my next action**. If the sources conflict, resolve the material gap before dependent work. A clear assignment needs no new approval just because the chat changed.
4. Update and read back the brief with the resumed state, preserving open work and the agent's identity. Report that the fresh chat has resumed only when the context is loaded and the read-back is grounded. Then continue the already authorized assignment. If persistence is unavailable, state that limitation separately.

The agent remains active across this handoff. Offboard-agent is for retirement; reboot-agent preserves the agent. No voice setup, account revocation, plugin changes, global roster, or developer-specific session IDs are required.
