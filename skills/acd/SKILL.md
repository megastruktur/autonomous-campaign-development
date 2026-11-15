---
name: acd
description: Orchestrate multi-agent dev campaigns in Orca worktrees
version: 1.7.0
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
self-reports, prove each task. Unattended coordinator wakeups are sustained only by a
verified wakeup mechanism - the bounded event watcher with completion notification
(Option A, recommended for unattended runs) or the native session heartbeat
(Option B) - never by the observer scripts.

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
- **Independent reviewer**: two engines, selected by the OCR gate at planning start
  (section 0): when OCR (`ocr` CLI) is installed and working, code review runs
  EXCLUSIVELY through OCR and the coordinator derives the verdict from its JSON output;
  otherwise an inquisitor-style profile or agent when actually available, else a
  separately spawned read-only session - never the implementing session. Either engine
  yields an explicit complete PASS or FAIL verdict plus actionable findings; no edits,
  commits, merges, pushes, or automatic fixes. Read-only is an enforced capability when
  available and an explicit mandate otherwise. Contract:
  [references/ocr-review.md](references/ocr-review.md).

## Procedure

### 0. Code-review engine gate (OCR, v1.7.0)

At the very start of planning, detect OCR (`ocr` CLI, alibaba/open-code-review):
resolve the binary (PATH plus the runtime's npm global bin dir when sandboxed PATHs
hide it) and run `ocr version`. If installed and working (`ocr llm test` passes), ALL
code review - per-task and final - runs EXCLUSIVELY through OCR: no inquisitor reviewer
sessions for code, and no silent fallback on OCR failure (remediate or escalate to the
user). If not installed, OFFER installation once at the start
(`npm install -g @alibaba-group/open-code-review`); a declined offer records the standard
session reviewer for this campaign. Record the decision (`review_engine`: `ocr` or
`session`) in HANDOFF and STATE. The planning critic and runtime testing are unchanged.
Full contract: [references/ocr-review.md](references/ocr-review.md).

### 1. Intent and mandatory repository discovery

Capture user intent, clarify consequential ambiguity, and brainstorm functionality; the
coordinator may reason and recommend scope. Perform MANDATORY bounded, read-only repository
discovery of relevant instructions, dependencies, interfaces, patterns, and test/runtime
entry points - trace symbols rather than guessing, but do not deeply implement or perform an
exhaustive review. Inspect repository manifests and lockfiles not only to list current
dependencies but also to identify (a) already-installed libraries or runtime standard-library
modules that can cover part of the requested work, and (b) dependency/license/footprint
policies constraining library adoption (for example `stdlib-only` or zero-dependency
mandates, license restrictions, bundle/binary constraints, package manager + lockfile).
Record candidate functional slices - both whole-feature and sub-problem building blocks -
to evaluate for open-source library coverage in Phase 2. Record outcomes and evidence in
`{prefix}_INTENT.md`. Do not create a DAG.
Full contract: [references/planning-and-design.md](references/planning-and-design.md).

### 2. Web research and architecture

Perform MANDATORY web research for every campaign, scaled to feature size, novelty, and risk.
Retrieve and cite current primary/authoritative sources; never substitute model memory for
failed web access. Search for open-source, popular, and non-deprecated libraries covering the
WHOLE requested functionality or specific parts/sub-problems (whole and partial coverage)
BEFORE designing custom implementations; search order: (1) existing repository dependencies
and the language standard library, (2) whole-functionality open-source libraries/plugins/
tools, (3) partial/sub-problem open-source libraries. Verify every candidate through LIVE
primary sources - both the package registry page/metadata AND the upstream source repository,
never model memory - and accept only libraries that are:

- Open-source and license-compatible: a verified OSI-approved license compatible with the
  repository license/policy - no proprietary/SSPL/BSL or conflicting copyleft unless the
  user explicitly approves it.
- Popular and battle-tested: live adoption evidence (downloads/dependents,
  stars/contributors, or ecosystem-standard standing proportionate to the niche).
- Actively maintained and NOT deprecated: upstream repository not archived, package not
  marked deprecated/yanked in registry metadata or README/issues, no upstream notice
  directing users to a successor, and compatibility with the repository's current
  language/runtime/framework versions - stable feature-complete maturity is not abandonment.
