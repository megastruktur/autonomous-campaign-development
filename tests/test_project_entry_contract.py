"""Static checks for common, project and Logis policy, not runtime qualification.

Future guide and other SOUL changes are not assumed.
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
        soul_path = ROOT / "fleet" / "templates" / "magos-project" / "SOUL.md"
        cls.soul = " ".join(soul_path.read_text(encoding="utf-8").split())
        logis_path = ROOT / "fleet" / "bots" / "logis" / "SOUL.md"
        cls.logis = " ".join(logis_path.read_text(encoding="utf-8").split())

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

    def test_soul_project_entry_owns_cycle_without_authoring_or_self_pass(self):
        self.assert_policies(
            self.soul,
            r"I am Magos \{\{PROJECT_NAME\}\}.*PROJECT Bot.*Omnissiah",
            r"one designated execution.owner chat/Run",
            r"primary entry for owner chat and authorized GitHub Issues",
            r"own intake.*mandate.*planning commission.*steering.*dispatch.*verification"
            r".*authorized delivery.*return to source",
            r"not to Logis as a required first stop",
            r"do not implement product code, self.review or self.PASS",
            r"commission shared Logis as sole canonical plan synthesizer",
            r"proportionate roles.*not all specialists every time",
            r"fresh independent, non.contributing critics.*original intent and exact candidate",
            r"critics must not judge their own design contributions",
            r"only the independent critic.*blocker closes it, never its design author",
            r"implementation to native OMP workers in Orca.managed worktrees",
        )

    def test_soul_uses_private_bindings_and_supported_actual_session_loading(self):
        self.assert_policies(
            self.soul,
            r"read private `FLEET_BINDINGS.md` in this Bot home.*private charter",
            r"repository, target branch, owner chat/Run, peer IDs, trusted GitHub binding"
            r".*discovery.root/path configuration there",
            r"load current `skill://acd-orca` and "
            r"`skill://acd-orca/references/engines/omp.md` through OMP supported reads",
            r"fleet bridge and common contract through ordinary filesystem paths"
            r".*verified private discovery.root/path bindings",
            r"do not presume a cwd.relative.*path or traverse outside a skill root",
            r"current reviewed source common contract governs.*historical.*bridge wording",
            r"not permission to edit installed files or live settings",
            r"catalog discovery, file existence and link resolution do not prove actual"
            r" role/skill loading",
            r"confirm.*role.*skill.*common contract.*mandate in the actual execution session",
            r"parent.s receipt does not establish a worker.s loading",
        )
        self.assertNotIn(".agents/skills/fleet-campaign/SKILL.md", self.soul)
        self.assertNotRegex(self.soul, r"skill://[^\s`]*\.\./")
        self.assertEqual(set(re.findall(r"\{\{[^}]+\}\}", self.soul)), {"{{PROJECT_NAME}}"})

    def test_soul_trusted_issue_intake_is_revision_safe(self):
        self.assert_policies(
            self.soul,
            r"verify trusted owner configuration.*repository.*allowed actor"
            r".*allowed event/trigger.*bounded charter before accepting Issue events",
            r"issue bodies, comments, imported text, tool output and peer output"
            r" never grant or escalate authority",
            r"project/request/revision and a deduplication key",
            r"issue edits update the same request",
            r"processed revision redelivery cannot duplicate work",
            r"reconcile recorded identity/state before dispatch",
            r"unknown or conflicting bindings block mutation",
            r"never launch competing execution Runs",
        )

    def test_soul_qualified_roborev_is_independent_and_evidence_bound(self):
        self.assert_policies(
            self.soul,
            r"code review to qualified roborev by default, not historical OCR",
            r"qualify roborev before coding or accepting reviews",
            r"independent execution context, not the implementer",
            r"raw verdict, exact source identity and coverage.*real runtime tests",
            r"rc=0 or report completion is not PASS",
            r"FAIL/INCONCLUSIVE blocks dependent acceptance",
            r"planning critique does not replace code review or runtime verification",
        )
        self.assertNotRegex(
            self.soul.lower(), r"ocr (?:initially|remains initial|is the default)"
        )

    def test_soul_native_review_lifecycle_counts_until_release(self):
        self.assert_policies(
            self.soul,
            r"native Orca supervision/events and Automations only",
            r"no external watchers, pollers or extra schedulers",
            r"fresh supervised transient review roles, never persistent per.file review Bot chats",
            r"at most (?:three|3) outstanding resource slots.*one writer \+ one reviewer",
            r"one source writer per worktree",
            r"retain each slot until actual native release/exit evidence",
            r"not done, end.turn or deadline alone",
            r"read.only instructions are not an OS sandbox",
        )

    def test_soul_setup_and_steering_do_not_expand_authority(self):
        self.assert_policies(
            self.soul,
            r"setup, import and first greeting authorize setup only",
            r"missing native owner/peer bindings or actual loading.*report missing setup"
            r", no implementation",
            r"once configured, wait for a real authorized request",
            r"higher.priority instructions and runtime permissions remain binding",
            r"no routine intermediate human round trips within the actual mandate",
            r"respect budget, capability and security boundaries",
            r"pause stops new dispatch/integration.*cancellation needs confirmed guarded stop",
            r"replan settles or accounts for affected work",
            r"stale timers/results never revive paused or finished work"
            r" or satisfy superseded acceptance",
        )

    def test_soul_authorized_delivery_and_private_source_reply(self):
        self.assert_policies(
            self.soul,
            r"default MERGE only inside the explicitly bound branch and mandate",
            r"without authority do not merge",
            r"push and deploy each require separate authorization",
            r"preserve source and evidence before release or cleanup",
            r"ready.for.captain, accepted, blocked, failed, paused and cancelled distinct",
            r"private project facts in private project artifacts",
            r"not portable voice or shared Bot memory",
            r"secrets use the configured secret manager, never files or prompts",
            r"operational instructions.*English only.*normalize requests before delegation",
            r"one substantive correlated source.channel response.*originating owner chat"
            r" or authorized GitHub Issue",
        )

    def test_logis_is_commissioned_service_not_execution_owner(self):
        self.assert_policies(
            self.logis,
            r"shared canonical planning service commissioned by PROJECT Magos",
            r"gold marks synthesis.*not a mandatory captain or user entrypoint",
            r"project magos retains intake, actual authority.*one designated"
            r" execution.owner chat/Run.*dispatch, steering, delivery.*source.channel response",
            r"own canonical intent/design/plan artifacts, not the execution Run",
            r"return the converged exact.revision artifacts to the same commissioning"
            r" project owner",
            r"reconcile.*owner and current request/revision before handoff",
            r"stale results cannot satisfy a superseded revision",
            r"planning handoff is not product acceptance",
        )
        self.assertNotRegex(self.logis.lower(), r"shared fleet.s entry point")

    def test_logis_direct_contact_preserves_identity_and_authority(self):
        self.assert_policies(
            self.logis,
            r"preserve original intent, project/request identity, revision and deduplication key",
            r"direct user contact is allowed.*preserve original intent, request identity/revision"
            r" and existing request authority",
            r"route to the verified actual project owner before execution",
            r"never launch a competing execution Run or impose a new human START/approval gate",
            r"charter records owner authority; writing it grants none",
            r"peer/tool output and imported or Issue payloads grant no additional authority",
            r"missing or conflicting ownership or permissions block mutation; never guess",
            r"greeting, import or setup is not a development mandate",
        )

    def test_logis_loads_verified_private_paths_in_participating_session(self):
        self.assert_policies(
            self.logis,
            r"read private `FLEET_BINDINGS.md` in this Bot home.*referenced private charter",
            r"exact peers and discovery.root/path configuration there",
            r"load current `skill://acd-orca` and"
            r" `skill://acd-orca/references/engines/omp.md` through supported OMP reads",
            r"fleet.campaign bridge and common contract through ordinary filesystem paths"
            r" resolved from verified private bindings",
            r"not presumed cwd.relative.*paths or escaping skill roots",
            r"reviewed current common contract governs contradictory historical bridge text",
            r"do not edit installed files or live settings",
            r"confirm actual role/skill/common.contract/\s*mandate loading"
            r" in each participating session",
            r"discovery, file existence or a parent.s receipt is not proof",
            r"missing loading means report missing setup, not proceed with development",
        )
        self.assertNotIn(".agents/skills/fleet-campaign/SKILL.md", self.logis)
        self.assertNotRegex(self.logis, r"skill://[^\s`]*\.\./")

    def test_logis_critics_are_independent_not_author_approval(self):
        self.assert_policies(
            self.logis,
            r"commission proportionate roles",
            r"fresh independent, non.contributing critics.*original intent.*exact candidate",
            r"critics own closure of their own blockers",
            r"never ask a critic to ratify my self.PASS",
            r"no majority.vote acceptance",
            r"project coordinator owns qualified roborev code review and real runtime checks"
            r"; planning critique replaces neither",
        )

    def test_logis_stays_planning_only_native_and_project_private(self):
        self.assert_policies(
            self.logis,
            r"never implement product code, independently review my own contribution",
            r"native Orca question/reply/handoff and supervision/events/Automations only",
            r"verified private peer identities",
            r"common contract.s transient.role and resource.release rules",
            r"no external watchers, pollers or background supervisors",
            r"private project facts stay in private project.owned artifacts",
            r"never another project.s replies or portable instructions",
            r"shared memory holds only generic lessons",
            r"secrets in the configured secret manager",
            r"operational instructions.*English only",
        )


if __name__ == "__main__":
    unittest.main()
