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


RUNTIME = ROOT / "skills/acd-orca/references/orca-runtime.md"
RUNTIME_SECTION = "native communication and waiting"
PIN = "https://github.com/stablyai/orca/blob/5dc5548b4570b276f231d81fbb51f8f7a066e40d/"
PINNED_SOURCES = {
    PIN + path for path in (
        "src/main/bots/bot-turn-ended.ts#L24-L35",
        "src/main/runtime/rpc/methods/orchestration/messaging/bot-request-outcome.ts#L109-L166",
        "src/main/runtime/orchestration/db/bot-requests/bot-request-outcomes.ts#L19-L48",
        "src/main/runtime/rpc/methods/orchestration/messaging/reply-method.ts#L158-L185",
        "src/main/bots/bot-request-policy.ts#L7-L14",
        "src/shared/bot-quiet-result.ts#L3-L16",
        "src/shared/rpc-contract/orchestration/orchestration-params.ts#L30-L79",
        "src/main/runtime/rpc/methods/orchestration/messaging/check-direct.ts#L75-L104",
    )
}

# Independent runtime obligations; slice-one validators remain unchanged.
RUNTIME_POLICIES = (
    ("worker", "ask the coordinator with native `ask`, then end the turn until its correlated reply arrives",
     "workers must keep their turn open after native ask"),
    ("nested", "an outbound question is not supervised Dispatch work",
     "an outbound question is supervised Dispatch work"),
    ("dispatch", "`pending`/`dispatched` Dispatches created by the answering session can suppress turn-end `unanswered` settlement",
     "pending Tasks suppress turn-end unanswered settlement"),
    ("session-scope", "session-wide last-50 Dispatch inspection, not guaranteed per-request dependency tracking",
     "guaranteed per-request dependency tracking"),
    ("fake-pending", "A pending Task/Run/registry cannot substitute; do not create Dispatches to evade the rule",
     "create Dispatches to evade turn-end settlement"),
    ("quiet", "`NO_REPLY` and ordinary prose neither register pending work nor answer the incoming question",
     "NO_REPLY registers pending work and answers the incoming question"),
    ("handoff", "Handoff changes actual authorized job ownership but still expects an answer; it is not an automatic fix or deferred-question flag",
     "handoff automatically fixes nested waiting and needs no answer"),
    ("reply-slot", "keep the incoming reply slot available: no premature pending native reply followed by an expected second final",
     "send a premature pending native reply then a second final"),
    ("own-wait", "Keep the answering turn open with your OWN bounded native wait",
     "When waiting on native work or input, end the turn"),
    ("check-syntax", "<ORCA> orchestration check --terminal <SELF> --wait --timeout-ms <WAIT_MS> --json",
     "<ORCA> orchestration check --terminal <SELF> --wait --json"),
    ("reply-syntax", '<ORCA> orchestration reply --id <INCOMING_ID> --body "<FINAL_BODY>" --json',
     '<ORCA> orchestration reply --id <DOWNSTREAM_ID> --body "<FINAL_BODY>" --json'),
    ("self-definition", "`<SELF>` is this answering agent's verified runtime-issued terminal/mailbox handle, never another actor's identity",
     "SELF may identify another actor's mailbox"),
    ("timeout-definition", "`<WAIT_MS>` is a positive integer number of milliseconds no greater than the freshly computed remaining budget",
     "WAIT_MS may exceed the remaining budget"),
    ("message-definition", "`<INCOMING_ID>` is the exact incoming question message ID, not its downstream peer request",
     "INCOMING_ID is the downstream peer request"),
    ("sender", "Reply uses the actual bound sender; never forge `--from`",
     "forge --from to deliver the answer"),
    ("no-observer", "No observer consumes another mailbox, script/sleep pollers, external watchers, new timers or interruption are authorized by this wait",
     "use an external observer to consume another mailbox"),
    ("deadline", "Before delegation freeze the original absolute UTC `deadline_at`; forward it unchanged each hop",
     "reset deadline_at at every hop"),
    ("reserve", "Declare upstream relay/final-delivery reserve before work as policy, not schema",
     "reserve is a native schema field"),
    ("recompute", "Before each dispatch and every wait recompute `deadline_at - current UTC - reserve`",
     "compute remaining budget only once before delegation"),
    ("admission", "Refuse insufficient-budget dispatch or subrequest; the wait timeout must fit that remaining budget",
     "allow insufficient-budget dispatch or subrequest"),
    ("cutoff", "At the reserve cutoff produce ONE explicit bounded final native answer to the incoming ID: known/unknown facts and correlated pending work, not invented absence of child work. There is no renewed deadline",
     "renew the deadline at cutoff instead of answering"),
    ("receipt", "Preserve the native receipt and source-owner correlation under the",
     "assistant prose replaces the native receipt"),
    ("unknown-send", "Reconcile an unknown reply outcome before retry; do not consume a second answer slot",
     "retry an unknown reply outcome without reconciliation"),
    ("all-mail", "Every native wake/wait reconciles ALL correlated returned messages, including automatic `unanswered` and late substantive answers, not only the first status/type",
     "reconcile only the first returned status"),
    ("fifo", "Check's `--types` controls the wait's wake condition, not the consumed FIFO batch contents",
     "--types filters consumed FIFO batch contents"),
    ("noanswer", "No-answer is a turn outcome, not proof that no child worked",
     "no-answer proves that no child worked"),
    ("binding", "Preserve project/request/revision/candidate/critic/owner/supersession/deadline bindings",
     "discard candidate and critic bindings on wake"),
    ("late-answer", "A first late answer after `unanswered` is supported; a second answer after `answered` is not. Use a new correlated informational update",
     "send a second answer after answered"),
    ("duplicate", "Duplicate notices never justify duplicate dispatch or delivery",
     "duplicate notices justify duplicate dispatch"),
    ("expiry", "Late evidence never retro-passes the cutoff or resumes superseded work; retain original expiry",
     "late evidence retro-passes the cutoff and resumes superseded work"),
    ("version", "These observed limitations are version-qualified, not an upstream patch claim or runtime guarantee. Pinned public sources for Orca 1.4.268",
     "this documentation proves an upstream runtime patch"),
)


