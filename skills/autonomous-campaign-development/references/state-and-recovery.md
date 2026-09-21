# Canonical State, Monitoring, and Recovery

The campaign's memory lives on disk inside the campaign directory, never in chat history
or temp directories. One canonical model: STATE.json is authoritative; TODO.md is its
human-readable projection; EVENTS.jsonl is the append-only audit trail; evidence/ holds
sanitized reports; REPORT.md is the final deliverable summary.

## Files and naming

All operational artifacts share the campaign prefix (for example `acd_`):

| File | Role | Writer |
|---|---|---|
| `{prefix}_STATE.json` | canonical machine state | coordinator only |
| `{prefix}_TODO.md` | human projection of state | coordinator only |
| `{prefix}_EVENTS.jsonl` | append-only chronological events | coordinator only |
| `{prefix}_evidence/` | sanitized reports, logs, screenshots per task | coordinator files what agents deliver |
| `{prefix}_REPORT.md` | final campaign report | coordinator only |

No secrets in state or evidence, ever. Sanitize tokens, keys, and personal data before
anything enters the evidence directory.

## Sole-writer and durability rules

- Exactly ONE coordinator writes shared state. Agents never write STATE/TODO/EVENTS; they
  report into their task-owned evidence slot.
- A stale timeout on a previous writer's timestamp is NOT proof the lock is free. Before
  taking over, reconcile ownership explicitly (see resume protocol) - the practical rule
  is: never run two coordinators; if another live coordinator session is detected, stop
  and reconcile with the user.
- Atomic replace: write a temp file in the SAME directory, flush/fsync as available, then
  rename over STATE.json. Bump `revision` on every write and record `last_updated_at`.
- Event-before-action: append a durable intent event to EVENTS.jsonl BEFORE performing an
  external operation (merge, dispatch, deletion), then checkpoint the result into state.
  Recovery uses the intent log to detect operations that may have happened without a
  checkpoint.
- Null semantics: unknown is `null`, always. Never invent a value to fill a field; absent
  evidence is recorded as absent.

## STATE.json schema

Template: [../templates/STATE.json](../templates/STATE.json). Key enums:

- `tasks[].stage`: `pending` -> `develop` -> `runtime_test` -> `review` -> `integrate` ->
  `post_merge_smoke` -> `cleanup` -> `done`; any task may be `paused`. `runtime_test` and
  `review` are loops (test->fix->test, review->fix->retest->re-review), not single passes.
- `tasks[].review.verdict`: `PASS` | `FAIL` | `null`, always paired with
  `review.bound_to` (exact commit/tree/build); a verdict without its binding is invalid.
- Status mapping: internal `in_review` <-> Orca external `in-review`; internal
  `in_progress` <-> Orca `in-progress`. No other spellings.
- `lifecycle`: `planning` -> `awaiting_fresh_session_start` -> `executing` ->
  `completed`; the `pause` block is orthogonal. `sessions.planning` and
  `sessions.execution` record session identities independently; `approval` (the plan
  gate) and `start` (the execution start, bound to `plan_manifest.sha256`) are separate
  records - see [handoff-and-start.md](handoff-and-start.md).

Per task, state stores: stage history and current stage, dependency edges, exclusive
resources, worktree name/path, actual returned git branch, task tip SHA, session handle
and session identity, resolved model in use, runtime evidence pointers, reviewer handle
and verdicts with bindings, remediation records (cause/action/expectation/result/next),
merge receipts, timestamps (`created_at`, `last_checked_at`, `last_progress_at`), pause
reason, cleanup inventory and verification. Campaign-level: pinned original target branch
and starting SHA, campaign branch/worktree, approval record (scope, final merge strategy,
push excluded), plan manifest binding, start record, session identities, lifecycle,
requested/resolved/pinned models, final-stage statuses, next action, active pause with
actor.

## State lifecycle and legacy migration

Lifecycle transitions are event-logged: `planning` -> `awaiting_fresh_session_start`
(HANDOFF + manifest written, planning session stopped) -> `executing` (fresh-session
START validated) -> `completed`. A restart never re-runs a completed transition.

Legacy states (`schema_version` 1 or missing, written by skill versions <= 1.0.0) have
no lifecycle/sessions/plan_manifest/start fields; under that contract a plan approval
could begin execution in the same session. Migration rules - the coordinator reconciles
and records honestly, never fabricates:

- Execution already verifiably began (worktrees, live sessions, or merge receipts
  exist): the original approval REMAINS valid and the campaign resumes as executing.
  Set `lifecycle: executing`, keep `sessions`/`start` null where unknown, do NOT invent
  a start record or manifest hash; append a migration event naming the evidence.
- Approved but nothing began: set `lifecycle: awaiting_fresh_session_start`; a
  first START under the current contract (fresh session, manifest validation) is
  required before any execution. A legacy campaign has no manifest: `plan_manifest`
  stays null, and START relies on explicit operator confirmation recorded in state -
  identity that cannot be verified is never claimed as enforced.
- Never auto-enforce: the coordinator must not silently rewrite a legacy state to look
  like a native schema-2 campaign; reconciliation decisions are recorded as events.

## TODO projection

