# Progress Semantics and the Optional Watchdog

Liveness wording is strict here because weak wording has caused false health calls:
transport or process activity, model responses, and task completion are three different
things. This reference defines what counts as each, and the actual contract of the
optional observer scripts. The scripts never run on their own and are never required by
the procedure - the coordinator can apply the same semantics manually.

## Activity is not progress is not completion

An open SSE stream, flowing bytes, a live PID, a growing mtime, or JSONL file growth
proves ONLY transport/process activity. A successful assistant response proves the model
answered - not that the task progressed, and never that it completed. Only an explicit
structured checkpoint proves task progress (below). Mixing these levels is the primary
false-health bug this skill guards against.

## OMP session event semantics (session format version 3)

- Successful assistant event: an assistant record whose `stopReason` is `stop` or
  `toolUse` AND which carries no `errorId`.
- `stopReason` values `error` and `aborted` are NEVER success - even when the record
  has `completedAt` or usage data.
- `model_usage`, `custom` service events, title/model-change/compaction events, and
  aborted/discarded branches are NOT progress.
- Tool completion: a tool result closes a tool call; `isError` is tracked separately -
  a completed failing tool is an error observation, never a success.
- Only the CURRENT live parent branch counts. `branch_summary` entries such as
  discarded-entry branches record abandoned work; they never create progress.
- Provider-global errors (for example a gateway 500) cannot be attributed to a specific
  session without an explicit correlation; never assign them to an arbitrary agent.

## Distinct timestamps

Never collapse these into one "last activity" value:

- `last_observed_at` - any transport/file/process evidence, weakest signal.
- `last_successful_assistant_at` - per the success rule above.
- `last_completed_tool_at` - with the `isError` distinction retained.
- `last_semantic_progress_at` - ONLY explicit structured checkpoints.

Semantic progress requires a structured checkpoint bound to task, session, and candidate
(a count/ID, not a vibe). An artifact hash change (commit, file change) is a CANDIDATE
signal requiring validation, never validation itself. There is deliberately no
code-growth-only detector: diff growth is not progress.

## Health and activity classification

Activity (what the session is doing): `generating` | `tool_running` | `waiting_input` |
`idle` | `exited` | `unknown`. Health (how the campaign is going): `ok` | `degraded` |
`suspect_stall` | `confirmed_retry_loop` | `unknown`. They are orthogonal - a session
can be `generating` and `degraded` at once.

- `ok`: successful steps within expectations.
- `degraded`: repeated errors WHILE successful steps continue - keep going, watch.
- `suspect_stall`: no successful step within the configurable diagnostic budget
  (default 600s). This triggers DIAGNOSIS - inspect for a pending interactive `ask`, an
  in-flight tool against its per-tool deadline, or a quiet long command - never
  automatic failure. A numerical threshold is a diagnosis trigger, not a permanent FAIL.
- `confirmed_retry_loop`: repeated session-scoped IDENTICAL transport failures with no
  useful steps between them. Requires session-scoped evidence; provider-global errors
  never qualify without correlation.
- `unknown`: missing schema, inaccessible input, stale observation, or any doubt -
  unknown is never reported as healthy. A capped read batch with remaining backlog
  cannot report healthy current activity.

A pending `ask` freezes the agent awaiting input (`waiting_input`) - answer it, do not
kill it. A live long-running command within its deadline is not a stall.

## Observer rules (any implementation)

- The observer NEVER kills, nudges, restarts sessions, switches models, merges, or
  executes shell commands; no LLM calls, no network. Remediation stays with the
  coordinator: preserve dirty work, fence the old writer, then restart; fallback model
  only if approved; no infrastructure changes.
- Writes ONLY its own sidecar directory (snapshot, cursor/state, transition journal) -
  never the canonical campaign STATE/TODO/EVENTS. Sidecars and output carry no raw
  messages, tool arguments, content, or error strings; errors surface as aggregated
  structural fingerprints (category or irreversible hash). Bounded incremental input
  and bounded output. Malformed, rotated, truncated, partial, or schema-unknown input
  fails safe to `unknown`. Registering an attempt does not imply its success.
- Per-task age persists across attempt changes and watcher restarts (sidecar state);
  a watcher restart never resets ages to zero.
- The observer is not a scheduler and not a coordinator wakeup: it does not cause
  anything to run. External notification (if wanted) is a separate explicitly
  configured and verified mechanism.
