# Static validation and synthetic tabletops

This is a documentation validation recipe, not an execution report. Static checks establish
syntax, inventory and binding facts; independent review establishes the written contract.
Every tabletop below is **SYNTHETIC reasoning**, not a runtime test, permission probe,
provider qualification or product PASS. Record actual commands and observations separately.

Use the [roles](roles.md) and [shared policy](../../../fleet/skills/fleet-campaign/references/common-contract.md)
without copying their personas. The unchanged [S1 specification](../../../fleet/planning/doc-cutover/SPEC.md)
and [R2 candidate](../../../fleet/planning/acd-portability/CANDIDATE.md) are historical frozen
inputs. [Amendment 1](../../../fleet/execution/fullauto/AMENDMENT_01_ROBOREV.md) selects roborev
and `code-review.md`; [Amendment 2](../../../fleet/execution/fullauto/AMENDMENT_02_OVERNIGHT.md)
removes the total campaign cutoff, not finite attempts, review bounds or acceptance gates.
Other campaigns must supply their own authority, not inherit these scoped grants.

## Scope and frozen inputs

Validate the uninstalled `skills/acd-orca` candidate alongside unchanged legacy `skills/acd`.
Do not install, commit, configure providers, touch Groups, edit frozen plans or mutate live
native gates to run this recipe. The [legacy tabletop](../../acd/references/validation-tabletop.md)
is migration evidence, not authority to run its START, watcher, heartbeat or OCR actions.

Use an exact accepted-reference packet: relative path, SHA-256, slice, independent verdict
and evidence pointer. Freeze each completed file and the prior-file review packet before
another author starts; reviewers never consume actively changing source. Compare the
snapshot hash to the acceptance hash before using it. A current disk file with a familiar
name is not that snapshot. Preserve the original attempt start/checkpoint/deadline.

One assignment owns one document, or one code module plus tests; one source writer per
worktree and at most three paid working agents. Independent next-file authoring may overlap
frozen previous-file review. At most two closely related small files share a review packet,
with separate exact-hash verdicts. Coordinators do not implement or resolve source conflicts.
For this campaign attempts are at most 15 minutes, checkpoint 10 minutes and reviews at most
10 minutes; null campaign cutoff is authorized absence, not unlimited attempts. Apply the
[handoff](handoff.md) and [state contract](state-and-recovery.md) with the later amendment
precedence; preserve superseded native nodes and their replacement mapping, never PASS them.

The following recipe has two modes. With no argument it checks the complete frozen 22-file
candidate. With one repository-relative candidate filename it checks only that settled
slice and reports absent candidate files as PENDING. Slice mode is not final acceptance;
it must not read other changing candidate files. For slice cross-links, use the frozen
review copy or defer target/anchor inspection to the final gate. Run from the repository
root of the approved snapshot, not against an unrelated installed skill.

## One-shot static command

Run the following exact shell command from the frozen repository root. For slice mode put
one quoted candidate path on the **same line** as the final closing quote, separated by
a space. It writes nothing and requires only Python's standard library. Retain the command,
mode, cwd identity, UTC, exit, complete output and input/candidate hashes in the assigned
receipt. Do not turn it into a persistent checker.

