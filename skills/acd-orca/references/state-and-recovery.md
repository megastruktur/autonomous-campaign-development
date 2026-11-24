# State and recovery

This reference owns durable campaign records, progress semantics and recovery admission
for the staged, uninstalled `skills/acd-orca/` candidate. Read [roles](roles.md) and the
[common fleet contract](../../../fleet/skills/fleet-campaign/references/common-contract.md)
for responsibility and shared policy; do not copy those definitions into campaign state.
Authority, immutable inputs and model identity come from [handoff](handoff.md).
Native operations use installed version-matched discovery through [Orca runtime](orca-runtime.md),
not the historical terminal, polling or watcher recipes.

The [owner amendment](../../../fleet/execution/fullauto/AMENDMENT_01_ROBOREV.md) selects
roborev for substantive code review. Historical OCR-first wording in unchanged shared
sources is superseded for this candidate, not an instruction to run OCR or retain its
state-field aliases. [Code review](code-review.md) owns qualification and verdict rules.
Scoped provider readiness is not candidate, API, runtime, recovery or engine-parity acceptance.

## Durable records and sole ownership

Keep campaign memory in its durable project directory, not chat history, a temporary
review directory or shared Bot memory. The project charter may name the directory and
prefix; `{prefix}` below means that recorded campaign prefix, not a literal runtime value.

| Record | Purpose and writer |
|---|---|
| `{prefix}_PLANNING_STATE.json` | Planning phases, evidence hashes and critic-owned convergence; Logis is the sole canonical planning writer. |
| `{prefix}_STATE.json` | Canonical campaign decision and evidence record; the designated project Magos is the sole execution writer. |
| `{prefix}_TODO.md` | Human projection of STATE, including final acceptance and cleanup; the same execution owner writes it. |
| `{prefix}_EVENTS.jsonl` | Append-only execution intents, results and reconciliation decisions; the same execution owner writes it. |
| `{prefix}_evidence/` | Sanitized source manifests, runtime/review reports and native receipts; workers write only their assigned evidence slots and the coordinator indexes preserved results. |
| `{prefix}_REPORT.md` | Final requirement-by-requirement outcomes, evidence and remaining work; the execution owner writes it. |

Exactly one verified execution-owner chat writes shared execution records and mutates
that campaign's native coordination state. A Bot name, role file, old timestamp or
apparently idle session is not a lock. Unknown or conflicting owner chat, Run, assignment
or worktree custody blocks mutation until reconciled. Workers never edit shared STATE,
TODO or EVENTS. Planning-to-execution custody is explicit; do not create concurrent
writers by mirroring another owner's mutable planning file.

Native Task, Dispatch, worker and Automation receipts are authoritative for observed
native operations; project files retain decisions, evidence and unresolved outcomes.
Neither overrides a contradiction in the other by assertion. Record and reconcile it.
A state file is not a scheduler, a successful worker report is not product acceptance,
and no actor edits Orca's runtime database to make its projection agree.

For every shared-state write, increment `revision`, record `last_updated_at` in aware
UTC and identify the owner and event. Write a temporary file in the same directory,
flush/fsync where available, then atomically rename it over STATE. Record durability
limits honestly; an atomic rename does not make the event log and external action one
transaction. Preserve the prior usable state if parsing or replacement fails. Never
silently repair corrupt history into a successful transition.

Unknown is JSON `null`: unknown identity, timestamp, model, tool outcome or verdict is
not an empty string, zero, guessed timestamp or success. Explicit negative evidence is
separate from unavailable evidence. Where native output says `unknown`, retain its raw
value in the receipt and use `null` for the unknown normalized fact with a reason and
observation time. Absent or stale evidence cannot be reported healthy. Sanitize secrets,
credentials and personal data before filing evidence; portable documents contain no
actual host paths, private IDs or credential values.

## Intent before mutation

