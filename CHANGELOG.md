# Changelog

## 1.3.0 — 2026-10-04

Focus: campaign worktree topology. Worktrees are created from branches end to end so a
campaign occupies one nested subtree in the Orca worktree tree.

### Changed

- Worktree topology is now explicitly branch-based. The campaign integration worktree
  is cut from the NAMED target branch at its pinned starting SHA
  (`--base-branch <named-target-branch> --no-parent`), and every task worktree is
  created as an Orca CHILD of the campaign worktree
  (`--parent-worktree name:<prefix>-campaign`) based on the campaign BRANCH Orca
  returned (`--base-branch <campaign-branch>`), with the returned HEAD compared to the
  recorded current campaign tip before each create. Raw SHAs and `HEAD` are never
  valid `--base-branch` values for campaign/task worktrees: they detach the checkout
  from the branch-based campaign grouping in the Orca tree and can base tasks on a
  stale tip. Command shapes verified live against `orca-ide`: root created from the
  named branch, child created with parent lineage + campaign-branch base
  (`parentWorktreeId` returned), teardown clean.
- Option A verification bar (1.2.0 follow-up): proving the wakeup chain now requires
  at least one full EVENT exit AND one `SLICE_TIMEOUT` exit, each -> completion
  notification -> coordinator turn acting on the exit summary; a timeout-only run
  exercises no event detection and proves nothing about events. SKILL.md sections 5
  and Verification now match the standard `references/coordinator-heartbeat.md`
  already carried.
- `templates/bounded_watcher.sh`: the emitted event line truncates `task` to 200
  chars (`detail` was already bounded at 400), keeping the one-line stdout receipt
  bounded regardless of watched-item names.

## 1.2.0 — 2026-10-03

Focus: unattended coordinator wakeups. Adds the bounded event-driven watcher as a
first-class wakeup mechanism (Option A) alongside the native session heartbeat
(Option B), closing the residual gap left by 1.1.1: the heartbeat is reliable but
must be installed and cleared by a terminal controller, and one forgotten at a
terminal state keeps burning tokens indefinitely.

### Added

- `templates/bounded_watcher.sh`: the bounded event watcher template (Option A).
  Spawned by the coordinator with `terminal(command="...", background=true,
  notify=true)`, it polls every ~20s and EXITS on the first coordinator-actionable
  event — `NEW_COMMIT` (a worktree's `git rev-list --count` moved off the
  spawn-time baseline), `WORKER_EXIT` (a pinned agent terminal handle left
  `orca-ide terminal list --json`), `SILENCE_NUDGE` (a session JSONL quiet >25m:
  exactly one bounded status nudge via `orca-ide terminal send`, then exit) — or
  after the slice budget (default 900s) with `SLICE_TIMEOUT`. Because Hermes
  `notify=true` is notify-on-COMPLETION, each exit creates the coordinator turn
  with a one-line JSON event summary and a distinct exit code (0 event/timeout,
  3 WORKER_EXIT, 2 ERROR). Auto-stop is procedural: at completed/paused/needs-user
  states the coordinator spawns no next slice — no daemon, no token drain, no
  `/heartbeat clear` needed. Guardrails: at most ONE nudge per slice, no
  remediation beyond it, single instance per slice, fresh handle verification at
  every respawn. Event paths and exit codes exercised end-to-end against a real
  `orca-ide terminal list`, real git worktrees, and signal delivery. Non-claim,
  mirroring 1.1.1's precedent: the middle link of the chain - Hermes completion
  notification turning a watcher exit into a live coordinator turn - was NOT
  live-tested in this release; that final gate remains an execution-time
  verification per the standard above.
- `references/coordinator-heartbeat.md`: full Option A contract — why
  notify-on-COMPLETION plus a bounded exit is a wakeup, the event table, the
  lifecycle (pin fresh identities -> baseline -> classify/act on wake -> re-arm or
  auto-stop -> record), the verification standard (one proven event exit ->
  completion notification -> coordinator-turn chain plus one `SLICE_TIMEOUT`
  check-in, with the dead-watcher-terminal limit disclosed), and guardrails. The
  forbidden-pattern entry is clarified: infinite `notify:true` loops are forbidden
  because completion notification fires only on exit; a bounded watcher that exits
  on an event or slice timeout is fully compatible and recommended.

### Changed

- `SKILL.md` (version 1.2.0): section 9 documents both sanctioned wakeup options
  (Option A recommended for unattended runs); START/adoption requires a verified
  wakeup mechanism — either option; pitfalls and the verification checklist now
  cover watcher-specific failure modes (unverified spawns, dead watcher-hosting
  terminals, pointless respawns at terminal states).
