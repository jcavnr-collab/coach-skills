#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["markdown-it-py==4.2.0", "playwright==1.60.0", "pypdfium2==5.14.0", "pillow==13.0.0"]
# ///
# SPDX-License-Identifier: MIT
"""Render local Markdown as a Cinch HTML, Letter PDF, and actual PDF page previews."""
import argparse
import base64
import hashlib
import html
import json
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
CSS = """:root{--ink:#15181C;--blue:#1E3A52;--muted:#41464D;--amber:#D89A3D;--teal:#2E9EA1;--line:#C2C7CD;}
*{box-sizing:border-box}html{background:#F7F5F0}body{margin:0;color:var(--ink);font:11pt/1.55 'Open Sans',sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact}
main{max-width:8.5in;margin:24px auto;padding:.62in .68in;background:white}
.brand{display:flex;align-items:center;justify-content:space-between;gap:20px;border-bottom:1px solid var(--line);padding-bottom:16px;margin-bottom:30px}
.brand-name{font:700 15pt 'Epilogue',sans-serif;letter-spacing:.04em;color:var(--blue)}.brand-name:before{content:'';display:inline-block;width:26px;height:4px;background:var(--amber);vertical-align:middle;margin-right:12px}
.edition{font-size:9pt;color:var(--muted);text-align:right}.cover{margin-bottom:25px}h1,h2,h3,h4{font-family:'Epilogue',sans-serif;color:var(--blue);font-weight:600;line-height:1.25;break-after:avoid}
h1{font-size:31pt;letter-spacing:-.045em;margin:0 0 15px}h2{font-size:18pt;letter-spacing:-.025em;border-top:1px solid var(--line);padding-top:18px;margin:29px 0 13px}h3{font-size:13pt;margin:22px 0 10px}h4{font-size:11pt}
.subtitle{font-size:14pt;line-height:1.45;color:var(--muted);margin:0 0 13px}.byline{font-size:9pt;color:var(--muted);margin:0}
p{margin:0 0 12px;orphans:3;widows:3}a{color:var(--blue);text-decoration:underline;text-underline-offset:2px;overflow-wrap:anywhere}
ul,ol{padding-left:24px;margin:9px 0 15px}li{padding-left:3px;margin:6px 0;orphans:2;widows:2}li::marker{color:var(--blue);font-weight:600}
strong{font-weight:650}blockquote{border-left:3px solid var(--teal);padding:5px 0 5px 16px;margin:20px 0;break-inside:avoid}blockquote p:last-child{margin-bottom:0}
table{border-collapse:collapse;width:100%;table-layout:fixed;font-size:9.5pt;margin:16px 0 21px;break-inside:avoid}thead{display:table-header-group}th{text-align:left;color:var(--blue);font-weight:650;border-bottom:1px solid var(--ink)}td,th{padding:9px 12px 9px 0;vertical-align:top;overflow-wrap:anywhere}td{border-bottom:1px solid var(--line)}tr{break-inside:avoid}
code{font:9.2pt/1.5 ui-monospace,SFMono-Regular,Consolas,monospace;overflow-wrap:anywhere}pre{border:1px solid var(--line);border-left:3px solid var(--amber);padding:14px 16px;margin:17px 0;white-space:pre-wrap;overflow-wrap:anywhere}pre code{white-space:pre-wrap}
img{display:block;max-width:100%;width:auto;height:auto;max-height:5.2in;object-fit:contain;margin:auto}figure{margin:22px 0;break-inside:avoid}figcaption{font-size:9pt;line-height:1.4;color:var(--muted);margin-top:10px}
hr{border:0;border-top:1px solid var(--line);margin:24px 0}.pagebreak{break-before:page}.cta{margin:26px 0;break-inside:avoid}.cta a{display:inline-block;background:var(--blue);color:white;padding:11px 18px;text-decoration:none;font-weight:600}.contact{margin-top:28px;border-top:1px solid var(--line);padding-top:16px;font-size:9.5pt;break-inside:avoid}
@page{size:Letter;margin:.58in .68in .65in}
@media print{html,body{background:white}main{margin:0;padding:0;max-width:none}.pagebreak+h2{margin-top:0}.brand{margin-bottom:27px}}
@media screen and (max-width:640px){main{padding:25px 20px;margin:0}h1{font-size:26pt}.brand{gap:12px}.brand-name{font-size:12pt}.edition{font-size:8pt}table{font-size:9pt}td,th{padding-right:7px}pre{padding:12px}}
"""