def runtime_policy_errors(text):
    body = sections(text).get(RUNTIME_SECTION, "").casefold()
    flat = " ".join(text.split()).casefold()
    errors = set()
    for key, required, unsafe in RUNTIME_POLICIES:
        if required.casefold() not in body:
            errors.add(key)
        # Sentence boundary avoids interpreting 'not guaranteed ...' as its opposite.
        if re.search(r"(?:^|[.!?]\s+|\n\s*)" + re.escape(unsafe.casefold()), flat):
            errors.add(key)
    return errors


def runtime_source_errors(text):
    targets = re.findall(r"\[[^]]+\]\(([^)]+)\)", text)
    urls = {target for target in targets if urlsplit(target).scheme}
    errors = list(urls ^ PINNED_SOURCES)
    for target in targets:
        parsed = urlsplit(target)
        if parsed.scheme:
            continue
        path = (RUNTIME.parent / parsed.path).resolve()
        if (parsed.netloc or parsed.query or Path(parsed.path).is_absolute()
                or not path.is_relative_to(ROOT) or not path.is_file()):
            errors.append(target)
            continue
        headings = re.findall(r"^#+\s+(.+)$", path.read_text(encoding="utf-8"), re.MULTILINE)
        slugs = {re.sub(r"[^\w\s-]", "", h.lower()).replace(" ", "-") for h in headings}
        if parsed.fragment and parsed.fragment not in slugs:
            errors.append(target)
    # Only exact reviewed public source URLs are exempt from the common privacy policy.
    sanitized = text
    for url in PINNED_SOURCES:
        sanitized = sanitized.replace(url, "PUBLIC_SOURCE")
    return errors + privacy_errors(sanitized)


class RuntimeDeliveryContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = RUNTIME.read_text(encoding="utf-8")

    def test_runtime_positive_and_reflow_control(self):
        self.assertEqual(runtime_policy_errors(self.text), set())
        self.assertEqual(runtime_policy_errors(self.text.swapcase().replace(" ", "  ")), set())

    def test_runtime_deletion_and_reversal_mutations(self):
        text = "\n\n".join(" ".join(p.split()) for p in self.text.split("\n\n"))
        for key, required, unsafe in RUNTIME_POLICIES:
            with self.subTest(policy=key):
                self.assertEqual(text.count(required), 1)
                for replacement in ("", unsafe):
                    self.assertIn(key, runtime_policy_errors(text.replace(required, replacement, 1)))

    def test_runtime_appended_contradictions(self):
        for key, _, unsafe in RUNTIME_POLICIES:
            with self.subTest(policy=key):
                self.assertIn(key, runtime_policy_errors(self.text + "\n\n" + unsafe + "."))

    def test_runtime_links_pinned_sources_and_privacy(self):
        self.assertEqual(runtime_source_errors(self.text), [])

    def test_runtime_source_deletion_unpinning_and_private_url_rejected(self):
        for url in PINNED_SOURCES:
            for replacement in ("", url.replace("5dc5548b4570b276f231d81fbb51f8f7a066e40d", "main"),
                                "https://example.invalid/private"):
                with self.subTest(url=url, replacement=replacement):
                    self.assertTrue(runtime_source_errors(self.text.replace(url, replacement)))
        for leak in ("/home/example/private", "msg_000000000000", "litellm/fictional/model",
                     "token=synthetic", PIN + "unreviewed.ts"):
            with self.subTest(leak=leak):
                self.assertTrue(runtime_source_errors(self.text + "\n" + leak))

    def test_runtime_relative_link_anchor_mutations(self):
        targets = re.findall(r"\[[^]]+\]\(([^)]+)\)", self.text)
        for target in targets:
            if not urlsplit(target).scheme:
                with self.subTest(target=target):
                    self.assertTrue(runtime_source_errors(self.text.replace(target, target + "-missing")))

    def test_runtime_placeholder_inventory(self):
        self.assertEqual(set(re.findall(r"<[A-Z_]+>", self.text)),
                         {"<ORCA>", "<OWNER_CHAT>", "<SELF>", "<WAIT_MS>",
                          "<INCOMING_ID>", "<FINAL_BODY>"})


RECOVERY = ROOT / "skills/acd-orca/references/state-and-recovery.md"
RECOVERY_WAIT = "native continuation and original clocks"
RECOVERY_FINAL = "durable final and correction delivery"
RECOVERY_SOURCES = {
    PIN + path for path in (
        "src/main/runtime/orchestration/db/bot-requests/bot-request-outcomes.ts#L19-L48",
        "src/main/runtime/rpc/methods/orchestration/messaging/reply-method.ts#L158-L185",
        "src/main/runtime/orchestration/mailbox/routing/structured-session-mail-address.ts#L147-L169",
        "src/main/runtime/rpc/methods/orchestration/messaging/reply-follow-up.ts#L115-L147",
    )
}
RECOVERY_POLICIES = (
    (RECOVERY_WAIT, "Workers using native `ask` end the turn until the correlated reply; genuine supervised work may yield under the actual active Dispatch exemption",
     "When waiting, end the turn"),
    (RECOVERY_WAIT, "A Bot owing an incoming question answer while awaiting a peer instead keeps its OWN bounded native wait open",
     "end the incoming question turn while awaiting a peer"),
    (RECOVERY_WAIT, "Only actual `pending`/`dispatched` Dispatches created by that answering session qualify: the observed session-wide last-50 inspection is not per-request dependency tracking",
     "pending Task/Run records qualify for the Dispatch exemption"),
    (RECOVERY_WAIT, "An outbound question, registry or pending Task/Run does not qualify. Handoff still expects an answer and requires authorized ownership transfer; neither `NO_REPLY` nor prose registers pending work or answers a question. Do not create Dispatches to evade settlement",
     "NO_REPLY and handoff automatically defer native settlement"),
    (RECOVERY_WAIT, "No observer consumes another mailbox; no script poller, external watcher, heartbeat emulation or second scheduler is authorized",
     "use an observer to consume another mailbox"),
    (RECOVERY_WAIT, "Freeze original absolute UTC `deadline_at` before delegation and forward it UNCHANGED each hop",
     "reset deadline_at on each hop"),
    (RECOVERY_WAIT, "Predeclare upstream relay/final-delivery reserve as PRIVATE POLICY, not native schema",
     "reserve is a new native schema field"),
    (RECOVERY_WAIT, "Before each dispatch/wait subtract fresh current UTC and that reserve from the original deadline; refuse insufficient remaining budget, including subrequests, and bound each wait timeout to the remainder. No reset on wake, retry, recovery or late output",
     "retry and recovery renew the original budget"),
    (RECOVERY_WAIT, "At the reserve cutoff issue one explicit bounded incomplete native answer with known, unknown and correlated pending facts, not a premature pending reply or renewed deadline",
     "send pending now and a second final reply later"),
    (RECOVERY_WAIT, "On every wake/wait reconcile ALL correlated mail against project/request/revision, downstream message, exact candidate, independent critic, owner, pause/supersession and original deadline",
     "reconcile only the first notice and ignore remaining mail"),
    (RECOVERY_WAIT, "Automatic no-answer is not proof of no child work. Notice, actual result, delivery and acceptance stay distinct",
     "automatic no-answer proves no child work"),
    (RECOVERY_WAIT, "Late valid facts correct the durable record once while preserving the original expired/superseded outcome: never retro-PASS, resume or product admission. Planning delivery cannot grant product acceptance; critics remain independent non-contributors judging the exact candidate",
     "late critique grants retro-PASS and product admission"),
    (RECOVERY_FINAL, "Before launch prebind a VERIFIED authorized durable owner conversation/source route independent of the disposable temporary starter",
     "use only the disposable starter as delivery route"),
    (RECOVERY_FINAL, "A missing authorized route blocks delivery: no invented recipient, sender spoof or disposed-terminal reopen",
     "reopen the disposed starter when the route is missing"),
    (RECOVERY_FINAL, "Native Run/Dispatch durability alone is NOT human delivery. Use one final native reply to the EXACT incoming native ID, not a downstream request. Preserve the actual native operation/message receipt and exact recipient/correlation READBACK",
     "native storage alone proves human delivery"),
    (RECOVERY_FINAL, "Distinguish accepted, stored and observed-delivered from human-read/unknown; storage alone does not prove a human read",
     "stored means human-read"),
    (RECOVERY_FINAL, "A first late answer after `unanswered` is supported. After already `answered`, use supported NEW correlated informational mail, where admitted `send --type status --thread-id …`, with original request/revision plus a UNIQUE update ID; never a second reply",
     "send a second reply after already answered"),
    (RECOVERY_FINAL, "The owner's private registry maps request + revision + delivery-kind/update identity to intent -> native operation/message ID -> receipt -> reconciliation, plus prior final/history",
     "deduplicate only by request and discard revision and update identity"),
    (RECOVERY_FINAL, "Resolve unknown outcomes before any resend. Native retry requires the exact PRINTED supported instruction and the same operation, not a fresh duplicate",
     "resend unknown outcomes with a fresh operation"),
    (RECOVERY_FINAL, "This owner idempotency record is not a native API/schema or scheduler. Reserve, correlation, delivery distinctions and registry contents live behind existing private record/evidence pointers, not new Orca or template fields",
     "add registry and reserve fields to the native schema"),
    (RECOVERY_FINAL, "do not replace an integration receipt with mail evidence or invent a merge",
     "replace integration receipts with mail evidence"),
    (RECOVERY_FINAL, "Synthetic reconciliation fixtures below are documentation examples ONLY, not native integration, delivery qualification or a runtime implementation",
     "synthetic fixtures prove native delivery qualification"),
    (RECOVERY_FINAL, "Observed Orca 1.4.268 behavior is version-qualified, not an upstream-patch claim or new runtime guarantee",
     "this documentation guarantees runtime recovery"),
)


