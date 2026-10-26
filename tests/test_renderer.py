"""Local input and output safety checks; no services or browsers required."""
import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "plugins/cinch-coach/skills/excalidraw-process-flow-diagram"
SPEC = importlib.util.spec_from_file_location("renderer", SKILL / "scripts/render.py")
renderer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(renderer)


class RendererSafety(unittest.TestCase):
    def setUp(self):
        self.scene = json.loads((SKILL / "assets/sample-process.excalidraw").read_text())

    def test_complete_sample_has_resolvable_bindings(self):
        ids = renderer.check_scene(self.scene)
        self.assertTrue(any(e.get("startBinding") for e in ids.values()))

    def test_duplicate_ids_are_rejected(self):
        self.scene["elements"].append(copy.deepcopy(self.scene["elements"][0]))
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            renderer.check_scene(self.scene)

    def test_missing_arrow_target_is_rejected(self):
        arrow = next(e for e in self.scene["elements"] if e.get("startBinding"))
        arrow["startBinding"]["elementId"] = "absent-node"
        with self.assertRaisesRegex(ValueError, "missing referenced"):
            renderer.check_scene(self.scene)

    def test_nonfinite_geometry_is_rejected(self):
        self.scene["elements"][0]["x"] = float("nan")
        with self.assertRaisesRegex(ValueError, "invalid x"):
            renderer.check_scene(self.scene)

    def test_preparation_allows_missing_text_dimensions(self):
        text = next(e for e in self.scene["elements"] if e["type"] == "text")
        del text["width"]
        with self.assertRaises(ValueError):
            renderer.check_scene(self.scene)
        renderer.check_scene(self.scene, repair=True)

    def test_outputs_cannot_overwrite_source(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "scene.excalidraw"
            with self.assertRaisesRegex(ValueError, "overwrite"):
                renderer.output_paths(source, source.with_suffix(".png"), source)

    def test_non_png_preview_is_rejected(self):
        with self.assertRaisesRegex(ValueError, ".png"):
            renderer.output_paths(Path("scene.excalidraw"), Path("scene.svg"))


if __name__ == "__main__":
    unittest.main()
