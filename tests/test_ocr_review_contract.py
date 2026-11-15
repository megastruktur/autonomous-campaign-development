"""Static contract tests for the OCR code-review engine gate (skill 1.7.0).

These tests verify the skill payload itself, not runtime behavior. OCR invocation
quality remains a procedural/tabletop concern (scenarios 51-56).
"""

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "skills" / "acd"
TEMPLATES = SKILL_ROOT / "templates"
REFERENCES = SKILL_ROOT / "references"


class OcrReviewContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        cls.ocr = (REFERENCES / "ocr-review.md").read_text(encoding="utf-8")
        cls.state = json.loads(
            (TEMPLATES / "STATE.json").read_text(encoding="utf-8")
        )
        cls.handoff = (TEMPLATES / "HANDOFF.md").read_text(encoding="utf-8")

    def test_engine_gate_precedes_phase_one(self):
        gate = "### 0. Code-review engine gate (OCR, v1.7.0)"
        phase1 = "### 1. Intent and mandatory repository discovery"
        self.assertIn(gate, self.skill)
        self.assertLess(self.skill.index(gate), self.skill.index(phase1))
        for marker in (
            "EXCLUSIVELY through OCR",
            "OFFER installation once",
            "npm install -g @alibaba-group/open-code-review",
            "review_engine",
        ):
            self.assertIn(marker, self.skill)

    def test_exclusive_engine_no_silent_fallback(self):
        flat = " ".join(self.ocr.split())
        self.assertIn("EXCLUSIVELY through OCR", flat)
        self.assertIn("no silent fallback", flat.lower())
        self.assertIn("never swapped", flat)
        # The offer happens once, at the very start of planning.
        self.assertIn("OFFER installation once", flat)
        self.assertIn("at the very start of planning", flat)

    def test_blocking_severity_policy_is_critical_high_medium(self):
        for text in (self.skill, self.ocr):
            flat = " ".join(text.split())
            self.assertIn("critical", flat)
            self.assertIn("medium", flat)
        self.assertIn(
            "`critical`, `high`, AND `medium` block", self.ocr
        )
        self.assertIn("low` and style-only findings never", self.ocr)

    def test_not_a_verdict_states_are_listed(self):
        flat = " ".join(self.ocr.split())
        for state in ("partial", "failed", "failed(budget)", "skipped"):
            self.assertIn(state, flat)
        self.assertIn("files_reviewed > 0", flat)
        self.assertIn("start_line = end_line = 0", flat)

    def test_reviewer_model_is_ocr_model(self):
        flat = " ".join(self.ocr.split())
        self.assertIn("reviewer model from the questionnaire is OCR's model", flat)
        self.assertIn("--provider <name> --model <id>", flat)
        self.assertIn("ocr llm test", flat)
        self.assertIn("native tool calling", flat)
        self.assertIn("api_key_cmd", flat)

    def test_economical_mode_and_forbidden_modes(self):
        flat = " ".join(self.ocr.split())
        self.assertIn("--effort low", flat)
        self.assertIn("--max-tokens-budget", flat)
        self.assertIn("--preview", flat)
        self.assertIn("Never use `ocr scan`", flat)
        self.assertIn("Delegation mode", flat)
        self.assertIn("MCP CLIENT, not an MCP server", flat)

    def test_state_template_carries_engine_fields(self):
        models = self.state["models"]
        self.assertIsNone(models["review_engine"])
        self.assertEqual(
            models["ocr"], {"binary": None, "version": None, "provider": None}
        )
        review = self.state["tasks"][0]["review"]
        for field in ("engine", "ocr_session_id", "ocr_output"):
            self.assertIn(field, review)
            self.assertIsNone(review[field])

    def test_handoff_template_records_engine_decision(self):
        self.assertIn("## Code-review engine (OCR gate)", self.handoff)
        self.assertIn("{{ocr_or_session}}", self.handoff)
        self.assertIn("review_engine", self.handoff)

    def test_review_references_route_through_engine_gate(self):
        runtime = (REFERENCES / "runtime-review-and-integration.md").read_text()
        dispatch = (REFERENCES / "hermes-orca-omp.md").read_text()
        handoff_ref = (REFERENCES / "handoff-and-start.md").read_text()
        planning = (REFERENCES / "planning-and-design.md").read_text()
        for text in (runtime, dispatch, handoff_ref, planning):
            self.assertIn("review_engine", text)
            self.assertIn("ocr-review.md", text)

    def test_tabletop_scenarios_51_to_56_are_well_formed(self):
        text = (REFERENCES / "validation-tabletop.md").read_text()
        rows = re.findall(r"^\| (5[1-6]) \|.*\|$", text, re.MULTILINE)
        self.assertEqual(rows, [str(n) for n in range(51, 57)])

    def test_ocr_reference_links_resolve(self):
        missing = []
        for target in re.findall(r"(?<!!)\[[^]]+\]\(([^)]+)\)", self.ocr):
            target = target.split()[0]
            if target.startswith(("http://", "https://", "#")):
                continue
            destination = REFERENCES / target.split("#")[0]
            if not destination.exists():
                missing.append(target)
        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