def recovery_policy_errors(text):
    bodies = sections(text)
    flat = " ".join(text.split()).casefold()
    errors = set()
    for heading, required, unsafe in RECOVERY_POLICIES:
        if (required.casefold() not in bodies.get(heading, "").casefold()
                or re.search(r"(?:^|[.!?]\s+)" + re.escape(unsafe.casefold()), flat)):
            errors.add(required)
    return errors


# These are documentary evidence/disposition pairs, NOT a state machine or sender.
# Swapping a disposition across rows must fail even when all policy keywords survive.
RECOVERY_CASES = (
    ("Delayed result", "Result arrives before reserve cutoff; no answer sent",
     "Reconcile result; send one final answer with receipt/readback"),
    ("Automatic no-answer", "Unanswered notice and real child result in same batch",
     "Retain both; no claim of absent child work"),
    ("Duplicate", "Same request/revision/update and native receipt repeated",
     "Reconcile existing record; no duplicate send or dispatch"),
    ("Expired result", "Valid critique arrives after original deadline",
     "Correct record once; preserve expired outcome; no retro-PASS"),
    ("Superseded result", "Valid critique belongs to replaced candidate/revision",
     "Archive old binding; no resume or product admission"),
    ("Disposed starter, valid route", "Starter closed; prebound authorized durable route exists",
     "Use durable route with receipt/readback; never reopen starter"),
    ("Disposed starter, missing route", "Starter closed; no authorized durable route",
     "Delivery blocked; no invented recipient or reopen"),
    ("Unknown receipt", "Intent recorded; native send outcome unknown",
     "Reconcile same operation before resend; no delivery claim"),
)