def data_uri(path, mime):
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def image_uri(source_dir, reference):
    parsed = urlsplit(reference)
    if parsed.scheme or parsed.netloc or parsed.query or parsed.fragment:
        raise ValueError("Use a local image within the Markdown folder: " + reference)
    path = (source_dir / unquote(parsed.path)).resolve()
    if not path.is_relative_to(source_dir.resolve()):
        raise ValueError("Image is outside the Markdown folder: " + reference)
    mime = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}.get(path.suffix.lower())
    if not mime or not path.is_file():
        raise ValueError("Missing or unsupported image (use PNG, JPEG, WebP): " + reference)
    from PIL import Image
    with Image.open(path) as picture:
        picture.verify()
    return data_uri(path, mime)


def build_html(source, args):
    from markdown_it import MarkdownIt
    parser = MarkdownIt("commonmark", {"html": False}).enable("table")
    text = source.read_text(encoding="utf-8")
    tokens = parser.parse(text)
    if not tokens or tokens[0].type != "heading_open" or tokens[0].tag != "h1":
        raise ValueError("Start the Markdown with one # Title.")
    if sum(t.type == "heading_open" and t.tag == "h1" for t in tokens) != 1:
        raise ValueError("Use one # Title and ## sections below it.")
    title = tokens[1].content
    title_lines = tokens[0].map
    body_source = "\n".join(text.splitlines()[title_lines[1]:])

    def figure_token(items, index):
        token = items[index]
        return token.type == "inline" and len(token.children or []) == 1 and token.children[0].type == "image"

    def image_rule(items, index, options, env):
        token = items[index]
        uri = image_uri(source.parent, token.attrGet("src"))
        return '<img src="' + uri + '" alt="' + html.escape(token.content, quote=True) + '">'

    def paragraph_open(items, index, options, env):
        return "<figure>" if figure_token(items, index + 1) else "<p>"

    def paragraph_close(items, index, options, env):
        if figure_token(items, index - 1):
            caption = html.escape(items[index - 1].children[0].content)
            return "<figcaption>" + caption + "</figcaption></figure>\n"
        return "</p>\n"

    parser.renderer.rules.update(image=image_rule, paragraph_open=paragraph_open, paragraph_close=paragraph_close)
    code_lines = set()
    for token in parser.parse(body_source):
        if token.type in ("fence", "code_block") and token.map:
            code_lines.update(range(*token.map))
    parts, current = [], []
    for index, line in enumerate(body_source.splitlines()):
        if line.strip() == "<!-- pagebreak -->" and index not in code_lines:
            parts.append("\n".join(current))
            current = []
        else:
            current.append(line)
    parts.append("\n".join(current))
    body = '<div class="pagebreak"></div>'.join(parser.render(part) for part in parts)
    font_css, licenses = [], []
    for family, filename, style in [("Epilogue", "Epilogue.ttf", "normal"), ("Open Sans", "OpenSans.ttf", "normal"), ("Open Sans", "OpenSans-Italic.ttf", "italic")]:
        font = ROOT / "assets" / "fonts" / filename
        font_css.append("@font-face{font-family:'" + family + "';font-style:" + style + ";font-weight:100 900;font-display:block;src:url('" + data_uri(font, "font/ttf") + "') format('truetype')}")
    for filename in ("Epilogue-OFL.txt", "OpenSans-OFL.txt"):
        licenses.append(html.escape((ROOT / "assets" / "fonts" / filename).read_text(encoding="utf-8")))
    esc = lambda value: html.escape(value or "", quote=True)
    subtitle = '<p class="subtitle">' + esc(args.subtitle) + "</p>" if args.subtitle else ""
    byline = '<p class="byline">' + esc(args.byline) + "</p>" if args.byline else ""
    cta = '<div class="cta"><a href="' + esc(args.cta_url) + '">' + esc(args.cta_label) + "</a></div>" if args.cta_url else ""
    contact = '<div class="contact">' + esc(args.contact) + "</div>" if args.contact else ""
    result = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src data:; font-src data:; style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'">
