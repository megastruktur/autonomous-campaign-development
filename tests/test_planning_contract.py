"""Static contract tests for the four-phase planning gate.

These tests verify the skill payload itself, not runtime behavior. The critique
loop and research quality remain procedural/tabletop concerns.
"""

import json
import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "skills" / "acd"
TEMPLATES = SKILL_ROOT / "templates"

SKILL_NAME = "acd"
SKILL_VERSION = "1.6.0"
OLD_SKILL_NAME = "-".join(["autonomous", "campaign", "development"])  # checked absent
REPO_SLUG = f"megastruktur/{OLD_SKILL_NAME}"  # preserved by design


class PlanningContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        cls.reference = (
            SKILL_ROOT / "references" / "planning-and-design.md"
        ).read_text(encoding="utf-8")
        cls.planning_state = json.loads(
            (TEMPLATES / "PLANNING_STATE.json").read_text(encoding="utf-8")
        )
        cls.state = json.loads(
            (TEMPLATES / "STATE.json").read_text(encoding="utf-8")
        )

    def test_phases_are_ordered_and_dag_follows_convergence(self):
        markers = [
            "### 1. Intent and mandatory repository discovery",
            "### 2. Web research and architecture",
            "### 3. Independent critique and revision loop",
            "### 4. DAG and task decomposition (only after convergence)",
            "### 5. Model questionnaire",
            "### 6. One approval gate (WHAT)",
        ]
        positions = [self.skill.index(marker) for marker in markers]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("only after the convergence", self.reference)
        self.assertIn("Do not create a DAG", self.skill)

    def test_repository_and_web_evidence_are_mandatory(self):
        self.assertIn("Repository discovery is MANDATORY and read-only", self.reference)
        self.assertIn("Web research is MANDATORY for every campaign", self.reference)
        self.assertIn("Search results alone are not research", self.reference)
        self.assertIn("PAUSE planning", self.reference)
        self.assertIn("Never silently substitute model memory", self.reference)

    def test_critique_has_five_lenses_and_hash_bound_fresh_rounds(self):
        for lens in (
            "Intent fidelity",
            "Architecture and research evidence",
            "Security",
            "UX",
            "Execution readiness",
        ):
            self.assertIn(lens, self.reference)
            self.assertIn(lens, (TEMPLATES / "CRITIQUE.md").read_text())
        self.assertIn("FRESH critique of the new exact artifact hashes", self.reference)
        self.assertIn("Do not critique only the delta", self.reference)
        self.assertIn("self-critique does not pass", self.reference)

    def test_user_intent_outranks_architecture(self):
        self.assertIn("Architecture is a means to satisfy intent", self.reference)
        self.assertIn("never silently drop or invert a requirement", self.reference)

    def test_skill_name_and_version_are_pinned(self):
        match = re.match(r"^---\n(.*?)\n---\n", self.skill, re.DOTALL)
        self.assertIsNotNone(match, "SKILL.md must open with frontmatter")
        frontmatter = match.group(1)
        self.assertRegex(frontmatter, rf"(?m)^name: {SKILL_NAME}$")
        self.assertRegex(frontmatter, rf"(?m)^version: {re.escape(SKILL_VERSION)}$")
        # The short identity replaces the old name; the full product title stays.
        self.assertIn("# Autonomous Campaign Development", self.skill)

    def test_skill_directory_is_acd(self):
        self.assertEqual(SKILL_ROOT.name, SKILL_NAME)
        self.assertTrue((SKILL_ROOT / "SKILL.md").is_file())

    def test_no_old_skill_identity_in_active_sources(self):
        # Active sources only: README, gitignore, the newest changelog entry,
        # tests, and the shipped skill payload. Campaign plans/ artifacts and
        # historical changelog entries are never scanned.
        candidates = [ROOT / "README.md", ROOT / ".gitignore", ROOT / "CHANGELOG.md"]
        candidates += sorted((ROOT / "tests").glob("*.py"))
        candidates += sorted(
            p for p in SKILL_ROOT.rglob("*")
            if p.is_file() and p.suffix in {".md", ".json", ".py", ".sh"}
        )
        offenders = []
        for path in candidates:
            text = path.read_text(encoding="utf-8", errors="replace")
            if path.name == "CHANGELOG.md":
                text = text.split("\n## ", 1)[0]  # newest entry only
            text = text.replace(REPO_SLUG, "<repo>")
            if OLD_SKILL_NAME in text:
                offenders.append(str(path.relative_to(ROOT)))
        self.assertEqual(offenders, [])

    def test_planning_state_tracks_gate_and_hashes(self):
        self.assertEqual(self.planning_state["phase"], "intent")
        self.assertFalse(
            self.planning_state["intent"]["repository_discovery_completed"]
        )
        self.assertFalse(self.planning_state["research"]["web_research_completed"])
        self.assertFalse(self.planning_state["convergence"]["passed"])
        self.assertIn("intent_sha256", self.planning_state["convergence"])
        self.assertIn("research_sha256", self.planning_state["convergence"])
        self.assertIn("input_hashes", self.planning_state["critique"])
        self.assertEqual(self.state["planning"]["phase"], "intent")

    def test_manifest_freezes_design_but_not_mutable_planning_state(self):
        handoff = (TEMPLATES / "HANDOFF.md").read_text()
        blocks = re.findall(r"```json\n(.*?)\n```", handoff, re.DOTALL)
        self.assertEqual(len(blocks), 1)
        manifest = json.loads(blocks[0])
        files = manifest["files"]
        for artifact in ("INTENT", "RESEARCH", "CRITIQUE", "PLAN", "HANDOFF"):
            self.assertTrue(any(f"_{artifact}.md" in path for path in files))
        self.assertFalse(any("PLANNING_STATE" in path for path in files))
        self.assertFalse(any("STATE.json" in path for path in files))

    def test_relative_markdown_links_resolve(self):
        missing = []
        for path in (ROOT / "README.md", *SKILL_ROOT.rglob("*.md")):
            text = path.read_text(encoding="utf-8")
            for target in re.findall(r"(?<!!)\[[^]]+\]\(([^)]+)\)", text):
                target = target.split()[0]
                if target.startswith(("http://", "https://", "#")):
                    continue
                destination = path.parent / target.split("#")[0]
                if not destination.exists():
                    missing.append(f"{path}: {target}")
        self.assertEqual(missing, [])

    def test_planning_state_template_is_not_ignored(self):
        result = subprocess.run(
            ["git", "check-ignore", "--quiet",
             "skills/acd/templates/PLANNING_STATE.json"],
            cwd=ROOT,
            check=False,
        )
        self.assertEqual(result.returncode, 1, "planning template must be committable")

    def test_new_tabletop_scenarios_are_well_formed(self):
        text = (SKILL_ROOT / "references" / "validation-tabletop.md").read_text()
        rows = re.findall(r"^\| (4[2-9]|50) \|.*\|$", text, re.MULTILINE)
        self.assertEqual(rows, [str(n) for n in range(42, 51)])

    def test_research_template_mandates_oss_library_evaluation(self):
        research = (TEMPLATES / "RESEARCH.md").read_text(encoding="utf-8")
        section = "## Open-source library evaluation (whole and partial coverage)"
        self.assertIn(section, research)
        self.assertLess(
            research.index("## Sources actually consulted"), research.index(section)
        )
        self.assertLess(
            research.index(section), research.index("## Patterns and options compared")
        )
        for column in (
            "Capability slice (whole/part)",
            "Candidate package & repo",
            "License",
            "Popularity signals",
            "Maintenance / deprecation status (live-verified)",
            "Fit, security & footprint",
            "Disposition",
        ):
            self.assertIn(column, research)

    def test_state_templates_initialize_oss_evaluation_gate_false(self):
        self.assertFalse(
            self.planning_state["research"]["oss_library_evaluation_completed"]
        )
        self.assertFalse(
            self.state["planning"]["research"]["oss_library_evaluation_completed"]
        )

    def test_oss_reuse_evaluation_is_enforced_in_skill_and_reference(self):
        for text in (self.skill, self.reference):
            flat = " ".join(text.split())
            self.assertIn("open-source, popular, and non-deprecated libraries", flat)
            self.assertIn("whole and partial coverage", flat)
            self.assertIn("package registry", flat)
            self.assertIn("upstream", flat)
            self.assertIn("NOT deprecated", flat)
            self.assertIn("not archived", flat)
            self.assertIn("anti-NIH", flat)
            self.assertIn("oss_library_evaluation_completed", flat)
            self.assertIn("lockfile", flat)
            self.assertIn("serializ", flat.lower())

    def test_oss_dependency_hooks_in_critique_plan_and_task_templates(self):
        critique = (TEMPLATES / "CRITIQUE.md").read_text(encoding="utf-8")
        self.assertIn("oss_build_vs_reuse", critique)
        self.assertIn("supply_chain", critique)
        self.assertIn("lockfile", critique)
        plan = (TEMPLATES / "PLAN.md").read_text(encoding="utf-8")
        self.assertIn(
            "- Approved dependencies: "
            "{{packages_versions_licenses_and_lockfile_owner_or_none_stdlib_only}}",
            plan,
        )
        self.assertIn("must not install unapproved packages", plan)
        task = (TEMPLATES / "TASK.md").read_text(encoding="utf-8")
        self.assertIn(
            "- Approved dependencies: "
            "{{exact_packages_and_versions_or_none_no_unapproved_installs}}",
            task,
        )

    def test_skill_payload_is_ascii_and_json_templates_parse(self):
        offenders = []
        for path in sorted(p for p in SKILL_ROOT.rglob("*") if p.is_file()):
            if path.suffix not in {".md", ".json"}:
                continue
            text = path.read_text(encoding="utf-8")
            if not text.isascii():
                offenders.append(f"non-ascii: {path.relative_to(ROOT)}")
            if path.suffix == ".json":
                try:
                    json.loads(text)
                except json.JSONDecodeError:
                    offenders.append(f"invalid json: {path.relative_to(ROOT)}")
        self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main()