def recovery_fixture_errors(text):
    rows = [tuple(cell.strip() for cell in line.strip().strip("|").split("|"))
            for line in text.splitlines() if line.startswith("| ")]
    return {case for case in RECOVERY_CASES if rows.count(case) != 1}


def recovery_source_errors(text):
    # Runtime and recovery are sibling references. Reuse link validation without
    # broadening either document's exact public-URL allowlist or common privacy rules.
    urls = set(re.findall(r"https?://[^\s)]+", text))
    errors = list(urls ^ RECOVERY_SOURCES)
    adapted = text
    for url in RECOVERY_SOURCES:
        adapted = re.sub(r"\[[^]]+\]\(" + re.escape(url) + r"\)", "PUBLIC_SOURCE", adapted)
    adapted += "\n" + "\n".join("[source](" + url + ")" for url in PINNED_SOURCES)
    return errors + runtime_source_errors(adapted)


class RecoveryDeliveryContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = RECOVERY.read_text(encoding="utf-8")

    def test_recovery_positive_and_reflow(self):
        self.assertEqual(recovery_policy_errors(self.text), set())
        self.assertEqual(recovery_policy_errors(self.text.swapcase().replace(" ", "  ")), set())

    def test_recovery_deletion_reversal_and_appended_contradiction(self):
        text = "\n\n".join(" ".join(p.split()) for p in self.text.split("\n\n"))
        for _, required, unsafe in RECOVERY_POLICIES:
            with self.subTest(policy=required):
                self.assertEqual(text.count(required), 1)
                for mutation in (text.replace(required, "", 1),
                                 text.replace(required, unsafe, 1), text + ". " + unsafe):
                    self.assertIn(required, recovery_policy_errors(mutation))

    def test_synthetic_reconciliation_table(self):
        self.assertEqual(recovery_fixture_errors(self.text), set())
        for case in RECOVERY_CASES:
            name, evidence, disposition = case
            with self.subTest(case=name):
                row = "| " + " | ".join(case) + " |"
                self.assertIn(case, recovery_fixture_errors(self.text.replace(row, "")))
                self.assertIn(case, recovery_fixture_errors(self.text + "\n" + row))
                self.assertIn(case, recovery_fixture_errors(self.text.replace(disposition, "Claim PASS")))

    def test_synthetic_dispositions_cannot_cross_evidence_bindings(self):
        for index, case in enumerate(RECOVERY_CASES):
            other = RECOVERY_CASES[(index + 1) % len(RECOVERY_CASES)]
            with self.subTest(case=case[0]):
                changed = self.text.replace(case[2], "SWAP").replace(other[2], case[2]).replace("SWAP", other[2])
                self.assertTrue({case, other}.issubset(recovery_fixture_errors(changed)))

    def test_recovery_sources_links_privacy(self):
        self.assertEqual(recovery_source_errors(self.text), [])
        for url in RECOVERY_SOURCES:
            for replacement in ("", url.replace("5dc5548b4570b276f231d81fbb51f8f7a066e40d", "main")):
                with self.subTest(url=url):
                    self.assertTrue(recovery_source_errors(self.text.replace(url, replacement)))
        for leak in ("/home/example/private", "msg_000000000000", "token=synthetic"):
            self.assertTrue(recovery_source_errors(self.text + "\n" + leak))

    def test_existing_template_seams_resolve_without_new_fields(self):
        import json

        expected = {
            "PLANNING_STATE": {
                "bounds.attempt.deadline_at", "bounds.review_deadline_at",
                "bounds.private_original_clocks_record", "continuation.private_owner_and_native_record",
                "continuation.pending_operations_evidence_id", "handoff.execution_owner_private_record",
                "handoff.handoff_receipt_evidence_id", "evidence", "history",
            },
            "STATE": {
                "tasks[].attempt.deadline_at", "tasks[].report.native_delivery_receipt_evidence_id",
                "bounds.private_original_clocks_record", "continuation.private_owner_and_native_record",
                "continuation.pending_operations_evidence_id", "operations", "final.delivery_route",
                "final.report_evidence_id", "final.final_operation.receipt_evidence_id", "evidence", "history",
            },
        }
        for name, paths in expected.items():
            row = next(line for line in self.text.splitlines() if line.startswith("| " + name + " |"))
            self.assertEqual(set(re.findall(r"`([^`]+)`", row)), paths)
            document = json.loads((ROOT / "skills/acd-orca/templates" / (name + ".json")).read_text())
            for path in paths:
                with self.subTest(template=name, path=path):
                    node = document
                    for part in path.split("."):
                        if part == "tasks[]":
                            self.assertIsInstance(document["tasks"], list)
                            node = document["_template"]["collection_shapes"]["tasks"]
                        else:
                            self.assertIn(part, node)
                            node = node[part]


