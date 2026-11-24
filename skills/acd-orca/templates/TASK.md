# {{prefix}} Task: {{task_name}}

This brief consumes the frozen [PLAN](PLAN.md) and [HANDOFF](HANDOFF.md); it grants no
new authority. Procedure owners: [roles](../references/roles.md),
[handoff](../references/handoff.md), [state and recovery](../references/state-and-recovery.md),
[runtime and integration](../references/runtime-review-and-integration.md),
[code review](../references/code-review.md) and [native Orca boundary](../references/orca-runtime.md).
Shared policy stays in the [common fleet contract](../../../fleet/skills/fleet-campaign/references/common-contract.md),
not a copied persona or CLI manual here.

## Filling this template

Replace every double-brace placeholder using the inventory below; repeat rows as needed.
Remove this section and the inventory when instantiating. Rebase relative links for the
project artifact location. Store the brief as `plans/{{campaign_name}}/{{prefix}}_{{task_name}}.md`.
Evidence bindings mean repository-relative path, immutable SHA-256 and relevant section,
not a mutable filename alone. Keep actual owner/chat/Run/Task/Dispatch identities, host
paths, model routes and native receipts in private binding records, never the reusable
payload or public export. Never include credentials or hidden reasoning.

Unknown is `null`, never an empty string, zero, invented timestamp or implied success.
Record its reason, provenance, consequence and resolution route separately. Authorized
absence and inapplicability require a separate disposition and evidence; neither follows
from null. In JSON use unquoted `null`, replacing the whole quoted placeholder value if
necessary. A parsed record with a missing required binding still cannot pass acceptance.

Freeze this brief with the planning inputs. Future launch observations, candidate hashes,
results and review verdicts belong in mutable private receipts, not silent edits to a
brief already hashed by the manifest. The result example below is an output recipe, not
an existing result, a new STATE schema or native scheduler.

## Authority and input bindings

| Record | Immutable binding or private pointer |
|---|---|
| Mandate, permitted phase and steering revision | {{authority_binding}} |
| Admitted owner and execution record | {{admission_record}} |
| Accepted PLAN | {{plan_binding}} |
| Accepted HANDOFF and external manifest | {{handoff_binding}} |
| Converged INTENT, RESEARCH and complete CRITIQUE | {{design_bindings}} |
| Critic-owned current-candidate attestation and blocker dispositions | {{critique_binding}} |
| Accepted owning procedural references and amendments | {{reference_bindings}} |

The actual mandate, not a ready plan, authorizes work. Planning convergence, execution
admission, pause, task outcome, completed delivery and captain acceptance remain distinct.
No fresh-session START ceremony supplies authority. The designated coordinator owns shared
STATE/TODO/EVENTS and native operations; workers write only assigned source and evidence.
Coordinators never implement, resolve source conflicts or perform substantive code review.

For this campaign, [Amendment 1](../../../fleet/execution/fullauto/AMENDMENT_01_ROBOREV.md)
selects roborev instead of historical OCR, and
[Amendment 2](../../../fleet/execution/fullauto/AMENDMENT_02_OVERNIGHT.md)
removes the total campaign cutoff and permits bounded independent pipelining. These scoped
amendments override superseded provider/cutoff/serial prescriptions in unchanged sources;
they do not rewrite frozen historical verdicts or waive technical acceptance. Existing
provider readiness is scoped evidence, not permission to repeat bootstrap probes or to
accept a candidate without its own review. Staging changes no installed loading paths.

## Goal and scope

Observable user or runtime outcome: {{goal}}.

| Explicit source allowlist | Assigned evidence allowlist | Non-goals |
|---|---|---|
| {{source_allowlist}} | {{evidence_allowlist}} | {{non_goals}} |

One source document, or one code module plus its tests, per source assignment. Anything
not listed is out of scope, including manifests and lockfiles unless expressly assigned.
No hidden helper workers, unrelated fixes or autofix formatters. Report out-of-scope
findings without editing them. A material design/intent conflict stops the affected path
and returns through the coordinator to planning; do not redesign shared contracts locally.

