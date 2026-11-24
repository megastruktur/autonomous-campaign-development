"""Public historical-document contracts, not runtime or reconstructed-history proof."""

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class HistoricalAmendmentPrivacyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = (ROOT / "fleet/execution/fullauto/AMENDMENT_03_RUNTIME_RESUME.md").read_text(
            encoding="utf-8"
        )
        cls.flat = " ".join(cls.text.split())

    def test_generic_exclusion_retains_connector_and_manual_testing_requirement(self):
        self.assertIn(
            "No actual external product project connector/business tasks: "
            "that project still requires captain connector setup and manual testing.",
            self.flat,
        )

    def test_editorial_notice_preserves_private_evidence_authority_and_verdicts(self):
        notice = " ".join(line.removeprefix("> ") for line in self.text.splitlines()
                          if line.startswith("> "))
        self.assertIn("This public copy generalizes project identities for privacy only.", notice)
        self.assertIn(
            "Original private evidence remains unchanged, as do historical authority and verdicts.",
            notice,
        )

    def test_recovery_scope_and_failure_limits_remain_explicit(self):
        for boundary in (
            "Preserve all historical failures and snapshots.",
            "Never bypass actual runtime owner-only access.",
            "No duplicate campaign/coordinator.",
            "Do not commit/push/merge/deploy or switch installed skills/Bots in this scoped recovery.",
            "if it fails twice, escalate a precise diagnosis to the planner, never silently mark PASS.",
            "The lost historical output remains INCONCLUSIVE and is never reconstructed by relabeling current data.",
            "It is NOT a prerequisite to future coding or a demand to prove impossible historical absence.",
            "Label simulated, source-only and untested cases precisely.",
            "Unsupported fault injection stays limited/UNTESTED; it cannot imply broad resilience PASS",
            "New tests are authorized, not a gate waiver.",
            "No source self-PASS.",
            "Do not modify global Bot instructions merely to implement this recovery",
            "No engine upgrade, resource limit rewrite, package install or restart is implied.",
        ):
            with self.subTest(boundary=boundary):
                self.assertIn(boundary, self.flat)
        self.assertEqual(re.findall(r"^(\d+)\. ", self.text, re.MULTILINE),
                         ["1", "2", "3", "4", "5", "6"])

    def test_cleanup_requires_identity_accounting_not_blanket_success(self):
        for boundary in (
            "Never kill reused or unproven process identity.",
            "no identity impersonation, backing-file mutation, raw process killing or service restart.",
            "Keep a baseline PID+birth ledger for ALL53",
            "Counts decreasing is not proof that specific old identities exited",
            "not interruption of ongoing real work or deletion of files/chats/worktrees",
            "do not use a wider operation to bypass it.",
            "Still-needed external work is reported explicitly as deferred; do not claim all53 cleaned if any remain.",
            "separate product acceptance, limited recovery proof and cleanup completeness.",
        ):
            with self.subTest(boundary=boundary):
                self.assertIn(boundary, self.flat)

    def test_public_amendment_has_no_concrete_personal_paths_or_hosts(self):
        patterns = (
            r"(?i)/(?:home|Users)/[^\s/]+",  # Concrete Unix user homes.
            r"(?i)\b[A-Z]:[\\/](?:Users|projects)[\\/]",  # Native local paths.
            r"(?i)\b(?:ssh|https?)://[^\s<>]+",  # No host URLs needed in this amendment.
            r"\b(?:\d{1,3}\.){3}\d{1,3}\b",  # Literal IPv4 hosts.
            r"(?i)\b[\w.-]+\.(?:local|lan|internal)\b",  # Private host names.
            r"(?:~|\$HOME)/(?:[^\s`]+)",  # Personal home-relative project paths.
        )
        for pattern in patterns:
            with self.subTest(pattern=pattern):
                self.assertNotRegex(self.text, pattern)


class HistoricalCharterPrivacyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = (ROOT / "fleet/execution/fullauto/CHARTER.md").read_text(encoding="utf-8")
        cls.flat = " ".join(cls.text.split())
        cls.models = " ".join(cls.text.split("All implementation uses OMP", 1)[1]
                              .split("## Native work DAG", 1)[0].split())

    def test_historical_notice_is_not_new_authority_or_installation_default(self):
        notice = " ".join(line.removeprefix("> ") for line in self.text.splitlines()
                          if line.startswith("> "))
        self.assertIn("historical authorization only, not a new-user mandate or installation default", notice)
        self.assertIn("Environment-specific model identities are redacted for privacy", notice)
        self.assertIn("original private evidence and verdicts remain unchanged", notice)

    def test_model_choices_are_explicit_private_redactions_not_public_defaults(self):
        redaction = "[environment-specific value redacted in this public copy]"
        self.assertIn(
            "Select the explicitly verified campaign model route recorded in private bindings " + redaction,
            self.models,
        )
        self.assertIn("The previous primary route was exhausted.", self.models)
        self.assertIn(
            "Project-only OMP judge/smol settings may reuse the already proven auxiliary route recorded in "
            "private bindings " + redaction + " in THESE new/test workspaces if needed",
            self.models,
        )
        # Selection clauses above require private bindings; reject route literals and assignments too.
        for pattern in (r"`[^`\s]+/[^`\s]+`", r"\b[\w.-]+(?:/[\w.-]+){2,}\b",
                        r"(?i)\b(?:model|provider|default_model)\s*[:=]"):
            with self.subTest(pattern=pattern):
                self.assertNotRegex(self.models, pattern)

    def test_model_health_and_mutation_boundaries_remain_explicit(self):
        for boundary in (
            "record backup and actual use, never mutate global provider config, existing Bot homes, permissions or secrets",
            "Configuration presence alone is not qualification",
            "A worker checks actual primary/auxiliary outcomes before claiming health",
            "Do not launch a known exhausted primary or silently swap review provider",
            "Missing Codex or invalid Hermes credentials are a parity boundary, not authority to install/sign in or fabricate compatibility",
        ):
            with self.subTest(boundary=boundary):
                self.assertIn(boundary, self.models)

    def test_historical_precedence_frozen_sources_and_evidence_gates_remain(self):
        for boundary in (
            "Historical OCR, four-hour and fully serial clauses below are superseded where explicitly stated in these amendments",
            "Individual attempt limits, independent quality gates and scope protections remain",
            "Do not commit Git changes",
            "Both frozen planning trees remain read-only. Reverify before relying on them",
            "a successful analysis with a FAIL/INCONCLUSIVE result must leave dependent product work unready",
            "Only independent accepted review + tests may complete the gate",
            "Never fabricate a transport error or claim an unexercised scenario passed",
            "critical/high/medium block, partial/skipped/budget failure is INCONCLUSIVE",
            "Unsupported fault injection stays UNTESTED with exact reason",
            "Each doc/code attempt <=15min, checkpoint at10min, original clock survives retries",
            "Total campaign horizon 4h from accepted handoff",
            "states PASSED/BLOCKED/UNTESTED per requirement",
        ):
            with self.subTest(boundary=boundary):
                self.assertIn(boundary, self.flat)
        self.assertIn("`f964b5e9006132f04961450fbbc3d6e5a38b9139`", self.text)
        self.assertIn("R2 candidate SHA-256: `89fa202f0d82ba2655e65a338e1eac2780a1e5d27cf5ce4771e18fcf934b629b`", self.text)
        self.assertIn("S1 SPEC SHA-256: `f3fcb1f72c98f41e9a98f732a396610f00166ed62a3037d44f4f00bac6b7117d`", self.text)
        for amendment in ("AMENDMENT_01_ROBOREV.md", "AMENDMENT_02_OVERNIGHT.md",
                          "AMENDMENT_03_RUNTIME_RESUME.md"):
            self.assertIn(f"]({amendment})", self.text)


if __name__ == "__main__":
    unittest.main()
