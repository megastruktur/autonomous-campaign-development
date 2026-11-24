"""Static checks for the current common policy, not runtime qualification.

Only the common contract is in scope; future SOUL and guide changes are not assumed.
"""

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "fleet" / "skills" / "fleet-campaign" / "references" / "common-contract.md"


class ProjectEntryContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        text = CONTRACT.read_text(encoding="utf-8")
        parts = re.split(r"^##\s+(.+)$", text, flags=re.MULTILINE)
        cls.sections = {
            heading.strip().lower(): " ".join(body.split())
            for heading, body in zip(parts[1::2], parts[2::2])
        }

    def section(self, heading):
        self.assertIn(heading, self.sections, f"Missing policy section: {heading}")
        return self.sections[heading]

    def assert_policies(self, text, *patterns):
        for pattern in patterns:
            with self.subTest(policy=pattern):
                self.assertRegex(text, re.compile(pattern, re.IGNORECASE))

    def test_project_entry_owns_ordered_cycle_and_logis_service(self):
        text = self.section("roles and actual authority")
        self.assert_policies(
            text,
            r"project magos.*entrypoint.*owner chat.*authorized github issues.*whole cycle",
            r"intake\s*->.*logis synthesis\s*->.*independent critique\s*->"
            r".*native omp worktree implementation\s*->.*qualified roborev\s*->"
            r".*real tests\s*->.*authorized delivery.*source.channel reply",
            r"logis.*shared planning service.*sole canonical plan writer",
            r"not a required captain entrypoint.*competing execution run",
            r"no contribution.*own independent pass",
            r"no routine.*human gates.*mandate.*capability.*security.*scope",
        )

    def test_owner_and_revision_identity_prevent_duplicate_execution(self):
        self.assert_policies(
            self.section("identity and communication"),
            r"one designated owner chat per project",
            r"unknown or conflicting ownership blocks mutation",
            r"project/request/revision.*deduplication key",
            r"issue edits revise the same request",
            r"redelivery.*cannot launch duplicate work.*competing execution run",
            r"reconcile.*state before dispatch",
            r"correlated reply.*source channel.*owner chat.*authorized issue",
        )

    def test_trusted_binding_not_payload_defines_intake_authority(self):
        self.assert_policies(
            self.section("trusted intake"),
            r"trusted owner configuration.*repository.*actor.*event",
            r"bounded charter.*authority within.*binding.*higher.priority",
            r"check.*binding before accepting.*github issue event",
            r"issue bodies.*comments.*tool output.*untrusted input",
            r"never grant or escalate permission.*change the binding.*authorize delivery",
        )

    def test_independent_qualified_roborev_requires_evidence_not_exit_code(self):
        text = self.section("evidence and independence")
        self.assert_policies(
            text,
            r"critics.*original intent.*exact candidate",
            r"must not have authored or contributed.*own closure.*blocking findings",
            r"default.*code review is roborev, not ocr",
            r"qualify.*before coding.*accepting code review",
            r"independent execution context.*not the implementer",
            r"raw verdict.*exact source identity.*coverage.*real runtime checks",
            r"rc\s*=\s*0.*not pass",
            r"fail/inconclusive block.*acceptance",
        )
        self.assertNotRegex(text.lower(), r"ocr remains (?:initial|default).*review")

    def test_native_transient_review_resources_require_actual_release(self):
        text = self.section("native supervision")
        self.assert_policies(
            text,
            r"only native orca events.*native automations",
            r"no external watcher.*poller.*extra supervisor",
            r"fresh supervised transient review roles",
            r"not persistent per.file bot review chats",
            r"at most (?:three|3) outstanding resource slots",
            r"one source writer per worktree",
            r"slot remains occupied until actual native release/exit evidence",
            r"completion.*end.turn.*alone do not free",
            r"read.only role instructions are not an os sandbox",
        )
        self.assertNotRegex(
            text.lower(), r"(?:must|require|create|use) persistent.*(?:review|critic).*chats"
        )

    def test_delivery_and_revisions_stay_within_mandate(self):
        self.assert_policies(
            self.section("steering and delivery"),
            r"project magos as a revision",
            r"late results cannot satisfy superseded acceptance",
            r"never restart paused or finished work from stale timers",
            r"merge.*default.*only within.*bound branch and mandate",
            r"without.*authority.*do not merge",
            r"push and deploy each require separate authorization",
            r"reply to the source channel.*delivery.*verification evidence",
        )

    def test_operational_language_and_private_facts_remain_bounded(self):
        self.assert_policies(
            self.section("language"),
            r"operational instructions.*english only",
            r"normalize operational instructions into english before delegation",
        )
        self.assert_policies(
            self.section("security, memory and runtime facts"),
            r"private project facts.*private project artifacts.*not shared bot memory",
            r"public sharing needs separate authority",
            r"do not change live bots.*installed skills.*models.*connectors.*history",
        )

    def test_setup_requires_binding_loading_and_actual_request(self):
        self.assert_policies(
            self.section("setup-only default"),
            r"until verified native owner/peer bindings.*actual role/skill loading",
            r"do not begin implementation",
            r"skill://acd-orca.*omp loader.*internal assets.*existing fleet bridge/common",
            r"reading a file does not prove actual loading",
            r"wait for an actual authorized development request.*not a first greeting",
        )


if __name__ == "__main__":
    unittest.main()