<title>{esc(title)} | Cinch Cycling</title><style>{''.join(font_css)}{CSS}</style></head>
<body><main><header class="brand"><div class="brand-name">Cinch Cycling</div><div class="edition">{esc(args.eyebrow)}<br>{esc(args.date)}</div></header>
<div class="cover"><h1>{esc(title)}</h1>{subtitle}{byline}</div>{body}{cta}{contact}</main>
<template id="font-license-notices">{'<hr>'.join(licenses)}</template></body></html>'''
    return result, title


def render_pdf(document, destination, browser_path=None):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as runtime:
        launch = {"executable_path": str(browser_path)} if browser_path else {}
        try:
            browser = runtime.chromium.launch(**launch)
        except Exception as error:
            fallback = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
            if browser_path or "Executable doesn't exist" not in str(error) or not fallback.is_file():
                raise RuntimeError("Browser could not start. Follow references/setup.md. " + str(error)) from error
            browser = runtime.chromium.launch(executable_path=str(fallback))
        try:
            page = browser.new_page(viewport={"width": 816, "height": 1056})
            page.route("**/*", lambda route: route.abort())
            page.set_content(document, wait_until="load")
            page.evaluate("async () => {await document.fonts.load('600 16px Epilogue'); await document.fonts.load('400 16px \"Open Sans\"'); await document.fonts.ready;}")
            checks = page.evaluate("""() => ({heading_color:getComputedStyle(document.querySelector('h1')).color, fonts:[...document.fonts].map(f=>({family:f.family,status:f.status})), images:[...document.images].map(i=>({ok:i.complete&&i.naturalWidth>0,width:i.naturalWidth,height:i.naturalHeight})), overflow:document.documentElement.scrollWidth>innerWidth})""")
            required = [f for f in checks["fonts"] if f["status"] == "loaded"]
            if not any("Epilogue" in f["family"] for f in required) or not any("Open Sans" in f["family"] for f in required):
                raise ValueError("The bundled fonts did not load.")
            if checks["heading_color"] != "rgb(30, 58, 82)":
                raise ValueError("The Cinch heading color did not load.")
            if checks["overflow"] or any(not i["ok"] for i in checks["images"]):
                raise ValueError("The document has horizontal overflow or an unloaded image.")
            page.pdf(path=str(destination), format="Letter", print_background=True, prefer_css_page_size=True,
                display_header_footer=True, header_template="<span></span>",
                footer_template='<div style="font:8px sans-serif;color:#41464D;width:100%;text-align:center"><span class="pageNumber"></span> / <span class="totalPages"></span></div>')
            return checks
        finally:
            browser.close()


def preview_pdf(pdf, directory):
    import pypdfium2 as pdfium
    directory.mkdir(parents=True, exist_ok=True)
    pages = []
    with pdfium.PdfDocument(pdf) as document:
        for index in range(len(document)):
            page = document[index]
            bitmap = page.render(scale=1.5)
            image = bitmap.to_pil()
            name = f"page-{index+1:02d}.png"
            image.save(directory / name)
            pages.append({"file": name, "pixels": list(image.size), "points": list(page.get_size())})
            image.close()
            bitmap.close()
            page.close()
    valid_names = {page["file"] for page in pages}
    for stale in directory.glob("page-*.png"):
        if stale.name not in valid_names:
            stale.unlink()
    return pages


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("input", type=Path)
    cli.add_argument("--output", "-o", required=True, type=Path)
    cli.add_argument("--subtitle", default="")
    cli.add_argument("--byline", default="")
    cli.add_argument("--date", default="")
    cli.add_argument("--eyebrow", default="Coaching guide")
    cli.add_argument("--contact", default="")
    cli.add_argument("--cta-label", default="")
    cli.add_argument("--cta-url", default="")
    cli.add_argument("--browser", type=Path)
    cli.add_argument("--html-only", action="store_true")
    args = cli.parse_args()
    try:
        source, output = args.input.resolve(), args.output.resolve()
        if output.suffix.lower() != ".pdf":
            raise ValueError("Output must end in .pdf.")
        if source in (output, output.with_suffix(".html"), output.with_suffix(".validation.json")):
            raise ValueError("Output must not overwrite the input.")
        if bool(args.cta_label) != bool(args.cta_url):
            raise ValueError("Supply both --cta-label and --cta-url, or neither.")
        if args.cta_url:
            parsed = urlsplit(args.cta_url)
            if parsed.scheme not in ("http", "https") or not parsed.netloc:
                raise ValueError("The next-step link must be an HTTP(S) URL.")
        document, title = build_html(source, args)
        output.parent.mkdir(parents=True, exist_ok=True)
        html_output = output.with_suffix(".html")
        html_output.write_text(document, encoding="utf-8")
        report = {"title": title, "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(), "html": html_output.name, "pdf_render": "not_performed", "visual_review": "not_performed"}
        if not args.html_only:
            report["browser_checks"] = render_pdf(document, output, args.browser)
            report["pages"] = preview_pdf(output, output.with_suffix(".pages"))
            report.update(pdf=output.name, pdf_render="passed", page_count=len(report["pages"]))
        output.with_suffix(".validation.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"html": str(html_output), "pdf": str(output) if not args.html_only else None, "page_count": report.get("page_count")}, indent=2))
    except (ValueError, OSError, RuntimeError) as error:
        cli.exit(1, str(error) + "\n")


if __name__ == "__main__":
    main()
