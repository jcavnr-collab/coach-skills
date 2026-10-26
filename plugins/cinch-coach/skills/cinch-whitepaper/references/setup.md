# First-use setup

The renderer works locally on macOS, Windows, or Linux with Python 3.10+ through [uv](https://docs.astral.sh/uv/getting-started/installation/) and Chromium through Playwright. Internet access is needed for the initial dependencies and browser download. Rendering itself uses bundled fonts and local images without network requests.

1. Check `uv --version`. If it is missing, use uv's official installation instructions for the coach's operating system.
2. Install the matching browser:

   ```bash
   uv run --with playwright==1.60.0 python -m playwright install chromium
   ```

   On Linux, Playwright may report missing system libraries. Follow its [browser dependency instructions](https://playwright.dev/python/docs/browsers#install-system-dependencies); explain any administrator-level install before making it. On macOS, the renderer can use the standard Google Chrome application if the managed browser is absent. `--browser /absolute/path/to/browser` selects a local Chromium executable explicitly.

3. Resolve `SKILL_DIR` to this skill's installed directory and render the sample to the coach's work folder:

   ```bash
   uv run --script "$SKILL_DIR/scripts/render.py" "$SKILL_DIR/assets/sample.md" \
     --output "/absolute/work/cinch-sample.pdf" \
     --subtitle "A fictional example of a clear coaching handoff" \
     --byline "Cinch Cycling" --date "Sample edition"
   ```

4. Open the PDF and **every** PNG in `cinch-sample.pages/`. These are rasterizations of the actual PDF pages, not screenshots of a separate layout.

`--html-only` builds the self-contained HTML without a browser. It is a useful fallback, but is not proof of a finished PDF. Missing images, unsupported external image URLs, or missing font files fail with a named error. Keep images in the Markdown source folder or its subfolders. Supported Markdown includes headings, emphasis, lists, blockquotes, fenced code, links, images, and tables; raw HTML is displayed as text.

Outputs replace earlier files with the same output name; choose a new name to retain an earlier edition. The renderer refuses to overwrite the Markdown input. Dependencies are pinned in the script; downloaded packages and browser binaries retain their upstream licenses.