INSTALLER = ROOT / "docs/INSTALL_AGENT.md"
INSTALLER_QUALIFICATION = "6. report readiness, qualify only authorized missing scope"
INSTALLER_LOADING = "5. obtain actual loading evidence without starting work"
INSTALLER_POLICIES = (
    (INSTALLER_QUALIFICATION, "Inventory actual engine/version/runtime and effective primary, auxiliary PURPOSES and FALLBACK routes using supported help/source/config/runtime evidence",
     "inventory only the primary route"),
    (INSTALLER_QUALIFICATION, "Never assume a judge maps to smol. Include latent role/task/commit/plan and fallback routes only as actually supported; healthy primary output does not prove auxiliary/fallback health",
     "a healthy primary qualifies every auxiliary and fallback route"),
    (INSTALLER_QUALIFICATION, "Unknown, cached or unexercised routes stay UNTESTED; nonapplicable roles need evidence",
     "unexercised routes are healthy by default"),
    (INSTALLER_QUALIFICATION, "Separate quota/usage exhaustion 429 from temporary rate limiting by reason and Retry-After evidence; missing or conflicting evidence is unknown, not permission to retry",
     "every 429 is temporary and safe to retry"),
    (INSTALLER_QUALIFICATION, "Only temporary limits permit bounded supported retry within the original authorized deadline/budget; never retry exhausted quota into success",
     "retry exhausted quota until success with a renewed deadline"),
    (INSTALLER_QUALIFICATION, "Qualify meaningful semantic purpose-specific output/schema/completion/tool roundtrip where relevant, not HTTP200, non429 or a main reply",
     "HTTP200 alone qualifies the route"),
    (INSTALLER_QUALIFICATION, "Truncation, empty output and incompatible provider/model semantics fail; retain abort, schema and fallback errors separately",
     "truncated or empty output qualifies when HTTP200"),
    (INSTALLER_QUALIFICATION, "Record requested/resolved/observed identity, purpose/route and timestamp proof privately; no promise of no future 429",
     "one success guarantees no future 429"),
    (INSTALLER_QUALIFICATION, "Paid probes require explicit scoped spend/context authority; this documentation slice performs none",
     "run paid probes automatically during installation"),
    (INSTALLER_QUALIFICATION, "Before ANY proposed configuration repair, produce an exact scoped config diff and impact inventory, including shared/default coupling to UNPINNED primaries, other roles/consumers and fallback routes",
     "repair the default role without inspecting unpinned primaries"),
    (INSTALLER_QUALIFICATION, "Preserve pinned primary identity and unrelated consumers/permissions/settings",
     "replace healthy pinned primaries to simplify auxiliary repair"),
    (INSTALLER_QUALIFICATION, "Obtain separate authorization for that actual scope, retain a backup and exact comparison-guarded rollback, then postwrite readback and ACTUAL consuming-session adoption evidence through supported authorized reload/restart if needed",
     "write configuration before scope authorization and treat readback as adoption"),
    (INSTALLER_QUALIFICATION, "Compare current content with the recorded applied version and backup with the original before rollback; mismatch stops restoration",
     "restore the backup even when current configuration changed"),
    (INSTALLER_QUALIFICATION, "Configuration-only evidence is neither adopted nor healthy; requalify the affected purpose after adoption within authorized bounds",
     "configuration readback proves the consuming session is healthy"),
    (INSTALLER_QUALIFICATION, "Never silently change global/provider/model/temperature settings, hide models, disable memory or rewrite quota/accounts. Missing scope stops the affected operation; no workaround or unrelated-worker interruption",
     "missing scope permits a global settings workaround"),
    (INSTALLER_QUALIFICATION, "Existing Bot upgrades require fresh own-session actual source/context reads of the updated complete relevant skill/common/runtime/recovery instructions with exact source identity, not symlink target/config/catalog/acknowledgment or inherited read receipts alone",
     "a changed symlink or acknowledgment proves upgrade adoption"),
    (INSTALLER_QUALIFICATION, "The legitimate owner uses only the existing designated Home and owner-only loading; no peer message, new Home/Run/campaign or permission expansion",
     "create a new Home and message peers to prove loading"),
    (INSTALLER_QUALIFICATION, "Adoption must include own bounded incoming-question waits, unchanged original deadline/reserve, all-mail reconciliation and one-answer/durable-source receipt rules; reading these contracts grants no mail operation or delivery qualification",
     "reading the delivery contract qualifies native delivery"),
    (INSTALLER_QUALIFICATION, "Setup-only remains setup-only; live migration, reload/restart and spend each require separate applicable authority",
     "setup approval authorizes live migration and paid probes"),
    (INSTALLER_LOADING, "bound filesystem bridge/common contract and complete relevant runtime/recovery instructions",
     "skip runtime and recovery instructions during upgrade"),
    (INSTALLER_LOADING, "Provide fresh own-session read-tool evidence of exact source paths and revision/hash, including updated instructions in this consuming session's actual context",
     "reuse the parent's read receipts as current session adoption"),
    (INSTALLER_LOADING, "Catalog discovery, symlink targets, configuration, inherited receipts and acknowledgment text do not prove loading or adoption",
     "catalog discovery proves loading and adoption"),
)
INSTALLER_LINKS = {
    "../fleet/skills/fleet-campaign/references/common-contract.md#purpose-specific-model-qualification",
    "../fleet/skills/fleet-campaign/references/common-contract.md#inbound-questions-and-bounded-waiting",
    "../fleet/skills/fleet-campaign/references/common-contract.md#native-answer-and-durable-source-delivery",
    "../skills/acd-orca/references/orca-runtime.md#native-communication-and-waiting",
    "../skills/acd-orca/references/state-and-recovery.md#native-continuation-and-original-clocks",
    "../skills/acd-orca/references/state-and-recovery.md#durable-final-and-correction-delivery",
}


