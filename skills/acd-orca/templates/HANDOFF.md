# {{prefix}} Campaign Handoff: {{campaign_name}}

> A curated pointer set for the designated execution owner, not a transcript or grant.
> Follow [handoff](../references/handoff.md), [roles](../references/roles.md) and the
> existing [common fleet contract](../../../fleet/skills/fleet-campaign/references/common-contract.md).
> This template supplies record slots, not another persona or orchestration implementation.

## Filling this template

Replace every double-brace placeholder using the inventory below; repeat rows where needed.
Remove this section and the inventory when instantiating. Rebase relative links for the
project artifact location. Bind evidence by repository-relative path, immutable SHA-256
and relevant section, not a mutable filename alone. Private binding pointers hold actual
host paths, owner/chat/Run/Task/Dispatch identities, model routes and native receipts;
never publish those values or credentials in the reusable template.

Unknown is `null`, never an empty string, zero, invented timestamp or implied success.
Record reason, provenance, consequence and resolution route separately. Explicit absence
or inapplicability needs its own disposition and evidence. JSON unknowns use unquoted
`null`, not the string "null"; replace the entire quoted placeholder value when necessary.
A missing required hash or authority value blocks admission even though JSON still parses.
Representative substitutions test syntax, not the truth of the substituted evidence.

This artifact becomes immutable when frozen. Future actual model observations, native
operations, admission and progress belong in mutable private state/receipts, not edits
that would silently change the HANDOFF already hashed by its manifest.

## Record and authority

- Campaign slug and prefix: `{{campaign_name}}` / `{{prefix}}`.
- Handoff revision and aware UTC recording time: {{handoff_revision}} / {{recorded_at}}.
- Original owner request and actual mandate provenance: {{request_evidence}}.
- Charter and steering revisions, exact hashes and precedence: {{authority_evidence}}.
- Private planning provenance and designated execution-owner/Run bindings: {{ownership_record}}.
- Private admission record and current lifecycle/pause/outcome pointers: {{admission_record}}.

The actual mandate controls phase, repository, host, scope and delivery rights. Planning
convergence, a plan, report success or this handoff cannot grant development authority.
No routine questionnaire, fresh-session START prompt or extra per-task approval is required
when the mandate already settles the decision. A fresh session expressly required by the
owner still binds. Missing authority or consequential unsettled choices block only the
dependent path and go to the actual owner; do not manufacture consent from agent prose.

For the active campaign, [Amendment 01](../../../fleet/execution/fullauto/AMENDMENT_01_ROBOREV.md)
selects roborev. Its provider selection/mechanics supersede historical OCR prescriptions
in unchanged shared sources, not their independence, evidence or acceptance guarantees.
[Amendment 02](../../../fleet/execution/fullauto/AMENDMENT_02_OVERNIGHT.md) supersedes older
fixed-campaign-cutoff and two-paid-worker wording in the accepted references: no total
campaign cutoff, maximum three paid working agents, and frozen previous-file review may
run alongside independent next-file authoring. Original finite attempt/review clocks,
one writer per worktree, genuine prerequisites and delivery denials remain binding.
These scoped amendments do not authorize another campaign or install this staged skill.

| Operation | Actual grant, denial or unknown | Binding and limits |
|---|---|---|
| Implementation, tests and independent review, each separately | {{development_permissions}} | {{authority_evidence}} |
| Integration, merge strategy and commits, each separately | {{integration_permissions}} | {{authority_evidence}} |
| Cleanup, push, publication, deployment and installation, each separately | {{delivery_permissions}} | {{authority_evidence}} |

Available tools are capabilities, not permissions. No generic development grant implies
all delivery actions. The current no-commit mandate requires attributable diffs, untracked
source and immutable snapshots; never create a commit to satisfy a historical review recipe.

## Goal and settled scope

{{goal}}

| Requirement and intended outcome | Explicit source/resource allowlist | Non-goals and preserved behavior |
|---|---|---|
| {{requirement}} | {{scope_allowlist}} | {{non_goals}} |

Key design decisions, owner answers and unresolved consequential choices: {{decision_record}}.
Preserve original intent; neither architecture nor a narrower test may silently reduce it.

## Durable artifact map

