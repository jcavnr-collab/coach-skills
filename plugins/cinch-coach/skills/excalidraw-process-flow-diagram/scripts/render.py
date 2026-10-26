#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["playwright==1.60.0"]
# ///
# SPDX-License-Identifier: MIT
"""Export a local Excalidraw scene through the official browser API."""
import argparse
import hashlib
import json
import math
import struct
from pathlib import Path


def check_scene(scene, repair=False):
    if not isinstance(scene, dict) or scene.get("type") != "excalidraw":
        raise ValueError("Input must be an Excalidraw document.")
    items = scene.get("elements")
    if not isinstance(items, list) or not items:
        raise ValueError("Input must contain elements.")
    by_id = {}
    for item in items:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str) or not item["id"]:
            raise ValueError("Every element needs a nonempty string id.")
        if item["id"] in by_id:
            raise ValueError("Duplicate element id: " + item["id"])
        by_id[item["id"]] = item
        keys = ["x", "y"]
        if not repair or item.get("type") != "text":
            keys += ["width", "height"]
        for key in keys:
            value = item.get(key)
            if type(value) not in (int, float) or not math.isfinite(value):
                raise ValueError(item["id"] + ": invalid " + key)
            if key in ("width", "height") and value < 0:
                raise ValueError(item["id"] + ": negative " + key)
        if item.get("type") == "text":
            if not isinstance(item.get("text"), str):
                raise ValueError(item["id"] + ": text must be a string.")
            if not repair:
                for key in ("originalText", "fontSize", "fontFamily", "lineHeight"):
                    if key not in item:
                        raise ValueError(item["id"] + ": missing " + key + "; use --prepare.")
    for item in items:
        references = [item.get("containerId"), item.get("frameId")]
        for side in ("startBinding", "endBinding"):
            binding = item.get(side)
            if binding:
                references.append(binding.get("elementId"))
        references += [bound.get("id") for bound in item.get("boundElements") or []]
        for target in references:
            if target is not None and target not in by_id:
                raise ValueError(item["id"] + ": missing referenced element " + str(target))
    return by_id


def output_paths(source, preview, prepared=None):
    if preview.suffix.lower() != ".png":
        raise ValueError("The preview path must end in .png.")
    if prepared and prepared.suffix.lower() != ".excalidraw":
        raise ValueError("The prepared path must end in .excalidraw.")
    paths = [preview, preview.with_suffix(".svg"), preview.with_suffix(".validation.json")]
    if prepared:
        paths.append(prepared)
    resolved = [path.resolve() for path in paths]
    if source.resolve() in resolved or len(set(resolved)) != len(resolved):
        raise ValueError("Output paths must be distinct and must not overwrite the source.")
    return paths


def export_scene(scene, max_width, scale, repair):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as runtime:
        try:
            browser = runtime.chromium.launch()
        except Exception as error:
            fallback = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
            if "Executable doesn't exist" not in str(error) or not fallback.is_file():
                raise
            browser = runtime.chromium.launch(executable_path=str(fallback))
        try:
            page = browser.new_page(
                viewport={"width": max_width, "height": 900},
                device_scale_factor=scale,
            )
            page.goto(Path(__file__).with_name("render_template.html").resolve().as_uri())
            page.wait_for_function(
                "window.coachReady || window.coachLoadError", timeout=45000
            )
            failure = page.evaluate("window.coachLoadError")
            if failure:
                raise RuntimeError("Excalidraw module could not load: " + failure)
            result = page.evaluate(
                "options => window.exportCoachScene(options)",
                {"scene": scene, "repair": repair, "maxWidth": max_width},
            )
            checked = check_scene(result["scene"])
            if set(checked) != {item["id"] for item in scene["elements"]}:
                raise ValueError("Native restoration changed the element inventory; review the source.")
            png = page.locator("#preview svg").screenshot(timeout=30000)
            return result, png
        finally:
            browser.close()


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("input", type=Path)
    cli.add_argument("-o", "--output", type=Path)
    cli.add_argument("--prepare", type=Path, help="Save native geometry restoration separately.")
    cli.add_argument("--max-width", type=int, default=2400)
    cli.add_argument("--scale", type=float, default=1)
    args = cli.parse_args()
    if not 320 <= args.max_width <= 10000 or not 0.25 <= args.scale <= 4:
        cli.error("Use a max width of 320–10000 and scale of 0.25–4.")
    preview = args.output or (args.prepare or args.input).with_suffix(".png")
    try:
        outputs = output_paths(args.input, preview, args.prepare)
        scene = json.loads(args.input.read_text(encoding="utf-8"))
        check_scene(scene, repair=bool(args.prepare))
        exported, png = export_scene(scene, args.max_width, args.scale, bool(args.prepare))
        width, height = struct.unpack(">II", png[16:24])
        report = {
            "source": str(args.input.resolve()),
            "source_sha256": hashlib.sha256(args.input.read_bytes()).hexdigest(),
            "elements": len(exported["scene"]["elements"]),
            "native_render": "passed",
            "structure": "passed",
            "geometry_prepared": bool(args.prepare),
            "dimensions": {"width": width, "height": height},
            "visual_review": "not_performed",
            "browser_import": "not_performed",
        }
        for path in outputs:
            path.parent.mkdir(parents=True, exist_ok=True)
        preview.write_bytes(png)
        preview.with_suffix(".svg").write_text(exported["svg"], encoding="utf-8")
        if args.prepare:
            args.prepare.write_text(json.dumps(exported["scene"], indent=2) + "\n", encoding="utf-8")
            report["prepared_source"] = str(args.prepare.resolve())
            report["prepared_sha256"] = hashlib.sha256(args.prepare.read_bytes()).hexdigest()
        preview.with_suffix(".validation.json").write_text(
            json.dumps(report, indent=2) + "\n", encoding="utf-8"
        )
        print(json.dumps(report, indent=2))
    except (ValueError, OSError) as error:
        cli.exit(1, str(error) + "\n")


if __name__ == "__main__":
    main()
