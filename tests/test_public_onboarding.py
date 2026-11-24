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


if __name__ == "__main__":
    unittest.main()