| Record | Exact binding or private operational pointer |
|---|---|
| Accepted PLAN, its revision and original requirement traceability | {{plan_binding}} |
| INTENT with bounded repository/interface/runtime discovery | {{intent_binding}} |
| RESEARCH with actual current primary sources and reuse/license/security/footprint evaluation | {{research_binding}} |
| Complete CRITIQUE history, critic-owned findings and current-hash CONVERGED | {{critique_binding}} |
| Current changed/affected-scope attestation and justified reuse of unaffected evidence | {{affected_scope_binding}} |
| Every task brief, acceptance/runtime scenario and standalone shared contract | {{task_contract_inventory}} |
| Frozen planning manifest location and external private digest/admission binding | {{manifest_record}} |
| Mutable PLANNING_STATE, STATE, TODO, EVENTS, evidence and REPORT locations | {{operational_records}} |

Convergence binds current INTENT/RESEARCH/request/contracts and all five planning lenses:
intent fidelity, architecture/research, Security, UX and readiness. The independent critic
owns closure and reused-evidence applicability. A delivered critique or an author's
checklist is not convergence. No DAG admission before the required planning gate.
The [PLAN template](PLAN.md) owns the detailed work/design tables; link its exact accepted
bytes rather than duplicating a competing plan in the handoff.

## Repository, topology and source custody

- Repository identity and private location evidence: {{repository_record}}.
- Original named target branch and full starting SHA: {{target_branch}} / {{starting_sha}}.
- Verified campaign/task lineage, returned branches/HEADs and sole-writer custody: {{topology_record}}.
- Existing dirty/untracked baseline and immutable inventories: {{baseline_record}}.
- Exclusive files, APIs, schemas, lockfiles, outputs, ports, fixtures, databases and effects: {{resource_record}}.
- Durable source/archive custody, recoverability verification and release prerequisites: {{preservation_record}}.

Never assume main/master, infer a named target from detached HEAD, or treat an existing
worktree as clean/owned. For an authorized new topology, the campaign root derives from
the named target branch; task worktrees are Orca children based on the actual campaign
branch. Verify returned branch/HEAD receipts; do not use a raw SHA as the branch-base
shortcut or merge a task straight into the target. Reuse existing worktrees only under
the mandate with verified custody and baseline. Coordinators never author source or
resolve source conflicts; bounded implementation workers do.

Source inventories include required source/tests/dependencies, ignored/untracked inputs,
deletions and renames. Preserve base material, attributable diff plus untracked bytes,
immutable input/result manifests and source-to-snapshot mappings outside disposable
workspaces. Under no-commit delivery, commit fields remain `null` with explicit
not-applicable evidence; do not invent a SHA or squash receipt. Preserve the only runnable
source until delivery and recoverability are verified. Assignment settlement, physical
exit and resource release are separate facts; unproven custody/release blocks reuse.

## Models and scoped provider readiness

Record requested, resolved and actual models per purpose, with selection authority,
resolution/startup evidence and purpose-specific tool outcomes. A permitted `default`
means that runtime/profile's actual configured default, resolved and pinned, not an
orchestrator-selected substitute. A picker or configuration alone proves no actual use.
Unknown observations stay `null`; startup mismatch blocks the affected path.

| Purpose | Private requested/resolved/actual model record | Correlated loading/startup/purpose evidence |
|---|---|---|
| Implementation | {{implementation_model_record}} | {{capability_record}} |
| Planning and independent critique/document review | {{planning_model_record}} | {{capability_record}} |
| Code review and optional final review, separately | {{review_model_record}} | {{provider_record}} |
| Auxiliary purposes actually used; optional disabled roles distinguished from unknowns | {{auxiliary_model_record}} | {{capability_record}} |

Authorized selection policy or explicit absence: {{selection_policy}}. It is not an
automatic fallback. Primary-model failure or permission refusal stops the affected path;
no blind retry, silent provider/model switch, owner impersonation or broader permission.

Use the accepted [code-review contract](../references/code-review.md):