Before dispatch, steering with side effects, stop, abandon, release, integration,
deletion or deadline creation/removal, append and durably preserve an intent event.
Include operation identity, expected state revision, mandate revision, exact target and
owner, source/input binding, preconditions, original deadlines and the expected receipt.
Retain any native request, operation or retry identity once returned. Then:

1. Check current authority, ownership, source binding, pause state and actual UTC against
   persisted bounds immediately before the affected action.
2. Perform the one authorized operation through the supported native interface.
3. Preserve its full sanitized receipt, including uncertainty and required next action.
4. Append the result and checkpoint STATE, then rebuild the affected TODO projection.

If the process stops between these steps, an intent proves only that an action was
planned. It proves neither that the action happened nor that it did not happen. Set an
unresolved result to `null`, preserve the pending operation and reconcile external truth
before any repetition. Replay only where the installed interface explicitly supports
idempotency for that exact request and its receipt authorizes it. Never turn a lost
response into a fresh launch, duplicate brief, second merge or second timer.

## State contract and acceptance boundaries

STATE records these facts without replacing native scheduling or provider evidence:

| Area | Required facts |
|---|---|
| Authority and ownership | Mandate/revision and permitted delivery actions; planning provenance; actual execution-owner chat and Run; admission receipt; pause actor/reason/time and explicit resume authority. |
| Frozen inputs | Manifest digest, immutable input paths/hashes and accepted critique bindings; expected versus observed source/ref identity on drift. Mutable observations do not rewrite the approved manifest. |
| Topology and resources | Named target branch/full starting SHA; actual campaign and task worktree branch/HEAD receipts; sole writer; exclusive files, lockfiles, schemas, ports, databases and effects. |
| Task execution | Native Task/Dispatch/retry identities, dependencies and acceptance-gate identity, stage/history, exact candidate revision/hash manifest, worker identity, models and assigned evidence slots. |
| Bounds | Original campaign cutoff, original attempt start/checkpoint/deadline, actual launch observation, predeclared phase/review bounds, fix and unproductive-attempt accounting, pending exact-owner deadline receipt. |
| Evidence and recovery | Distinct progress facts, native observations, runtime/scenario/build bindings, review records, pending intents, diagnosed cause/action/expectation/result/next step, integration and source-preservation receipts. |
| Settlement | Assignment state separately from physical agent/process state, stop/release evidence, retained dirty/untracked source, cleanup inventory, next action and unresolved ownership. |

Use `tasks[].attempt` for `label`, `started_at`, `budget_seconds`,
`checkpoint_due_at`, `deadline_at` and any `predeclared_deadline`, with the original
slice clock and attempt history retained. A phase deadline is specific to that phase,
not a replacement for a campaign cutoff or permission to slide a slice budget.
`unproductive_attempts` counts diagnosed executions without a useful artifact, evidence
or actionable finding; preserve failed-start history separately.

