# {{prefix}} Intent and Repository Discovery: {{campaign_name}}

> Phase 1 artifact, not a plan, execution admission or acceptance verdict. Follow
> [planning and design](../references/planning-and-design.md#intent-and-repository-discovery),
> [role ownership](../references/roles.md) and the existing
> [common fleet contract](../../../fleet/skills/fleet-campaign/references/common-contract.md).
> Logis owns the canonical planning record; bounded contributors do not become competing
> writers or approve their own contributions. Actual mandate controls permitted work.

## Filling this template

Replace every double-brace placeholder using the inventory below; repeat table rows as
needed. Record only observed evidence and actual owner decisions. Use English operational
text; when the original request is in another language, retain its immutable provenance
and provide a faithful English rendering, identified as a translation rather than a quote.
Remove this section and the placeholder inventory after filling the artifact. Rebase the
ordinary relative links for the artifact's actual repository location; template-relative
links must not silently become broken project links.

An unknown fact is `null`, including in any resulting machine-readable data; never use
an empty string, zero, guessed value or success to stand for unavailable evidence. Add
its reason, consequence and resolution route in Remaining unknowns. Distinguish an
explicitly absent or inapplicable item with evidence and rationale; `null` means unknown,
not none or permission. No JSON payload is prescribed by this Markdown template.

Keep live owner/chat/Run/Task/Dispatch IDs, host paths and exact model routes in private
project bindings. Use repository-relative record pointers here, not private values or
credentials. A pointer alone does not prove instruction loading, identity or capability.
Keep requested, resolved and actual models separate in the private record governed by
[handoff](../references/handoff.md#model-and-review-identity); do not copy execution state
into INTENT or infer a model from a picker.

## Record and authority

- Intent status: `draft`. Change to `intent_captured` only after recording the request,
  bounded discovery, proposed outcomes and all consequential unknowns. These are local
  artifact statuses, not campaign lifecycle states or independent convergence.
- Recorded at, aware UTC: {{recorded_at}}
- Intent revision: {{intent_revision}}
- Private planning ownership and model/loading evidence record: {{planning_record}}
- Original request evidence ID and immutable provenance: {{request_evidence}}
- Governing mandate, charter and steering revision evidence IDs: {{authority_evidence}}
- Work actually authorized for this phase, including explicit limits: {{phase_authority}}
- Delivery grants and exclusions, recorded separately: {{delivery_permissions}}
- Private original clocks and bounds record: {{bounds_record}}

Authority follows [mandate-bound handoff](../references/handoff.md#authority-and-precedence),
not this template or a successful analysis report. Planning-only permission does not
permit implementation. Distinguish implementation, tests, review, integration/merge,
commits, cleanup, push, publication, deployment and installation rights; an unspecified
right stays unknown and cannot authorize its operation. Preserve owner answers and
superseded revisions without editing history. Escalate missing authority or consequential
choices only when the actual mandate has not settled them; no ritual START is required.

The bounds record preserves original attempt start, checkpoint, absolute attempt deadline,
fixed campaign cutoff and any predeclared phase/review, fix and resource limits. A revision,
fix or resume never resets those clocks. Before every affected dispatch, integration or
acceptance-gate completion, the coordinator checks actual UTC against persisted absolute
bounds and refuses new affected work after the earliest applicable cutoff. Native deadline
wakes can queue behind a busy turn; they reconcile, not enforce an exact-time barrier or
prove exit. Follow [original clocks and recovery](../references/state-and-recovery.md#native-continuation-and-original-clocks);
this artifact schedules nothing and grants no automatic stop, restart or self-resume.

## Original request and observable outcome

Original request, verbatim in English or faithfully rendered with its provenance:

{{original_request}}

Observable user outcome and value:

{{observable_outcome}}

### Requested capabilities

{{requested_capabilities}}

Assign stable requirement IDs and distinguish explicit requests from recommendations.
Capture failure behavior as well as successful behavior; do not silently drop a requested
capability because the preferred architecture cannot support it.

### User journeys

{{user_journeys}}

For each relevant actor/journey, record starting conditions, action, observable success,
loading/empty/error states, recovery and accessibility needs. Include trust/data boundaries
and affected integration seams. For non-interactive work, describe its actual consumer
path and failure outcome instead of inventing a UI; justify genuinely inapplicable states.

### Constraints and non-goals

- Explicit constraints, including security, UX and compatibility: {{constraints}}
- Explicit non-goals and excluded effects: {{non_goals}}
- Assumptions requiring validation, with impact and evidence IDs: {{assumptions}}

## Recommendations and consequential decisions

{{recommendations}}

Record each option's benefit, tradeoff, recommendation and owner's accepted/rejected/pending
or explicitly not-needed disposition, with decision provenance. A sensible design detail
within authority is not a new user requirement. Preserve rejected alternatives and do not
turn an unanswered proposal into scope.

{{decisions}}

For each question, record its stable ID, affected requirements, why it matters, answer or
`null`, decision authority, evidence ID and aware-UTC date. Escalate unresolved choices
that materially change functionality, risk, architecture or permission; show which path
is blocked. Do not manufacture routine human gates where the mandate already answers.

## Immutable input and discovery evidence

| Evidence ID | Repository-relative artifact or preserved receipt | Revision or source identity | SHA-256 | Inspected scope and claim supported |
|---|---|---|---|---|
| {{evidence_id}} | {{evidence_path}} | {{source_identity}} | {{source_sha256}} | {{evidence_scope}} |

Inventory every consulted authority revision, request record, contract and relevant
repository source or immutable inspection receipt. Name exact paths, symbols/consumers,
line ranges where useful and observation times. Preserve source bytes or a recoverable
snapshot; a mutable path or timestamp alone is not an immutable binding. A Git revision
alone cannot identify dirty/untracked inputs: include their byte hashes and provenance.
Unknown identity/hash stays `null` with its limitation, never a fabricated digest.
Evidence IDs below refer to these rows, not to an author's unbound assertion.

INTENT's own SHA-256 belongs in the external planning record, critique packet and later
frozen manifest, not inside the file it hashes. After each pre-freeze revision, Logis
updates its planning binding; the execution owner records any campaign-state binding
without creating a second writer. Preserve old critique inputs/verdicts. After freeze,
changed bytes require [drift reconciliation](../references/handoff.md#drift-and-resume),
not silent re-hashing or relabeling a stale verdict as current acceptance.

## Bounded read-only repository discovery

{{discovery_findings}}

Record exact inspected paths/symbols, source evidence IDs, findings and unknowns for each:

- Repository instructions, architecture documentation and established implementation patterns.
- Manifests, package manager, lockfiles, installed reusable dependencies and standard-library
  capabilities; dependency/license policies, stdlib-only or zero-dependency constraints,
  bundle/native-build weight and deployment limits.
- Participating modules and public interfaces, traced definitions and consumers; do not
  guess APIs or infer installed packages from model memory.
- Existing tests and actual runtime entry points/commands, including verified environment
  requirements and limitations. A discovered command is not an executed passing scenario.
- Integration/compatibility seams, data/schema ownership, shared files and resources,
  ports/databases/external effects and contention relevant to implementation or verification.

Discovery is mandatory even for greenfield work and stays bounded and read-only. Do not
implement, conduct exhaustive history review, create a DAG or decompose native execution
Tasks here. Bounded contributions and critique follow role/mandate authority, not a blanket
ban on all delegated analysis. Repository evidence informs intent; it cannot override it.

## Proposed acceptance outcomes

| Requirement or journey IDs | Observable outcome, including relevant negative case | Verification approach and exact evidence IDs | Unresolved proof or dependency |
|---|---|---|---|
| {{requirement_ids}} | {{acceptance_outcome}} | {{verification_evidence}} | {{proof_gap}} |

Cover functionality, security, UX, failure/recovery and integration where relevant. These
are proposed outcomes and verification approaches, not assertions that tests or reviews
ran. Identify existing scenario definitions by path, version and SHA-256; a scenario not
yet defined remains an explicit proof gap. Later results bind exact source manifest,
base/tip where available, build/configuration where relevant, scenario version/hash and
evidence identity under [runtime and integration](../references/runtime-review-and-integration.md#exact-candidate-and-stage-ordering).
No-commit delivery uses preserved exact bytes/manifests, not invented commit identities.

Product successors later depend on separate **blocked native acceptance Tasks**, never
on author or analysis success. They are never dispatched or made ready as work; only the
coordinator completes them with current exact-candidate independent review, required API
evidence, authorized integrated-source identity and actual post-integration smoke receipts.
Document-only gates instead require assigned static evidence and an independent exact-byte
document verdict, not fabricated runtime proof. FAIL/INCONCLUSIVE analysis can be delivered
successfully while the product gate stays blocked. Native mechanics remain in
[Orca runtime](../references/orca-runtime.md#acceptance-tasks-are-not-work); do not create
these Tasks during intent capture. [Code review](../references/code-review.md) owns current
provider selection and scoped qualification; this artifact establishes neither readiness
nor acceptance and supplies no fallback. Its amended provider contract takes precedence
over historical provider wording in unchanged linked common policy.

## Remaining unknowns and research handoff

{{remaining_unknowns}}

For each unknown, include the affected requirement, missing fact (`null`), evidence of
what was inspected, consequence, resolution owner/route and whether it blocks the next
phase. An empty unknowns list requires evidence-backed rationale, not implied certainty.

Whole-functionality and partial/sub-problem capability slices for reuse research:

{{reuse_slices}}

Questions and evidence still needed for the research phase:

{{research_questions}}

These are research subjects, not task assignments or a DAG. Research must evaluate existing
dependencies/stdlib first, then whole-library and partial-library coverage with live primary
sources. Do not set `research.oss_library_evaluation_completed` from discovery alone; the
[research contract](../references/planning-and-design.md#reuse-evaluation) owns that gate.
Continue to RESEARCH, then independent five-lens CRITIQUE. Only current-hash `CONVERGED`
critique permits DAG creation under the [planning gate](../references/planning-and-design.md#mandatory-sequence-and-gate).

Related templates: [RESEARCH](RESEARCH.md), [CRITIQUE](CRITIQUE.md),
[PLANNING_STATE](PLANNING_STATE.json), [HANDOFF](HANDOFF.md) and [STATE](STATE.json).
These five targets are **PENDING** future files at this staged slice; final cross-document
validation must resolve their links and field semantics at exact hashes. File existence
alone is not independent acceptance. Staging this template changes no installed loading
path, grants no execution or successor authority and does not qualify any engine.

## Placeholder inventory

The following names are the complete inventory; each is wrapped in double braces at its
use site. Values are Markdown text unless a stricter format is stated. Multi-row content
must carry the fields required by its section; missing facts use `null` with a reason.

| Names | Replacement contract |
|---|---|
| `prefix`, `campaign_name` | Unique short prefix and English lowercase campaign slug. |
| `recorded_at`, `intent_revision` | Aware-UTC timestamp and explicit artifact revision. |
| `planning_record` | Repository-relative private planning ownership, model and loading evidence pointer. |
| `request_evidence`, `authority_evidence` | IDs resolving to immutable request/mandate/charter/steering entries in the evidence register. |
| `phase_authority`, `delivery_permissions`, `bounds_record` | Granted phase scope; separately evidenced delivery rights/exclusions; private persisted original-clocks record pointer. |
| `original_request`, `observable_outcome` | Faithful request with provenance and observable user result/value. |
| `requested_capabilities`, `user_journeys` | Requirement-ID list and scenario-based consumer journeys with failure/recovery coverage. |
| `constraints`, `non_goals`, `assumptions` | Explicit limits/exclusions and assumptions with their evidence and validation impact. |
| `recommendations`, `decisions` | Options/dispositions and consequential questions/answers with authority, evidence, date and unresolved consequences. |
| `evidence_id`, `evidence_path`, `source_identity`, `source_sha256`, `evidence_scope` | Stable evidence key; repository-relative artifact/receipt; revision or snapshot identity; 64 lowercase hexadecimal digest; inspected scope/claim. Unknown identity/hash is `null`. |
| `discovery_findings` | Actual bounded inspection findings covering every discovery category and referencing exact source evidence IDs. |
| `requirement_ids`, `acceptance_outcome`, `verification_evidence`, `proof_gap` | Traceable requirement/journey keys, observable acceptance, verification approach with evidence/scenario bindings, and missing proof/dependencies or justified absence. |
| `remaining_unknowns`, `reuse_slices`, `research_questions` | Missing facts/consequences/routes, whole and partial reuse subjects, and next-phase research questions. |