| Field | Meaning |
|---|---|
| `models.review_engine`, `tasks[].review.engine` | `roborev`, the selected provider; never OMP, which is an execution engine. |
| `models.code_review` | Binary/version, independently resolved `execution_engine`, requested/resolved/actual model route, qualification status, exact receipt and limits. |
| `tasks[].review` | `run_id`, `raw_output`, completion, coverage, raw findings, verdict and `bound_to` exact source/base/tip/scenario identity. |

The provider record must bind the already accepted qualification's actual host/container,
binaries, interface/model and operational limits. Retain clean, known-defect/error-case,
raw schema/severity and uncommitted/untracked-scope evidence. Reuse only within its proven
scope; do not rerun bootstrap greetings or infer OMP compatibility from generic executable
support. Changed/unqualified environments need authorized resolution before dependent code.
Operational read-only tools are not OS sandbox confinement. Shared model/executable never
permits reuse of the implementer's reasoning context. No adapter, package, global config,
hook, permission, service or daemon change is implied.

Scoped provider readiness opens only its dependent readiness boundary. It is not candidate,
API, runtime, recovery, auxiliary or other-engine acceptance. Documentation review needs no
code-tool qualification and does not qualify a provider. Historical OCR is superseded,
not newly qualified; no operative provider/session fallback or old field aliases remain.

## Execution-host capabilities and permissions

Loading and capability record: {{capability_record}}. Bind supported instruction loading
on the actual host, executable/version, discoverable session/output, tool calls, native
result/wake behavior and supported release to exact receipts. Discover installed
[Orca instructions](../references/orca-runtime.md) and narrow help; do not copy guessed
commands or assume that staging a Markdown file loads it in an engine.

| Permission scope | Effective value | Observation time, provenance or unavailable reason | Proven operations, dependent operations and unresolved consequence |
|---|---|---|---|
| Bot defaults | {{bot_permission}} | {{bot_permission_evidence}} | {{bot_permission_dependencies}} |
| Existing chat | {{chat_permission}} | {{chat_permission_evidence}} | {{chat_permission_dependencies}} |
| Engine-specific launch override | {{launch_permission}} | {{launch_permission_evidence}} | {{launch_permission_dependencies}} |
| Existing workers | {{worker_permission}} | {{worker_permission_evidence}} | {{worker_permission_dependencies}} |

Inspect scopes independently; one setting does not retroactively migrate another. An
individual approval or successful operation is not proof of Full access. An unavailable
effective value may remain `null` with exact supported observations and operation-specific
dependencies; do not infer the value, weaken permissions, or automatically claim all
operations unavailable. A dependent operation whose required permission remains unproven
stays blocked. Real refusals stop the affected operation without bypass; only the actual
owner may perform owner-reserved changes. Distinguish instructed from enforced restrictions.

| Runtime command/action or capability | Actual host/cwd/prerequisites/fixtures | How verified and immutable receipt | Limits or blocker |
|---|---|---|---|
| {{runtime_command}} | {{runtime_environment}} | {{command_verification}} | {{runtime_limits}} |

Resolve required runtime entry points before dispatch. Record expected output/exit/state,
negative scenarios and cleanup; missing capability is a scoped blocker, never an invented
command or a mocked success. Real tests exercise the production consumer path and seams;
a green unit suite alone does not replace them. Document-only slices use static checks
and independent exact-byte review. Synthetic tabletops are labeled synthetic.

## Native work and acceptance plan

| Slice and immutable brief | Work node | Independent review node/packet | Required API node | Separate acceptance gate | Successor dependencies and resources |
|---|---|---|---|---|---|
| {{task_name}} / {{task_binding}} | {{work_node}} | {{review_node}} | {{api_node}} | {{acceptance_gate}} | {{dependency_resources}} |

Use logical labels and private identity pointers, not live IDs in this reusable table.
Record inapplicable API inspection explicitly with reason. Keep each acceptance Task
**blocked**, **never dispatched**, and **never made ready** as work. Only the designated
coordinator completes it after all required bound evidence passes. Successors depend on
that gate, not the author or review-analysis Task. Qualify native transitions on the actual
target; writing the plan does not prove enforcement. Successful reporting of FAIL or
INCONCLUSIVE settles analysis only, never the product prerequisite.