- Reviewer-relevant boundaries: the reviewer needs no source mutation to review; small
  completed calls and review chunks are preferred over giant single calls; a partial
  review is never PASS; the final verdict stays compact and links evidence. A short
  smoke route does not prove long-stream stability - budget long scenarios explicitly.
  A hard output token cap is only set through options actually verified to exist.

## Observer CLI (actual contract, aligned with `scripts/campaign_watch.py`)

Two Python 3 standard-library-only scripts ship with this skill (release 1.1.0):
`scripts/omp_events.py`, a metadata-only incremental OMP session-JSONL adapter, and
`scripts/campaign_watch.py`, the deterministic watcher CLI. The command surface below is
the implemented one; do not script against flags or fields not listed here.

```
campaign_watch.py poll     --config PATH             one bounded sample, writes sidecars
campaign_watch.py watch    --config PATH             poll loop: initial poll line, then
                                                     change lines (immediate) + heartbeat
campaign_watch.py status   --config PATH [--task T]  cached snapshot, stale check
campaign_watch.py diagnose --config PATH [--task T]  cached per-task detail
```

- Every output is ONE JSON line on stdout. `status`/heartbeat lines are ALWAYS
  <=1024 UTF-8 bytes including the newline; `diagnose`/`poll` lines are <=4096 bytes
  (as implemented - a smaller poll budget was a goal, not a promise). Change lines are
  terse: `{"v":1,"kind":"change","at":...,"task":...,"from":"h/a","to":"h/a","reason":...}`.
  Over-capacity task lists are truncated to a stable task-sorted prefix with an
  `omitted` count; `counts` always covers ALL tasks; JSON is never broken.
- Errors are safe JSON: `{"v":1,"kind":"error","error":CODE}` with exit code 2 -
  codes `config_unreadable`, `config_invalid`, `state_corrupt`, `no_snapshot`,
  `config_changed`, `observer_locked`, `task_unknown`, `internal`. No tracebacks, host
  paths, or secret strings ever appear. `--help` is normal argparse.
- `status`/`diagnose` are read-only (no lock, no writes); a snapshot older than
  `stale_seconds` is reported with every health forced to `unknown`
  (`reason: stale_snapshot`). Editing the config after a poll yields `config_changed`
  until the next poll.

### Config file (`templates/WATCH.json`, schema_version 1)

The shipped template is valid JSON and copies the documented defaults, but it is NOT
runnable as-is: replace every `/path/to/...` path and the `registered_at` placeholder
before the first run. The CLI validates strictly and rejects a placeholder config with
`config_invalid`; unknown extra keys are dropped at load, so the replacement legend
lives here, not in the JSON. All interval keys and `repeat_error_count` are REQUIRED -
the code applies no defaults; the values below are the template's defaults:

- `poll_seconds` 30, `heartbeat_seconds` 300, `stale_seconds` 120,
  `no_step_seconds` 600, `retry_window_seconds` 600: positive floats <=86400
  (fractional allowed).
- `repeat_error_count` 3: integer 1..100.
- `sidecar_dir`: absolute path, <=512 chars. The campaign root is
  `dirname(sidecar_dir)`; checkpoint/artifact allowlists must resolve inside it.
- `tasks`: 1..1024 entries; excess is REJECTED (`config_invalid`), never silently
  ignored. Per task:
  - `task`, `attempt`: ids matching `^[A-Za-z0-9][A-Za-z0-9_.\-]{0,127}$`, unique per
    config. `phase` optional (same charset, <=64).
  - `session_log`: absolute path to the OMP session JSONL, <=512 chars.
  - `session_id`: null = capture and persist the first valid session header; a later
    change is rejected as `session_changed` (health `unknown`) unless the attempt label
    changed.
  - `registered_at`: REQUIRED ISO-8601 UTC, not in the future. Its first-sight value
    persists: later config edits and attempt-label changes cannot mint a new no-step
    baseline.
  - `candidate`: null or an opaque string <=256 chars, matched against checkpoints.
  - `checkpoint_files`/`artifact_files`: optional explicit allowlists, <=64 absolute
    entries each, no symlinks, must resolve under the campaign root; violations are
    `config_invalid`.
  - `tool_deadline_seconds`: REQUIRED, positive float <=604800.
  - `process`: null or `{"pid":int,"start_ticks":int,"boot_id":str}` - a Linux /proc
    identity (starttime field 22 + boot_id). Unsupported platform or inaccessible proc
    => `unknown`, NEVER `exited`. boot_id mismatch (pre-reboot) or start_ticks
    mismatch (PID reuse) => `exited`. An omitted process does not override JSONL
    semantics.

### No-step age vs semantic progress vs artifact signals

