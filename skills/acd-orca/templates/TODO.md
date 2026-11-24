# {{prefix}} Campaign TODO

> Coordinator-owned projection of `{{prefix}}_STATE.json`, not a scheduler or a source
> of authority. A checked box requires current bound evidence, never a promise, display
> status or worker report alone. Rebuild this projection from reconciled STATE after
> recovery; absence of a todo-list tool does not remove the durable checklist.

## Filling and ownership

Replace every double-brace placeholder from the inventory; repeat the task block for
**each original slice**, even when administration or review is grouped. Remove this
section and the inventory in the instantiated checklist. Rebase relative links for its
project location. Use repository-relative evidence paths with SHA-256 and relevant
section, plus source/scenario identities; a mutable filename alone is not a binding.
Keep actual host paths, owner/chat/Run/Task/Dispatch IDs and model routes in private
records, not in reusable templates or public exports. Never store secrets or hidden
reasoning here.

The designated execution-owner chat alone writes STATE, TODO, EVENTS and native campaign
decisions. Workers write only assigned source/evidence; independent reviewers own their
verdicts. Logis owns PLANNING_STATE; TODO does not become a second planning writer.
Follow [roles](../references/roles.md) and the linked shared policy rather than copying
personas. Coordinators do not implement, resolve source conflicts or perform substantive
code review. Native receipts establish native operations; reconcile contradictions with
STATE rather than overwriting either history.

Unknown is `null`, not an empty string, zero, a guessed timestamp or success. Record
reason, provenance, observation time and acceptance consequence separately. An empty
findings list or evidence array is not proof of coverage or PASS. Authorized absence and
inapplicability need explicit reason and authority; they do not follow from null. In JSON
use unquoted null, replacing the whole quoted placeholder value when necessary.

## Campaign projection and authority

| Record | Current binding or private pointer |
|---|---|
| Project and campaign | {{campaign_name}} |
| STATE revision, owner, update event and aware UTC timestamp | {{state_record}} |
| Actual mandate, permitted phase and amendment hashes | {{authority_binding}} |
| Planning provenance, admitted owner/Run and execution receipt | {{admission_record}} |
| Frozen INTENT/RESEARCH/CRITIQUE/PLAN/HANDOFF/task/shared-contract manifest | {{input_manifest_record}} |
| Requested/resolved/actual models, loading and purpose-specific qualification | {{model_record}} |
| Named target/base, actual branch/HEAD, placement and worktree custody | {{topology_record}} |
| Lifecycle, explicit pause, task outcome, delivery outcome and captain decision | {{lifecycle_record}} |
| Original clocks, phase/review bounds and current admission checks | {{bounds_record}} |
| Pending native operation/question/deadline and exact-owner continuation | {{continuation_record}} |
| Unresolved blockers, affected descendants and next authorized action | {{blocker_record}} |

Planning convergence, admitted execution and completed delivery are distinct facts;
pause is orthogonal. Preserve the canonical lifecycle rather than introducing a TODO
lifecycle. Ready-for-captain is not captain acceptance. A fresh-session START ceremony,
analysis success or a ready plan supplies no authority. Mutable STATE/TODO/EVENTS and
new execution evidence are not silently added to or rehashed into the frozen inputs.
Input drift blocks affected work until authorized reconciliation.

For this campaign, [Amendment 1](../../../fleet/execution/fullauto/AMENDMENT_01_ROBOREV.md)
selects roborev and [Amendment 2](../../../fleet/execution/fullauto/AMENDMENT_02_OVERNIGHT.md)
removes the total campaign cutoff and permits bounded independent pipelining. These
scoped amendments override historical provider, cutoff and artificial serial prescriptions
in unchanged references; frozen historical verdicts remain unchanged. Staging changes no
installed loading paths. See [handoff](../references/handoff.md) for admission and
[state and recovery](../references/state-and-recovery.md) for durable ownership.

## Admission checklist

- [ ] Actual authority and delivery grants/denials verified; no inferred commit, install,
      push, publication or deployment permission.