One source document or one code module plus tests per assignment; one source writer per
worktree and no hidden helpers. Independent next-file authoring may overlap review of a
frozen previous-file snapshot; no review of changing source. At most two related small
files per administrative/review packet, with separate per-file hashes, criteria and
verdicts. Removing artificial edges needs authority and original-to-replacement mapping;
genuine dependencies and final cross-document integration remain. Superseded Tasks are
historical, never falsely PASS. Pending next operation and prerequisite evidence:
{{next_action_record}}.

## Exact evidence and gate bindings

Per-stage immutable evidence inventory: {{evidence_record}}. Each result binds candidate
revision, repository/base/tip where applicable, source/test/dependency SHA-256 manifest,
scenario ID/version/hash, build identity where applicable, exact evidence identity and
outputs. Required unknowns block acceptance, not JSON parsing. Source/build/config/scenario
drift invalidates applicable eligibility; preserve old receipts at their old bindings.

| Stage | Required exact binding |
|---|---|
| Runtime | Actual tested source/build, scenario inputs, verified commands/environment, outputs/exits/state and failures. |
| Independent review | Original acceptance/contracts, frozen candidate, neutral packet/diff, fresh separate reviewer/model/config, raw completion/findings and complete coverage. |
| Required API inspection | Exact candidate/interface/criteria and independent receipt; not a replacement semantic code review. |
| Authorized integration | Intent, starting destination and reviewed incoming manifests, actual operation/mapping and resulting manifest/tree; squash SHAs only when authorized. |
| Post-integration smoke | Actual resulting integrated source/build, scenario/version/hash, commands, outputs and outcome; not relabeled task-source tests. |
| Coordinator acceptance | Matching review/API/integration/smoke bindings, current authority/source/time checks and native blocked-to-completed receipt. |
| Document-only acceptance | Assigned static checks and independent exact-byte verdict; no invented runtime or transferred code-readiness claim. |