Keep these separate when reading output:

- `no_step_age` is the age of the last valid successful assistant event (genuine event
  timestamp, else `registered_at`). It drives `suspect_stall`/`confirmed_retry_loop`.
  Failed tool results never refresh it; `live:false` successes anchor age by their
  genuine event ts but manufacture no NOW progress; retracted-branch successes are
  dropped by the adapter.
- `last_progress_at` moves ONLY on a confirmed structured checkpoint (below). Nothing
  else sets it.
- Artifact diffs (sha256+size, <=1MiB/file) are candidate signals only, surfaced as
  `artifacts_changed`; unreadable or oversized files become `artifact_unverifiable`
  uncertainty, not success. There is no code-growth-only progress detector.

### Structured checkpoints (producer attestation, not truth)

`{schema_version:1,task,attempt,session_id,candidate,checkpoint_id,completed_at,kind,
verified:true}` with kind `runtime_scenario|review_checkpoint|artifact_checkpoint`.
Identity must match task/attempt/bound-session/candidate; same id or older ts is a
replay and ignored; a confirmed checkpoint is monotonic across restarts and attempts.
`verified:true` is the producer's attestation only - the watcher does not verify the
underlying claim. Checkpoint files are read-only inputs; the producer (executor or
reviewer per procedure) writes them, the watcher never does.

### Sidecar files (the ONLY writes)

The scripts write only inside `sidecar_dir` - never STATE/TODO/EVENTS, session logs, or
sources: `state.json` (baselines, adapter cursors, confirmed checkpoints, removed-task
ring <=128, transition journal <=256 metadata-only; atomic replace; corruption =>
`state_corrupt` with the file untouched, baselines kept), `snapshot.json` (`written_at`,
`config_digest`, task views; atomic), `observer.lock` (fcntl flock, non-blocking,
single writer for poll/watch, crash-safe; status/diagnose take no lock). Removed tasks
are pruned from the snapshot but their baseline (registered_at/session/checkpoint)
resumes on re-add: pruning and re-adding or relabeling an attempt cannot reset the
no-progress budget.

### Run workflow

1. Copy `templates/WATCH.json`, replace paths, `registered_at`, and task/session
   identity for the tasks to watch.
2. Run one `poll --config PATH`; expect one JSON line per run, health per task.
3. Check `status --config PATH` (compact) and `diagnose --config PATH --task T`
   (detail) as needed.
4. For continuous watching, run `watch --config PATH` as an explicitly owned,
   supervised background process: decide who owns it and how it is supervised BEFORE
   starting it. A background watcher does not wake a sleeping coordinator TUI and
   sends no notifications by itself; it only prints lines. It is a reporter, not a
   scheduler.

Nothing auto-starts: the scripts run only when explicitly invoked.

### Known constraints and open concerns (accurate as of CLI commit e080ba1)

- `observer.lock` uses fcntl flock: POSIX only.
- The process probe is Linux-only (/proc) and works only in the same PID namespace;
  elsewhere process and activity stay `unknown`.
- OPEN CONCERN: the current source labels activity `generating` when a validated live
  process exists and no ask/tool is pending - a live PID alone cannot prove the model
  is generating. Coordinator review must fix or relabel this before release; do not
  treat `generating` as proof of model activity.
- OPEN CONCERN: checkpoint `completed_at` currently tolerates up to 300s of future
  skew; the desired policy is no future actual progress at all. Flagged to the
  coordinator for correction.
- Retry-loop confirmation needs adapter error fingerprints; runtimes that never emit
  them can at most reach `suspect_stall`.
- Invalid, corrupt, stale, rotated, or truncated input fails safe to `unknown`;
  bounded parent history (removed ring <=128, journal <=256) is explicit.
- Validation status: exercised against adapter fixtures (adapter 919e864,
  simple-envelope). A real-session integration check against the corrected adapter is
  still required before relying on classification against live OMP sessions; no
  real-session PASS is claimed here.

### Relationship to the attempt budget (procedural, not CLI)

The watchdog's numerical thresholds (`no_step_seconds`, `retry_window_seconds`,
`stale_seconds`) are DIAGNOSIS triggers only. The campaign's attempt budget
(`attempt_budget_seconds`, default 2100; see SKILL.md section 10 and
[state-and-recovery.md](state-and-recovery.md)) is a separate hard procedural cap
enforced by the coordinator/runtime through scoped control - never by the observer,
which never kills, nudges, or remediates. The observer has no CLI flags or config
options for budget enforcement; that enforcement is procedure, not code.