- [ ] Bounded discovery, live research/reuse evidence and critic-owned current-hash
      convergence verified before the accepted DAG; affected-scope attestations are bound.
- [ ] Input manifest hashes match the accepted design, PLAN, HANDOFF, task briefs and
      shared contracts; observed drift is reconciled, not quietly rehashed.
- [ ] Sole execution ownership, native Run/assignment custody, named repository target,
      full starting SHA and actual Orca worktree branch/HEAD receipts verified.
- [ ] Engine instruction loading, discoverable session/output, four permission scopes and
      requested/resolved/actual models verified for each required purpose; unknowns block
      only dependent claims and paths, not by invented healthy defaults.
- [ ] Required code-review provider readiness bound to its accepted host/configuration
      scope; roborev qualification retained without repeating bootstrap probes.
- [ ] Original absolute bounds and spend/resource exclusions persisted; actual UTC,
      authority, pause, revision and custody checked before affected work.
- [ ] Separate blocked coordinator acceptance Tasks exist, never made ready or dispatched
      as work; product successors depend on those gates, not worker/analysis Task success.
- [ ] Native result-wake and bounded exact-owner recovery continuation recorded; capability
      and actual wake evidence kept distinct from configuration presence.

Admission is not product acceptance. A document-only slice uses its specified static
checks and independent exact-byte document review; code-tool qualification is not a
new prerequisite for that document verdict.

## Original clocks and bounded continuation

The bounds record preserves `campaign_cutoff_utc` with its disposition and authority.
Under Amendment 2 its value is null with `absent_by_authority`; a null **unknown** cutoff
is different and cannot authorize work. The former cutoff is historical only.
`tasks[].attempt` retains `label`, original `started_at`, `budget_seconds`,
`checkpoint_due_at`, `deadline_at`, actual launch observation and phase-specific
`predeclared_deadline`, with attempt history. Unknown actual launch time stays null while
the prelaunch absolute cutoff still binds.

Current limits: attempt at most 900 seconds, checkpoint at 600 seconds, review at most
600 seconds unless an expressly authorized bounded extension precedes it; at most two
unproductive executions, one slice defect-fix round and two feature-integration fix
rounds. No style-only revisions. Maximum three paid working agents and three coders
including fixes; one source writer per worktree. Independent next-file authoring may
run alongside review of an immutable previous-file snapshot, never review of changing
source. Group at most two closely related small documents administratively, retaining
separate per-file verdicts and actual prerequisite edges.

Retain low-effort/500000-token slice and medium-effort/2000000-token final constraints
through supported observation or explicit bounded reconciliation; do not invent tool
flags or silently drop limits. Longer phases need predeclared absolute bounds and
completion/checkpoint evidence, not retrospective extensions.

Before **every affected dispatch, integration or gate completion releasing work**, check
actual UTC against the earliest applicable finite persisted deadline plus current
mandate, pause/revision, ownership and exclusions. Ignore only a cutoff explicitly absent
by authority; an unknown required bound blocks admission. Refuse new affected work after
expiry. Workers stop source edits at their original attempt cutoff and preserve partials.
Fixes, retries, new sessions, reads, provider changes and late replies never reset clocks.
At checkpoint inspect structured criterion-bound progress and permit at most one scoped
steer if needed. Productive findings do not waive the numerical limits.

