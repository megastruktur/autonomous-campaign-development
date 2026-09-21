---
name: autonomous-campaign-development
description: Orchestrate multi-agent dev campaigns in Orca worktrees
version: 1.1.0
metadata:
  hermes:
    category: software-development
---

# Autonomous Campaign Development

Run a multi-task development campaign with OMP coding agents in Orca-managed worktrees.
You are the coordinator: you plan, dispatch, integrate, monitor, and clean up - you never
write source code. One explicit plan approval authorizes WHAT the campaign may do; a
separate explicit START, given in a distinct fresh session bound to a frozen manifest,
begins execution. Runtime evidence plus independent review, never unit tests or agent
self-reports, prove each task.

## When to Use

- The request decomposes into several coding tasks with dependencies, shared contracts, or
  parallelizable work, and you can dispatch OMP agents into Orca worktrees and at least one
  independent reviewer session.
- Not for: single-task fixes you do yourself, pure research, or operations without code.
- This skill is a generic default. Repository instructions (for example AGENTS.md), hooks,
  permission systems, and the current campaign approval always bind; surface conflicts
  instead of bypassing them.

## Roles

- **Coordinator (you)**: plans, settles shared contracts centrally, dispatches, integrates,
  monitors, keeps state. Never implements features or fixes, never performs substantive
  code review, never edits source - conflict resolutions go back to an OMP agent.
- **OMP coding agent**: exactly one writer per task worktree; develops, fixes, retests,
  writes evidence.
- **Runtime test executor**: exercises real-runtime scenarios per task; may be separate
  from the coding agent; its report never substitutes for independent review.
- **Independent reviewer**: an inquisitor-style profile or agent when actually available,
  otherwise a separately spawned read-only session - never the implementing session.
  Returns an explicit complete PASS or FAIL verdict plus actionable findings; no edits,
  commits, merges, pushes, or automatic fixes. Read-only is an enforced capability when
  available and an explicit mandate otherwise.

## Procedure

### 1. Intake

Read the request; ask focused clarification questions; propose improvements before locking
the plan. Bounded context discovery only - do not deeply explore implementation code while
planning. Settle shared API/schema/resource contracts centrally; sibling tasks never
design shared interfaces independently. Size tasks for the actually chosen worker model,
not a hard-coded model.

### 2. Plan

Create durable files inside the repository (never chat memory or temporary directories):
`plans/{campaign_name}/{prefix}_PLAN.md` plus one `{prefix}_{task_name}.md` per task.
Templates: [templates/PLAN.md](templates/PLAN.md), [templates/TASK.md](templates/TASK.md).

- Campaign/task names are English lowercase slugs; `{prefix}` is a unique short
  abbreviation. Worktree display names are `{prefix}-{task_name}`; reserve
  `{prefix}-campaign` for the integration worktree.
- Every task file carries: goal, scope allowlist (explicit paths), non-goals,
  dependencies, shared resource/API/schema contracts, acceptance criteria, and an
  actionable Real Runtime Testing section.
- Resolve every unknown runtime command honestly before dispatch - never invent commands,
  never let a green unit suite substitute for a real one.

Plan the DAG with explicit dependency edges and resource exclusions (files, APIs,
migration ordering, schema ownership, lockfiles, build output, ports, fixture data,
databases, external side effects). Possible parallel groups are explanatory views, never
fixed-wave barriers.

### 3. Model questionnaire

Before development, ask once: coding model, fallback model, independent reviewer model.
Each answer is `default` (the relevant runtime/profile's actual configured default - never
an orchestrator-chosen stand-in) or an exact available ID; fallback may additionally be
none. Record requested AND resolved IDs, verify the actual startup model of every agent,
and pin resolved defaults for reproducibility after restart unless the user changes them.
With no fallback: same-model session repair is allowed; a failure requiring another
provider or model pauses for user input. Never silently pick an unapproved model, never
print credentials. Mechanics: [references/hermes-orca-omp.md](references/hermes-orca-omp.md).

### 4. One approval gate (WHAT)

Present the plan plus resolved models; obtain ONE explicit approval of WHAT the campaign
may do. It authorizes scoped development, tests, reviews, task squash merges, the
campaign completion merge, and safe cleanup - record the final-merge strategy (default
`--no-ff`) in the approval. Approval is NOT START and adds no per-task human gates: the
planning session then writes the durable HANDOFF plus its hash manifest
([templates/HANDOFF.md](templates/HANDOFF.md)), records state lifecycle
`awaiting_fresh_session_start`, and STOPS - it never creates execution worktrees or
starts agents, even though the plan is approved. STOP and ask the user when: scope or
contracts change in a way that needs a decision, a destructive action looms, capability
or access is missing, or non-convergence is evidence-based. Push, publication, and
deployment are separate explicit permissions.

