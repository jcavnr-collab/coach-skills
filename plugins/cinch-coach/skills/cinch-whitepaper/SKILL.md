---
name: cinch-whitepaper
description: Create a Cinch Cycling branded white paper, coaching how-to guide, or multi-page brief from notes or Markdown, with an editable source, self-contained HTML, PDF, and page previews.
---

# Cinch white paper

Make a useful document in Cinch's colors and type. This is a local document workflow; it needs no CinchOS, ElevenLabs, or paid design account. Save the coach's work outside the plugin folder.

## Write the paper

Use the user's source and intended audience. If these are missing and affect the result, ask while drafting what is already clear. Keep supplied facts, names, and approved copy intact. Label illustrative numbers and fictional examples. Confirm coaching claims against the supplied material; do not invent athlete results, testimonials, or promises.

Write one Markdown file with a single leading `# Title`, then sections, short paragraphs, useful examples, and sources where needed. Tables should compare a small number of short columns. Use a diagram or photo when it explains something; imagery is optional. Use local PNG, JPEG, or WebP images within the source folder, with descriptive alt text. Export diagram SVGs to PNG first. A standalone `<!-- pagebreak -->` starts a new page when pagination needs help.

Use an existing approval of the copy or direction. Drafting, rendering, and fixing local layout can proceed within the request. Sending, publishing, or adding private athlete information to a shared repository requires the user's authorization for that action and audience.

## Render in Cinch's brand

Read [brand.md](references/brand.md) for the palette, font roles, and document layout. Use the bundled renderer instead of recreating the styles. It embeds the bundled Epilogue and Open Sans fonts, local images, and font license notices. It does not fetch document images or run raw HTML from the Markdown.

On first use, follow [setup.md](references/setup.md). Resolve `SKILL_DIR` to this installed skill's actual folder; it is not the coach's work folder.

```bash
uv run --script "$SKILL_DIR/scripts/render.py" "/absolute/work/paper.md" \
  --output "/absolute/work/Cinch paper.pdf" \
  --subtitle "A practical guide for athletes and coaches" \
  --byline "Cinch Cycling" --date "October 2026"
```

The renderer writes a PDF, a self-contained `.html`, a `.pages/` folder with every PDF page as PNG, and a `.validation.json`. Add a coach-supplied `--contact` if needed. A next-step link is optional: use both `--cta-label` and `--cta-url`. No personal contact, QR code, booking link, or signature is assumed.

## Inspect and hand over

Open **every** page PNG. Check readable Epilogue headings and Open Sans body text; unclipped tables, commands, links, and images; useful page breaks; correct contact and sources; and no near-empty last page. Check the HTML on a narrow viewport if it will be shared for screen reading. Fix the Markdown or scoped renderer styling and render again when needed.

The validation JSON reports render checks, not editorial or visual approval. Record which pages you actually inspected in the delivery note. Keep the Markdown, original images, HTML, PDF, and previews together. Return the PDF and editable source paths. Upload or email through the user's authorized tools only when requested; this skill has no account-specific Drive, Notion, or email dependency.

Try the included [fictional sample](assets/sample.md) to verify first-use setup. It is a layout example, not a training prescription.
