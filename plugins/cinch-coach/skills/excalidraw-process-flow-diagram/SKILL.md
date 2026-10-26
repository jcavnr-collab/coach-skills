---
name: excalidraw-process-flow-diagram
description: Create editable Excalidraw process diagrams with PNG and SVG previews. Use for coaching operations, athlete onboarding, lesson production, handoffs, decisions and approval flows.
---

# Excalidraw Process Flow Diagram

Map the process the coach actually describes. Save the editable document and previews in their work folder. This skill includes a local renderer; no CinchOS or audio account is needed.

## Establish the process

Read the current brief and any diagram being revised. Identify the trigger, responsible people, decisions, outputs and exceptions. Distinguish observed behavior from proposals. Resolve missing facts that would change the flow; label remaining assumptions rather than inventing integrations or permissions.

For larger systems, use the [process checklist](references/architecture.md). Match the coach's requested style, or use [the default style](references/style.md) and view the fictional sample in assets/sample-process.png.

## Draw

Create standard Excalidraw JSON with descriptive element IDs. The editable sample in assets/sample-process.excalidraw demonstrates shapes, text, bound arrows and a revision loop.

Use shapes to distinguish actions, decisions and outcomes. Route arrows so the intended order is unambiguous. Put approvals before the external action they control. Label both decision branches and return revision paths to the appropriate step. Group by responsibility only where it helps explain a handoff.

Keep real athlete information out of examples unless the coach explicitly needs it in the requested diagram. A diagram of a proposed integration does not prove the account is connected.

## Render and inspect

Read [setup](references/setup.md) on a new computer, and [rendering](references/rendering.md) for command options and source requirements. Resolve the installed skill directory from this file's location.

~~~bash
uv run --script "<skill-dir>/scripts/render.py" "process.excalidraw" --output "process.png"
~~~

The renderer writes PNG, SVG and a report. Inspect the actual PNG at readable size: check every label, arrowhead, branch, boundary and feedback loop. Repair overlaps or clipped text and render again. A successful process exit proves only that rendering ran.

Open the final editable document in Excalidraw and confirm labels and bindings survived import. Keep the document local unless online sharing was requested. Do not create an external share link merely to test installation.

## Deliver

Return the editable source and useful previews. State whether browser import was checked and identify any unverified process assumptions. Preserve earlier versions when revising an existing diagram. Keep outputs outside the plugin cache so updates cannot replace the coach's work.
