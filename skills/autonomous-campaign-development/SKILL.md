---
name: autonomous-campaign-development
description: Orchestrate multi-agent dev campaigns in Orca worktrees
version: 1.0.0
metadata:
  hermes:
    category: software-development
---

# Autonomous Campaign Development

Run a multi-task development campaign with OMP coding agents in Orca-managed worktrees.
You are the coordinator: you plan, dispatch, integrate, monitor, and clean up - you never
write source code. One explicit plan approval authorizes the whole campaign; runtime
evidence plus independent review, never unit tests or agent self-reports, prove each task.

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

### 4. One approval gate

Present the plan plus resolved models; obtain ONE explicit approval before execution. It
authorizes scoped development, tests, reviews, task squash merges, the campaign completion
merge, and safe cleanup - record the final-merge strategy (default `--no-ff`) in the
approval. No automatic per-task or per-phase human review gates afterwards. STOP and ask
the user when: scope or contracts change in a way that needs a decision, a destructive
action looms, capability or access is missing, or non-convergence is evidence-based.
Push, publication, and deployment are separate explicit permissions.

### 5. Topology

Capture the original NAMED target branch and its full starting SHA; do not assume
main/master and do not reinterpret a detached HEAD later - a detached start requires the
user to name the target. Create the Orca-managed `{prefix}-campaign` integration worktree
from the pinned start, then task worktrees from the appropriate current campaign tip.
Orca may auto-generate branch names: record the actually returned branch and HEAD; on a
HEAD mismatch, do not start. Full contract:
[references/runtime-review-and-integration.md](references/runtime-review-and-integration.md).

### 6. Per-task loop

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

### 7. Concurrency

At most THREE simultaneously active coding agents, fix and remediation agents included;
no hidden fanout. One writer per worktree; reviewer ownership prevents simultaneous
mutation. A task starts only after its prerequisites are independently reviewed,
squash-integrated into the campaign, and post-merge smoke tested. A task releases its
dependents the same way - never on the executor's done message. Cleanup is mandatory,
tracked, and gates resource reuse.

### 8. State and monitoring

Canonical campaign state lives in the campaign directory as `{prefix}_STATE.json`,
`{prefix}_TODO.md`, `{prefix}_EVENTS.jsonl`, `{prefix}_evidence/`, and
`{prefix}_REPORT.md` ([templates/STATE.json](templates/STATE.json),
[templates/TODO.md](templates/TODO.md)). The coordinator is the sole writer of shared
state; agents report into task-owned evidence. Update state at every meaningful
transition and on a ten-minute cadence while active: poll EVERY active development,
testing, review, and remediation session; compare processes, commands, and checkpoint
evidence - output silence alone proves nothing, and an idle ready task is not a crash.
Schema, crash windows, resume and remediation: [references/state-and-recovery.md](references/state-and-recovery.md).

### 9. Remediation and non-convergence

Ladder: diagnose -> targeted nudge, verified by new progress -> approved fallback switch
where appropriate -> fresh session with durable handoff when needed. Never blind repeated
nudges or model toggles; a live long-running command is not a stall. Non-convergence is
an evidence-based pause, not an attempt counter: pause a task (and its descendants; safe
unrelated branches continue) on a repeated identical failure fingerprint with no
measurable progress after materially different attempts, oscillating fixes/reverts, model
cycling without diagnosis, growing out-of-scope diff, contradictory requirements,
unavailable capability, or risk to user data - presenting evidence, attempts, hypothesis,
and options. Numerical thresholds, if configured, only trigger diagnosis. An operator
pause is never self-resumed. Rules: [references/state-and-recovery.md](references/state-and-recovery.md#remediation-and-non-convergence).

### 10. End of campaign

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
- Before relying on a modified copy of this skill, run the static checks and tabletop
  walkthroughs in [references/validation-tabletop.md](references/validation-tabletop.md).
- Dispatch mechanics and command shapes: [references/hermes-orca-omp.md](references/hermes-orca-omp.md);
  state and recovery: [references/state-and-recovery.md](references/state-and-recovery.md).