Native result/question/escalation wakes and exact-owner deadline reconciliation provide
continuation; end the turn while waiting. Only explicit authority permits a same-owner
native continuity backstop. No mailbox polling, external watcher, heartbeat emulation or
background supervisor. A queued wake can arrive late; it proves neither exact-time
interruption nor physical exit. Expiry is not automatic acceptance, a hard-kill/restart
instruction or permanent feature FAIL. Operator pause never self-resumes. Unknown launch
or `stop_unknown` blocks replacement and resource reuse; follow guarded settlement in
[state and recovery](../references/state-and-recovery.md#guarded-settlement-and-duplicate-prevention).

## Per-slice checklist

### {{prefix}}-{{task_name}}

Projection label: {{task_projection}}. Labels here are human summaries, not new native
Task or STATE enums: **pending** means no proven start, **working** means current assigned
work with its native binding, **report delivered** means only a settled report outcome,
and **accepted** requires the coordinator's eligible gate receipt. FAIL/INCONCLUSIVE can
be a successfully delivered analysis report while product acceptance stays blocked.
Record failure, pause, expiry, supersession and unresolved launch separately; never label
a superseded original Task PASS because a replacement was wired.

| Required record | Exact binding or null with reason |
|---|---|
| Original slice, accepted TASK brief, Task/Dispatch/retry and worker custody | {{assignment_record}} |
| Separate native acceptance gate, predecessor gates and successor edges | {{gate_record}} |
| Scope allowlist, non-goals, shared contracts and exclusive resources | {{scope_record}} |
| Current source/test/dependency/config manifest and candidate revision | {{candidate_record}} |
| Final-batch ready handoff and requested/resolved/actual model/loading evidence | {{ready_record}} |
| Runtime or document-static commands, actual output/exits and scenario identities | {{validation_record}} |
| Independent review packet, raw output, coverage, findings and verdict | {{review_record}} |
| Required independent API/contract inspection or evidenced inapplicability | {{api_record}} |
| Authorized integration intent, before/input/result mapping and resulting manifest | {{integration_record}} |
| Actual post-integration source/build/scenario and smoke result | {{smoke_record}} |
| Coordinator gate-completion receipt and exact evidence set | {{acceptance_record}} |
| Durable source/evidence archive and verified recovery inventory | {{preservation_record}} |
| Settlement, physical exit, native release/removal and retained resources | {{cleanup_record}} |
| Observed/assistant/tool/semantic-progress facts and pending operation | {{progress_record}} |
| Findings, affected dependents, remaining work and next action | {{remaining_work_record}} |

- [ ] Develop or fix the allowlisted batch; explicit final ready handoff preserved.
- [ ] Run assigned real production-path scenarios on the current candidate, or assigned
      static checks for a document-only slice; record failures, limits and actual results.
- [ ] Freeze source/tests/relevant dependencies/configuration and neutral review packet;
      obtain complete independent exact-candidate verdict and required API evidence.
- [ ] Integrate only the reviewed bytes through the authorized operation; preserve the
      input-to-result mapping and resolve source conflicts through a bounded worker.
- [ ] Smoke the actual integrated campaign source/build with the bound scenarios.
- [ ] Preserve source and evidence before any disposal; archive hashes and recoverability
      verified outside every disposable worktree.
- [ ] Coordinator alone completes the separate blocked acceptance gate after all required
      evidence passes; native receipt and released successor edges recorded.
- [ ] Cleanup actually verified; unresolved or deliberately retained resources listed,
      never checked off as removed. Reuse waits for proven release and custody.

For document-only slices, inapplicable runtime/integration stages need reasoned explicit
dispositions; leave their boxes unchecked and mark them not applicable, never fabricate
runtime PASS. Their document gate needs the assigned static receipt, independent exact-byte
PASS and preserved file/hash. A document verdict cannot open a code-product gate.
For code, review, required API evidence, authorized integration and actual post-integration
smoke must all match the candidate before acceptance. Dependencies release on coordinator
acceptance, never on worker_done, provider readiness, expiry or author self-review.

## Evidence and invalidation rules

The candidate manifest inventories source, tests, relevant dependencies/configuration,
deletions, renames, untracked and required ignored inputs with exact hashes. Each result
binds repository/base/tip where available, candidate manifest/revision, build when relevant,
scenario version/hash and its own immutable evidence identity. No-commit delivery uses
preserved exact bytes, attributable diffs and manifests, not invented commits. If source
already occupies the authorized worktree, identify the actual composition rather than
inventing a merge. Follow [runtime and integration](../references/runtime-review-and-integration.md).

`models.review_engine` and `tasks[].review.engine` select `roborev`, not its execution
engine. `models.code_review` retains binary/version, independently resolved
`execution_engine`, requested/resolved/actual model and qualification evidence/status.
Each `tasks[].review` records `run_id`, `raw_output`, completion, coverage, raw findings,
verdict and `bound_to` exact source/base/tip/scenario identity. No review yet is null.

[Code review](../references/code-review.md) owns the per-candidate protocol: immutable
no-hooks snapshot outside the live checkout, fresh neutral context/configuration, exact
source/config/diff/tool-policy/hook guards, raw schema 3 findings, sanitized provider stop
and error evidence, successful tool results and external complete file-to-tool-ID-to-line-
range-to-returned-content/hash reconciliation. Scoped qualification is retained, not a
candidate coverage certificate. Exit zero, ACP `end_turn`, empty findings or a file count
alone never establish PASS. Missing/malformed/partial/failed/skipped/unknown/truncated or
zero-required coverage is INCONCLUSIVE; critical/high/medium acceptance or security
findings block; low/style alone does not. No silent provider replacement or session fallback.

Changed source, relevant configuration, build or scenario invalidates affected results
and current gate eligibility. Preserve historical verdicts with their original bindings;
drift makes their applicability INVALIDATED, not retroactively FAIL or PASS. A fix returns
the slice to work, then retest and fresh independent changed/affected-scope review,
including sibling defect paths and regressions. Reused unaffected evidence needs explicit
current-candidate attestation where permitted, never automatic carryover. Clear checked
stages no longer supported by the current candidate; preserve their prior history in
STATE/EVENTS. Display `in-review` is not a review trigger. Bounded diagnosed iterations
replace an unlimited test/review loop; unchanged provider/permission failure stops the
affected path without unauthorized retries or model switches.

Keep `last_observed_at`, `last_successful_assistant_at`, `last_completed_tool_at` with
separate tool outcome, and `last_semantic_progress_at` distinct. Streams, process presence,
log growth or a successful model response are not task progress. Only a validated
criterion-bound structured checkpoint proves semantic progress; stale or unknown is not
healthy. Preserve pending intent/request/retry identities before reconciling lost receipts;
never duplicate a launch, integration, stop or timer merely to obtain clearer output.

## Final campaign checklist

Final evidence and remaining action record: {{final_record}}.

- [ ] Every original slice has an accounted outcome, current stage evidence, blocker
      dispositions and the required separate acceptance receipt; no superseded false PASS.
- [ ] Full campaign acceptance and integration-seam scenarios exercised on the exact final
      source/build; document-only delivery instead has its final static/cross-document gate.
- [ ] Independent final review covers that exact final candidate and complete required
      surface; per-slice PASS is not a substitute. All template links resolve at this gate.
- [ ] Original named target rechecked; any movement reconciled without clobbering user
      changes, with affected tests/review repeated on the new composition within authority.
- [ ] Expected refs/source manifests and deadlines checked immediately before the authorized
      final operation. A final merge uses only the recorded grant/strategy; otherwise retain
      the authorized no-commit delivery snapshot and explicitly record no target merge.
- [ ] Post-final-operation smoke runs on the actual target or authorized delivery snapshot,
      with exact source/build/scenario binding; campaign-tree smoke is not target smoke.
- [ ] Source, attributable diffs and untracked files, scenarios, failures, raw review,
      integration/smoke receipts and checksummed archive preserved and recoverable outside
      disposable worktrees. Keep the only runnable source until delivery is verified.
- [ ] Exact owned assignments settled; physical exit, scoped test processes/ports and
      native release/removal verified. Dirty/untracked source rescued or cleanup blocked.
- [ ] Only obsolete owned timers removed/disabled at terminal, pause or true needs-owner
      state; queued stale wakes ignored. No removal of unrelated or retained live resources.
- [ ] `{{prefix}}_REPORT.md` records exact deliverable identity, exercised commands,
      requirement-by-requirement PASSED/BLOCKED/UNTESTED, limits, retained resources and next
      work. Completed delivery and final captain decision remain separate evidence.

Push, publication, deployment, installation, Groups and global configuration are not
implicit final stages. Do not dispose of the current retained feature worktree, installed
skill/Bot sources or the only runnable pilot merely because a checklist reached its end.

## Companions and staged validation

Use accepted [PLAN](PLAN.md), [HANDOFF](HANDOFF.md), [TASK](TASK.md) and
[PLANNING_STATE](PLANNING_STATE.json); [STATE](STATE.json) is PENDING until its separately
owned slice is authored and accepted. Final integration requires zero missing links and
consistent field meanings, authority, lifecycle, clocks and evidence across the complete
candidate. This template defines no new STATE schema and contains no executable scheduler.
The [legacy TODO](../../acd/templates/TODO.md) is migration evidence only; its operative
START, polling, provider-install/fallback and unlimited-loop prescriptions are not inherited.

## Placeholder inventory

Every listed name is used above. Values are scalar text or a private immutable record
pointer with path, SHA-256 and relevant section, not unescaped JSON fragments. This
Markdown checklist has no fenced JSON; validate any referenced JSON record independently.

| Placeholder | Meaning |
|---|---|
| `{{prefix}}` | Unique campaign slug used in artifact and task names. |
| `{{campaign_name}}` | Project/campaign identity, not an execution grant. |
| `{{state_record}}` | Current canonical revision, owner, event and update timestamp. |
| `{{authority_binding}}` | Actual mandate, grants/denials, phase and amendment hashes. |
| `{{admission_record}}` | Planning provenance and verified execution-owner/Run admission. |
| `{{input_manifest_record}}` | Accepted immutable planning/task/shared-contract manifest. |
| `{{model_record}}` | Requested/resolved/actual routes, loading and qualification evidence. |
| `{{topology_record}}` | Named target/base and actual worktree/branch/HEAD/custody receipts. |
| `{{lifecycle_record}}` | Canonical lifecycle, pause, outcomes and separate captain decision. |
| `{{bounds_record}}` | Original absolute clocks, cutoff disposition, limits and admission checks. |
| `{{continuation_record}}` | Pending native continuation and exact-owner deadline binding. |
| `{{blocker_record}}` | Campaign blockers, descendants and next authorized action. |
| `{{task_name}}` | Original slice slug, repeated once per separately accepted slice. |
| `{{task_projection}}` | Evidence-backed pending/working/report delivered/accepted summary. |
| `{{assignment_record}}` | TASK brief and native Task/Dispatch/retry/worker custody bindings. |
| `{{gate_record}}` | Separate blocked coordinator-only gate and actual dependency edges. |
| `{{scope_record}}` | Allowlist, exclusions, non-goals, shared contracts and resource owners. |
| `{{candidate_record}}` | Exact current source/test/dependency/configuration manifest. |
| `{{ready_record}}` | Completed batch handoff, model and execution-host loading evidence. |
| `{{validation_record}}` | Actual scenario/static commands, output, exit and source bindings. |
| `{{review_record}}` | Independent exact-candidate packet, raw evidence, coverage and verdict. |
| `{{api_record}}` | Required independent API inspection or evidenced inapplicability. |
| `{{integration_record}}` | Authorized intent/operation and exact input-to-result mapping. |
| `{{smoke_record}}` | Actual integrated-source/build/scenario smoke result. |
| `{{acceptance_record}}` | Coordinator gate-completion receipt and bound required evidence. |
| `{{preservation_record}}` | Verified durable source/evidence archive and recovery inventory. |
| `{{cleanup_record}}` | Settlement/exit/release/removal evidence and retained resources. |
| `{{progress_record}}` | Distinct progress observations and unresolved operation identity. |
| `{{remaining_work_record}}` | Slice findings, affected dependents, remaining work and next action. |
| `{{final_record}}` | Exact final candidate, acceptance/review/delivery/cleanup and next action. |