`{prefix}_TODO.md` mirrors state for humans and covers BOTH per-task stages and the final
campaign stages. If the environment offers a todo-list tool, it mirrors the same data;
otherwise the file on disk IS the operational checklist - an absent tool never means "no
checklist", it means read the disk. A checkbox is checked only after the action is
actually verified (e.g. cleanup proves removal; it is never a promise). Rebuild the TODO
from state after any restart; never trust a possibly stale copy.

## Ten-minute monitoring loop

While the coordinator is active, every ten minutes poll EVERY active development,
testing, review, and remediation session:

1. Session alive? Terminal/process/session-file evidence - this is transport/process
   activity ONLY, not progress.
2. Progressing? Apply the progress semantics from
   [progress-watchdog.md](progress-watchdog.md): keep last observed, last successful
   assistant, last completed tool (isError separate), and last semantic progress
   distinct; only explicit structured checkpoints update `last_progress_at`. An idle
   ready agent is not a crash; a long-running command within its deadline is not a
   stall. The optional observer scripts may feed this loop; their output is never
   authoritative and they never write canonical state.
3. Finished or `in-review`? Validate a clean committed snapshot plus runtime report, then
   commission independent review EXACTLY ONCE per candidate (dedupe by commit SHA).
4. Fix rounds dispatched? Reset worktree status to `in-progress` so stale `in-review`
   cannot re-trigger review.
5. Append an event and checkpoint state each loop.

A status file is not a running scheduler: after the coordinator closes or the host
reboots, nothing polls autonomously unless a separately verified watcher exists. Do not
assume one.

## Crash windows and recovery

Designed windows: (a) intent logged, external operation not yet done -> safe to redo;
(b) operation done, state not yet checkpointed -> detect via intent + external truth.
Recovery rule per operation class:

- Squash merge: compare the campaign branch log/tree against recorded receipts BEFORE any
  re-merge. A squash source tip is not an ancestor of its squash commit, so
  ancestor-based idempotency checks are useless - match the receipt (pre-squash SHA,
  squash SHA, tree) instead. Receipt match => already integrated; do not merge again.
  If the crash happened before the receipt was checkpointed, reconstruct the candidate
  from the intent event's inputs (task tip, pre-squash campaign SHA): squash those inputs
  in a dry comparison and check whether the actual campaign tip's tree already equals the
  expected result - tree equality means integrated, tree mismatch means not integrated.
- Dispatch: session handle in state may be stale after restart - refresh handles from
  `terminal list`, reconcile the agent's actual working state from its session and tree.
- Review: a review in flight during a crash is simply re-commissioned against the same
  frozen commit; a verdict referencing a commit that no longer matches the candidate tip
  is stale by construction and never reused.

## Continue-execution resume protocol

On `continue execution` (or any restart), in order:

0. No `start.started` in state and lifecycle `awaiting_fresh_session_start`: this is a
   FIRST START, not a resume - follow [handoff-and-start.md](handoff-and-start.md).
1. Read STATE, TODO, PLAN, and current task reports - no long history research.
2. Acquire/reconcile coordinator ownership; exactly one coordinator proceeds.
3. Validate the repo: target branch and starting SHA unchanged or consciously re-pinned;
   campaign branch/worktree exist; recorded commits present.
4. Refresh stale session handles (`terminal list`), verify liveness of agents claimed
   running; a dead agent is remediated, not duplicated.
5. Reconcile in-flight reviews and merges against the crash-window rules above.
6. Rebuild TODO from state; resume from the next incomplete stage.
7. A restart is NEVER a new approval: the recorded approval and its scope still bind, and
   anything exceeding them still stops for the user.

No duplicate workers, no duplicate merges, no lost dirty work, no re-planning from
scratch.

## Remediation and non-convergence

Remediation ladder, each rung verified before the next:

1. Diagnose from evidence (session tail, process state, diff, events).
2. Targeted nudge into the live session with concrete state and the exact next step;
   verify NEW progress afterwards. One nudge, then evaluate.
3. Approved fallback switch: stop the session, start a new one with the approved fallback
   model. No fallback configured, or failure needs a different provider -> pause for user
   input.
4. Fresh session with durable handoff (preserve commits, dirty changes, untracked files,
   reports, failing scenarios, session identifiers FIRST; ensure the prior writer is
   stopped/fenced and its scoped processes accounted for). Recreating the session in the
   SAME worktree is normal; recreating the WORKTREE is a last resort only after a full
   recovery archive exists.

Never: blind repeated nudges, model toggles without diagnosis, global kill/pkill, broad
`git clean`/`reset`, unauthorized service changes. Record cause, action, expectation,
result, and next step for every rung.

Non-convergence is NOT an attempt counter. Pause the task (and its descendants; safe
unrelated DAG branches continue) only on evidence: repeated identical failure fingerprint
with no measurable progress after materially different attempts; oscillating
fixes/reverts; model cycling without diagnosis; growing out-of-scope diff; contradictory
requirements; unavailable capability; risk to user data. Present evidence, attempts,
hypothesis, and proposed options. Do NOT impose an arbitrary N-strike test/review cutoff;
numerical thresholds, if configured in the campaign approval, trigger diagnosis, never
automatic permanent FAIL. The user can stop anything at any time; an operator pause is
never self-resumed. This conservative default is configurable in campaign approval -
never a secret fixed loop cap.
