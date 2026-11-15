# Changelog

## 1.7.0 — 2026-11-15

Focus: OCR code-review engine. When alibaba/open-code-review (`ocr` CLI) is installed
and working, ALL campaign code review runs exclusively through OCR instead of
inquisitor-style reviewer sessions; the reviewer model from the questionnaire becomes
OCR's model. Planning critique and runtime testing are unchanged.

### Added

- Section-0 code-review engine gate at planning start: detect OCR (PATH plus npm global
  bin dirs under sandboxed PATHs), offer installation once if absent
  (`npm install -g @alibaba-group/open-code-review`), verify `ocr llm test`, and record
  `review_engine` (`ocr` | `session`) in HANDOFF and STATE.
- `references/ocr-review.md`: full OCR protocol — commit-mode per-task review
  (`--effort low`, JSON output, `--background-file` packet, `--preview` coverage check,
  `--max-tokens-budget` guard), range-mode final review (`--effort medium`),
  coordinator-derived verdicts (critical/high/medium block; low never blocks;
  partial/failed/budget/skipped runs are never verdicts; positioning-failed findings
  stay valid), `--resume` crash recovery, secrets via `api_key_cmd` (no keys in config
  or shell args), and token-economy rationale. `ocr scan` and delegation mode are
  explicitly excluded; OCR is an MCP client, not a server — the CLI is the integration
  surface.
- STATE template: `models.review_engine`, `models.ocr` (binary/version/provider), and
  per-task `review.engine`/`ocr_session_id`/`ocr_output` evidence fields (schema_version
  unchanged). HANDOFF/PLAN/TODO templates record the engine decision and gate.
- Tabletop scenarios 51-56 (engine selection, install offer, not-a-verdict states,
  blocking severities, positioning failures, no-fallback rule) and static OCR checks;
  new `tests/test_ocr_review_contract.py`.

### Changed

- Exclusive-engine rule: with OCR recorded, no inquisitor code-review sessions are
  commissioned and OCR failures are remediated or escalated — never silently swapped
  for another engine. Reviewer dispatch, START capability checks, crash-window review
  recovery, and the review contract all route through the engine gate.
- SKILL.md version bumped to 1.7.0; README requirements/contents updated.

## 1.6.0 — 2026-11-13

Focus: reuse-first planning. Planning now mandates a live-verified open-source library
evaluation of whole and partial functionality before any custom implementation.

### Added

- Mandatory open-source library evaluation in phase 2: search existing repository
  dependencies and the standard library first, then whole-functionality and
  partial/sub-problem libraries. Every candidate is verified through live primary sources
  - package registry metadata AND the upstream source repository - for OSI/license
  compatibility, popularity signals, active/not-deprecated/unarchived status, and
  CVE/footprint fit. `RESEARCH.md` gains the evaluation table; the planning gate records
  `research.oss_library_evaluation_completed`.
- Reuse-first anti-NIH default with the anti-micro-package counterweight (no external
  packages for trivial ~10-20 line standard-library operations), plus a whole-coverage
  disclosure: when one library covers ~80-100% of the capability and collapses the build
  into thin integration, that option is surfaced to the user instead of padding custom
  tasks. Custom implementation requires an evidence-backed justification in RESEARCH.
- Approved dependencies (package, version constraint, license, lockfile owner) are pinned
  in PLAN/TASK shared contracts; manifest + lockfile updates are serialized through a
  dedicated prerequisite or exclusive-owner task so parallel worktrees never collide.
  Newly adopted third-party dependencies are presented inside the single WHAT approval
  gate (earlier pauses only for license conflicts, new host/system binary prerequisites,
  or whole-campaign collapse).
- Critic lenses now audit OSS build-vs-reuse coverage, live non-deprecation/popularity/
  license evidence, NIH justification, third-party supply-chain/CVE posture, and
  manifest/lockfile ownership readiness. Tabletop scenarios 48-50 cover NIH
  reimplementation, model-memory/deprecated package selection, and
  whole-coverage/`stdlib-only` dispositions.

### Changed

- Phase 1 repository discovery now records dependency/license/footprint policies
  (including `stdlib-only` mandates) and already-installed reusable libraries, and seeds
  candidate capability slices for the phase 2 evaluation.
- SKILL.md version bumped to 1.6.0; planning STATE templates initialize the new gate
  flag (schema_version unchanged).

## 1.5.0 — 2026-10-31

Focus: skill identity. The skill directory and invocation name are now `acd`; the
product, procedure, and repository are unchanged.

### Changed

- Skill directory is now `skills/acd`; frontmatter `name` is `acd` and `version` is
  `1.5.0`. The full product title "Autonomous Campaign Development" and the repository
  (`megastruktur/autonomous-campaign-development`) are unchanged.
- README install/update/uninstall commands and the Hermes route use the `acd` skill
  name and the `/acd` invocation; installed-path examples use `~/.hermes/skills/acd`.
- Static tests pin the `acd` directory/frontmatter identity, version `1.5.0`, and the
  absence of the old skill path or invocation in active sources; campaign plans and
  historical changelog entries are excluded from that check.

## 1.4.0 — 2026-10-31

Focus: evidence-based planning. Planning now has four mandatory phases with an auditable
convergence gate before any DAG or task decomposition.

### Added

- Mandatory bounded, read-only repository discovery during intent capture: inspect actual
  instructions, dependencies, relevant interfaces/patterns, and runtime/test entry points.
- Mandatory web research for every campaign, scaled to novelty/risk, with retrieved sources,
  citations, architecture option comparison, and decision traceability. Failed web access
  pauses planning rather than silently substituting model knowledge.
- Independent critique -> revision -> fresh full critique loop across intent fidelity,
  architecture/research evidence, Security, UX, and execution readiness. `CONVERGED` must
  bind exact current INTENT/RESEARCH hashes; all findings require resolution/disposition.
  Architecture never silently overrides explicit user intent.
- New planning reference and INTENT, RESEARCH, CRITIQUE, and PLANNING_STATE templates;
  campaign STATE records phase/convergence and the manifest freezes all design evidence.
- Validation tabletop scenarios for premature DAG creation, unavailable research, intent
  conflicts, Security/UX findings, stale critique hashes, and proportionate research depth.

### Changed

- DAG and task decomposition now happen only after design convergence; tasks trace back to
  intent, architecture decisions, Security/UX requirements, and shared contracts.
- Existing one-WHAT-approval and distinct fresh-session START boundaries are unchanged.

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
