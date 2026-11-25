"""Documentation-contract tests only: no native delivery or model runtime proof.

Section-scoped obligations and unsafe counter-policies are checked independently.
Mutations exercise deletion, replacement and appended contradictions, not a runtime
simulator. Synthetic privacy fixtures contain no real runtime identities or secrets.
"""

import re
import unittest
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "fleet/skills/fleet-campaign/references/common-contract.md"
WAIT = "inbound questions and bounded waiting"
CLOCK = "original deadline and reconciliation"
DELIVERY = "native answer and durable source delivery"
MODEL = "purpose-specific model qualification"

# key, section, required relationship, replaceable clause, unsafe counter-policy.
# Matching relationships rather than isolated vocabulary keeps polarity and scope.
POLICIES = (
    ("question-dispatch", WAIT,
     r"inbound Bot question awaiting a peer question is not genuine supervised Dispatch work",
     "is not genuine supervised Dispatch work", "is genuine supervised Dispatch work"),
    ("unanswered", WAIT,
     r"`unanswered` is a turn outcome, neither pending registration nor proof the child did not work",
     "neither pending registration nor proof the child did not work",
     "pending registration and proof the child did not work"),
    ("quiet", WAIT,
     r"`NO_REPLY` is quiet output, not waiting registration or a native answer.*prose is not a native answer",
     "not waiting registration or a native answer", "valid waiting registration and a native answer"),
    ("handoff", WAIT,
     r"Handoff transfers responsibility only when authorized and still expects an answer.*not a deferred-question flag",
     "only when authorized and still expects an answer", "without authorization and expects no answer"),
    ("actual-dispatch", WAIT,
     r"Only actual active Dispatches created by the answering session.*fake pending Task/Run.*cannot substitute.*Do not assume.*dependencies exactly",
     "cannot substitute for them", "can substitute for them"),
    ("own-wait", WAIT,
     r"While owing an inbound answer.*keep the answering turn open.*own bounded native `orchestration check --wait --timeout-ms .*verified mailbox identity",
     "keep the answering turn open", "end the answering turn immediately"),
    ("mailbox", WAIT,
     r"No external polling or observer may consume another mailbox",
     "No external polling or observer may consume another mailbox",
     "An external observer may consume another mailbox"),
    ("precedence", WAIT,
     r"common exception governs blanket end-turn advice.*until those specialized references are updated.*does not change worker `ask`.*Dispatch end-turn behavior.*pending flag or authorize workers",
     "common exception governs blanket end-turn advice",
     "blanket end-turn advice overrides this common exception"),
    ("absolute-deadline", CLOCK,
     r"Before delegation, freeze the original absolute UTC `deadline_at` and forward it unchanged at every hop",
     "forward it unchanged at every hop", "replace it with a fresh deadline at every hop"),
    ("reserve", CLOCK,
     r"Declare the upstream relay/final-delivery reserve before work; reserve is policy, not a native schema field.*`deadline_at - current UTC - declared upstream relay/final-delivery reserve`",
     "policy, not a native schema field", "a required native schema field"),
    ("budget-admission", CLOCK,
     r"Refuse insufficient-budget dispatch.*subrequest.*each native wait timeout must fit the remaining budget.*Recompute before each dispatch or wait; no clock reset",
     "Refuse insufficient-budget dispatch", "Allow insufficient-budget dispatch"),
    ("cutoff", CLOCK,
     r"At cutoff report bounded incompleteness with known and unknown facts, not invented absence of peer work or a renewed deadline",
     "not invented absence of peer work or a renewed deadline",
     "using invented absence of peer work and a renewed deadline"),
    ("wake-binding", CLOCK,
     r"On each wake reconcile all correlated notices/results, not just the first status, against project/request/revision, downstream message, exact candidate and independent critic bindings.*current owner, pause/supersession state and original expiry",
     "reconcile all correlated notices/results, not just the first status",
     "reconcile only the first status and discard remaining results"),
    ("late-evidence", CLOCK,
     r"Keep an unanswered notice, substantive result and acceptance separate.*Duplicate notices cannot launch another critic.*late critique never resumes superseded work, changes candidate binding or grants retro-PASS.*Preserve the original expired outcome",
     "late critique never resumes superseded work", "late critique always resumes superseded work"),
    ("one-answer", DELIVERY,
     r"One request has one native answer\. Do not consume it with a premature pending reply and expect a second final reply",
     "Do not consume it with a premature pending reply",
     "Must consume it with a premature pending reply"),
    ("owner-route", DELIVERY,
     r"Before delegation prebind an authorized durable owner source route independent of the disposable terminal.*source-owner and request/revision correlation.*mailbox durability alone is not human delivery",
     "route independent of the disposable terminal", "route dependent on the disposable terminal"),
    ("blocked-route", DELIVERY,
     r"Do not reopen a disposed terminal, impersonate a sender or silently select another owner.*unavailable authorized route leaves delivery explicitly blocked",
     "unavailable authorized route leaves delivery explicitly blocked",
     "unavailable authorized route allows silently selecting another owner"),
    ("late-update", DELIVERY,
     r"first late native answer may reconcile `unanswered`; once answered, use a supported new correlated informational update to the prebound route, not a second reply.*Where admitted.*`send --type status --thread-id .*original correlation.*distinct update identity.*resolve installed support",
     "not a second reply", "by sending a second reply"),
    ("update-expiry", DELIVERY,
     r"Preserve original expiry and supersession in the update: correction is not retro-PASS or new work authority",
     "correction is not retro-PASS or new work authority",
     "correction grants retro-PASS and new work authority"),
    ("receipt", DELIVERY,
     r"Require an actual native receipt plus exact recipient/correlation readback before claiming delivery.*accepted, stored and observed-delivered evidence; human-read remains unknown without separate evidence.*prose is not a delivery receipt",
     "human-read remains unknown without separate evidence", "human-read is proven by storage alone"),
    ("idempotency", DELIVERY,
     r"idempotent private final/update record keyed by request \+ revision \+ kind/update identity.*intent, native operation/message receipt, reconciliation status and prior final\. Reconcile unknown outcomes before retry",
     "Reconcile unknown outcomes before retry", "Retry unknown outcomes before reconciliation"),
    ("no-guarantee", DELIVERY,
     r"receipt's supported recovery, not a fresh duplicate send.*record is not a scheduler, ownership transfer or durable human-delivery guarantee; no new native pending flags",
     "record is not a scheduler, ownership transfer or durable human-delivery guarantee",
     "record is a scheduler, ownership transfer and durable human-delivery guarantee"),
    ("route-inventory", MODEL,
     r"Inventory actual primary and purpose-specific auxiliary routes plus fallback paths.*effective runtime/version/backend-specific role mapping; do not assume auxiliary means `smol`",
     "do not assume auxiliary means `smol`", "always assume auxiliary means `smol`"),
    ("role-scope", MODEL,
     r"shared/default role can affect unpinned primaries and other consumers: identify that scope and obtain authorization before a local compatible-route repair.*Retain rollback and healthy explicit primaries/fallbacks",
     "obtain authorization before a local compatible-route repair",
     "perform a local compatible-route repair without authorization"),
    ("configuration-authority", MODEL,
     r"documentation grants no live configuration authority: no global quota/account rewrite, model hiding, memory disable or unapproved role changes",
     "no global quota/account rewrite, model hiding, memory disable or unapproved role changes",
     "allow global quota/account rewrite, model hiding, memory disable and unapproved role changes"),
    ("reasoned-retry", MODEL,
     r"Separate quota/usage exhaustion 429 from temporary rate limiting using reason evidence, not the HTTP status alone.*Only bounded supported retry.*reason permits it and the original budget permits it.*exhaustion is not an invitation to retry blindly",
     "reason permits it and the original budget permits it",
     "HTTP status is 429 regardless of reason or original budget"),
    ("semantic-proof", MODEL,
     r"Verify semantic useful purpose-specific output, including schema validation, completion and tool roundtrip where relevant, not HTTP 200, a main answer or non-429 alone",
     "not HTTP 200, a main answer or non-429 alone",
     "accepting HTTP 200, a main answer or non-429 alone"),
    ("outcomes", MODEL,
     r"Truncation, abort, schema and fallback errors remain separate outcomes.*Cache hits or no observed purpose are UNTESTED",
     "Cache hits or no observed purpose are UNTESTED", "Cache hits or no observed purpose are PASS"),
    ("private-proof", MODEL,
     r"Timestamp exact purpose/model/route proof privately.*success at one timestamp does not promise future absence of 429",
     "does not promise future absence of 429", "guarantees future absence of 429"),
)


