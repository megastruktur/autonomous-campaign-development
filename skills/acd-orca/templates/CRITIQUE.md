# {{prefix}} Design Critique and Convergence: {{campaign_name}}

> Phase 3 evidence record, not execution authority or product acceptance. Follow
> [planning and design](../references/planning-and-design.md#independent-critique-and-revision)
> and [critic independence](../references/roles.md#critic-independence). Logis preserves
> canonical rounds and responses; each independent critic owns its findings and closure.
> Existing [common policy](../../../fleet/skills/fleet-campaign/references/common-contract.md)
> remains linked, not copied into this template.

## Filling this template

Replace every double-brace placeholder using the inventory below. Repeat evidence,
finding and disposition rows as needed; append a new numbered round rather than replacing
an old one. Remove this section and the placeholder inventory after filling. Rebase all
ordinary relative links for the artifact's actual repository location. Use English text;
preserve immutable provenance and identify translations of non-English original requests.

Unknown facts are `null`, including unknown verdicts, identities, timestamps and hashes;
never substitute an empty string, zero, guessed digest or success. Record why the fact is
unknown, its consequence and its resolution route. An explicitly absent or inapplicable
item needs evidence and rationale. No JSON payload is prescribed by this Markdown template.
Keep live identities, host paths, exact model routes and credentials out of this portable
artifact; use repository-relative private-record pointers. A pointer is not proof of loading,
independence or actual model use. Private records distinguish requested, resolved and actual
models under [handoff](../references/handoff.md#model-and-review-identity).

Preserve immutable input snapshots for every round. The reviewer reads frozen bytes, never
an actively changing sibling file. A revision produces new hashes and a new round; it does
not turn an old verdict into approval of the new candidate. CRITIQUE's own current SHA-256
belongs in the external planning record and eventual frozen manifest, not inside the file
it hashes. A final manifest binds the complete ordered history.

## Record, authority and bounds

- Recorded at, aware UTC: {{recorded_at}}
- Critique record revision: {{critique_revision}}
- Private planning ownership, critic identities and model/loading record: {{planning_record}}
- Original request and actual mandate evidence IDs: {{authority_evidence}}
- Permitted critique scope and delivery exclusions: {{phase_authority}}
- Private original clocks, phase limits and native receipt record: {{bounds_record}}
- Latest round number: {{latest_round}}
- Local convergence status: `IN_PROGRESS`. Allowed values: `IN_PROGRESS`, `REVISE`, `CONVERGED`.
- Latest independent result: `null`. Once received: `PASS`, `FAIL` or `INCONCLUSIVE`.
- Current INTENT SHA-256 attested by all required critics: `null`.
- Current RESEARCH SHA-256 attested by all required critics: `null`.
- Aggregate current-candidate attestation and required-critic coverage receipt: `null`.

These are critique facts, not campaign lifecycle states. `IN_PROGRESS` or `REVISE` never
means admitted execution; even `CONVERGED` is only a planning gate. An incomplete report
remains INCONCLUSIVE without changing old evidence into a new verdict. Only fill the
aggregate attestation and convergence hashes after every required critic supplies a
complete current-candidate PASS and all blocking findings are closed by their owners.

Actual mandate and recorded steering control scope under
[authority and precedence](../references/handoff.md#authority-and-precedence), not file
existence or report delivery. Planning-only authority does not authorize implementation.
No fresh-session START, model questionnaire or routine human approval ritual substitutes
for authority, evidence or permissions. A real owner constraint still binds.

The bounds record preserves original attempt start, checkpoint, absolute attempt deadline,
review/phase deadlines, fix limits and resource limits. Before every affected dispatch,
integration or acceptance-gate completion, the coordinator reads real UTC and refuses new
affected work after the earliest applicable persisted absolute cutoff. Revisions, fixes,
restarts and late receipts never reset the clock. The current
[overnight amendment](../../../fleet/execution/fullauto/AMENDMENT_02_OVERNIGHT.md) explicitly
sets this campaign's cutoff to `null`: known absence of a total cutoff, with that authority
recorded, not an unknown deadline or permission to drop finite attempt/review bounds.
Earlier fixed-cutoff wording is historical for that campaign only. Another campaign uses
its actual mandate. Current bounds remain checkpoint 10 minutes, attempt at most 15 minutes,
review at most 10 minutes and the assigned defect-fix limit; persist absolute timestamps
before launch rather than reconstructing them from these durations on resume.

Native result wakes and exact-owner deadline reconciliation follow
[state and recovery](../references/state-and-recovery.md#native-continuation-and-original-clocks).
A delayed wake is not an exact-time barrier, proof of exit or authority to kill/restart.
This record schedules nothing: no polling loop, external watcher, automatic retry or
self-resume from a pause. Preserve and report incomplete work when bounds are exhausted.

## Round {{round_number}}

### Frozen inputs and neutral packet

- Round opened at, aware UTC: {{round_opened_at}}
- Independent critic private-record pointer and read-only enforcement evidence: {{critic_record}}
- Neutral request/packet path, version and SHA-256: {{packet_binding}}
- Original request provenance and evidence ID supplied to the critic: {{request_evidence}}
- INTENT repository-relative snapshot path, revision and SHA-256: {{intent_binding}}
- RESEARCH repository-relative snapshot path, revision and SHA-256: {{research_binding}}
- Previous round and exact input identities, or explicit initial-round declaration: {{prior_round}}
- Required critics and the scope each must attest: {{required_critics}}

| Evidence ID | Repository-relative immutable artifact or receipt | Revision or source identity | SHA-256 | Scope, observation time and supported claim |
|---|---|---|---|---|
| {{evidence_id}} | {{evidence_path}} | {{source_identity}} | {{source_sha256}} | {{evidence_scope}} |

Inventory the original request, mandate/amendments, both planning inputs, consulted contracts,
repository paths/symbols/consumers, research sources and retained retrieval evidence, known
findings and prior attestations actually supplied. A mutable path, citation or timestamp
alone is not an immutable binding. Include exact byte hashes and provenance for dirty and
untracked files; no-commit delivery does not justify inventing base/tip commits. Preserve
recoverable source snapshots and identify any missing evidence as `null` with a consequence.

The packet includes raw acceptance criteria and known findings without an instruction to
agree or an author's reassuring verdict. Record whether read-only is enforced or merely
instructed. A critic cannot have authored the candidate or contributed the design it judges.
Missing independent capability blocks convergence; author self-checks are preparation only.

### Critic-selected changed and affected scope

{{affected_scope}}

The initial round explicitly inspects all five lenses below. On later rounds the independent
critic, not the author, identifies changed inputs and affected requirements, contracts,
consumers and evidence. Recheck corrected findings, sibling paths of the same defect class
and regressions across every affected lens. If the effect cannot be bounded, widen inspection,
including a fresh full critique when necessary. Do not demand blanket re-review of justified
unaffected evidence merely because a new round exists.

### Lens 1 - Intent fidelity

{{intent_findings}}

Check requested functionality, constraints, non-goals, user journeys and observable outcomes.
Identify omissions, scope creep and architectural preferences that override the original
request. Link every finding or reasoned no-finding conclusion to the frozen request and inputs.

### Lens 2 - Architecture and research evidence

{{architecture_findings}}

Check pattern fit, feasibility, repository constraints, shared contracts, data/control flow,
migration, compatibility, failure behavior and current primary-source evidence. Inspect the
written whole/partial OSS evaluation: existing dependencies/stdlib first, then whole-library
and partial-library options; live registry and upstream license, adoption, maintenance,
non-deprecation, compatibility, security and footprint evidence; concrete reuse/rejection or
custom-code justification. Missing live evaluation, memory-only verification, deprecated or
superseded selections and unjustified reimplementation are blocking defects, not style nits.

### Lens 3 - Security

{{security_findings}}

Check assets, threats, trust boundaries, abuse cases, data protection, access control,
secure defaults, failure behavior and verification. Include third-party license compatibility,
advisories/CVEs and supply-chain exposure, proportionate to the proposed capability.

### Lens 4 - UX

{{ux_findings}}

Check real consumer journeys, loading/empty/error/success states, feedback, recovery,
accessibility, responsiveness and product consistency. Non-interactive work still has a
consumer path and failure outcome; any inapplicable subcase needs an explicit rationale.

### Lens 5 - Execution readiness

{{readiness_findings}}

Check observable acceptance and actionable real-runtime scenarios, feasible task boundaries,
dependencies, exclusions and resource contention. Verify pinned package/version constraints,
license fit and single-owner manifest/lockfile sequencing before decomposition. Distinguish
known commands and scenario definitions from executed tests; this critique supplies no
runtime PASS, engine parity or provider-readiness proof. Do not create the DAG to fill a
readiness gap before convergence.

### All-lens coverage and evidence reuse

| Lens | Inspection mode | Exact evidence and inspected scope | Critic rationale for reuse and applicability to current INTENT/RESEARCH hashes | Limits or missing coverage |
|---|---|---|---|---|
| 1 - Intent fidelity | {{intent_mode}} | {{intent_coverage}} | {{intent_attestation}} | {{intent_limits}} |
| 2 - Architecture and research | {{architecture_mode}} | {{architecture_coverage}} | {{architecture_attestation}} | {{architecture_limits}} |
| 3 - Security | {{security_mode}} | {{security_coverage}} | {{security_attestation}} | {{security_limits}} |
| 4 - UX | {{ux_mode}} | {{ux_coverage}} | {{ux_attestation}} | {{ux_limits}} |
| 5 - Execution readiness | {{readiness_mode}} | {{readiness_coverage}} | {{readiness_attestation}} | {{readiness_limits}} |

Modes are `inspected`, `reused` or `mixed`; an unknown mode is `null`, not covered.
For every reused scope cite its prior round, exact input hashes and immutable evidence,
explain why this change does not invalidate it, and obtain the critic's explicit applicability
attestation to BOTH current hashes. Mixed coverage separates newly inspected and reused
scope. A bare "unchanged", author-selected exemption or old PASS is insufficient. Every
round accounts for all five lenses; missing or unbounded coverage prevents convergence.

### Findings and dispositions

| Finding ID | Owning critic record | Severity and lens | Finding, exact evidence and rationale | Required resolution | Author response and changed input binding | Disposition and critic closure evidence |
|---|---|---|---|---|---|---|
| {{finding_id}} | {{finding_owner}} | {{finding_class}} | {{finding_evidence}} | {{required_resolution}} | {{author_response}} | {{closure_evidence}} |

Assign stable IDs; keep every old finding visible across rounds. Planning severities are
`critical`, `major`, `minor`: critical/major block convergence; minor findings require
resolution or explicit acceptance with rationale. They are NOT a mapping of code-provider
severity. Dispositions are `open`, `resolved`, `accepted`; `accepted` cannot waive a
critical/major blocker. A proposed fix or rebuttal remains open until its owning critic
verifies the current bytes. Preserve owner decisions resolving genuine tradeoffs and the
critic's assessment of the resulting design; neither author, coordinator nor majority vote
can close another critic's blocker. If no findings exist, record an explicit evidence-backed
no-findings entry instead of leaving an ambiguous empty table.

### Round verdict and current-candidate attestation

- Completed at, aware UTC, or `null`: {{round_completed_at}}
- Critic result (`PASS`, `FAIL`, `INCONCLUSIVE`, or `null` before receipt): {{critic_verdict}}
- Preserved raw critic response path, revision and SHA-256: {{critic_response}}
- Exact current INTENT and RESEARCH hashes attested in that response: {{attested_hashes}}
- Completion, all-lens coverage and reused-evidence reconciliation: {{coverage_result}}
- Unresolved critical/major finding IDs: {{blocking_findings}}
- Minor finding IDs and resolved/accepted rationale: {{minor_dispositions}}
- Contradictions with original intent and their disposition: {{intent_contradictions}}
- Critic's rationale, limits and current-scope attestation: {{verdict_rationale}}
- Next permitted phase or blocked path, owner and required evidence: {{next_action}}

Only a complete independent PASS with both exact current hashes, full all-lens accounting,
critic-owned blocker closure, dispositions for all minor findings and no unresolved intent
contradiction can carry `CONVERGED`. FAIL requires revision; absent, partial, failed,
malformed or missing-coverage evidence is INCONCLUSIVE, never PASS. Preserve useful findings
from an incomplete report without treating it as completed coverage. With multiple required
critics, each supplies its own current-hash attestation and closes its own blockers before
aggregate convergence. Logis records those attestations rather than granting convergence.

Source drift invalidates current acceptance eligibility while retaining the original
verdict and its old hashes. Revise INTENT/RESEARCH, answer every finding, record new hashes
and append the critic-owned affected-scope round. Material intent changes return to intent
and discovery; material architecture/research changes return to research. After freeze,
follow [drift reconciliation](../references/handoff.md#drift-and-resume), never quietly
re-hash to manufacture continued consent. Productive revisions remain within original
attempt/review/fix bounds; oscillation, exhausted bounds or unresolved conflicts require
preserving evidence and pausing the affected path, not forcing convergence.

## Downstream gate and handoff

Only the [planning gate](../references/planning-and-design.md#mandatory-sequence-and-gate)
permits DAG/task creation: intent and actual discovery, retrieved research, written OSS
evaluation and `research.oss_library_evaluation_completed: true`, plus independent
current-hash convergence. This file's existence or a successfully delivered FAIL or
INCONCLUSIVE analysis report never opens that gate. Record planning state bindings without
claiming admitted execution or completing the campaign lifecycle.

Later product successors depend on separate **blocked native acceptance Tasks**, never
analysis-worker success. Those gates are never dispatched or made ready as work; only the
coordinator completes them with required exact-candidate independent review, API evidence,
authorized integrated-source identity and actual post-integration smoke receipts. Review,
integration and smoke bind source manifest/base/tip or preserved no-commit bytes, relevant
build/configuration and scenario version/hash; changed bytes require current proof under
[runtime and integration](../references/runtime-review-and-integration.md#exact-candidate-and-stage-ordering).
Document-only gates require assigned static evidence and an independent exact-byte document
verdict instead of invented runtime results. Native transitions belong to
[Orca runtime](../references/orca-runtime.md#acceptance-tasks-are-not-work).

Planning/document critique is distinct from substantive code review. The amended
[code-review contract](../references/code-review.md#authority-and-provider-selection) owns
roborev selection, accepted scoped qualification and per-candidate evidence requirements;
historical OCR prescriptions in unchanged policy are non-operative. Existing qualified
host/container evidence is not discarded or retried as a planning prerequisite. Qualification
alone is not a candidate PASS: fresh neutral context, immutable source/config binding,
complete coverage, raw provider/tool completion and error evidence remain mandatory for
actual code review. A critic, analysis success or this template supplies no provider fallback,
installation authority or cross-engine qualification.

Related templates: [INTENT](INTENT.md), [RESEARCH](RESEARCH.md), [PLAN](PLAN.md),
[HANDOFF](HANDOFF.md), [PLANNING_STATE](PLANNING_STATE.json) and [STATE](STATE.json).
RESEARCH is an independently owned template, not an input consumed by this source slice;
its acceptance and the four later template targets remain PENDING here. The final integrated
cross-document gate must resolve all links and reconcile fields/enums at exact hashes.
Staging changes no installed loading path, legacy skill or shared policy.

## Placeholder inventory

These names are the complete inventory; each use is wrapped in double braces. Values are
Markdown text unless a narrower format is stated. Multi-field bindings contain the fields
specified above. Unknown values are `null` with their reason, impact and resolution route.

| Names | Replacement contract |
|---|---|
| `prefix`, `campaign_name` | Unique short prefix and English lowercase campaign slug. |
| `recorded_at`, `critique_revision`, `latest_round` | Aware-UTC recording time, artifact revision and current positive round number. |
| `planning_record`, `authority_evidence`, `phase_authority`, `bounds_record` | Private ownership/model/loading pointer; immutable request/mandate evidence IDs; authorized scope/exclusions; private original-clocks and bounds pointer. |
| `round_number`, `round_opened_at`, `round_completed_at` | Positive ordered round number and aware-UTC start/completion observations; completion may be `null`. |
| `critic_record`, `packet_binding`, `request_evidence`, `required_critics` | Independent identity/read-only evidence pointer; neutral packet path/version/hash; original request evidence ID; every required critic and scope. |
| `intent_binding`, `research_binding`, `prior_round` | Each current input's snapshot path/revision/SHA-256; previous round with original bindings or evidenced initial-round declaration. |
| `evidence_id`, `evidence_path`, `source_identity`, `source_sha256`, `evidence_scope` | Stable evidence key; repository-relative immutable receipt/snapshot; revision identity; 64 lowercase hexadecimal digest; inspected scope/time/claim. Unknown identity/hash is `null`. |
| `affected_scope` | Critic-determined changed inputs, affected requirements/contracts/consumers, corrected and sibling defects, regression scope and review limits. |
| `intent_findings`, `architecture_findings`, `security_findings`, `ux_findings`, `readiness_findings` | Lens-specific evidence-backed findings or reasoned no-findings conclusion; reused scopes explicitly cite their coverage row. |
| `intent_mode`, `architecture_mode`, `security_mode`, `ux_mode`, `readiness_mode` | `inspected`, `reused`, `mixed`, or `null`; first round requires actual inspection of all lenses. |
| `intent_coverage`, `architecture_coverage`, `security_coverage`, `ux_coverage`, `readiness_coverage` | Exact inspected scopes and evidence IDs, plus prior round/input/evidence identities for any reused portion. |
| `intent_attestation`, `architecture_attestation`, `security_attestation`, `ux_attestation`, `readiness_attestation` | Critic's explicit applicability to both current hashes and reasoned non-invalidation of each reused portion. |
| `intent_limits`, `architecture_limits`, `security_limits`, `ux_limits`, `readiness_limits` | Coverage limits/missing facts and their consequences, or evidenced absence. |
| `finding_id`, `finding_owner`, `finding_class`, `finding_evidence`, `required_resolution`, `author_response`, `closure_evidence` | Stable ID; owning critic pointer; planning severity/lens; evidence/rationale; required fix; concrete response/new binding; open/resolved/accepted disposition and critic-owned closure receipt. |
| `critic_verdict`, `critic_response`, `attested_hashes`, `coverage_result` | Independent result or `null`; immutable raw response path/version/hash; both exact current digests; completion and all-lens reconciliation. |
| `blocking_findings`, `minor_dispositions`, `intent_contradictions`, `verdict_rationale`, `next_action` | Unresolved blocker IDs; minor dispositions/rationale; intent conflicts or evidence-backed absence; critic's reasoning/limits/attestation; bounded permitted next phase or blocked path. |