- Security and footprint fit: no unpatched critical advisories/CVEs, proportionate
  transitive/native build weight, and compliance with explicit `stdlib-only` or bundle
  constraints.

Reuse-first anti-NIH default balanced against bloat: adopt qualifying libraries by default
for non-trivial functionality; writing custom code where a qualifying library exists
requires explicit evidence-backed justification in `{prefix}_RESEARCH.md`. Conversely, do
not add external micro-packages for trivial ~10-20 line standard-library operations. If a
library covers ~80-100% of the requested capability and collapses a multi-task build into
thin integration, surface that whole-coverage finding to the user instead of padding custom
tasks to justify a multi-agent DAG. Produce `{prefix}_RESEARCH.md`: compare architecture
patterns, choose one using repository evidence and research, and map decisions back to
intent. Include substantive, proportionate Security and UX analysis, especially for big,
sensitive, or user-facing features. Settle shared API/schema/resource direction centrally.
Set `research.oss_library_evaluation_completed: true` in `{prefix}_PLANNING_STATE.json` and
`{prefix}_STATE.json` only after the live-verified OSS evaluation is written into
`{prefix}_RESEARCH.md`. No task DAG yet.

### 3. Independent critique and revision loop

Commission an independent read-only critic and preserve rounds in `{prefix}_CRITIQUE.md`.
architecture/research evidence, Security, UX, and execution readiness. The critic audits OSS
build-vs-reuse coverage: live non-deprecation/popularity/license evidence, anti-NIH
justifications, supply-chain/CVE posture, and dependency/lockfile execution readiness. Revise
the design, answer every finding, and repeat a fresh full critique. Loop until `CONVERGED` with no
unresolved blocking findings, bound to the current artifact hashes. If architecture
contradicts explicit user intent, user intent wins: revise the architecture or surface a
genuine infeasibility/trade-off; never silently change requirements. Material intent changes
return to phase 1; material architecture/research changes return to phase 2. Non-convergence
pauses with evidence and options.

### 4. DAG and task decomposition (only after convergence)

The DAG gate requires completed intent + repository discovery, actual cited web research,
and a `CONVERGED` independent critique bound to current INTENT/RESEARCH hashes; record these
in `{prefix}_PLANNING_STATE.json` and STATE. Only now create durable files inside the
repository (never chat memory or temporary directories):
`plans/{campaign_name}/{prefix}_PLAN.md` plus one `{prefix}_{task_name}.md` per task.
Templates: [templates/PLAN.md](templates/PLAN.md), [templates/TASK.md](templates/TASK.md).
Preserve traceability from intent through research/converged architecture to each task and
its acceptance/runtime scenarios; decomposition may not silently expand or contradict intent.

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
databases, external side effects). Pin exact approved package names, version constraints,
and purpose in shared contracts; forbid coding agents from ad-hoc unapproved package
installs, and serialize manifest + lockfile updates through a dedicated prerequisite
foundation task or exclusive resource ownership so parallel worktrees never collide on
lockfiles. Possible parallel groups are explanatory views, never
fixed-wave barriers. Size tasks for the actually chosen worker model, not a hard-coded model.

### 5. Model questionnaire

Before development, ask once: coding model, fallback model, independent reviewer model,
and optionally a heavyweight final-review model for exact-head final reviews. Each
answer is `default` (the relevant runtime/profile's actual configured default - never
an orchestrator-chosen stand-in) or an exact available ID; fallback and final-review
may additionally be none. Record requested AND resolved IDs, verify the actual startup
model of every agent, and pin resolved defaults for reproducibility after restart
unless the user changes them. Never hardcode specific vendor models into the plan
(neither for wave execution nor for final review); a heavyweight final-review model is
the user's explicit choice, not a requirement. With no fallback: same-model session
repair is allowed; a failure requiring another provider or model pauses for user
input. Never silently pick an unapproved model, never print credentials. When the OCR
engine is selected, the reviewer model (and the optional final-review model) is OCR's
model: verify it is served by OCR's endpoint and supports native tool calling, pin it
in OCR's provider config, and pass it explicitly on every run
([references/ocr-review.md](references/ocr-review.md)). Mechanics:
[references/hermes-orca-omp.md](references/hermes-orca-omp.md).