```sh
python3 -B -c '
import hashlib, json, pathlib, re, sys, unicodedata
root = pathlib.Path.cwd().resolve()
base = root / "skills/acd-orca"
refs = "roles planning-and-design handoff code-review state-and-recovery runtime-review-and-integration orca-runtime validation-tabletop obligation-ledger".split()
md_templates = "INTENT RESEARCH CRITIQUE PLAN HANDOFF TASK TODO".split()
allowed = {"SKILL.md"} | {"references/" + n + ".md" for n in refs} | {"references/engines/" + n + ".md" for n in ("omp", "hermes", "codex")} | {"templates/" + n + ".md" for n in md_templates} | {"templates/PLANNING_STATE.json", "templates/STATE.json"}
assert len(allowed) == 22
errors = []
diagnostics = []
def error(where, message):
    errors.append(str(where) + ": " + message)
def diagnostic(where, message):
    diagnostics.append(str(where) + ": " + message)
def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def pairs(rows):
    result = {}
    for k, v in rows:
        if k in result:
            raise ValueError("duplicate JSON key: " + k)
        result[k] = v
    return result
def parse(text):
    return json.loads(text, object_pairs_hook=pairs, parse_constant=lambda x: (_ for _ in ()).throw(ValueError("nonfinite JSON: " + x)))
def prose(text):
    return re.sub(r"(?ms)^```[^\n]*\n.*?^```[ \t]*$", lambda m: "\n" * m.group().count("\n"), text)
def anchors(text):
    rows = re.findall(r"(?m)^#{1,6} +(.+?) *#* *$", prose(text))
    return [re.sub(r"[^a-z0-9 _-]", "", h.lower()).replace(" ", "-") for h in rows]
def placeholder_names(text):
    return set(re.findall(r"\{\{([a-z][a-z0-9_]*)\}\}", text))
def representative(name):
    if "sha256" in name:
        return "a" * 64
    if name == "prefix":
        return "demo"
    if name == "campaign_name":
        return "sample-campaign"
    if name == "task_name":
        return "sample-task"
    if name.endswith("_path"):
        return "fixtures/" + name + ".md"
    if name.endswith("_at"):
        return "2030-01-01T00:00:00Z"
    return "sample-" + name.replace("_", "-")
full = len(sys.argv) == 1
if len(sys.argv) > 2:
    raise SystemExit("Use no arguments or one candidate path")
actual = {p.relative_to(base).as_posix() for p in base.rglob("*") if p.is_file() or p.is_symlink()}
for n in sorted(actual - allowed):
    error(n, "outside explicit 22-file allowlist")
for n in sorted(allowed - actual):
    if full:
        error(n, "missing required candidate file")
    else:
        print("PENDING inventory " + n)
if full:
    selected = sorted(allowed & actual)
else:
    selected_path = (root / sys.argv[1]).resolve()
    if not selected_path.is_relative_to(base.resolve()):
        raise SystemExit("Slice must be inside skills/acd-orca")
    selected = [selected_path.relative_to(base.resolve()).as_posix()]
    if selected[0] not in allowed or selected[0] not in actual:
        raise SystemExit("Slice is absent or not allowlisted")
pins = {
    "fleet/planning/doc-cutover/SPEC.md": "f3fcb1f72c98f41e9a98f732a396610f00166ed62a3037d44f4f00bac6b7117d",
    "fleet/planning/acd-portability/CANDIDATE.md": "89fa202f0d82ba2655e65a338e1eac2780a1e5d27cf5ce4771e18fcf934b629b",
    "skills/acd/references/validation-tabletop.md": "193396f3d8eb06a15b320a146ff010dfe2ae11a6daed97ac0aa948ac494e4e29"
}
for n, expected in pins.items():
    p = root / n
    if not p.is_file() or digest(p) != expected:
        error(n, "immutable source hash mismatch")
    else:
        print("PIN " + expected + " " + n)
for n in selected:
    p = base / n
    where = p.relative_to(root).as_posix()
    if p.is_symlink() or not p.resolve().is_relative_to(root):
        error(where, "symlink or repository escape")
        continue
    text = p.read_text(encoding="utf-8")
    print("SOURCE " + digest(p) + " " + where)
    if n == "SKILL.md":
        parts = text.split("\n---\n", 1)
        if not text.startswith("---\n") or len(parts) != 2:
            error(where, "missing flat frontmatter")
        else:
            fm = {}
            for row in parts[0].splitlines()[1:]:
                m = re.fullmatch(r"(name|description|version): ([A-Za-z0-9][A-Za-z0-9 .,_/-]*)", row)
                if not m or m[1] in fm:
                    error(where, "unsupported YAML or duplicate key: " + row)
                else:
                    fm[m[1]] = m[2]
            if set(fm) != {"name", "description", "version"} or fm.get("name") != "acd-orca" or not 1 <= len(fm.get("description", "")) <= 60 or not fm.get("version"):
                error(where, "frontmatter name/description/version contract")
    a = anchors(text)
    if len(a) != len(set(a)) or "" in a:
        error(where, "nonunique or empty heading anchor")
    blocks = []
    rows = text.split("\n")
    opened = None
    for line, row in enumerate(rows):
        if re.fullmatch(r"```json[ \t]*", row):
            if opened is not None:
                error(where, "unclosed JSON fence at line " + str(opened + 1))
            opened = line
        elif opened is not None and re.match(r"[ \t]*(?:`{3,}|~{3,})", row):
            if re.fullmatch(r"```[ \t]*", row):
                blocks.append("\n".join(rows[opened + 1:line]))
            else:
                error(where, "mispaired JSON fence at line " + str(line + 1))
            opened = None
    if opened is not None:
        error(where, "unclosed JSON fence at line " + str(opened + 1))
    if n.endswith(".json"):
        blocks.insert(0, text)
    loaded = []
    for i, block in enumerate(blocks):
        try:
            loaded.append(parse(block))
            substituted = re.sub(r"\{\{([a-z][a-z0-9_]*)\}\}", lambda m: representative(m[1]), block)
            parse(substituted)
        except (ValueError, TypeError) as exc:
            error(where, "JSON block " + str(i) + ": " + str(exc))
    if n.startswith("templates/"):
        used = placeholder_names(text)
        if n.endswith(".json") and loaded:
            declared = set(loaded[0].get("_template", {}).get("placeholder_inventory", {}))
            if loaded[0].get("schema_version") != 1:
                error(where, "unexpected candidate template schema_version")
        else:
            body, separator, legend = text.partition("## Placeholder inventory\n")
            used = placeholder_names(body)
            if not separator:
                error(where, "missing placeholder inventory")
            declared = set()
            for row in legend.splitlines():
                if row.startswith("|"):
                    cell = row.split("|")[1]
                    declared.update(re.findall(r"`([a-z][a-z0-9_]*)`", cell))
                    declared.update(placeholder_names(cell))
        if used != declared:
            error(where, "placeholder mismatch missing=" + repr(sorted(used - declared)) + " unused=" + repr(sorted(declared - used)))
        print("SUBSTITUTIONS " + where + " " + json.dumps({k: representative(k) for k in sorted(used)}, sort_keys=True))
    links = re.findall(r"\[[^\]\n]+\]\(([^)\s]+)\)", prose(text))
    if n.endswith(".json") and loaded:
        meta = loaded[0].get("_template", {})
        links += list(meta.get("references", {}).values()) + list(meta.get("companion_templates", {}).values())
    for link in links:
        if re.match(r"https?://", link):
            continue
        if re.match(r"[A-Za-z][A-Za-z0-9+.-]*:", link) or link.startswith("/") or "\\" in link:
            error(where, "unsupported or absolute link " + link)
            continue
        target, _, fragment = link.partition("#")
        q = (p.parent / target).resolve() if target else p.resolve()
        if not q.is_relative_to(root):
            error(where, "link escapes repository " + link)
        elif not full and q != p.resolve() and q.is_relative_to(base.resolve()):
            print("PENDING frozen cross-link " + where + " -> " + link)
        elif not q.is_file():
            error(where, "missing link " + link)
        elif fragment and fragment not in anchors(q.read_text(encoding="utf-8")):
            error(where, "missing anchor " + link)
    for line, row in enumerate(text.splitlines(), 1):
        at = where + ":" + str(line)
        if any(c.isalpha() and "LATIN" not in unicodedata.name(c, "") for c in row):
            diagnostic(at, "non-English-letter candidate")
        if re.search(r"(?i)ocr|fresh.session.START|awaiting_fresh_session_start|watcher|heartbeat|poll|fallback|unbounded|four.hour|two.paid", row):
            diagnostic(at, "obsolete-term candidate")
        if re.search(r"(?i)[0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12}|(?:orca_session_id|task|ctx|run|msg)_[0-9a-f]{8,}|/(?:home|Users|root)/[^\s]+|[A-Z]:\\", row):
            diagnostic(at, "private identity or host path candidate")
        if re.search(r"(?i)-----BEGIN .*PRIVATE KEY|\bBearer\s+\S+|\bsk-[A-Za-z0-9]{16,}|(?:api_key|password|secret)\s*[:=]\s*[\x22\x27]?[A-Za-z0-9_/-]{12,}", row):
            diagnostic(at, "credential candidate; inspect privately, do not export value")