def sections(text):
    parts = re.split(r"^##\s+(.+)$", text, flags=re.MULTILINE)
    return {" ".join(heading.lower().split()): " ".join(body.split())
            for heading, body in zip(parts[1::2], parts[2::2])}


def policy_errors(text):
    bodies = sections(text)
    flat = " ".join(text.split()).casefold()
    errors = set()
    for key, heading, required, _, unsafe in POLICIES:
        if not re.search(required, bodies.get(heading, ""), re.IGNORECASE):
            errors.add(key)
        # Also reject a conflicting instruction appended outside its proper section.
        if unsafe.casefold() in flat:
            errors.add(key)
    return errors


def link_errors(text):
    errors = []
    targets = re.findall(r"\[[^]]+\]\(([^)]+)\)", text)
    required = {
        "orca-runtime.md#native-communication-and-waiting",
        "state-and-recovery.md#native-continuation-and-original-clocks",
        "state-and-recovery.md#guarded-settlement-and-duplicate-prevention",
    }
    seen = set()
    for target in targets:
        parsed = urlsplit(target)
        path = (CONTRACT.parent / parsed.path).resolve()
        if (parsed.scheme or parsed.netloc or parsed.query or Path(parsed.path).is_absolute()
                or not path.is_relative_to(ROOT) or not path.is_file()):
            errors.append(target)
            continue
        headings = re.findall(r"^#+\s+(.+)$", path.read_text(encoding="utf-8"), re.MULTILINE)
        slugs = {re.sub(r"[^\w\s-]", "", heading.lower()).replace(" ", "-")
                 for heading in headings}
        if parsed.fragment and parsed.fragment not in slugs:
            errors.append(target)
        seen.add(path.name + "#" + parsed.fragment)
    return errors + sorted(required - seen)