def installer_policy_errors(text):
    bodies = sections(text)
    flat = " ".join(text.split()).casefold()
    return {required for heading, required, unsafe in INSTALLER_POLICIES
            if required.casefold() not in bodies.get(heading, "").casefold()
            or re.search(r"(?:^|[.!?]\s+)" + re.escape(unsafe.casefold()), flat)}


def installer_link_errors(text):
    body = sections(text).get(INSTALLER_QUALIFICATION, "")
    targets = set(re.findall(r"\[[^]]+\]\(([^)]+)\)", body))
    errors = list(INSTALLER_LINKS - targets)
    for target in targets:
        parsed = urlsplit(target)
        path = (INSTALLER.parent / parsed.path).resolve()
        if (parsed.scheme or parsed.netloc or parsed.query or Path(parsed.path).is_absolute()
                or not path.is_relative_to(ROOT) or not path.is_file()):
            errors.append(target)
            continue
        headings = re.findall(r"^#+\s+(.+)$", path.read_text(encoding="utf-8"), re.MULTILINE)
        slugs = {re.sub(r"[^\w\s-]", "", h.lower()).replace(" ", "-") for h in headings}
        if parsed.fragment and parsed.fragment not in slugs:
            errors.append(target)
    # Existing install paths elsewhere remain legitimate; the new portable policy
    # needs neither concrete identities nor home paths nor public provider URLs.
    return errors + privacy_errors(body)


class InstallerQualificationContractTests(unittest.TestCase):
    """Document mutations only, not installation, provider or native qualification."""

    @classmethod
    def setUpClass(cls):
        cls.text = INSTALLER.read_text(encoding="utf-8")

    def test_installer_policy_positive_and_reflow(self):
        self.assertEqual(installer_policy_errors(self.text), set())
        self.assertEqual(installer_policy_errors(self.text.swapcase().replace(" ", "  ")), set())

    def test_installer_clause_deletions_and_dangerous_replacements(self):
        text = "\n\n".join(" ".join(p.split()) for p in self.text.split("\n\n"))
        for _, required, unsafe in INSTALLER_POLICIES:
            with self.subTest(policy=required):
                self.assertEqual(text.count(required), 1)
                for replacement in ("", unsafe):
                    self.assertIn(required, installer_policy_errors(text.replace(required, replacement, 1)))

    def test_installer_contradictions_cannot_hide_behind_required_clauses(self):
        for _, required, unsafe in INSTALLER_POLICIES:
            with self.subTest(policy=required):
                self.assertIn(required, installer_policy_errors(self.text + "\n\n" + unsafe + "."))

    def test_installer_upgrade_links_and_portable_policy(self):
        self.assertEqual(installer_link_errors(self.text), [])
        for target in INSTALLER_LINKS:
            for replacement in ("", target + "-missing"):
                with self.subTest(target=target, replacement=replacement):
                    self.assertTrue(installer_link_errors(self.text.replace(target, replacement)))

    def test_installer_new_policy_rejects_private_examples(self):
        for leak in ("/home/example/private", "msg_000000000000", "litellm/fictional/model",
                     "token=synthetic", "https://example.invalid/provider"):
            with self.subTest(leak=leak):
                text = self.text.replace("## 7.", leak + "\n\n## 7.", 1)
                self.assertTrue(installer_link_errors(text))


