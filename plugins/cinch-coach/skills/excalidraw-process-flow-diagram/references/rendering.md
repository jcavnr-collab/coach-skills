# Native renderer

The public renderer uses the official Excalidraw 0.18.0 exportToSvg API and Playwright 1.60.0. It loads the module and fonts over the network, then creates previews in a local browser.

## Inputs and outputs

Provide a standard .excalidraw document with an elements array. Give each element a unique ID and numeric coordinates and dimensions. Text needs text, originalText, fontSize, fontFamily and lineHeight. All arrow, container and reverse-binding references must name existing elements.

~~~bash
uv run --script "<skill-dir>/scripts/render.py" "process.excalidraw" --output "process.png"
~~~

Outputs are process.png, process.svg and process.validation.json. SVG keeps its native dimensions. PNG is scaled proportionally to --max-width (default 2400); --scale controls pixel density (default 1).

## Repairing text geometry

For incomplete text geometry, use a separate prepared source:

~~~bash
uv run --script "<skill-dir>/scripts/render.py" "draft.excalidraw" --prepare "prepared.excalidraw" --output "prepared.png"
~~~

This uses Excalidraw's restoreElements API with text measurement and binding repair. It does not design a layout or reroute the process. The input is preserved. Inspect the prepared file and its render before replacing an earlier revision.

The report records source hashes, output pixel dimensions and whether native export passed. Visual inspection and editor import begin as not_performed; they are separate human or agent observations, not inferred from a successful export.

## Failure recovery

For a missing browser, follow setup.md. For module/font loading failures, verify network access and report the actual error. For invalid IDs, references or dimensions, repair the source; do not hide a missing branch by deleting it. Preserve existing files when a render fails.

API references: [export](https://docs.excalidraw.com/docs/@excalidraw/excalidraw/api/utils/export), [restore](https://docs.excalidraw.com/docs/@excalidraw/excalidraw/api/utils/restore).
