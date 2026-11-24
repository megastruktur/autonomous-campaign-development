# {{prefix}} Campaign Plan: {{campaign_name}}

> Create this artifact only after current-hash planning convergence under
> [planning and design](../references/planning-and-design.md#mandatory-sequence-and-gate).
> Follow [role ownership](../references/roles.md) and the existing
> [common fleet contract](../../../fleet/skills/fleet-campaign/references/common-contract.md);
> this template does not duplicate personas, grant execution authority or approve itself.

## Filling this template

Replace every double-brace placeholder using the inventory below; repeat table rows as
needed. Remove this section and the inventory when instantiating. Rebase relative links
for the actual project artifact location. Keep the plan in the repository, not chat memory.
No JSON payload is prescribed by this Markdown template; any added fenced JSON must parse
before and after representative placeholder substitution.

Unknown facts are `null`, never an empty string, zero, a guessed value or implied success.
Record the reason, consequence and resolution route. Explicit absence or inapplicability
requires a separate status and evidence, not an unexplained null. In particular, an
authorized absence of a campaign cutoff is different from an unknown cutoff; see Bounds.
Never fill a verdict, launch time, commit or native receipt slot speculatively.

Use repository-relative evidence pointers. Keep live host paths, owner/chat/Run/Task/
Dispatch identities, exact model routes and native receipts in private project bindings,
not this reusable template or public exports. Evidence pointers identify a record plus
its immutable SHA-256 and relevant section; a mutable path alone is not evidence.

## Record and mandate

- Campaign slug and unique prefix: `{{campaign_name}}` / `{{prefix}}`.
- Plan revision and aware UTC recording time: {{plan_revision}} / {{recorded_at}}.
- Original request and immutable owner-mandate evidence: {{request_evidence}}.
- Charter and steering revision identities, hashes and precedence: {{authority_evidence}}.
- Private planning ownership, designated execution owner and admission record: {{ownership_record}}.
- Verified repository identity and private location record: {{repository_record}}.
- Original named target branch and full starting SHA: {{target_branch}} / {{starting_sha}}.
- Verified campaign/task worktree custody, actual branch/HEAD and dirty/untracked baseline: {{topology_record}}.
- Frozen-input inventory and private manifest-binding record: {{manifest_record}}.

The [actual mandate](../references/handoff.md#authority-and-precedence), not a plan or
successful report, controls execution. Planning-only permission is not development
permission. No routine questionnaire, fresh-session START or extra per-task human approval
is required where the actual mandate already settles the decision. Missing authority or a
consequential unsettled choice still blocks its dependent operation. A mandate-required
fresh session remains binding; a display name proves no clean-context boundary.

Record grants separately from capabilities. Do not infer any delivery permission from
available CLI commands, provider readiness or a generic development grant.

| Operation | Explicit grant, denial or unknown | Authority revision and limits |
|---|---|---|
| Implementation, tests and independent review | {{development_permissions}} | {{authority_evidence}} |
| Integration, merge strategy and commits | {{integration_permissions}} | {{authority_evidence}} |
| Cleanup, push, publication, deployment and installation, each separately | {{delivery_permissions}} | {{authority_evidence}} |

The staged candidate remains uninstalled; this template changes no existing skill/SOUL
loading paths or legacy source. For the active campaign,
[Amendment 01](../../../fleet/execution/fullauto/AMENDMENT_01_ROBOREV.md) selects roborev,
and [Amendment 02](../../../fleet/execution/fullauto/AMENDMENT_02_OVERNIGHT.md) supersedes
older fixed-campaign-cutoff and two-paid-worker wording in accepted references. It removes
the total cutoff, permits at most three paid working agents and permits prior frozen-file
review alongside independent next-file authoring. It does not supersede technical gates,
original finite attempt clocks, one writer per worktree or delivery denials. These scoped
authorities do not grant rights to another campaign.

## Goal and scope

Observable user outcome and value:

{{goal}}

| In-scope requirement ID and outcome | Source/path allowlist | Non-goals and preserved behavior |
|---|---|---|
| {{requirement}} | {{scope_allowlist}} | {{non_goals}} |

Maintain original intent when decomposing work. No omitted capability, unreviewed scope,
architecture-driven reinterpretation or recommendation disguised as an owner request.
Record open consequential questions before dispatch; already settled choices need no
ritual reapproval.

| Decision or proposed improvement | Owner answer or accepted/rejected disposition | Evidence and affected requirement |
|---|---|---|
| {{decision}} | {{decision_disposition}} | {{decision_evidence}} |

## Converged design evidence

The [DAG gate](../references/planning-and-design.md#mandatory-sequence-and-gate) must already
be open before authoring this plan, task files or native execution Tasks. An author's
checklist, file existence or a delivered critique report cannot open it.

| Required artifact or fact | Exact immutable evidence binding |
|---|---|
| INTENT and bounded repository/interface/test discovery | {{intent_binding}} |
| RESEARCH, actually retrieved current primary sources and architecture | {{research_binding}} |
| Native/stdlib, whole-library and partial-library reuse evaluation; registry/upstream license, maintenance, security and footprint evidence | {{reuse_binding}} |
| Complete ordered CRITIQUE history and independent current-candidate attestation | {{critique_binding}} |
| Final critic-issued CONVERGED, critic/round, exact current INTENT and RESEARCH SHA-256, original request/contracts | {{convergence_binding}} |
| Every finding and critic-owned disposition; no unresolved critical/major finding or intent contradiction | {{finding_dispositions}} |
| Changed/affected-scope recheck and justified reuse of prior evidence at current hashes | {{affected_scope_binding}} |

Account for all five lenses: intent fidelity, architecture/research, Security, UX and
execution readiness. Initial critique covers every lens; on revisions the independent
critic chooses affected scope, rechecks defect siblings/regressions and explicitly attests
the applicability of reused unaffected evidence to current hashes. An author cannot waive
blockers or reuse old approval without that attestation. Planning critical/major/minor
severities do not silently map onto the code-review provider's severity schema.

Set `research.oss_library_evaluation_completed` to true in planning and campaign state
only after the live-verified evaluation is written. Preserve actual evidence for rejected
libraries and evidence-backed custom implementation decisions; do not invent research.
Material intent or architecture changes reopen the relevant planning phase and critique
within bounds, rather than quietly changing this plan.

## Traceability and shared contracts

| Task/outcome | Original intent requirement | Design decision and research IDs | Security and UX requirements | Acceptance/scenario IDs |
|---|---|---|---|---|
| {{task_name}} | {{requirement}} | {{design_sources}} | {{security_ux}} | {{acceptance_scenarios}} |

| Shared contract | Exact binding, owner and consumer obligations |
|---|---|
| API signatures, errors and compatibility | {{api_contract}} |
| Schema/data ownership, migrations and ordering | {{schema_contract}} |
| Approved packages, version constraints, purpose, license and manifest/lockfile owner, or evidenced stdlib-only policy | {{dependency_contract}} |
| Files, APIs, schemas, manifests/lockfiles, build outputs, ports, fixtures, databases and external effects | {{resource_contract}} |

Settle contracts centrally; sibling workers consume them, not redesign them. No ad-hoc
package installation. Serialize manifest/lockfile updates through a prerequisite owner or
exclusive ownership. Distinct branches do not isolate shared databases, outputs or effects.

## Work and acceptance DAG

Each task has its own durable brief with goal, allowlist, non-goals, dependencies, exact
shared contracts, acceptance criteria and actionable runtime/static validation. Size the
slice for the resolved worker model. For this campaign use one document, or one code module
plus its tests, per source assignment; no hidden helper fanout. Coordinators do not write
source or resolve source conflicts.

| Product slice | Work node and brief binding | Independent review node and packet | Required API inspection node | Separate acceptance gate | Product successor depends on | Exclusive resources/worktree |
|---|---|---|---|---|---|---|
| {{task_name}} | {{work_node}} | {{review_node}} | {{api_node}} | {{acceptance_gate}} | {{dependency_gates}} | {{task_resources}} |

Node values here are logical labels plus private binding pointers, not portable native
IDs. Record an inapplicable API inspection with rationale; unknown is `null`. A separate
native acceptance Task stays **blocked**, is **never dispatched** and is **never made ready**
as work. Only the designated coordinator sets it completed, after its required exact-bound
evidence passes. Product successors depend on this gate, never on worker or review-analysis
Task success. Native behavior must be qualified on the actual target; writing this table
does not prove those transitions.

For implementation, the gate requires independent exact-candidate review, required API
evidence, authorized integration and actual post-integration smoke on the resulting source.
For document-only slices, require assigned static evidence plus independent exact-byte
document acceptance; do not fabricate runtime evidence or use that verdict as code readiness.
A successful report containing FAIL or INCONCLUSIVE settles analysis only, not the product
prerequisite. Provider qualification and author self-review cannot complete acceptance.

Available parallel work, subject to dependencies and exclusions: {{parallel_view}}.
This is not a fixed-wave barrier. Remove an artificial serial edge only under authority,
when the next file consumes accepted contracts rather than changing/unaccepted siblings.
Preserve original-to-replacement node mapping and separate per-file verdicts; superseded
Tasks never become PASS. Group administrative/review packets for at most two related small
files, retaining each original slice and exact-hash acceptance. Review a frozen previous-file
snapshot, never the file currently being authored; final cross-document integration still
waits for its genuine dependencies.

## Models and execution-host readiness

Retain requested, resolved and actual observations separately under
[model identity](../references/handoff.md#model-and-review-identity). A permitted `default`
means the actual runtime/profile default, resolved and pinned with evidence, never an
orchestrator-selected substitute. Startup/configuration presence is not proof of actual
purpose-specific model/tool success. Missing evidence stays `null`; a mismatch blocks the
affected path. Actual observations after plan freeze belong in mutable private receipts,
not edits to this frozen plan.

| Purpose | Private requested/resolved/actual model and authority record | Loading/startup/purpose evidence or blocker |
|---|---|---|
| Implementation | {{implementation_model_record}} | {{capability_record}} |
| Planning and independent critique/document review | {{planning_model_record}} | {{capability_record}} |
| Code review and optional final review, each separately | {{review_model_record}} | {{provider_record}} |
| Auxiliary purposes actually used; disabled optional roles distinguished from unknowns | {{auxiliary_model_record}} | {{capability_record}} |

Record approved alternative-selection policy or explicit absence in {{selection_policy}}.
It is not an automatic fallback. Primary-model failure or permission denial stops the
affected path for diagnosed reconciliation; no silent route switch, blind retry, broader
permission or duplicate writer. No model vendor is hardcoded by this template.

The selected provider is `roborev`: `models.review_engine` and `tasks[].review.engine`
name the provider, not OMP. `models.code_review` records binary/version, independently
resolved `execution_engine`, requested/resolved/actual model, qualification status and
exact receipt. `tasks[].review` uses `run_id`, `raw_output`, completion, coverage, findings,
verdict and `bound_to`; unknowns are `null`. Do not retain operative OCR field aliases or
provider/session fallback. The historical OCR choice is superseded, not qualified.

The private provider record must bind the existing accepted host/container qualification
and its limitations, not repeat bootstrap probes or infer portable parity. Scoped qualified
OMP use does not establish Hermes/Codex or auxiliary readiness. Before dependent coding,
verify applicability to the actual execution host and resolve any genuine qualification
change under [code review](../references/code-review.md). Documentation acceptance needs
no code-tool qualification and does not itself qualify one.

The capability record binds instruction loading, executable/version, discoverable session
and output, actual tool calls, native result/one-shot wake handling and separate permission
scopes: Bot defaults, existing chat, engine-specific launch override and existing workers.
One scope does not migrate another. Read installed version-matched
[Orca mechanics](../references/orca-runtime.md); do not copy guessed flags, install packages,
change global configuration or claim unattended/reboot resilience from a status file.

## Acceptance and real-runtime plan

| Criterion ID and observable outcome | Production path or document-only static surface | Scenario ID/version and immutable hash | Expected result, including negative behavior | Evidence destination |
|---|---|---|---|---|
| {{acceptance_criterion}} | {{production_path}} | {{scenario_binding}} | {{expected_result}} | {{evidence_destination}} |

| Actual command/action sequence | Execution host, cwd, fixtures, prerequisites and cleanup | Entry-point existence verification | Known mocks, limits and blockers |
|---|---|---|---|
| {{runtime_commands}} | {{runtime_environment}} | {{command_verification}} | {{runtime_limits}} |

Before dispatch, resolve every command honestly on target. Record exact argv or UI actions,
expected exit/output/state, test data and resource ownership. Real-runtime scenarios must
exercise the production consumer path and integration seams, not just mocks or a green unit
suite. Unit/static tests are supplemental. Documentation uses static checks and semantic
review; synthetic tabletop expectations are explicitly synthetic, never runtime PASS.
Record unavailable required scenarios as BLOCKED or UNTESTED, not silently narrowed coverage.

## Candidate evidence and review contract

Keep per-task evidence in {{evidence_record}}. Every result binds exact repository/base/tip
where available, source/test/relevant-dependency inventory and SHA-256 manifest, required
ignored/untracked inputs, deletions/renames, build identity where relevant, scenario version
and hash, evidence identity and candidate revision. A missing commit is not filled with a
fictional SHA: for no-commit delivery use preserved byte manifests and explicit not-applicable
commit status. Freeze only completed runtime-tested source, not an intermediate author
handoff. Relevant source, build, config or scenario drift invalidates applicable eligibility;
retain historical results at their original bindings.

| Stage | Binding required in its immutable receipt |
|---|---|
| Runtime | Exact source/build and scenario inputs, verified commands/environment, actual outputs/exits/state, failures, time and evidence hashes. |
| Independent review | Original acceptance/contracts, neutral packet and diff hashes, exact frozen source/base/tip/scenarios, fresh separate reviewer context, provider/model/config/tool-policy identity, raw findings and completion. |
| Authorized integration | Intent, starting destination and reviewed incoming manifests, operation and source-to-result mapping, resulting manifest/tree; actual squash receipt only where commits/merges are authorized. |
| Post-integration smoke | Actual resulting integrated source/build, scenario version/hash, commands, outputs and outcome; never task-source tests relabeled as integrated smoke. |
| Coordinator acceptance | Matching review/integration/smoke and required API receipts, current hashes, authority, UTC/deadline check and native gate transition receipt. |

Each real code candidate requires the full
[raw result and coverage contract](../references/code-review.md#raw-result-and-coverage-receipt):
immutable no-hooks review-only snapshot outside the live checkout, fresh neutral context,
source/config/diff/hook guards, original schema 3 JSON separately from rendered output,
sanitized provider completion/errors and required tool results, plus external complete
file-to-tool-ID-to-line-range-to-returned-content/hash reconciliation. Roborev provides no
native complete-coverage certificate; exit zero, ACP end_turn, empty findings and exhaustive
mode do not prove PASS. Operational tool restriction is not OS sandbox confinement.

The coordinator derives the result from independent evidence under
[verdict and acceptance](../references/code-review.md#verdict-and-acceptance): binding drift
is INVALIDATED; missing, malformed, partial, skipped, failed, budget-stopped, unknown or
zero-required-coverage evidence is INCONCLUSIVE. A valid fail or critical/high/medium
acceptance/security finding is FAIL. Only valid pass, full nonzero coverage, successful
provider/tools, complete preserved provenance and no blocking findings permit PASS for
that exact candidate/scenario. Unknown severity is INCONCLUSIVE; low/style findings do not
create fix work. Preserve raw findings and independent dispositions. No routine second
semantic code review or silent alternate provider; API inspection and runtime remain
distinct obligations. Author completion never substitutes for independent acceptance.

## Bounds and native continuation

Private authority-bound limits and original absolute clocks: {{bounds_record}}.

| Field or policy | Required meaning |
|---|---|
| `campaign_cutoff_utc` | An authorized absolute aware UTC cutoff, or `null` with separate cutoff disposition, reason and authority binding. |
| Cutoff disposition | `absent_by_authority` means no total horizon was authorized; `unknown` means admission is blocked until resolved. For this campaign Amendment 02 establishes `absent_by_authority` and `campaign_cutoff_utc: null`; the removed cutoff is historical only. |
| `tasks[].attempt` | `label`, original `started_at`, `budget_seconds`, persisted `checkpoint_due_at`, `deadline_at`, actual launch observation and any phase-specific `predeclared_deadline`; preserve history. |
| Attempt and checkpoint | At most 900 seconds and checkpoint at 600 seconds for this campaign; record original absolute times before launch, not just durations. |
| Independent review | At most 600 seconds per review unless a prior bounded extension is expressly authorized; never a retrospective extension. |
| Productive and unproductive work | At most two unproductive executions; one slice defect-fix round and at most two feature-integration fix rounds. Useful findings do not authorize unlimited iterations. |
| Spend | Preserve inherited low-effort/500000-token slice and medium-effort/2000000-token final constraints with supported observation or explicit bounded reconciliation. No guessed roborev flags, silently dropped controls or broadening. |
| Concurrency | Maximum three paid working agents across this campaign and maximum three coding agents including fixes; no hidden fanout. One source writer per worktree; a possibly live writer retains custody/capacity until reconciled. |
| Predeclared long phase | {{long_phase_bounds}}; a bounded build/test phase never renews the slice clock or grants new affected work beyond its applicable deadline. |

An unknown actual launch time stays `null` while the prelaunch absolute cutoff remains
binding. Fixes, retries, restarts, model/session changes, log churn, repeated reads and late
receipts never reset original attempt clocks. Genuine retry launch observations are separate
from inherited bounds. No total campaign cutoff does not mean an unlimited attempt.

Before every affected dispatch, integration or gate completion that releases work, read
actual UTC and check the earliest applicable persisted finite deadline, current authority,
pause/revision, custody and exclusions. Ignore only a cutoff explicitly absent by authority;
never ignore an unknown one. Refuse new affected work after expiry. At checkpoint inspect
correlated semantic progress and issue at most one scoped steer if needed. Transport bytes,
PID activity, assistant response, completed tool and semantic progress remain distinct;
unknown is not healthy.

Use native results/questions/escalations and exact-owner deadline reconciliation under
[state and recovery](../references/state-and-recovery.md#native-continuation-and-original-clocks).
Persist the pending event/one-shot receipt before ending the turn. Any campaign-level native
continuity backstop requires the specific mandate, same-owner routing and terminal-state
cleanup; it is not a second owner or a shell polling loop. A queued deadline may be late:
it reconciles rather than guaranteeing exact-time enforcement, proving exit or authorizing
kill/restart. No active watcher, heartbeat emulation, mailbox consumer or ten-minute polling
prescription belongs in this plan.

Pause blocks new affected dispatch/integration and never self-resumes. Archive late output
under its original revision. Unknown launch or stop outcome blocks duplicate launch and
resource reuse; settlement, process exit and release are separate facts. After diagnosed
unproductive attempts exhaust the bound, preserve work and escalate rather than retrying
unchanged. Follow native guarded settlement, not a hard-expiry automatic restart.

## Integration and delivery

Authorized integration/delivery route and exact receipt destinations: {{integration_record}}.

Follow [runtime review and integration](../references/runtime-review-and-integration.md).
For an authorized new topology, campaign root derives from the original named target branch;
task worktrees are Orca children based on the recorded campaign branch, with returned
branch/HEAD checked. Reuse existing worktrees only with mandate and verified custody/baseline.
No raw-SHA branch-base shortcut or direct task-to-target merge. Integration is serialized;
source conflict resolution belongs to a bounded worker, never the coordinator.

For the current no-commit mandate, preserve attributable diffs plus untracked source,
starting/incoming/result manifests and original-to-result mapping. If source already lives
in the authorized worktree, freeze that actual composition instead of inventing a merge.
No commits, staging, install or target merge are implied. Where a different mandate
explicitly grants commits and integration, retain squash source/pre-destination/result SHA
and tree; final merge strategy is the one actually authorized, not a template default grant.

Final acceptance requires all criteria and seam runtime scenarios on the exact integrated
delivery candidate, independent final exact-source review, moved-target reconciliation,
and current ref/source checks before any authorized final operation. Changed composition
requires worker fixes, retesting and fresh applicable review. Smoke the actual target only
when a target operation occurred; otherwise smoke the authorized delivery snapshot and
explicitly record that no target merge occurred. Document-only final gates use their
assigned complete static/cross-document checks and independent exact-manifest verdict.

Preserve recoverable source, base material, diff and untracked files, immutable manifests,
runtime/review/API/integration/smoke receipts and a checksummed archive outside disposable
workspaces before cleanup or release. Verify inventory and recoverability. A settled Task
does not prove resource release; preserve the only runnable source until delivery is
verified. Retain dirty or unproven resources and report the blocker, never delete evidence
to make cleanup look complete. Push, publication, deployment and installation remain
separate grants. Ready-for-captain is not captain acceptance.

## Durable artifacts and lifecycle

Private operational record map and remaining unknowns: {{operational_records}} / {{remaining_unknowns}}.

Use `plans/{{campaign_name}}/` with `{{prefix}}_PLAN.md`, `{{prefix}}_INTENT.md`,
`{{prefix}}_RESEARCH.md`, complete `{{prefix}}_CRITIQUE.md`, `{{prefix}}_HANDOFF.md`,
every task brief and standalone shared contract. The handoff manifest freezes those exact
bytes and immutable authority revisions. Exclude the manifest itself and mutable planning
state, STATE, TODO, EVENTS and execution evidence. Record the finished manifest digest
privately outside the HANDOFF it hashes; avoid recursive hashes. Unknown future execution
facts are added to mutable receipts, not the frozen plan. Drift stops affected work for
reconciliation and a separately identified authorized manifest, never silent re-hashing.

Lifecycle distinguishes planning, admitted execution and completed delivery. Keep mandate,
convergence, admission, pause, failed/blocked/cancelled outcomes and captain acceptance
separate; no obsolete fresh-session lifecycle is operative. The planning writer owns
canonical planning records; designated execution owner alone writes shared operational
state and mirrors only verified stages into TODO. Reports retain PASSED, BLOCKED and
UNTESTED outcomes, exact deliverable identity, reproducible commands, residual findings,
retained resources and next actual action. Successful reporting is not product PASS.

Companion templates: [INTENT](INTENT.md), [RESEARCH](RESEARCH.md), [CRITIQUE](CRITIQUE.md),
[HANDOFF](HANDOFF.md), [TASK](TASK.md), [TODO](TODO.md),
[PLANNING_STATE](PLANNING_STATE.json) and [STATE](STATE.json).
During staged authoring, absent companions are PENDING, not resolved-link or acceptance
claims. Do not read changing/unaccepted siblings to infer their contract; owning accepted
references govern. Final integration must reconcile all field meanings, exact evidence
bindings and lifecycle/authority/deadline semantics, with zero missing links.

## Placeholder inventory

Each listed name is used inside double braces above. IDs, pointers and record names below
are logical portable labels, not live runtime identities; concrete private observations
belong only in the project bindings. Use a syntactically valid representative value for
each name during static validation, without claiming that substitution is real evidence.

| Names | Required replacement |
|---|---|
| `prefix`, `campaign_name` | Unique short prefix and English lowercase campaign slug. |
| `plan_revision`, `recorded_at` | Plan revision and aware UTC timestamp. |
| `request_evidence`, `authority_evidence` | Immutable original request and actual mandate/steering record pointers, hashes and sections. |
| `ownership_record`, `repository_record`, `topology_record`, `manifest_record` | Private ownership/admission, repository identity, verified custody/baseline and frozen-manifest binding records. |
| `target_branch`, `starting_sha` | Verified original named branch and full starting SHA; never an assumed default branch. |
| `development_permissions`, `integration_permissions`, `delivery_permissions` | Separately evidenced grants, denials or unknowns for every named operation. |
| `goal`, `requirement`, `scope_allowlist`, `non_goals` | Observable outcome, original requirement ID, explicit paths and excluded/preserved behavior. |
| `decision`, `decision_disposition`, `decision_evidence` | Consequential choice or improvement, actual disposition and provenance. |
| `intent_binding`, `research_binding`, `reuse_binding`, `critique_binding`, `convergence_binding`, `finding_dispositions`, `affected_scope_binding` | Exact source/evidence hashes, current independent convergence and all-lens finding/reuse attestations. |
| `task_name`, `design_sources`, `security_ux`, `acceptance_scenarios` | Task slug and traceability to design sources, Security/UX requirements and scenario IDs. |
| `api_contract`, `schema_contract`, `dependency_contract`, `resource_contract` | Settled shared interfaces, schema/order, approved dependencies/licenses and exclusive ownership. |
| `work_node`, `review_node`, `api_node`, `acceptance_gate`, `dependency_gates`, `task_resources`, `parallel_view` | Work/review/API labels and evidence, blocked gate/dependency map, resource/worktree allocation and non-wave parallel view. |
| `implementation_model_record`, `planning_model_record`, `review_model_record`, `auxiliary_model_record`, `selection_policy` | Private requested/resolved/actual purpose evidence and authorized selection or explicit absence. |
| `capability_record`, `provider_record` | Actual host loading/permissions/native receipts and scoped provider qualification identity, status, hash and limits. |
| `acceptance_criterion`, `production_path`, `scenario_binding`, `expected_result`, `evidence_destination` | Observable acceptance, real path or static surface, version/hash, expected positive/negative behavior and receipt destination. |
| `runtime_commands`, `runtime_environment`, `command_verification`, `runtime_limits` | Verified actual commands/actions, prerequisites/cleanup, existence evidence and mocks/unknowns/limits. |
| `evidence_record`, `bounds_record`, `long_phase_bounds`, `integration_record`, `operational_records`, `remaining_unknowns` | Private per-stage evidence, absolute-clock/spend authority, prior phase bounds or evidenced absence, integration route, operational pointers and unresolved facts/consequences/routes. |