### 5. HANDOFF and fresh-session START

Execution begins ONLY in a distinct, new, clean coordinator session when the user
explicitly says START (the exact prompt from the HANDOFF), never in the planning
session. On START: record the execution session identity; recompute the manifest
(frozen PLAN/task/contract/HANDOFF hashes) and match it against state - drift invalidates
consent and stops for reconciliation, never a quiet re-hash; validate repo, named target
branch, starting SHA, worktree absence/ownership, and actual capabilities; resolve every
runtime command honestly, never guess. Record start and approval independently; missing
runtime identity cannot claim enforced clean context (explicit operator confirmation,
still no knowingly same-session start). Already-started campaigns resume under their
recorded start without re-gating. Full contract:
[references/handoff-and-start.md](references/handoff-and-start.md).

### 6. Topology

The EXECUTION session (after START) captures/validates the original NAMED target branch
and its full starting SHA; do not assume main/master and do not reinterpret a detached
HEAD later - a detached start requires the user to name the target. Create the
Orca-managed `{prefix}-campaign` integration worktree from the pinned start, then task
worktrees from the appropriate current campaign tip. Orca may auto-generate branch
names: record the actually returned branch and HEAD; on a HEAD mismatch, do not start.
Full contract:
[references/runtime-review-and-integration.md](references/runtime-review-and-integration.md).

### 7. Per-task loop

Mandatory stages in order: develop -> runtime test-loop -> independent review-loop -> squash
integration/conflict handling -> post-merge runtime smoke -> preserve evidence and cleanup
([templates/TODO.md](templates/TODO.md)). Test -> fix batch -> test; review FAIL -> executor
fix -> runtime retest -> fresh independent review. No fixed iteration limit: repeat while
evidence shows progress. New tested or reviewed changes invalidate prior verdicts; bind
every result to the exact commit/tree/build and scenario version. The coordinator
commissions the independent review itself, with an unbiased packet (acceptance criteria,
contracts, diff base/tip, runtime evidence, known findings) - author self-review is
optional preparation, never a gate. Detailed contracts:
[references/runtime-review-and-integration.md](references/runtime-review-and-integration.md).

### 8. Concurrency

At most THREE simultaneously active coding agents, fix and remediation agents included;
no hidden fanout. One writer per worktree; reviewer ownership prevents simultaneous
mutation. A task starts only after its prerequisites are independently reviewed,
squash-integrated into the campaign, and post-merge smoke tested. A task releases its
dependents the same way - never on the executor's done message. Cleanup is mandatory,
tracked, and gates resource reuse.

### 9. State and monitoring

Canonical campaign state lives in the campaign directory as `{prefix}_STATE.json`
(schema 2: lifecycle `planning`/`awaiting_fresh_session_start`/`executing`/`completed`
with planning and execution sessions and the start recorded independently),
`{prefix}_TODO.md`, `{prefix}_EVENTS.jsonl`, `{prefix}_evidence/`, and
`{prefix}_REPORT.md` ([templates/STATE.json](templates/STATE.json),
[templates/TODO.md](templates/TODO.md)). The coordinator is the sole writer of shared
state; agents report into task-owned evidence. Update state at every meaningful
transition and on a ten-minute cadence while active: poll EVERY active session.
Liveness semantics are strict: transport or process activity (stream, bytes, PID,
mtime, JSONL growth) is not progress, a successful assistant response is not task
progress, and neither is completion - keep last observed, last successful assistant,
last completed tool (errors separate), and last semantic progress distinct; only
explicit structured checkpoints are semantic progress; unknown is reported as unknown,
never healthy. The bundled observer scripts are optional, observer-only helpers, never
authoritative and never mutating. Semantics and CLI contract:
[references/progress-watchdog.md](references/progress-watchdog.md). Schema, crash
windows, resume and remediation: [references/state-and-recovery.md](references/state-and-recovery.md).

### 10. Remediation and non-convergence