### 6. One approval gate (WHAT)

Present the plan plus resolved models and the converged design; obtain ONE explicit
approval of WHAT the campaign
may do. Newly adopted third-party dependencies (package, version constraint, license) are
presented clearly inside this single WHAT gate - pausing earlier only for license conflicts,
new host/system binary prerequisites, or the Phase 2 whole-campaign collapse disclosure. It
authorizes scoped development, tests, reviews, task squash merges, the
campaign completion merge, and safe cleanup - record the final-merge strategy (default
`--no-ff`) in the approval. Approval is NOT START and adds no per-task human gates: the
planning session then writes the durable HANDOFF plus its hash manifest
([templates/HANDOFF.md](templates/HANDOFF.md)), records state lifecycle
`awaiting_fresh_session_start`, and STOPS - it never creates execution worktrees or
starts coding/execution agents, even though the plan is approved. The phase-3 read-only
planning critic is the sole planning-time delegated-session exception, not execution START.
STOP and ask the user when: scope or
contracts change in a way that needs a decision, a destructive action looms, capability
or access is missing, or non-convergence is evidence-based. Push, publication, and
deployment are separate explicit permissions.

### 7. HANDOFF and fresh-session START

Execution begins ONLY in a distinct, new, clean coordinator session when the user
explicitly says START (the exact prompt from the HANDOFF), never in the planning
session. On START: record the execution session identity; recompute the manifest
(frozen PLAN/task/contract/HANDOFF hashes) and match it against state - drift invalidates
consent and stops for reconciliation, never a quiet re-hash; validate repo, named target
branch, starting SHA, worktree absence/ownership, and actual capabilities; resolve every
runtime command honestly, never guess. Record start and approval independently; missing
runtime identity cannot claim enforced clean context (explicit operator confirmation,
recorded start without re-gating. START - and adoption of an already-running campaign -
must ALSO establish and verify a sanctioned coordinator wakeup mechanism in the
execution session before any claim of autonomous monitoring. Option A: spawn the
bounded event watcher with `notify=true` and prove the chain - at least one event
exit AND one `SLICE_TIMEOUT` exit, each -> completion notification -> coordinator
turn acting on the exit summary. Option B: a terminal controller (the operator, approved
automation, or the safely pinned owning coordinator) installs `/heartbeat every 5m`
with a bounded campaign instruction through the guarded, identity-verified Orca
terminal path - the slash interface is user-side input and the coordinator model
cannot type it - then TWO automatic no-nudge cycles with duty receipts,
completion/stall handling, and stop control are proven. An armed-but-unverified
heartbeat, an unverified watcher spawn, or a missing controller means the campaign
is NOT autonomous: say so. Full wakeup contract:
[references/coordinator-heartbeat.md](references/coordinator-heartbeat.md). Full START
contract: [references/handoff-and-start.md](references/handoff-and-start.md).

### 8. Topology

The EXECUTION session (after START) captures/validates the original NAMED target branch
and its full starting SHA; do not assume main/master and do not reinterpret a detached
HEAD later - a detached start requires the user to name the target. At START create ONE
campaign worktree `{prefix}-campaign` whose branch is cut from the NAMED target branch,
then create every task worktree as an Orca CHILD of the campaign worktree based on the
recorded campaign BRANCH - always branch bases, never a raw SHA or HEAD - so the whole
campaign nests under one root in the Orca worktree tree. Orca may auto-generate branch
names: record the actually returned branch and HEAD; on a HEAD mismatch, do not start.
Full contract:
[references/runtime-review-and-integration.md](references/runtime-review-and-integration.md).

### 9. Per-task loop

Mandatory stages in order: develop -> runtime test-loop -> independent review-loop -> squash
integration/conflict handling -> post-merge runtime smoke -> preserve evidence and cleanup
([templates/TODO.md](templates/TODO.md)). Test -> fix batch -> test; review FAIL -> executor
fix -> runtime retest -> fresh independent review. No fixed iteration limit: repeat while
evidence shows progress. New tested or reviewed changes invalidate prior verdicts; bind
every result to the exact commit/tree/build and scenario version. The coordinator
commissions the independent review itself, with an unbiased packet (acceptance criteria,
contracts, diff base/tip, runtime evidence, known findings) - author self-review is
optional preparation, never a gate. With the OCR engine the review is one `ocr review`
run per frozen candidate (commit mode, effort low, JSON output, budget-capped); the
coordinator derives PASS/FAIL from the findings - severity critical/high/medium all
block, low never blocks - and a partial/failed/skipped run is never a verdict. Detailed
contracts:
[references/runtime-review-and-integration.md](references/runtime-review-and-integration.md);
OCR protocol: [references/ocr-review.md](references/ocr-review.md).

### 10. Concurrency

At most THREE simultaneously active coding agents, fix and remediation agents included;
no hidden fanout. One writer per worktree; reviewer ownership prevents simultaneous
mutation. A task starts only after its prerequisites are independently reviewed,
squash-integrated into the campaign, and post-merge smoke tested. A task releases its
dependents the same way - never on the executor's done message. Cleanup is mandatory,
tracked, and gates resource reuse.

### 11. State and monitoring

Canonical campaign state lives in the campaign directory as `{prefix}_STATE.json`
(schema 2: lifecycle `planning`/`awaiting_fresh_session_start`/`executing`/`completed`
with planning and execution sessions and the start recorded independently),
`{prefix}_TODO.md`, `{prefix}_EVENTS.jsonl`, `{prefix}_evidence/`, and
`{prefix}_REPORT.md` ([templates/STATE.json](templates/STATE.json),
[templates/TODO.md](templates/TODO.md)). The coordinator is the sole writer of shared
state; agents report into task-owned evidence. Update state at every meaningful
transition and on a ten-minute cadence while active: poll EVERY active session.
Coordinator wakeups between user visits are sustained ONLY by one of the two
sanctioned mechanisms - the observer never wakes anyone:

- **Option A (recommended for unattended runs): bounded event watcher.** Spawn
  [templates/bounded_watcher.sh](templates/bounded_watcher.sh) as a background
  process with completion notification (`terminal(command="...", background=true,
  notify=true)`). The script polls every ~20s and EXITS on the first
  coordinator-actionable event - `NEW_COMMIT` (a watched worktree's
  `git rev-list --count` moved), `WORKER_EXIT` (a pinned agent terminal left the
  terminal list), `SILENCE_NUDGE` (a session JSONL quiet > 25m: it sends ONE
  bounded status nudge, then exits) - or when the slice budget expires (default
  900s) with `SLICE_TIMEOUT`. Hermes `notify=true` is notify-on-COMPLETION, so the
  exit - not its stdout - creates the coordinator turn with the exit summary. On
  wake, classify the event, act within the approved plan and attempt budget, then
  spawn a FRESH watcher with FRESHLY verified handles for the next slice.
  Auto-stop is the token-safety property: at `completed`, paused, or needs-user
  states the coordinator simply does NOT spawn another watcher - no daemon, no
  idle token drain, no manual cleanup. Guardrails: at most ONE nudge per slice;
  the watcher never kills, merges, switches models, or remediates beyond that
  nudge; one watcher instance per slice.
- **Option B: native session heartbeat.** `/heartbeat every 5m` with a bounded
  instruction in the execution session: sole-writer fresh poll per cycle,
  timestamped duty receipts, WATCH task membership updated at every
  dispatch/integration transition; installed and cleared only through the guarded
  terminal-controller path, with controller identity and duty receipts persisted
  in state; the controller clears or pauses the heartbeat at
  completed/paused/needs-user states so idle cycles never burn tokens.

Full contract (both options, verification standards, forbidden patterns):
[references/coordinator-heartbeat.md](references/coordinator-heartbeat.md).
Liveness semantics are strict: transport or process activity (stream, bytes, PID,
mtime, JSONL growth) is not progress, a successful assistant response is not task
progress, and neither is completion - keep last observed, last successful assistant,
last completed tool (errors separate), and last semantic progress distinct; only
explicit structured checkpoints are semantic progress; unknown is reported as unknown,
never healthy. The bundled observer scripts are optional, observer-only helpers, never
authoritative and never mutating. USE the packaged observer or bounded manual status
checks as shipped: do not keep editing or rebuilding watchers during execution - if
monitoring is uncertain, report unknown and apply the declared attempt budget
(section 12), and spin watcher improvements off as a separate maintenance task.
Execution stays visible: dispatch agents as interactive OMP TUIs in ordinary Orca
worktree tabs, not hidden background (`-p`) runs, by default; if the user explicitly
approves a headless run, verify the session is discoverable/linkable and disclose it
to the user - a `terminal focus` result of `navigated:false` is not proof the user can
see anything. Bind terminal handles and session identities, and never leave a
duplicate writer behind when moving an agent between UIs. Semantics and CLI contract:
[references/progress-watchdog.md](references/progress-watchdog.md). Schema, crash
windows, resume and remediation: [references/state-and-recovery.md](references/state-and-recovery.md).

### 12. Remediation and non-convergence

Ladder: diagnose -> targeted nudge, verified by new progress -> approved fallback switch
where appropriate -> fresh session with durable handoff when needed. Never blind repeated
nudges or model toggles; a live long-running command within its deadline is not a stall,
and the observer (if used) never kills or remediates - it only reports. Non-convergence is
an evidence-based pause, not an attempt counter: pause a task (and its descendants; safe
unrelated branches continue) on a repeated identical failure fingerprint with no
measurable progress after materially different attempts, oscillating fixes/reverts, model
cycling without diagnosis, growing out-of-scope diff, contradictory requirements,
unavailable capability, or risk to user data - presenting evidence, attempts, hypothesis,
and options. An operator pause is never self-resumed.

Every execution attempt runs under the approved bounded-attempt policy (defaults in
`execution_policy`; record per-attempt start in `tasks[].attempt`):

- The attempt budget (`attempt_budget_seconds`, default 2100 = 35 min) starts at ACTUAL
  attempt launch and never resets on SSE/IO/log metadata churn, an empty verdict shell,
  repeated reads, or a watchdog or coordinator restart. Tool success alone is not a
  useful artifact.
- At `checkpoint_due_seconds` (default 1200 = 20 min), inspect progress evidence and
  issue at most ONE scoped steer if needed - never queue redundant nudges.
- At budget expiry, settle the attempt: either complete the deliverable and verify it,
  or stop/fence the writer, preserve partial work and logs, shorten the brief, and
  restart scoped. A budgeted stop is NOT a permanent feature FAIL and never an automatic
  acceptance.
- Longer builds/tests may run only under a PREDECLARED bounded phase deadline recorded
  before launch, backed by real completion/checkpoint evidence - no retroactive or
  open-ended sliding budgets.
- Waiting on human input means pause with no automatic retry.
- After two UNPRODUCTIVE executions of the same slice, never blindly retry the same
  route a third time: use the approved fallback for THIS task/attempt, else pause with
  concise evidence and options. A useful review FAIL with fixable findings is a
  productive outcome, not an unproductive provider attempt; the NO FIXED LIMIT rule for
  substantive test/fix/review cycles stands while evidence shows progress.
- Two distinct numerical regimes do not conflict: the observer's thresholds
  (`no_step_seconds` etc.) only trigger DIAGNOSIS, while the approved attempt budget is
  a hard procedural cap enforced by the coordinator/runtime through scoped control -
  never by the observer scripts, which have no enforcement flags.

Rules: [references/state-and-recovery.md](references/state-and-recovery.md#remediation-and-non-convergence).

### 13. End of campaign

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
- Creating a DAG before mandatory repository discovery, actual cited web research, and an
  independent `CONVERGED` critique bound to the current INTENT/RESEARCH hashes; file
  existence or self-critique alone never opens the gate.
- Treating web snippets or model memory as research, inventing sources, or continuing after
  web-access failure without recording a blocker and pausing.
- Writing a custom parser/scheduler/UI component (NIH reimplementation) without first
  searching for and evaluating mature open-source libraries; reuse-first is the default and
  custom code needs evidence-backed justification in RESEARCH.
- Selecting a package from model memory, or adopting an archived/deprecated/yanked/
  superseded or license-incompatible library, without live registry + upstream repository
  verification.
- Parallel tasks independently mutating manifests/lockfiles or installing unapproved
  packages; dependency adoption is pinned in shared contracts and lockfile updates are
  serialized through one prerequisite/exclusive-owner task.
- Letting an architectural pattern silently override explicit user intent; revise the design
  or surface a real infeasibility/trade-off instead.
- Declaring convergence after fixing only a critic's named example: every revision gets a
  fresh full five-lens critique, including Security and UX, and changed hashes invalidate
  every earlier verdict.
- Treating plan approval as execution start: the planning session never creates execution
  worktrees or coding/execution agents (the phase-3 read-only planning critic is the sole
  delegated-session exception); START belongs to a distinct fresh session bound to the manifest.
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
- Substituting a fake wakeup for a sanctioned mechanism: `notify:true` on a
  persistent process is notify-on-COMPLETION (stdout is not a wakeup - only a
  BOUNDED watcher that exits on an event or slice timeout turns completion
  notification into a wakeup), one observer poll or a written config schedules
  nothing, and `notify:[watch_patterns]` is permanently
  disabled after 8 matches - none of these is a scheduler
  ([coordinator-heartbeat.md](references/coordinator-heartbeat.md)).
- Claiming autonomous monitoring from an armed heartbeat status line or fire count
  without two verified no-nudge cycles with duty receipts and stop-control proof,
  or from merely spawning a watcher without proving at least one full
  event exit -> completion notification -> coordinator-turn chain; overwriting a
  session heartbeat that belongs to another task instead of escalating;
  forgetting that a dead session-owner process - or a dead watcher-hosting
  terminal - means monitoring is down, with no
  reboot/process-death recovery promised.
- Leaving a wakeup mechanism armed at a completed, paused, or needs-user campaign -
  idle heartbeat cycles burn tokens, and a re-spawned watcher at a terminal state
  burns a slice for nothing: auto-stop means spawning nothing new; and resuming
  with stale instructions instead of re-validating state.
- Pretending to type: printing `/heartbeat ...` in a coordinator reply, or running
  heartbeat strings as shell commands, is not control - the slash is installed,
  paused, and cleared only by an identity-verified terminal controller
  (`orca-ide terminal list/send` to the exact owner terminal plus read-back of the
  native response; no SQL/state edits; ambiguous identity means no send); with no
  controller the campaign is not autonomous - request operator assist.
- Treating the 60-second floor as an exact cadence or `fire_count` as ground truth:
  busy sessions coalesce ticks, turns lag, and durable counters may diverge from
  session messages - proof is actual session messages and output receipts.
- Editing or rebuilding the observer scripts mid-campaign instead of using them as
  shipped; monitoring uncertainty is reported as unknown and governed by the declared
  attempt budget, and watcher work becomes a separate maintenance task.
- Letting an attempt run unbounded: transport churn, empty verdict shells, repeated
  reads, or watcher/coordinator restarts never reset the attempt budget clock.
- Treating a budgeted stop as a permanent feature FAIL, or extending a long job
  retroactively instead of predeclaring a bounded phase deadline.
- Blindly retrying the same route after two unproductive attempts on the same slice,
  or confusing substantive review FAIL/fix cycles (no fixed limit while progress is
  evidenced) with unproductive provider attempts.
- Dispatching agents as hidden background runs the user cannot see; `terminal focus`
  with `navigated:false` is not proof of visibility, and moving an agent between UIs
  without rebinding handles/session risks duplicate writers.
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
- Cutting a worktree from a raw SHA/HEAD instead of a branch base: the campaign root
  takes the NAMED target branch and tasks take the recorded campaign branch, or the
  worktree detaches from the campaign grouping in Orca and can sit on a stale tip.
- Squash-merged branches look "unmerged" to git: never force-delete on status text; prove
  the recorded receipt instead.
- Crash between squash and state checkpoint: compare campaign log/tree against receipts
  before any re-merge; ancestor checks do not work for squash.
- Keeping state in chat memory or a temp directory; assuming main/master; running two
  coordinators; treating a status file as a scheduler that survives reboot.
- Releasing dependents on an executor done message instead of post-merge smoke.
- Bare `orca` on the host is the wrong program - the host CLI is `orca-ide`.
- With OCR installed, commissioning an inquisitor/session code review anyway, or
  silently falling back to one when OCR fails - the recorded engine binds the campaign;
  failures are remediated or escalated, never swapped.
- Treating an OCR run as a verdict because rc=0: `partial`, `failed`, `failed(budget)`,
  `skipped`, or zero reviewed files are not verdicts; `comments: []` is clean only when
  files were actually reviewed. Dropping blocking findings because line positioning
  failed (`start_line=end_line=0`) - locate them via `existing_code` instead.
- Letting `low`/style findings block, or letting `medium` findings pass: the blocking
  set is critical/high/medium. Using `ocr scan` for campaign review (its whole-file
  token model is far heavier) or delegation mode (review must run on OCR's own model).
- Storing OCR API keys in config or shell arguments instead of `api_key_cmd` against
  the secret store, or verifying the key helper under a sandboxed `$HOME` that cannot
  see the real token file.

## Verification

- Planning gate: INTENT records actual bounded read-only repository discovery; RESEARCH
  contains actually retrieved/cited web evidence plus architecture, Security, and UX
  analysis; `research.oss_library_evaluation_completed` is true in PLANNING_STATE and STATE
  with the live-verified OSS build-vs-reuse coverage (whole and partial) recorded in
  RESEARCH; an independent critic's final `CONVERGED` verdict binds the current exact
  INTENT/RESEARCH hashes and all findings have dispositions. DAG/task files do not predate
  this gate, and each task preserves design traceability. The manifest freezes INTENT,
  RESEARCH, CRITIQUE, PLAN, tasks/contracts, and HANDOFF.
- Campaign health: state revision advances with matching events; every active session has
  recent evidence; no task sits at a later stage than its bound evidence supports;
  dependents released only after prerequisite post-merge smoke; cleanup checkboxes reflect
  actual verified actions, not promises.
- Wakeup boundary: the execution session runs a VERIFIED wakeup mechanism whenever
  autonomous monitoring is claimed. Option A: the bounded event watcher proven by at
  least one full event exit AND one `SLICE_TIMEOUT` exit, each -> coordinator-turn
  cycle acting on the exit summary, fresh handle verification at every respawn, and
  NO respawn at terminal campaign states - a timeout-only run never exercises event
  detection and proves nothing about events. Option B: two automatic no-nudge heartbeat cycles with
  observer-timestamped duty receipts, completion/stall handling, stop control,
  installed via the guarded terminal-controller path with controller identity and
  duty receipts persisted in state; the controller clears/pauses it at terminal
  campaign states, reading the actual response back from the terminal.
- Start boundary: state lifecycle, sessions, and start records are coherent - start
  exists only in a distinct execution session whose recorded manifest hash matches the
  frozen files; the planning session created no execution worktrees or coding agents;
  resumes of a started campaign carry the original approval without re-gating.
- Progress claims distinguish last observed, last successful assistant, last completed
  tool (errors separate), and last semantic progress; unknown is never reported healthy.
- Review engine: the OCR gate ran at planning start; `review_engine` is recorded in
  HANDOFF/STATE; when `ocr`, every per-task and final review has an OCR output JSON with
  a valid run status, coverage of the acceptance surface, a coordinator-derived verdict
  bound to the exact SHA, and no inquisitor code-review session was commissioned;
  blocking severities are critical/high/medium. When `session`, the standard independent
  reviewer contract applies unchanged.
- Before relying on a modified copy of this skill, run the static checks and tabletop
  walkthroughs in [references/validation-tabletop.md](references/validation-tabletop.md).
- Dispatch mechanics and command shapes: [references/hermes-orca-omp.md](references/hermes-orca-omp.md);
  state and recovery: [references/state-and-recovery.md](references/state-and-recovery.md).
