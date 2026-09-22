# Changelog

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