Ladder: diagnose -> targeted nudge, verified by new progress -> approved fallback switch
where appropriate -> fresh session with durable handoff when needed. Never blind repeated
nudges or model toggles; a live long-running command within its deadline is not a stall,
and the observer (if used) never kills or remediates - it only reports. Non-convergence is
an evidence-based pause, not an attempt counter: pause a task (and its descendants; safe
unrelated branches continue) on a repeated identical failure fingerprint with no
measurable progress after materially different attempts, oscillating fixes/reverts, model
cycling without diagnosis, growing out-of-scope diff, contradictory requirements,
unavailable capability, or risk to user data - presenting evidence, attempts, hypothesis,
and options. Numerical thresholds, if configured, only trigger diagnosis. An operator
pause is never self-resumed. Rules: [references/state-and-recovery.md](references/state-and-recovery.md#remediation-and-non-convergence).

### 11. End of campaign

Preconditions: every task TODO done, every required runtime scenario exercised, full
campaign acceptance/seams runtime test plus independent final review at the exact
campaign tip. If the original target moved, integrate the latest target into the campaign
through the same fix/test/review rules and re-run final verification. Verify expected
refs immediately before the coordinator-only final merge (default `--no-ff`, recorded in
approval), run a post-merge runtime smoke ON the target, archive receipts and evidence,
stop scoped test resources, then remove the campaign worktree. Push stays disabled unless
separately approved; merge is not user delivery. Endgame and cleanup contract:
[references/runtime-review-and-integration.md](references/runtime-review-and-integration.md#cleanup).

## Pitfalls
- Treating plan approval as execution start: the planning session never creates
  worktrees or agents; START belongs to a distinct fresh session bound to the manifest.
- Starting execution in the planning session because the user says "go" - refuse and
  hand over the START prompt; missing session identity never claims enforced clean
  context.
- Manifest drift: quietly re-hashing the manifest to match edited plan files instead of
  stopping - changed frozen files invalidate consent until re-approved.
- Reading transport activity (stream, bytes, PID, mtime, JSONL growth) or a successful
  assistant response as task progress or completion; attributing provider-global errors
  to a specific session without correlation.
- Treating the optional observer as a scheduler, killer, or authoritative health
  source; it only reports, and stale/unknown observations stay unknown.
- A green unit suite is not a working feature; mock-only or unexecuted real integration is
  never "verified". A passing rerun does not make a failing acceptance run "flaky".
- A commit arriving is not "feature done": wait for the executor's explicit ready handoff,
  final runtime evidence, a clean frozen candidate, and an explicit complete independent
  verdict - shell rc=0 or a terminated review process is not PASS.
- Reviewing with the author's reassuring summary or a "already PASS, confirm" framing
  biases the reviewer; commission with the raw packet instead.
- Fixing one occurrence of a defect class (for example the claim path) and missing its
  siblings (release, rebind): re-review covers the corrected finding, sibling paths of
  the same class, and introduced regressions.
- Pasting a brief into the worktree startup shell or any fallback shell; JSON send
  success does not prove execution started.
- Stale `in-review` status triggering early review after a fix dispatch - reset to
  in-progress on every remediation round.
- A fresh worktree inherits the base branch's tracked brief file - overwrite and verify
  the title before dispatch.
- Squash-merged branches look "unmerged" to git: never force-delete on status text; prove
  the recorded receipt instead.
- Crash between squash and state checkpoint: compare campaign log/tree against receipts
  before any re-merge; ancestor checks do not work for squash.
- Keeping state in chat memory or a temp directory; assuming main/master; running two
  coordinators; treating a status file as a scheduler that survives reboot.
- Releasing dependents on an executor done message instead of post-merge smoke.
- Bare `orca` on the host is the wrong program - the host CLI is `orca-ide`.

## Verification

- Campaign health: state revision advances with matching events; every active session has
  recent evidence; no task sits at a later stage than its bound evidence supports;
  dependents released only after prerequisite post-merge smoke; cleanup checkboxes reflect
  actual verified actions, not promises.
- Start boundary: state lifecycle, sessions, and start records are coherent - start
  exists only in a distinct execution session whose recorded manifest hash matches the
  frozen files; the planning session created no worktrees or agents; resumes of a
  started campaign carry the original approval without re-gating.
- Progress claims distinguish last observed, last successful assistant, last completed
  tool (errors separate), and last semantic progress; unknown is never reported healthy.
- Before relying on a modified copy of this skill, run the static checks and tabletop
  walkthroughs in [references/validation-tabletop.md](references/validation-tabletop.md).
- Dispatch mechanics and command shapes: [references/hermes-orca-omp.md](references/hermes-orca-omp.md);
  state and recovery: [references/state-and-recovery.md](references/state-and-recovery.md).