PRIVACY_PATTERNS = (
    r"(?i)/(?:home|Users|workspaces|projects)/[^\s/]+",
    r"(?i)\b[A-Z]:[\\/](?:Users|projects)[\\/]",
    r"(?:~|\$HOME)/[^\s`]+",
    r"(?i)\b[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}\b",
    r"\b(?:msg|chat|bot|run|dispatch)_[0-9a-f]{8,}\b",
    r"(?i)\b(?:litellm(?:-[\w]+)?|openai|anthropic)/[\w./-]+",
    r"(?i)\b(?:api[_-]?key|token|password)\s*[:=]\s*[^\s]+",
    r"(?i)\b(?:ssh|https?)://[^\s<>]+",
    r"(?i)\b[\w.-]+\.(?:local|lan|internal)\b",
)


def privacy_errors(text):
    return [pattern for pattern in PRIVACY_PATTERNS if re.search(pattern, text)]


class DeliveryContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = CONTRACT.read_text(encoding="utf-8")

    def test_documented_obligations(self):
        self.assertEqual(policy_errors(self.text), set())

    def test_reflow_and_case_positive_control(self):
        # Presentation-only changes must not invalidate the policy relationships.
        reflowed = "\n".join(line if line.startswith("## ") else line.swapcase()
                             for line in self.text.splitlines())
        reflowed = reflowed.replace(" ", "  ")
        self.assertEqual(policy_errors(reflowed), set())

    def test_each_obligation_rejects_deletion(self):
        for key, _, _, clause, _ in POLICIES:
            with self.subTest(policy=key):
                # Flatten paragraphs, keeping headings: mutations work across line wraps.
                text = "\n\n".join(" ".join(p.split()) for p in self.text.split("\n\n"))
                self.assertEqual(text.count(clause), 1, clause)
                self.assertIn(key, policy_errors(text.replace(clause, "", 1)))

    def test_each_obligation_rejects_contradictory_replacement(self):
        text = "\n\n".join(" ".join(p.split()) for p in self.text.split("\n\n"))
        for key, _, _, clause, unsafe in POLICIES:
            with self.subTest(policy=key):
                self.assertEqual(text.count(clause), 1, clause)
                self.assertIn(key, policy_errors(text.replace(clause, unsafe, 1)))

    def test_appended_contradictions_cannot_hide_behind_valid_clauses(self):
        for key, _, _, _, unsafe in POLICIES:
            with self.subTest(policy=key):
                self.assertIn(key, policy_errors(self.text + "\n\n" + unsafe + ".\n"))

    def test_obligations_cannot_move_to_unrelated_sections(self):
        for heading in (WAIT, CLOCK, DELIVERY, MODEL):
            with self.subTest(section=heading):
                original = next(h for h in re.findall(r"^## (.+)$", self.text, re.MULTILINE)
                                if h.lower() == heading)
                mutated = self.text.replace("## " + original, "## Unrelated notes", 1)
                expected = {key for key, section, *_ in POLICIES if section == heading}
                self.assertTrue(expected.issubset(policy_errors(mutated)))

    def test_relative_runtime_recovery_links_resolve(self):
        self.assertEqual(link_errors(self.text), [])

    def test_link_deletion_missing_file_and_wrong_anchor_are_rejected(self):
        links = re.findall(r"\[[^]]+\]\([^)]+\)", self.text)
        self.assertEqual(len(links), 3)
        for link in links:
            for replacement in ("", link.replace(".md#", "-missing.md#"),
                                link[:-1] + "-missing)"):
                with self.subTest(link=link, replacement=replacement):
                    self.assertTrue(link_errors(self.text.replace(link, replacement, 1)))

    def test_public_contract_remains_generic(self):
        self.assertEqual(privacy_errors(self.text), [])

    def test_private_binding_and_secret_mutations_are_rejected(self):
        fixtures = (
            "/home/example/private-project", "C:\\Users\\example\\project",
            "$HOME/private-project", "00000000-0000-0000-0000-000000000000",
            "msg_000000000000", "litellm/fictional/model-example",
            "api_key=synthetic-not-a-secret", "https://example.invalid/private-project",
            "example.internal",
        )
        for fixture in fixtures:
            with self.subTest(fixture=fixture):
                self.assertTrue(privacy_errors(self.text + "\n" + fixture))


if __name__ == "__main__":
    unittest.main()