- `references/progress-watchdog.md`: observer-rules and run-workflow now name both
  sanctioned wakeup mechanisms; the observer scripts themselves stay unable to
  wake or nudge anything.
- `README.md`: version 1.2.0; the wakeup bullet documents both options; repository
  contents list the watcher template.
- `references/validation-tabletop.md`: new scenario 40 (silence at spawn fires the
  nudge and wakes the coordinator; auto-stop at terminal states).

## 1.1.1 — 2026-09-22

Focus: coordinator wakeups. Response to the 2026-09-22 watcher incident
(`plans/watcher-incident-2026-09-22/REPORT.md` in the source repo): two campaigns ran
overnight without a verified observation → wakeup → coordinator-action chain.

### Added

- `references/coordinator-heartbeat.md`: the native coordinator wakeup contract.
  Standard is the Hermes session heartbeat — `/heartbeat every 5m <bounded
  instruction>` in the owning coordinator TUI session (subcommands `status`, `pause`,
  `resume`, `clear`; alias `hb`), verified against installed Hermes source. Covers the
  heartbeat instruction content (pinned campaign paths, fresh observer poll, bounded
  diagnosis, authorized continuation, timestamped duty receipts, one cycle per firing),
  the two sampling modes (preferred sole-writer fresh poll per heartbeat; or an
  explicitly owned persistent `watch` whose sample the heartbeat reads — never two
  writers), establishment/verification before any autonomy claim (two automatic
  no-nudge cycles with receipts, completion/stall handling, stop control), stop
  conditions, and the missing-capability fallback.
- `CHANGELOG.md` (this file).

### Changed

- `SKILL.md` (version 1.1.1): START — and adoption of a running campaign — must
  establish AND verify the native heartbeat before claiming autonomous monitoring;
  monitoring section names the heartbeat as the only wakeup mechanism; new pitfalls
  (fake wakeup mechanisms, armed-but-unverified heartbeats, foreign-heartbeat
  overwrite, idle token burn at terminal states); new verification bullet.
- `references/progress-watchdog.md`: observer-rules and run-workflow sections now
  point to the heartbeat contract; explicit sole-writer note for poll-per-heartbeat vs
  a persistent `watch` process.
- `README.md`: version 1.1.1; heartbeat contract summarized; repository contents
  updated.
- Docs amendment (same 1.1.1, post-review F-1): `/heartbeat` is user-side slash
  input - the coordinator model cannot type it. `references/coordinator-heartbeat.md`
  adds the guarded terminal-controller path for setting AND clearing
  (identity-verified `orca-ide terminal list` + `terminal send` + read-back of the
  native response; no blind retries; no SQL/state edits; controller/owner identity
  and duty receipts persisted in campaign state; no controller means
  not-autonomous); SKILL.md mirrors it. Cadence honesty: the 60s floor is not an
  exact schedule and `fire_count` is not ground truth - actual session messages and
  output receipts are.

### Explicitly rejected as wakeup mechanisms (documented, not implemented)

- `notify:true` on a persistent background process — notify-on-COMPLETION semantics;
  persistent stdout is not a wakeup.
- Writing the observer config or one successful `poll` — schedules nothing.
- Repeated `notify:[watch_patterns]` — permanently disabled by Hermes after 8
  delivered matches; not a durable scheduler.
- `/tmp` duty scripts and cron targeting unverified transports.

Note: install/clear procedure is the identity-verified terminal-controller path
documented above (the transport was runtime-tested: `orca-ide terminal send` delivers
slash input with native response read-back - acceptance alone is not proof); full
live end-to-end proof of the heartbeat protocol remains the separate final gate -
this release does not claim it.

## 1.1.0

- Planning/execution boundary: one approval gate for WHAT, separate explicit START in
  a distinct fresh session bound to a frozen HANDOFF + SHA-256 manifest; schema-2
  campaign state with independent planning/execution session records.
- Optional observer utility (`scripts/omp_events.py`, `scripts/campaign_watch.py`,
  stdlib-only, observer-only) with strict progress semantics: activity ≠ progress ≠
  completion; structured checkpoints as the only progress signal.
- Bounded execution attempts as coordinator procedure (default 35-minute budget,
  checkpoint inspection at 20 minutes, max two unproductive attempts per slice).

## 1.0.0

- Initial release: coordinator contract for multi-task campaigns in Orca worktrees —
  intake, plan, model questionnaire, one approval gate, topology, per-task loop with
  runtime testing and independent review, concurrency cap of three, durable state,
  evidence-based non-convergence pauses, endgame and cleanup.