For every real code candidate retain the
[raw result and coverage receipt](../references/code-review.md#raw-result-and-coverage-receipt):
fresh neutral session/config, immutable no-hooks review-only snapshot outside the live
checkout, source/test/dependency inventory, source/config/diff/tool-policy/hook guards,
actual invocation/cwd/bounds/exit, raw schema 3 JSON separately from rendered output,
sanitary provider stop reasons/errors and required tool results. Require external complete
file-to-tool-ID-to-line-range-to-returned-content/hash full-read reconciliation against
frozen bytes. Roborev has no native coverage certificate. Exit zero, ACP end_turn, empty
findings or exhaustive mode alone is not PASS; provider errors can still end a turn.
Preserve raw findings, never hidden reasoning or credentials.

The [verdict contract](../references/code-review.md#verdict-and-acceptance) is fail-closed:
binding drift is INVALIDATED; missing/malformed/partial/skipped/failed/budget-stopped/
unknown/truncated/zero-required-coverage or unmappable evidence is INCONCLUSIVE. A complete
valid fail or critical/high/medium acceptance/security finding means FAIL. Only valid
pass, complete nonzero coverage, provider/tool success, preserved provenance and no
blocking findings permit PASS for that exact candidate/scenario. Unknown severity is
INCONCLUSIVE; low/style-only findings do not create fix work. Independent closure owns
blocking dispositions; author self-review is not acceptance. No routine second semantic
code review or silent provider substitution; API and runtime obligations stay distinct.

## Original clocks and continuation

Authority-bound absolute times and spend/resource record: {{bounds_record}}.

| Field/policy | Required value or meaning |
|---|---|
| `campaign_cutoff_utc` | An authorized absolute aware UTC cutoff, or `null` with separate disposition, reason and authority binding. |
| Cutoff disposition | `absent_by_authority` means explicitly no total horizon; `unknown` blocks admission until resolved. Amendment 02 establishes `absent_by_authority` and `campaign_cutoff_utc: null` here; the removed cutoff is historical only. |
| `tasks[].attempt` | `label`, original `started_at`, `budget_seconds`, persisted `checkpoint_due_at`, `deadline_at`, actual launch observation and any phase-specific `predeclared_deadline`, preserving history. |
| Attempt/checkpoint | At most 900 seconds per attempt, checkpoint at 600 seconds for this campaign; record absolute times before launch, not durations alone. |
| Independent review | At most 600 seconds unless a prior bounded extension is expressly authorized; no retrospective extension. |
| Iterations | At most two unproductive executions; one slice defect-fix round and at most two feature-integration fix rounds. Useful findings do not create unlimited cycles. |
| Spend | Retain low-effort/500000-token slice and medium-effort/2000000-token final constraints with supported observation or explicit bounded reconciliation, not fabricated tool flags or dropped limits. |
| Concurrency | Maximum three paid working agents across this campaign and maximum three coders including fixes; one source writer per worktree. Possibly live writers retain custody/capacity until reconciled. |
| Predeclared longer phase | {{long_phase_bounds}}; a bounded build/test phase cannot renew the original attempt or permit new affected work after its applicable deadline. |

Unknown actual launch time stays `null` while the prelaunch absolute cutoff still binds.
Fixes, retries, restarts, session/model changes, transport churn, reads and late receipts
never reset original clocks. Genuine retry launch observations stay separate. No campaign
cutoff does not mean unlimited attempts. Before every affected dispatch, integration or
gate completion that releases work, read actual UTC and check the earliest applicable
finite persisted deadline, mandate, pause/revision, custody and resource exclusions.
Ignore only a cutoff explicitly absent by authority, never an unknown one. Refuse new
affected work after expiry. At checkpoint inspect correlated semantic progress and issue
at most one scoped steer if needed; assistant response, transport activity, completed tool
and semantic progress are separate facts, and unknown is never healthy.

Native result/question/escalation and exact-owner deadline continuation record:
{{continuation_record}}. Persist the next event and one-shot receipt before ending the
turn. Only the specific mandate may permit a campaign-level native continuity backstop:
same actual owner chat, no duplicate dispatch or second owner, no more frequent than its
authorized cadence, disabled at terminal/pause/true needs-owner state. Amendment 02's
backstop is at most every 20 minutes, not shell polling or a replacement scheduler.
Do not install a watcher, heartbeat emulator or mailbox-consumer loop. A Run/state file
schedules nothing; configured wakeup is not proof of delivery or reboot resilience.

A queued deadline may arrive late: it triggers scoped reconciliation, not exact-time
hard enforcement, exit proof or authority to kill/restart. Expiry stops admission and
preserves partial source/receipts; it is neither automatic acceptance nor permanent
feature FAIL. Pause blocks new affected work and never self-resumes on a late reply.

## Admission, drift and resume

The designated execution owner records admission separately from mandate and convergence,
following [execution admission](../references/handoff.md#execution-admission):

1. Verify phase/scope/host/delivery authority, sole owner/Run/assignment and pending intents.
2. Recompute frozen files and manifest digest against the private binding; verify current
   independent critique and required accepted prerequisites. Missing/drifted bytes stop
   affected mutation; never silently re-hash consent.
3. Verify repository/named target/start SHA, returned branches/HEADs, source inventories,
   existing dirty/untracked custody and exclusions. Reconcile moved/ambiguous refs.
4. Verify actual loading/models, operation-specific permissions, runtime commands and
   applicable provider readiness; keep unknown facts and blockers explicit.
5. Check actual UTC against persisted bounds and pause state; verify native continuation.
6. Persist admission time, authority revision, manifest digest, exact owner/source,
   capabilities, blockers and next operation in mutable state before authorized mutation.

Lifecycle distinguishes planning, admitted execution and completed delivery; keep mandate,
convergence, admission, pause, blocked/failed/cancelled outcomes and captain acceptance
separate. No obsolete fresh-session lifecycle grants authority. Planning ownership and
execution ownership remain distinct; only the designated execution owner mutates shared
STATE/TODO/EVENTS/native coordination. Workers write only assigned source/evidence.

On drift preserve expected/observed hashes and history, stop affected dispatch/integration,
classify the cause and route changed design through authorized revision and critic-owned
affected-scope review. A separately identified immutable manifest replaces no old bytes
or verdict history. Future actual observations go into mutable receipts. Resume reconciles
original authority, owner, source, models, clocks and pending launch/review/integration/
stop/release operations under [state and recovery](../references/state-and-recovery.md).
Unknown launch/stop outcome forbids duplicate dispatch/reuse; silence is not exit.
Use supported guarded settlement with confirmed receipts, never a blind automatic restart.
An operator pause needs explicit authorized resume. Archive late output under its original
revision; remove only owned obsolete timers and ignore terminal-state wakes.

## Integration, delivery and remaining work

Authorized composition/delivery route and exact receipt destinations: {{integration_record}}.
For no-commit work, record starting/incoming/result byte manifests and attributable mapping;
if source already lives in the authorized worktree, identify that actual composition rather
than inventing a merge. Serialize integration; changed composition needs worker fixes,
affected tests and fresh applicable review before gate completion. Smoke the actual result.

Final acceptance requires all criteria/seams on the exact integrated delivery candidate,
independent final review, moved-target reconciliation and current named-ref/source checks
before any authorized final action. A target merge requires its separate grant and actual
target smoke; otherwise identify the delivery snapshot and explicitly record no target
merge. Document-only final acceptance requires complete static/cross-document checks and
independent exact-manifest verdict. Ready-for-captain is not captain acceptance.

Before cleanup/release, verify a checksummed recoverable source/evidence archive outside
disposable workspaces, including base, diff, untracked files, scenarios and raw review/API/
integration/smoke receipts. Preserve the runnable source and report retained resources if
release or recoverability is unproven. Push, publication, deployment, installation, Groups,
global changes and unrelated campaigns are not granted here. Staging leaves existing
skill/SOUL loading paths and legacy files unchanged.

Remaining findings, BLOCKED/UNTESTED requirements, retained resources and exact next action:
{{remaining_work}}. Successful author reporting is not independent product PASS.

## Companion manifest

Create `plans/{{campaign_name}}/{{prefix}}_MANIFEST.json` as a separate immutable file.
Extract the fenced object below into that separate file, then delete the fenced example
from the instantiated HANDOFF before freezing it. Only then compute the HANDOFF hash and
fill the external manifest's HANDOFF entry; never put that self-hash back in this document.
Replace every manifest hash independently from exact bytes; expand entries for every task,
standalone shared contract, complete critique history and immutable authority revision.
Paths must be repository-relative, non-traversing and unique. JSON parsing alone is not
hash validation. Do not reuse a representative hash as real evidence.

```json
{
  "manifest_version": 1,
  "campaign": "{{campaign_name}}",
  "prefix": "{{prefix}}",
  "created_at": "{{recorded_at}}",
  "algorithm": "sha256",
  "files": {
    "plans/{{campaign_name}}/{{prefix}}_INTENT.md": "{{intent_sha256}}",
    "plans/{{campaign_name}}/{{prefix}}_RESEARCH.md": "{{research_sha256}}",
    "plans/{{campaign_name}}/{{prefix}}_CRITIQUE.md": "{{critique_sha256}}",
    "plans/{{campaign_name}}/{{prefix}}_PLAN.md": "{{plan_sha256}}",
    "plans/{{campaign_name}}/{{prefix}}_{{task_name}}.md": "{{task_sha256}}",
    "{{shared_contract_path}}": "{{shared_contract_sha256}}",
    "{{authority_snapshot_path}}": "{{authority_snapshot_sha256}}",
    "plans/{{campaign_name}}/{{prefix}}_HANDOFF.md": "{{handoff_sha256}}"
  }
}
```

Exclude mutable planning state, STATE, TODO, EVENTS and execution evidence; exclude the
manifest itself. Finish HANDOFF before hashing it. Record the completed manifest's own
digest in private state and the admission receipt, **not in this HANDOFF**: no recursive
self-hash. Preserve every manifest version and its source outside disposable workspaces.
Mutable evidence growth does not invalidate the planning freeze; changed source/scenario
still needs its own current-candidate evidence. No silent re-hash on drift.

Companion templates: [PLAN](PLAN.md), [INTENT](INTENT.md), [RESEARCH](RESEARCH.md),
[CRITIQUE](CRITIQUE.md), [TASK](TASK.md), [TODO](TODO.md),
[PLANNING_STATE](PLANNING_STATE.json) and [STATE](STATE.json).
Absent companions are PENDING during staged authoring, not resolved-link or acceptance
claims. Do not read changing siblings to infer a contract. Final integration reconciles
all fields, placeholder meanings, authority/lifecycle/deadline semantics and exact evidence
bindings with zero missing links. Mapped [legacy HANDOFF](../../acd/templates/HANDOFF.md)
and [legacy boundary](../../acd/references/handoff-and-start.md) are migration evidence only,
not operative START, polling, provider setup or fallback instructions.

## Placeholder inventory

Each listed name is used in double braces above. Concrete private identities stay in the
project binding records. Evidence replacements carry a path/hash/section or a truthful
`null` with its separate reason and consequence; synthetic substitutions are not evidence.

| Names | Required replacement |
|---|---|
| `prefix`, `campaign_name` | Unique short prefix and English lowercase campaign slug. |
| `handoff_revision`, `recorded_at` | Handoff revision and aware UTC recording time. |
| `request_evidence`, `authority_evidence` | Original request, actual mandate and steering revision provenance, hashes and limits. |
| `ownership_record`, `admission_record` | Private planning/execution custody and separate admission/lifecycle/pause/outcome records. |
| `development_permissions`, `integration_permissions`, `delivery_permissions` | Per-operation grant, denial or unknown, with authority and limits. |
| `goal`, `requirement`, `scope_allowlist`, `non_goals`, `decision_record` | Observable outcome, requirement ID, exact allowlist, exclusions and settled/open decisions. |
| `plan_binding`, `intent_binding`, `research_binding`, `critique_binding`, `affected_scope_binding`, `task_contract_inventory` | Exact accepted artifacts, current critic-owned evidence and complete task/scenario/contract inventories. |
| `manifest_record`, `operational_records` | Manifest location plus external private digest/admission record; mutable artifact map. Never insert the manifest digest into the HANDOFF it hashes. |
| `repository_record`, `target_branch`, `starting_sha`, `topology_record`, `baseline_record` | Verified repo identity/private location, original named branch/full SHA, lineage/custody and dirty/untracked baseline. |
| `resource_record`, `preservation_record` | Exclusive resource ownership and verified recoverable source/evidence custody. |
| `implementation_model_record`, `planning_model_record`, `review_model_record`, `auxiliary_model_record`, `selection_policy` | Private requested/resolved/actual purpose evidence and authorized selection policy or explicit absence. |
| `provider_record`, `capability_record` | Scoped provider qualification and actual host loading/model/tool/native capability receipts with limitations. |
| `bot_permission`, `chat_permission`, `launch_permission`, `worker_permission` | Effective value in each separate scope, or `null` when unavailable. |
| `bot_permission_evidence`, `chat_permission_evidence`, `launch_permission_evidence`, `worker_permission_evidence` | Scope-specific observation time, exact supported evidence and unavailable reason. |
| `bot_permission_dependencies`, `chat_permission_dependencies`, `launch_permission_dependencies`, `worker_permission_dependencies` | Proven operations, dependent operations, unresolved consequences and resolution route without inferred Full access. |
| `runtime_command`, `runtime_environment`, `command_verification`, `runtime_limits` | Actual action/argv, host/cwd/prerequisites, entry-point verification and missing/mocked/unavailable limits. |
| `task_name`, `task_binding`, `work_node`, `review_node`, `api_node`, `acceptance_gate`, `dependency_resources` | Task slug/binding, logical native-node/private pointers, blocked gate and successor/exclusion mapping. |
| `next_action_record`, `evidence_record`, `bounds_record`, `long_phase_bounds`, `continuation_record` | Admissible next operation, exact stage evidence, original absolute/spend limits, prior phase bounds and native event/deadline receipts. |
| `integration_record`, `remaining_work` | Authorized integration/delivery route; findings, BLOCKED/UNTESTED outcomes, retained resources and next action. |
| `intent_sha256`, `research_sha256`, `critique_sha256`, `plan_sha256`, `task_sha256`, `handoff_sha256` | Separately computed lowercase 64-hex SHA-256 of each exact frozen artifact. |
| `shared_contract_path`, `shared_contract_sha256`, `authority_snapshot_path`, `authority_snapshot_sha256` | Unique repository-relative immutable contract/authority paths and their separately computed SHA-256; expand for all inputs. |