For the current selected provider, `models.review_engine` and `tasks[].review.engine`
are `roborev`; these name the provider, not its execution engine. `models.code_review`
records binary/version, independently resolved `execution_engine`, requested/resolved/
actual model route and qualification evidence/status. Each review records `run_id`,
`raw_output`, completion, coverage, raw findings, verdict and `bound_to` exact source/
base/tip/scenario identity. Never migrate unknown legacy provider facts by inventing a
roborev run. The [review contract](code-review.md#verdict-and-acceptance) determines
PASS, FAIL and INCONCLUSIVE; drift makes acceptance INVALIDATED while preserving the
historical verdict and its old binding. No review yet means `null`, not PASS or FAIL.

Lifecycle describes facts: planning, admitted execution and completed delivery remain
distinct; mandate and admission are separate from planning convergence. No fresh-session
START ceremony or `awaiting_fresh_session_start` state grants or gates authority here.
Pause is an explicit orthogonal record; completion, cancellation and failed/blocked
outcomes must not be conflated with ready-for-captain. Retain per-task development,
runtime testing, review, integration, post-integration smoke and cleanup history.
Document-only tasks instead record their assigned static validation and independent
exact-byte document verdict; never invent runtime tests to fill a stage.

A fix returns the task to active work and clears current acceptance eligibility before
another review. If worktree display status is used, internal `in_progress` maps to
`in-progress` and `in_review` to `in-review`; display text is not a review trigger.
Deduplicate review by the exact candidate/packet/scenario and recorded run, not a stale
card status or the arrival of a commit. Changed bytes invalidate earlier eligibility.

Product successors depend on a separate native acceptance Task kept **blocked**, never
made ready or dispatched as work. Only the designated coordinator completes that gate
with the required exact-candidate independent review, API evidence where required,
authorized integration and actual post-integration smoke. Document gates require their
specified static receipt and independent exact-byte verdict. Successful delivery of an
analysis reporting FAIL or INCONCLUSIVE can settle that analysis Task but cannot complete
a product prerequisite. Deadline expiry, provider readiness and author self-review also
cannot open the gate.

TODO mirrors verified STATE, not promises or the last chat response. Rebuild it after
recovery. Check off a stage only when its bound evidence proves it, including final
campaign acceptance, target smoke, source retention and actual resource release. An
unavailable todo tool does not remove the durable checklist obligation.

## Observation and semantic progress

Retain separate timestamps and provenance, never a single last-activity field:

| Fact | What it proves |
|---|---|
| `last_observed_at` | Transport, file or process evidence only; streams, bytes, PID, mtime and log growth are not task progress. |
| `last_successful_assistant_at` | A successful model response under the observed engine/version's event semantics, not a useful artifact or completion. |
| `last_completed_tool_at` | A completed tool call, with `last_tool_outcome` separately `successful`, `failed` or `null` when unknown; errors do not refresh a successful-step clock. |
| `last_semantic_progress_at` | A validated structured checkpoint for the current task/attempt/session/candidate and a completed criterion. |

Keep event time separate from observation time. A late read of an old success does not
manufacture progress now. Only the current live branch counts: abandoned/discarded
branches, compaction, title/model changes and usage metadata do not establish success.
Provider-global errors need explicit session correlation before being attributed to a
worker. For a verified OMP event schema, `error`/`aborted` or an `errorId` is not assistant
success; a tool outcome is successful only when its evidence explicitly confirms success
(`isError` strictly false where that field is authoritative). Missing/null outcome is
unknown. Do not assume another engine or version shares that schema; its startup sheet
must establish the mapping. ACP `end_turn` and process exit zero alone do not establish
provider success, progress or review PASS.

A checkpoint includes task, attempt, session, candidate, checkpoint ID, aware-UTC
completion time, criterion/kind and evidence pointer/hash. Confirm identity and source
binding, then inspect the claimed evidence. Reject future times, times before the original
attempt baseline, replayed IDs, older checkpoints and superseded candidates. Preserve an
old attempt's valid checkpoint as historical only. Retract current eligibility when its
identity or source binding no longer matches. A producer's `verified: true` is an
attestation, not independent validation. Artifact or diff growth is merely a candidate
signal requiring inspection; it is not a checkpoint by itself.

Activity and health are separate observations. A worker may be generating while failing
repeatedly; a live PID alone establishes neither generating nor healthy. Unknown schema,
inaccessible input, truncated/backlogged evidence or stale observations yields unknown
health, not a clean bill of health. Silence or a diagnosis threshold permits inspection,
not a FAIL, kill, abandon or restart. A pending question means waiting for input; a live
command within its declared deadline is not a stall. Answer a question through native
correlated reply when authorized; human-dependent input pauses the affected path rather
than triggering automatic retries.

## Native continuation and original clocks

Only native result/question/escalation wakes and exact-owner one-shot Automations provide
continuation. Before waiting, verify a pending native continuation or save one bounded
deadline to the actual coordinator chat and retain its receipt. Discover current trigger
options and help: where supported use the native `--once` and `--by` deadline mechanism
with an explicit exact-chat target, not a Bot default or a new conversation. Do not copy
these option names into a guessed command. Persist the Automation identity, recipient,
Run/task/attempt/revision, absolute UTC deadline and instruction to reconcile only that
scope. Configuration presence is not delivery proof; claims of autonomous supervision
require observed native wake handling for the actual owner/environment.

When waiting, end the turn. Do not consume mail in a script, poll files/Tasks in a loop,
install an external watcher, emulate heartbeat, or run a background supervisor. A Run
status file schedules nothing. Missing continuation capability blocks unattended claims;
it is not permission to invent a substitute. No broad host-death or reboot-liveness
promise follows from a native receipt.

Persist absolute bounds before launch and read real UTC before **every affected dispatch
or integration**, including retries and gate completion that would release dependent work.
Refuse new affected work after the earliest applicable cutoff. A deadline message may
queue behind a busy turn: it causes delayed reconciliation, not an exact-time enforcement
barrier against a malfunctioning agent. The procedural admission check remains mandatory.

The general R2 defaults are a 20-minute checkpoint, 35-minute attempt and at most two
unproductive executions. A tighter charter wins: the active full-auto contract uses
10-minute checkpoints, attempts no longer than 15 minutes, reviews no longer than
10 minutes, one slice defect-fix round and at most two integration-fix rounds, within a
fixed campaign cutoff. Persist the charter's actual absolute timestamps privately; do
not replace them with these durations on recovery. Resource, concurrency and spend limits
also remain binding; unsupported controls require explicit reconciliation, not fabricated
flags or silently dropped limits.

The original attempt clock starts at actual attempt launch; record an unknown actual
launch time as `null` while retaining the prelaunch absolute cutoff. An ambiguous launch
must not gain time by resetting the submission baseline. Restarts, late receipts, log
churn, repeated reads, empty verdicts, relabeling, new sessions and defect fixes do not
reset original slice or campaign clocks. Keep genuine retry launch observations separately;
they do not erase the bound inherited from the original attempt. A changed charter needs
recorded owner authority, never an after-the-fact extension to make expired work valid.
Long builds/tests require their own bounded phase deadline declared before launch and
real completion/checkpoint evidence; an in-flight phase does not authorize new work after
an overall cutoff.

At checkpoint, inspect correlated evidence and issue at most one scoped steer if needed.
Record its expectation and evaluate new semantic progress before another intervention.
At expiry, stop admitting affected work, preserve receipts/partial artifacts and reconcile
in-flight ownership. Expiry is not proof of exit, authority to kill/restart, automatic
acceptance or permanent feature FAIL. Apply guarded settlement below only with the
required authority. Report incomplete work honestly rather than renew timers indefinitely.

On each wake, first check owner, current revision, pause/terminal state and deadlines.
Archive late output under its original binding; never apply it to a superseding candidate.
Remove only the campaign's obsolete timers on completion, cancellation, pause or needs-user
state, recording removal/uncertainty. Ignore already-queued stale wakes for execution.
An operator pause never self-resumes, even when a worker finishes or a deadline fires.

## Guarded settlement and duplicate prevention

Assignment settlement, agent exit and resource release are three different facts. Use
installed native recovery guidance and the receipt's exact next action. No timeout,
silence, startup acceptance or `unverifiable` liveness proves physical exit.

| Situation | Required decision |
|---|---|
| Unknown launch or lost receipt | Inspect the same Task/Dispatch and actual owned session/workspace, preserve any operation/retry identity and follow its reconciliation action. Do not launch again or resend the brief to obtain a clearer receipt. |
| Explicit authorized cancellation | Request guarded stop for the exact owned Dispatch. Respect identity, custody, permission and Keep open refusals; no terminal injection or broad process kill. Claim stopped only on confirmed native evidence. |
| `stop_unknown` | Inspect the same worker and receipt, record unresolved physical state and escalate. It blocks replacement; no blind repeated stop, fresh launch or resource reuse. |
| Explicit intentional abandonment | Native fencing may settle the assignment while retaining possibly live resources. It is not cancellation or exit. Record the retained resources; wait for an in-flight stop to finish and never reuse an unproven/busy predecessor or its write surface. |
| Failed/stopped attempt with diagnosed changed cause | Retry the same native Task, using the newest failed Dispatch/retry identity and freshly verified placement, only after custody/settlement and original authority/bounds permit it. No new Task/Run to hide attempts. |
| Release pending or unknown | Preserve source/evidence and follow the receipt's supported recovery. Do not replace release with terminal close or treat a settled Task as proof of resource disposal. |

A failed start may still own a live agent or terminal. Before replacement, account for all
retained attempts and their resources; one selected reusable agent must be positively
proven settled and available. Abandonment cannot create a second writer in a worktree
that the old agent may still mutate. Recreating a worktree is a last resort after a
complete durable recovery archive, not a shortcut around uncertain ownership.

The native three-failed-start circuit breaker is an additional ceiling, not a target or
permission to exceed the charter's two-unproductive-attempt bound. Do not bypass it by
resetting coordination state, starting a fresh Run/Task or restarting the coordinator.
Reopening after that breaker needs explicit user-directed recovery of the same Task by
its current owner and reconciliation of all predecessors; keep the old chain in history.
A worker's failed deliverable and a native failed start are distinct evidence categories.

## Crash windows and reconciliation

Read pending intents and current native/source truth before repeating any operation.
A result not checkpointed may already have happened; a matching result is adopted with
its provenance, not executed again. Unknown stays unresolved.

- **Dispatch or steering:** reconcile native receipt, exact Task/Dispatch, delivered brief
  and current session identity. Discoverability and actual work begun are separate from
  launch acceptance. Refresh stale handles without dual-sending to old and new ones.
- **Integration:** compare recorded pre-integration tip, task candidate, resulting commit
  and tree with the campaign's actual history/tree before any re-merge. Squash source-tip
  ancestry is not an idempotency test. If a result receipt was lost, reconstruct the
  expected result read-only or in an authorized isolated comparison, never mutate the
  live branch merely to find out. A moved tip or mismatch may be unresolved history,
  not proof that integration did not happen. No matching evidence means no duplicate
  integration until reconciled. No-commit delivery instead retains exact attributable
  diff, untracked source and immutable byte manifests; do not invent commit receipts.
- **Review:** inspect the recorded run and raw output before commissioning another run.
  Reuse completed evidence only if its entire current source/scenario/config binding,
  completeness and independent validity still hold. An interrupted or unknown run is
  not PASS or permission for a concurrent review. Settle it first; an authorized
  changed-cause retry uses a fresh neutral session/config and frozen no-hooks snapshot
  under [code review](code-review.md#correction-final-review-and-preservation), never
  resumes the implementer's or interrupted reviewer's reasoning context.
- **Stop, release or deletion:** reconcile exact owned resources and native outcome;
  assignment fencing is not exit. Preserve dirty changes, untracked files, source
  manifests, reports, failing scenarios and sanitized logs outside disposable resources
  before any authorized disposal. Missing preservation or unknown release blocks reuse.
- **Deadline:** reconcile saved Automation identity, exact owner and current revision
  before replacing or removing it. A lost creation receipt does not justify a second
  timer, and timer delivery cannot authorize work the current state forbids.

Integration, final target movement and source-retention details belong to
[runtime review and integration](runtime-review-and-integration.md). No global kills,
broad reset/clean, unrequested service repair or permission weakening is recovery.

## Resume and legacy reconciliation

1. Read durable STATE, pending EVENTS, PLAN/HANDOFF, manifest and current task evidence;
   use concise pointers rather than rebuilding the campaign from a transcript dump.
2. Reconcile the actual sole execution owner and native Run/Task/Dispatch custody before
   mutation. Another live or possibly live owner is not displaced by timestamp age.
3. Check pause/cancel state and current authority. Only an explicit authorized resume
   clears an operator pause; a restart, late result or timer is not that instruction.
4. Revalidate immutable inputs, repository, named target and original starting SHA,
   actual worktree branches/HEADs and source preservation. Do not silently repin refs or
   re-hash a changed manifest to match. Route drift through the handoff/critic closure
   process and invalidate affected acceptance until rebound.
5. Refresh supported native observations, actual models/permissions and outstanding
   launch/review/integration/stop/release/deadline operations. Apply crash-window rules;
   do not duplicate a worker, review or merge to test whether the old one exists.
6. Reconcile original slice/attempt/campaign clocks and actual UTC. Rebuild TODO from
   verified state and re-establish only the required exact-owner native continuation.
7. Continue only the next incomplete authorized stage whose prerequisites and bounds
   hold. A resume is neither a new approval nor broader authority.

Legacy state is evidence to reconcile, not a template to relabel. Preserve original
schema, provider, authority and source records. If execution verifiably began, record
that evidence and retain the original mandate; leave unavailable admission/session/model
facts `null`. If only planning exists, do not manufacture execution from files or old
approval wording: apply current mandate-bound admission. Record each migration decision
as an event, without inventing START receipts, a manifest, roborev qualification or a
successful native release. An unrelated paused legacy campaign remains untouched.

## Remediation and non-convergence

Diagnose from correlated receipts, actual tool/provider outcomes, current candidate and
pending operations. Record cause, action, expected new evidence, result and next step.
One scoped steer can test a concrete hypothesis; repeated identical nudges are not a
strategy. Primary-model failure or permission refusal stops the affected path for honest
reconciliation. No silent model/provider switch, install, sign-in, global configuration
change or owner impersonation is permitted. A recorded fallback option is not automatic
authority; any changed route needs its granted policy, actual qualification and remaining
original bounds.

After two unproductive executions of the same slice, do not blindly take the same route
a third time. Escalate with evidence and options. A useful review FAIL with actionable
findings is productive, not an empty provider attempt, but substantive fix/test/review
cycles still obey declared deadlines and fix-round limits. No arbitrary counter turns
a feature into permanent FAIL, and no productive label creates an unlimited loop.

Pause the affected task and descendants when evidence shows unchanged failure after
materially different attempts, oscillating fixes/reverts, model cycling without diagnosis,
growing out-of-scope changes, contradictory requirements, unavailable capability or risk
to user data. Safe unrelated branches may proceed only when their own authority, resources
and bounds remain valid. Preserve the failure fingerprint, attempts, hypothesis, partial
source/evidence and proposed next action. An owner decision, not a late wake or agent's
optimism, resumes an operator-paused path.

## Sources and staged links

Mapped guarantees: [legacy state and recovery](../../acd/references/state-and-recovery.md),
[legacy progress semantics](../../acd/references/progress-watchdog.md) and
[legacy entrypoint sections 11 and 12](../../acd/SKILL.md). These are migration sources,
not operative polling, hard-expiry restart, fallback or watcher instructions. The
[obligation ledger](obligation-ledger.md#reference-obligations) retains their identities;
its historical pending provider/destination wording awaits separately owned amendment
and cannot override the accepted handoff/code-review interfaces.

At this slice, [Orca runtime](orca-runtime.md),
[runtime review and integration](runtime-review-and-integration.md),
[STATE](../templates/STATE.json), [PLANNING_STATE](../templates/PLANNING_STATE.json) and
[TODO](../templates/TODO.md) are **PENDING** future targets. Final cross-document validation
must reconcile all fields, enums, links, anchors and placeholder legends at exact hashes.
The one placeholder in this reference is `{prefix}`, the private campaign artifact prefix;
no runnable JSON or command recipe is supplied. Earlier files' pending-link statements
are historical slice observations, not automatic acceptance of this file.

This document is a contract, not runtime recovery proof. Synthetic tabletops must be
labeled synthetic; unavailable fault injection stays UNTESTED. Staging changes no installed
loading path and grants no installation, publication, successor dispatch or production
cutover authority. The author's receipt leaves independent acceptance PENDING.