| Consumed contract | Exact accepted binding and required behavior |
|---|---|
| API/interface and error semantics | {{api_contract}} |
| Schema/data, persistence and migration ordering | {{data_contract}} |
| Approved packages, versions, purpose and install rights, or explicit none | {{dependency_contract}} |
| Other shared contracts and resource boundaries | {{other_contracts}} |
| Design-to-criterion traceability, Security/abuse cases and UX journeys/states | {{traceability}} |

No ad-hoc installs, provider changes, permission bypass, global configuration, Groups,
commits, staging, push, publication or deployment are authorized by this template. The
current campaign forbids those actions. A different mandate must explicitly grant each
needed delivery operation; an unresolved right is null and blocks that operation.

## Placement, dependencies and custody

| Binding | Required record |
|---|---|
| Repository, named target and full starting SHA | {{repository_binding}} |
| Native campaign/task worktree lineage, returned branch and HEAD | {{worktree_binding}} |
| Dirty, untracked and required ignored input baseline with owner | {{baseline_binding}} |
| Original work Task, current Task/Dispatch, retry lineage and caller custody | {{assignment_binding}} |
| Source writer and exact worktree custody | {{writer_binding}} |
| Prerequisite acceptance gates and exact accepted receipts | {{dependency_gates}} |
| Independent review node and neutral packet owner | {{review_node}} |
| Required independent API inspection node, or explicit inapplicability | {{api_node}} |
| Separate product acceptance gate and successor dependencies | {{acceptance_gate}} |
| Exclusive files, schemas, APIs, lockfiles, build output, ports, fixtures, databases and effects | {{resource_exclusions}} |

Discover the installed native interface and version-matched guides; do not invent commands
or create bare Git worktrees. Record actual returned placement, not an assumed clean base.
Unknown ownership, launch or stop outcome blocks duplicate launch and resource reuse;
a possibly live writer still occupies custody and capacity. A worker reports through the
active injected Task/Dispatch, retaining the original assignment and supersession history.
Superseded Tasks are never marked PASS. Replacement mappings require native receipts.

Independent next-file authoring may overlap review of a frozen previous-file snapshot when
it consumes only accepted contracts. Never read changing siblings to infer a contract or
review changing source. Administrative/review packets may contain at most two related small
files, with separate per-file hashes, criteria and verdicts. Genuine prerequisites and
final cross-document integration remain; no generic ready-work loop may dispatch gates.

Every product acceptance Task is **blocked**, **never dispatched** and **never made ready**
as work. Only the designated coordinator completes it with all required exact-bound
review, API, integration and smoke evidence. Document gates instead require assigned static
checks and independent exact-byte document acceptance; never invent runtime evidence for
Markdown. Successors depend on this gate, not author or review-analysis Task success.
A successful report containing FAIL or INCONCLUSIVE settles analysis only, never product
acceptance. Native blocked-to-completed behavior needs actual target qualification.

## Models and execution readiness

Private requested/resolved/actual worker, reviewer and required auxiliary model records,
startup engine/version, instruction-loading evidence and effective permission scopes:
{{capability_record}}. Record Bot defaults, existing chat, engine-specific launch override
and existing-worker permissions separately; configuration and model-picker values do not
prove actual use. Missing capability stops only its dependent path, never invites a bypass.

`models.review_engine` and `tasks[].review.engine` select `roborev`, not OMP.
`models.code_review` holds binary/version, separately resolved `execution_engine`,
requested/resolved/actual model and qualification receipt/status: {{provider_record}}.
Reuse accepted scoped host/container qualification only when its environment and guards
match. No inherited Hermes/Codex or auxiliary parity, silent alternate provider, author
context reuse, setup installation or repeated readiness greeting. Document review is an
independent textual acceptance task, not a substitute code-review engine.

## Original clocks and bounded work

The authority-bound private clock record is {{bounds_record}}. Persist aware UTC absolute
times before launch, not just durations. Follow the accepted PLAN/HANDOFF field meanings:

| Field or limit | Binding semantics |
|---|---|
| `campaign_cutoff_utc` | Absolute authorized cutoff, or null plus disposition/reason/authority; `absent_by_authority` is not `unknown`. Amendment 2 establishes `absent_by_authority` here; the former cutoff is historical only. |
| `tasks[].attempt` | `label`, original `started_at`, `budget_seconds`, `checkpoint_due_at`, `deadline_at`, actual launch observation and any phase-specific `predeclared_deadline`, with history retained. |
| Attempt/checkpoint | At most 900 seconds, checkpoint at 600 seconds for this campaign. |
| Review | Separate persisted absolute review deadline, at most 600 seconds unless expressly extended beforehand within authority. |
| Iterations | At most two unproductive executions, one slice defect-fix round and at most two feature-integration fix rounds; no style-only fixes. |
| Concurrency | At most three paid working agents and at most three coders including fixes; one source writer per worktree. |
| Spend | Retain low-effort/500000-token slice and medium-effort/2000000-token final constraints by supported observation or explicit bounded reconciliation, not guessed roborev flags or silently dropped limits. |
| Longer phase | {{phase_bounds}}; predeclare its bounded completion/checkpoint evidence, never renew the slice clock. |

Unknown actual launch time remains null while the prelaunch cutoff still binds. Fixes,
retries, restarts, new sessions, model changes, reads, transport churn and late replies
never reset original clocks. No total campaign horizon does not mean unlimited attempts.
Before every affected dispatch, integration or gate completion that releases work, the
coordinator checks actual UTC against the earliest applicable finite persisted deadline,
authority, pause/revision, custody and exclusions. Ignore only a cutoff explicitly absent
by authority; an unknown required bound blocks admission. Refuse new affected work after
expiry. Workers stop source edits at their original attempt cutoff and preserve partials.

At checkpoint inspect structured criterion-bound semantic evidence and permit at most one
scoped steer if needed. Last observed activity, successful assistant response, completed
tool with outcome and semantic progress are separate facts; unknown is not healthy.
Diagnosed productive findings do not waive fix caps or deadlines. Repeated unchanged
provider/permission failure or exhausted limits stops the affected path for escalation.

Native continuation pointer: {{continuation_record}}. Use result/question/escalation wakes
and exact-owner deadline reconciliation, then end the turn when waiting. No external watcher,
mailbox polling, heartbeat emulation or background supervisor. Only the explicit mandate
permits the same-owner native continuity backstop; it creates no second owner. A queued
wake may be late and proves neither exit nor exact-time enforcement. Expiry is not a
hard-kill/restart instruction, automatic acceptance or permanent feature FAIL. Operator
pause never self-resumes; archive late output under its original revision. The coordinator
removes only obsolete owned timers at terminal/pause/true needs-owner state.

## Acceptance and real-runtime testing

Repeat rows for every required positive, negative and seam criterion. Resolve exact
commands and prerequisites on the target before dispatch; do not invent an entry point.

| Criterion and observable outcome | Production path or document static surface | Scenario ID/version/hash | Expected output, exit or state | Evidence slot |
|---|---|---|---|---|
| {{criterion}} | {{surface}} | {{scenario_binding}} | {{expected_result}} | {{evidence_slot}} |

| Exact argv or UI actions | Host/cwd, fixtures, prerequisites and cleanup | Entry-point verification | External mocks, limits and blockers |
|---|---|---|---|
| {{test_actions}} | {{test_environment}} | {{command_verification}} | {{test_limits}} |

Run narrow checks after the completed development/fix batch. Real tests exercise the
production consumer path and integration seams; UI criteria need the actual rendered
interaction. Unit/static or mock-only success does not replace runtime acceptance. Declare
external dependency mocks, never mock the feature under test. Preserve failures, including
pre-fix bug evidence; a passing rerun does not erase an earlier failure. Label synthetic
fixtures/tabletops as synthetic. Required unavailable cases remain BLOCKED or UNTESTED.
For a document-only slice use exact static checks and independent semantic review instead.

