# First use on a coach's computer

Use this skill in Claude Code with local file and terminal access. It needs no paid Excalidraw account, API key, or audio service. A chat-only environment can draft source, but cannot claim the renderer ran without those capabilities.

## Install the renderer prerequisites

1. Check `uv --version`. If uv is missing and Homebrew is already available, install it with `brew install uv`. Otherwise follow the [official uv installation instructions](https://docs.astral.sh/uv/getting-started/installation/). Respect the coach's existing software-install permissions; do not install Homebrew solely to get uv.
2. The bundled script declares Python 3.10 or later and pins Playwright to 1.60.0. `uv run --script` resolves its Python environment and dependencies without a shared virtual environment. See [uv's script guide](https://docs.astral.sh/uv/guides/scripts/).
3. Install the matching browser once if Chromium and the supported Mac Chrome fallback are unavailable:

   ```bash
   uv run --with playwright==1.60.0 python -m playwright install chromium
   ```

   Playwright browser binaries must match its version; see [the browser installation guide](https://playwright.dev/python/docs/browsers).

The first render needs network access for dependencies, the pinned Excalidraw module, and fonts. Keep network access available for later renders too: a fresh browser may fetch module/font resources again. The script renders in a local browser; it does not create a public share link or upload the scene as a shared document.

## Render in the work folder

Resolve the real installed skill folder from the SKILL.md being read. Quote paths containing spaces. Replace the example paths below; do not assume a coach has global developer skill directories.

```bash
uv run --script "/actual/installed/skill/scripts/render.py" "/actual/work/folder/process.excalidraw" --output "/actual/work/folder/process.png"
```

For an incomplete source, use `--prepare` with a different output filename; see [rendering.md](rendering.md). The helper produces a PNG, SVG, and validation report. Open the PNG and inspect the actual labels, branches, and arrows. Its initial report correctly leaves visual review and browser import as `not_performed` until someone observes them.

For the first-use check, render the bundled fictional [sample-process.excalidraw](../assets/sample-process.excalidraw) to the coach's work folder. Its [reference preview](../assets/sample-process.png) shows a decision and labeled branches. Open the editable file in Excalidraw and verify the text and connectors. The example is fictional; keep real coaching documents local unless sharing is requested. No Excalidraw CLI is required to create or render files. Online publishing is optional and requires a separate request.

```bash
uv run --script "/actual/installed/skill/scripts/render.py" "/actual/installed/skill/assets/sample-process.excalidraw" --output "/actual/work/folder/diagram-check.png"
```

## If setup fails

- Missing browser executable: install the matching Chromium binary with the command above and retry once.
- Module or font load timeout: check network access to the module/font hosts, including `esm.sh`; report the actual failure. A package download is not proof that rendering worked.
- Invalid geometry or bindings: repair the source or use a separate prepared file; preserve the original.
- No terminal or image-viewing capability: provide the editable source and state which verification could not run.

Keep personal diagrams and browser caches outside the plugin. Updating the plugin should replace its reusable instructions and code, not the coach's work.