REVIEWED_ENTRY_REVISION = "df8ed09acfbb612e7bc9dfb7649ef9903d662f55"
OLD_ENTRY_REVISION = "6016d52b1daf0b15b0848da9978a301731290c9d"


def publication_pin_errors(text):
    body = sections(text).get("install with your agent prompt", "")
    guide_pins = re.findall(
        r"https://raw\.githubusercontent\.com/megastruktur/autonomous-campaign-development/"
        r"([0-9a-f]{40})/docs/INSTALL_AGENT\.md(?=\s)", body)
    source_pins = re.findall(r"\bsource_revision=([0-9a-f]{40})(?=;|\s)", body)
    errors = set()
    if guide_pins != [REVIEWED_ENTRY_REVISION]:
        errors.add("guide-pin")
    if source_pins != [REVIEWED_ENTRY_REVISION]:
        errors.add("source-pin")
    if guide_pins != source_pins:
        errors.add("pin-mismatch")
    return errors


class PublicationEntryContractTests(unittest.TestCase):
    """Local immutable Git blobs only; never public HTTP or installation proof."""

    @classmethod
    def setUpClass(cls):
        import os

        cls.text = (ROOT / "README.md").read_text(encoding="utf-8")
        cls.git_env = {**os.environ, "GIT_NO_LAZY_FETCH": "1", "GIT_TERMINAL_PROMPT": "0"}
        cls.contracts = (
            (CONTRACT, policy_errors), (RUNTIME, runtime_policy_errors),
            (RECOVERY, recovery_policy_errors), (INSTALLER, installer_policy_errors),
        )

    def blob(self, revision, path):
        import subprocess

        return subprocess.check_output(
            ["git", "-C", str(ROOT), "show", f"{revision}:{path.relative_to(ROOT).as_posix()}"],
            env=self.git_env, text=True, encoding="utf-8", timeout=10)

    def test_publication_pins_bind_exact_reviewed_tree(self):
        self.assertEqual(publication_pin_errors(self.text), set())

    def test_old_mismatched_missing_and_mutable_pins_fail(self):
        for replacement in (OLD_ENTRY_REVISION, "main", "0" * 40, ""):
            with self.subTest(replacement=replacement):
                self.assertTrue(publication_pin_errors(self.text.replace(REVIEWED_ENTRY_REVISION, replacement)))
        for marker in ("/" + REVIEWED_ENTRY_REVISION + "/", "source_revision=" + REVIEWED_ENTRY_REVISION):
            with self.subTest(marker=marker):
                mutated = self.text.replace(marker, marker.replace(REVIEWED_ENTRY_REVISION, OLD_ENTRY_REVISION))
                self.assertIn("pin-mismatch", publication_pin_errors(mutated))

    def test_reviewed_local_blobs_satisfy_all_four_contracts(self):
        for path, validator in self.contracts:
            with self.subTest(path=str(path.relative_to(ROOT))):
                self.assertEqual(validator(self.blob(REVIEWED_ENTRY_REVISION, path)), set())

    def test_old_local_blobs_fail_each_repaired_contract(self):
        for path, validator in self.contracts:
            with self.subTest(path=str(path.relative_to(ROOT))):
                self.assertTrue(validator(self.blob(OLD_ENTRY_REVISION, path)))

    def test_readme_diff_is_exactly_two_pin_replacements(self):
        previous = self.blob(REVIEWED_ENTRY_REVISION, ROOT / "README.md")
        self.assertEqual(previous.count(OLD_ENTRY_REVISION), 2)
        self.assertEqual(self.text, previous.replace(OLD_ENTRY_REVISION, REVIEWED_ENTRY_REVISION))


if __name__ == "__main__":
    unittest.main()