for item in errors:
    print("ERROR " + item)
for item in diagnostics:
    print("DIAGNOSTIC " + item)
print("STATIC mode=" + ("full" if full else "slice") + " errors=" + str(len(errors)) + " diagnostics=" + str(len(diagnostics)) + " independent_semantic_verdict=PENDING")
raise SystemExit(bool(errors))
'
```

This intentionally supports a restricted Markdown/YAML surface, not arbitrary parsers.
Independent inspection must reject unsupported reference-style links, HTML links/anchors,
multiline links, alternative fence syntax and YAML features rather than let them escape the
scan. JSON openers are column-zero triple backticks immediately followed by lowercase `json`
and optional spaces/tabs; closers are column-zero triple backticks with optional spaces/tabs.
Every supported opener is accounted for, including at EOF and after a mispaired fence;
unclosed or mispaired JSON fences are errors, even when their payload is valid JSON.
Use ordinary inline relative links and unique simple heading anchors. A version
string is a skill version; `schema_version: 1` is the candidate template family, not a
claim of legacy schema compatibility. Reject unexpected version/schema drift explicitly.

The three pins are the baseline required for this migration. Extend the receipt's immutable
input manifest with every consulted legacy source, accepted reference/template and owner
amendment; compare those expected hashes before and after the boundary. Do not silently
re-pin changed files. Also inventory every candidate byte, including untracked files.
A final reviewer must receive the complete 22-file manifest, not only this script's pins.

Each diagnostic needs a narrow disposition: exact file/hash/line, token, category, reason,
reviewer and outcome. Historical OCR links, explicit prohibitions, diagnostic regexes,
angle-bracket examples and documented placeholders may be justified individually. Do not
whitelist a whole file, all code fences or every occurrence of a word. Non-English prose,
actual credentials, runtime IDs or host paths block portable acceptance. A regex finding
is not automatically a secret or an operative instruction; absence of matches is not
proof that the document is English or secret-free. Never copy detected secrets into receipts.

## Template and interface reconciliation

Check all nine templates against accepted owning references, not against mutually agreeing
but wrong copies. Preserve per-file hashes and record the exact section/JSON pointer on
both sides of every comparison. The command checks parseability and inventory; the following
independent checks are mandatory and are not implied by its exit status.

| Templates or surface | Required cross-document check |
|---|---|
| [INTENT](../templates/INTENT.md) and [RESEARCH](../templates/RESEARCH.md) | Request/authority/evidence IDs, actual bounded discovery, live source retrieval and whole/partial OSS evaluation agree with [planning](planning-and-design.md); no invented citations or dependency grants. |
| [CRITIQUE](../templates/CRITIQUE.md) and [PLANNING_STATE](../templates/PLANNING_STATE.json) | Intent and research hashes, five lenses, required critics, complete rounds, critic-owned closure and current-hash reuse attestation gate DAG creation. Planning critical/major block; minor needs disposition. Do not confuse these severities with code review. |
| [PLAN](../templates/PLAN.md) and [HANDOFF](../templates/HANDOFF.md) | Original mandate, named base, task/contract/scenario inventory, topology, delivery rights and frozen manifest agree. INTENT/RESEARCH/CRITIQUE belong in the freeze; mutable STATE/TODO/EVENTS/PLANNING_STATE and the manifest itself do not. No recursive self-hash. |
| [TASK](../templates/TASK.md) and [TODO](../templates/TODO.md) | Same scope, exclusions, dependencies, original clocks, runtime scenarios and criteria; develop/static-or-runtime/review/integration/smoke/acceptance/preservation/cleanup and final campaign stages are not silently dropped. Document-only nonapplicability has a reason, never invented runtime PASS. |
| [STATE](../templates/STATE.json) and PLANNING_STATE | Both parse raw and after representative substitution; schema family agrees, but planning phase and execution lifecycle are different fields. Compare shared enum values and actual value types, null meanings, evidence registry pointers and collection shapes. Do not require unlike records to share every field. |
| PLAN/HANDOFF/TASK/TODO and both state templates | `models.review_engine` and `tasks[].review.engine` select roborev; `models.code_review` owns binary/version, execution engine, requested/resolved/actual model and qualification. Planning state references this runtime owner rather than duplicating its model/run record. |
| Review records and [code review](code-review.md) | `run_id`, `raw_output`, completion, coverage, findings and exact `bound_to` source/base/tip/scenario agree. Raw live verdicts `pass`, `fail`, `unable_to_review` are not normalized `PASS`, `FAIL`, `INCONCLUSIVE`; drift sets eligibility `INVALIDATED`, retaining the historical verdict. No active OCR field aliases. |
| Bounds, admission and [native runtime](orca-runtime.md) | Authorized absent campaign cutoff uses null plus `absent_by_authority` evidence; unknown cutoff is not absence. Finite original attempt/review clocks, actual UTC admission, pause/custody/revision checks and delayed deadline wakes agree. A backstop exists only under explicit native same-owner authority; no extra scheduler. |
| Acceptance and [integration](runtime-review-and-integration.md) | Separate coordinator-only blocked, never-ready, never-dispatched gate; successors depend on it, not worker report success. Code gates need bound review, required API inspection, authorized integrated source and actual post-integration smoke; document gates need static evidence and independent exact-byte verdict. |
| Preservation and [recovery](state-and-recovery.md) | Unknown=null with reason/consequence/resolution route; false eligibility is not observed failure, empty inventory is not proven completeness. Intent precedes mutation; no duplicate launch/merge on uncertainty, no source loss or reuse before verified custody/release. |

Representative substitution is **synthetic syntax validation**. For each placeholder, inspect
its inventory's type/format; use a distinct valid synthetic path/ID or 64-hex digest as
appropriate. Record the actual replacement map. The command's generic prose values are not
a populated authority, identity or evidence registry. Reject replacement collisions in JSON
keys; duplicate-key parsing catches them. For nullable observations replace the entire JSON
value with unquoted null and retain its reason separately; never use the string "null".
Exercise native number/boolean/null fields without turning them into strings. Check aware
UTC timestamps, nonnegative bounded durations, unique evidence IDs, resolvable required
references, enum membership and source/scenario hash formats in any instantiated example.
Remove no required unknown merely to make an example appear admissible.

Map the [obligation ledger](obligation-ledger.md) row by row to destinations and these
checks: all legacy sections/references/templates/scripts have RETAIN/REPLACE/EXCLUDE/DEFER
dispositions with reasons, not unexplained omissions. Preserve safety and binding while
replacing provider and transport mechanics. Legacy scripts and watcher templates remain
unchanged outside the candidate; no executable migration is authorized. Existing accepted
ledger bytes still need the separately owned provider-destination/amendment reconciliation;
this is PENDING final integration, not a waiver or authority for this author to edit them.

## Synthetic tabletop protocol

For every row record scenario ID, frozen file/hash/section, initial conditions, the prescribed
transition, forbidden transition, reasoned outcome, contradiction and independent disposition.
No command in this section is an instruction to inject live faults. A conforming walkthrough
means only **SYNTHETIC: text prescribes expected outcome**. An unexecuted runtime case stays
UNTESTED. Contradictions are documentation findings; scoped correction and affected-neighbor
recheck require new hashes and independent attestation, never relabeled old PASS.

| ID | Synthetic situation | Prescribed outcome and forbidden shortcut |
|---|---|---|
| S01 | Source or scenario changes after a clean review; a planning input changes after convergence. | Compare frozen expected/observed hashes, retain old verdict, mark current eligibility INVALIDATED and close affected gates. Reconcile authorized input revision and obtain current affected-scope review; no silent re-hash, old PASS reuse or DAG release on stale convergence. |
| S02 | A complete code review finds medium/high/critical acceptance defects, while the analysis worker reports delivery succeeded. | Valid review is FAIL; preserve raw findings and keep the separate acceptance Task blocked, never dispatch it. Route useful fixes within original bounds, retest and review the new frozen candidate. Successful reporting does not release the product successor; low/style alone does not make a fix card. |
| S03 | Review exits zero or ACP ends a turn, but required files are unread, tools/provider errored, raw schema is malformed, budget expired or coverage is zero. | INCONCLUSIVE, not PASS. Preserve raw output, errors and partial findings; complete external file/tool-ID/line/content-hash reconciliation is still required. Unknown severity or missing provenance cannot be guessed. Diagnose within authority; no silent provider/engine fallback or repeated bootstrap probe. |
| S04 | Coordinator is busy when the attempt deadline passes; a native deadline wake is queued; campaign cutoff is authorized null. | Before any affected dispatch, integration or gate completion read real UTC and refuse admission after the finite applicable deadline. Stop source edits at the worker cutoff, preserve partial artifacts, then reconcile late wake. Null total cutoff does not renew attempt/review clocks. Expiry proves neither physical exit nor permission to kill/restart. |
| S05 | Bot, chat, launch override or existing-worker permission denies a needed action; another scope appears permissive. | Record scope-specific denial or unknown and block only dependent work. No inferred Full access, permission weakening, owner impersonation, install, reset or provider switch. Effective capability remains unproven until authorized evidence resolves it; do not perform a live denial test here. |
| S06 | Operator pauses; a successful worker reply and deadline/backstop wake arrive later, possibly for a superseded revision. | No dispatch, integration or self-resume. Archive output under original task/attempt/revision/hash; ignore stale wakes for execution and disable only owned obsolete continuation with evidence. Pause is not physical stop proof. Explicit resume authority plus current custody/source/bounds reconciliation is required. |
| S07 | Launch or stop reply is lost; liveness is unverifiable; a replacement appears convenient. | Preserve request/operation/retry identity, inspect supported native receipts and reconcile ownership. Unknown launch or `stop_unknown` blocks duplicate/replacement/reuse. Use only receipt-authorized exact replay; silence, task abandonment or a deadline never proves exit. |
| S08 | Cleanup would delete the only dirty/untracked source; assignment says done but process/release state is unknown. | Preserve recoverable base, attributable diff, untracked files, hashes and all evidence outside disposable worktrees, or pause cleanup. Verify archive inventory/recoverability and separate assignment settlement, physical exit and native release. No force deletion, fake clean checkbox or resource reuse while custody is unknown. |
| S09 | Integration response is lost after possible squash/composition, or target branch moved before delivery. | Reconcile intent with exact starting/incoming/result identities and receipts before another integration. Squash ancestry alone is insufficient. Revalidate changed composition, expected named refs and authorized final route; run actual result/target smoke when authorized. No duplicate merge or fabricated no-commit SHA. |
| S10 | Unit checks pass but the actual application path fails; only a tabletop exists for a negative runtime case. | Keep runtime/product acceptance blocked and preserve failure. Units and this document are supplemental, never production-path proof. Unavailable fault injection stays UNTESTED, not passed by text; a passing rerun alone does not explain the original failure. |
| S11 | Streams/logs grow and assistant metadata changes, but no criterion-bound artifact advances; two unchanged unproductive executions already occurred. | Keep observed/assistant/completed-tool/semantic-progress facts distinct. Diagnose, do not reset clocks or mark healthy from transport. No blind third unchanged retry or new Task to hide failures; useful FAIL findings are productive but do not waive finite bounds/fix limits. |
| S12 | Research retrieval failed, reuse evaluation was skipped, or only the author's reassuring summary was reviewed. | Required discovery/live research and independent five-lens current-hash convergence remain missing. No invented citations, author self-approval, premature DAG or implicit library installation. Critic owns closure and reuse attestation; scope changes return to the affected planning phase. |
| S13 | Prior provider readiness, document acceptance or another engine's success is offered as proof of this candidate. | Retain actual scoped roborev qualification without rerunning it, but require this candidate's fresh neutral immutable no-hooks snapshot, exact config/diff/source/hook guards, raw schema 3 and sanitized provider/tool results. Operational read-only tools are not OS confinement. API inspection and runtime integration are distinct gates; auxiliary and Hermes/Codex parity remain unproven. |
| S14 | A new independent file could overlap previous-file review, or old task wiring still blocks it artificially. | Use only accepted references and frozen prior-file review bytes under the three-agent/one-writer ceiling. Coordinator records supported replacement wiring before retiring superseded nodes; no false PASS, hidden helper or lost genuine prerequisite. Each original file retains its own exact-hash verdict. |

## Recording and final gate

A slice receipt contains authority/attempt identity privately; requested, resolved and observed
model plus instruction-loading evidence; every consulted input hash; candidate hash; exact
static commands/output; per-line diagnostic exemptions; synthetic outcomes separately from
actual tests; pending links and unresolved findings; independent verdict initially PENDING.
Freeze delivered bytes before independent review. A clean static exit is not self-PASS.

The final documentation gate requires all 22 files and nine templates, no missing links or
anchors, reconciled interface/types/enums and ledger obligations, all diagnostic dispositions,
unchanged frozen inputs and independent exact-manifest PASS. The entrypoint `SKILL.md` and
ledger amendment reconciliation remain pending until separately authored and accepted.
Retain qualified provider evidence; every real code candidate still needs the full raw
provider/coverage/error contract in [code review](code-review.md). Do not run paid qualification
greetings or require code-provider bootstrap for Markdown review.

At final integration only, run the unchanged legacy contract guard once:

```sh
python3 -B -m unittest discover -s tests -p 'test_*contract.py'
```

It protects legacy `skills/acd`, not this candidate. Do not rewrite wording-bound legacy
tests to manufacture candidate acceptance. Preserve the actual output and its limited claim.
Document acceptance neither installs the staged skill nor proves useful pilot behavior.
Any later code/pilot acceptance requires its own authorized real production-path runtime,
independent review, API where required, integration, smoke and retention evidence. Only the
coordinator completes the separate blocked acceptance gate; worker_done success means the
assigned report was delivered, not product PASS or captain acceptance.