Bind every result to candidate revision, repository/base/tip where available, source/tests/
relevant dependencies and required ignored/untracked inputs, deletions/renames, SHA-256
manifest, build identity where relevant, scenario version/hash and evidence hashes. No
commit permission means exact preserved bytes and explicit not-applicable commit status,
not a fictional SHA or a demand to clean a dirty tree. Freeze only the final tested batch.

## Independent review and source validity

The coordinator commissions a fresh separate read-only context with original acceptance,
contracts, exact source/base/tip, packet/diff hashes, runtime/scenario evidence and known
findings; never an expected verdict or implementation transcript. Record whether read-only
is enforced or merely instructed. No reviewer edits, autofixes, commits, merges or pushes.
Reconcile any unknown prior review run before commissioning another for the same binding.

Every real code candidate follows the [raw coverage contract](../references/code-review.md#raw-result-and-coverage-receipt):
immutable no-hooks review-only snapshot outside the live checkout; exact source/test/
dependency inventory and original-to-snapshot mapping; fresh private session/config;
source/config/diff/tool-policy/hook guards; actual argv/cwd/timeout/exit; raw schema 3 JSON
separate from rendered output; sanitized provider stop reason/errors and required tool
results. Require complete external file-to-tool-ID-to-line-range-to-returned-content/hash
full-read reconciliation. Roborev has no native coverage certificate. Exit zero, ACP
end_turn, empty findings and exhaustive mode alone do not prove provider/tool success or
PASS. Preserve raw findings and provenance, not hidden reasoning or credentials.

`tasks[].review` records `engine`, `run_id`, `raw_output`, completion, coverage, findings,
verdict and `bound_to` exact source/base/tip/scenario. No review yet means null, not PASS.
Apply [verdict and acceptance](../references/code-review.md#verdict-and-acceptance): binding
drift INVALIDATES applicability; missing, malformed, unknown, partial, skipped, truncated,
failed, budget-stopped, zero-required-coverage or unmappable evidence is INCONCLUSIVE. A
complete valid fail or critical/high/medium acceptance/security finding is FAIL. Only valid
pass, complete nonzero coverage, successful provider/tools, preserved provenance and no
blocking findings permit PASS for that exact candidate/scenario. Low/style-only findings
do not create fix work; unknown severity is INCONCLUSIVE. Independent closure owns disputed
blocking findings; author and coordinator cannot waive them.

No routine duplicate semantic code review or silent provider substitution. Required
independent API inspection and actual runtime integration remain separate gates. A defect
fix returns the task to active work, clears current acceptance eligibility, then needs
runtime retest and fresh exact-source review within the original bounds. Re-review covers
the defect class, sibling paths and regressions. Relevant source/build/config/scenario
drift preserves old receipts as history, never relabels them for the new candidate.

## Integration, smoke and preservation

Authorized delivery route, source-to-destination composition and scope limits:
{{integration_contract}}. Exact post-integration smoke scenario/commands and actual resulting
source binding: {{smoke_contract}}. Preservation/archive and owned cleanup plan:
{{preservation_contract}}.

Persist intent before any authorized mutation. Immediately before integration recheck UTC,
mandate, pause, custody, exclusions and exact incoming/destination identities. A moved
source or destination stops the operation for reconciliation, affected runtime testing and
independent review of the new composition. The worker, never the coordinator, resolves
source conflicts within its allowlist and remaining bounds. An unknown operation result
blocks repetition; reconcile native receipts and actual bytes before any duplicate action.

With authorized commits, retain actual task tip, pre-squash destination, squash result/tree
and mapping. This campaign forbids commits: preserve starting/incoming/result manifests,
attributable diff including deletions/renames and full untracked source. If source already
resides in the authorized worktree, identify its actual composition rather than inventing
a merge. Run smoke on that resulting integrated source/build, not relabeled task tests.
Required review/API/integration/smoke bindings must all match before coordinator acceptance.
A failed smoke keeps successors blocked. Later final verification still covers the exact
complete deliverable and moved target, not just this slice's report.

Preserve recoverable source, base material, scenario definitions, raw review and runtime
results, manifests and a verified checksummed archive outside disposable workspaces before
release or disposal. A diff alone omits untracked files. Native assignment settlement,
physical process exit and resource release need separate receipts; done, silence, fencing
or a stop request is not exit. Unknown custody/stop/release blocks reuse. Retain dirty work
when safe preservation/removal is unproven; no broad clean/reset or unrelated deletion.
No cleanup removes the original feature worktree or source used by live Bots.

## Reporting and stage evidence

Assigned worker report and evidence location: {{report_record}}. Include exact candidate
identity, commands/actions and actual outputs/exits per scenario, hashes, requested/resolved/
actual model and loading evidence, failures/limits, out-of-scope findings and next work.
Give an explicit final-batch ready handoff only when its evidence exists. Ready for review
is not an independent verdict or product PASS. Report incomplete work honestly.

Copy this illustrative JSON into the assigned private report, not shared STATE. Substitute
real bindings after freezing source; parse it before handoff. The null fields mean the
worker has no independent acceptance evidence yet. Only the coordinator updates shared
acceptance records after independently checking the required receipts.

```json
{
  "task_name": "{{task_name}}",
  "assignment_record": "{{assignment_binding}}",
  "candidate_manifest_record": "{{candidate_manifest_record}}",
  "runtime_or_static_record": "{{validation_record}}",
  "out_of_scope_findings_record": "{{out_of_scope_record}}",
  "independent_review_record": null,
  "integration_record": null,
  "post_integration_smoke_record": null,
  "product_acceptance_record": null,
  "preservation_record": "{{preservation_record}}",
  "remaining_work_record": "{{remaining_work_record}}"
}
```

| Stage mirrored by coordinator into TODO | Required proof before checking it off |
|---|---|
| Development or defect fix | Completed allowlisted batch and explicit ready handoff. |
| Runtime/static validation | Current source/scenario-bound actual results; correct document-only classification. |
| Independent review and required API inspection | Exact current-candidate independent verdict and complete required evidence. |
| Authorized integration | Actual operation, input-to-result mapping and resulting manifest; no invented commit. |
| Post-integration smoke | Actual integrated source/build and scenario-bound passing result. |
| Product acceptance | Coordinator-only native blocked-to-completed receipt with matching required evidence. |
| Preservation and cleanup | Verified source/evidence archive, settlement/exit/release receipts or explicit retained resources. |

Inapplicable document-only stages receive a reasoned disposition, never fabricated runtime
PASS. Display `in-review` is not a review trigger or acceptance receipt. Follow the injected
native worker preamble: ask the coordinator and end the turn when input is required; report
a genuine blocker by escalation; send worker_done exactly once with the active Task/Dispatch
and honest delivery outcome. Follow any failed send's printed recovery. Do not mutate a
product gate, merge, push or delete source as part of reporting. After acknowledged delivery,
end this assignment; new work needs its own scoped native instruction and custody.

Companions: [TODO](TODO.md), [STATE](STATE.json) and [PLANNING_STATE](PLANNING_STATE.json).
Absent companions are PENDING during staged authoring; final cross-document integration
requires zero missing links and consistent authority/lifecycle/deadline/field meanings.
The [legacy TASK](../../acd/templates/TASK.md) is migration evidence only, not an operative
committed-tree, START, polling, provider-setup or fallback prescription.

## Placeholder inventory

Each listed name is used above; no implicit placeholders. Values are scalar text or
repository-relative immutable evidence pointers; tables may expand to cover multiple
records. JSON substitutions must be JSON-escaped strings, or the whole value becomes
unquoted null with a separate explanation when genuinely unknown. Representative values
prove syntax only. Do not put actual private bindings in this reusable template.

| Placeholder | Meaning |
|---|---|
| `{{prefix}}` | Unique campaign abbreviation. |
| `{{task_name}}` | English lowercase task slug. |
| `{{campaign_name}}` | English lowercase campaign slug. |
| `{{authority_binding}}` | Current mandate/amendments, immutable hashes, revision, phase and rights. |
| `{{admission_record}}` | Private sole-owner, Run, admission, lifecycle, pause and outcome record. |
| `{{plan_binding}}` | Accepted PLAN path/hash. |
| `{{handoff_binding}}` | Accepted HANDOFF path/hash and external manifest-binding pointer. |
| `{{design_bindings}}` | Exact INTENT/RESEARCH/complete CRITIQUE bindings. |
| `{{critique_binding}}` | Current-candidate convergence, affected-scope attestation and dispositions. |
| `{{reference_bindings}}` | Accepted procedural reference/amendment paths, hashes and affected sections. |
| `{{goal}}` | Observable delivered outcome. |
| `{{source_allowlist}}` | Exact one-document or module-plus-tests paths. |
| `{{evidence_allowlist}}` | Exact assigned evidence/report destinations. |
| `{{non_goals}}` | Explicit excluded behavior and operations. |
| `{{api_contract}}` | Accepted interface and error contract. |
| `{{data_contract}}` | Accepted schema/persistence/migration contract. |
| `{{dependency_contract}}` | Approved packages/versions/purpose/rights or evidenced none. |
| `{{other_contracts}}` | Other immutable shared contracts. |
| `{{traceability}}` | Design, Security and UX requirements mapped to criteria. |
| `{{repository_binding}}` | Private repository/named target/full starting SHA receipt. |
| `{{worktree_binding}}` | Native lineage, actual branch/HEAD and placement receipt. |
| `{{baseline_binding}}` | Owned dirty/untracked/required ignored baseline inventory and hashes. |
| `{{assignment_binding}}` | Private original/current Task, Dispatch, retry and caller identity record. |
| `{{writer_binding}}` | Exact sole-writer custody receipt. |
| `{{dependency_gates}}` | Required predecessor acceptance identities and bound receipts. |
| `{{review_node}}` | Independent review node, packet and commissioning owner. |
| `{{api_node}}` | Required API inspection node or reasoned inapplicability. |
| `{{acceptance_gate}}` | Coordinator-only blocked gate and product successor edges. |
| `{{resource_exclusions}}` | Exclusive resources, owner and release conditions. |
| `{{capability_record}}` | Actual model, loading, engine, permission and auxiliary observations. |
| `{{provider_record}}` | Scoped roborev readiness/model/engine/config qualification evidence. |
| `{{bounds_record}}` | Original aware UTC campaign/attempt/checkpoint/review clocks and counters. |
| `{{phase_bounds}}` | Prior bounded long-phase authority and evidence, or explicit none. |
| `{{continuation_record}}` | Exact-owner pending native event/deadline and removal obligations. |
| `{{criterion}}` | Criterion ID and observable acceptance outcome. |
| `{{surface}}` | Actual consumer entry point or document-only static surface. |
| `{{scenario_binding}}` | Immutable scenario ID/version/path/hash. |
| `{{expected_result}}` | Required output, exit/state and negative behavior. |
| `{{evidence_slot}}` | Assigned per-scenario evidence path. |
| `{{test_actions}}` | Verified exact argv or rendered UI interactions. |
| `{{test_environment}}` | Private host/cwd, fixtures, prerequisites and owned cleanup. |
| `{{command_verification}}` | Actual entry-point availability receipt. |
| `{{test_limits}}` | Declared external mocks, unsupported cases and blockers. |
| `{{integration_contract}}` | Authorized composition route, source/destination mapping and limits. |
| `{{smoke_contract}}` | Integrated-source smoke scenario, commands and required bindings. |
| `{{preservation_contract}}` | Recoverable archive and verified owned-resource cleanup plan. |
| `{{report_record}}` | Assigned worker report path and immutable evidence index. |
| `{{candidate_manifest_record}}` | Actual frozen source/test/dependency/base/tip/build inventory and hashes. |
| `{{validation_record}}` | Actual source/scenario-bound runtime or static results and output hashes. |
| `{{out_of_scope_record}}` | Findings outside the allowlist or explicit no-findings receipt. |
| `{{preservation_record}}` | Actual source/archive inventory and integrity receipt. |
| `{{remaining_work_record}}` | Honest pending review/integration/acceptance/cleanup and next action. |
