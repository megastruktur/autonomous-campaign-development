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
- Tool completion: a tool result closes a tool call; only `isError` strictly `false`
  counts as success - a completed failing tool is an error observation, and a
  null/missing `isError` is unknown; neither is ever a success.
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
- Writes ONLY its own sidecar directory (snapshot, cursor/state, transition journal,
  ownership marker) - never the canonical campaign STATE/TODO/EVENTS, and never a
  sidecar aliased with any input. Sidecars and output carry no raw
  messages, tool arguments, content, or error strings; errors surface as aggregated
  structural fingerprints (category or irreversible hash). Bounded incremental input
  and bounded output. Malformed, rotated, truncated, partial, or schema-unknown input
  fails safe to `unknown`. Registering an attempt does not imply its success.
- Per-task age persists across attempt changes and watcher restarts (sidecar state);
  a watcher restart never resets ages to zero.
- The observer is not a scheduler and not a coordinator wakeup: it does not cause
  anything to run. The sanctioned wakeup mechanisms are the coordinator's bounded
  event watcher (Option A) and native session heartbeat (Option B), established and
  verified per [coordinator-heartbeat.md](coordinator-heartbeat.md) - completion
  notifications from an unbounded process, one-shot polls, and watch patterns are
  not schedulers.
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
  codes `config_unreadable`, `config_invalid`, `state_corrupt`, `state_capacity`,
  `no_snapshot`, `config_changed`, `observer_locked`, `sidecar_unmanaged`,
  `sidecar_refused`, `task_unknown`, `internal`. No tracebacks, host
  paths, or secret strings ever appear. `--help` is normal argparse.
- `status`/`diagnose` are read-only (no lock, no writes); a snapshot older than
  `stale_seconds` is reported with every health forced to `unknown`
  (`reason: stale_snapshot`). Editing the config after a poll yields `config_changed`
  until the next poll. Health-`unknown` reasons include `stale_snapshot`,
  `session_changed`, `adapter_bootstrap`, `adapter_fault`, and `adapter_uncertain`
  (non-empty adapter uncertainty holds health at `unknown` until actual adapter
  recovery - one clean poll cannot flip it back on its own).

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
- `tasks`: 1..64 entries; excess is REJECTED (`config_invalid`), never silently
  ignored (serialized state is also byte-capped - sidecar files below). Per task:
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
- Path aliasing is rejected up front with `config_invalid`, before any sidecar
  creation or write: the config file, every `session_log`, and every
  checkpoint/artifact allowlist entry must not equal a managed output (`state.json`,
  `snapshot.json`, `observer.lock`, `.watch_managed`), the sidecar dir itself, or a
  path inside it (realpath-resolved; symlink bypass impossible).

### No-step age vs semantic progress vs artifact signals

Keep these separate when reading output:

- `no_step_age` is the age of the last useful step: the maximum of the last valid
  successful assistant event and the last valid successful current-branch tool
  completion (genuine event timestamps, else `registered_at`). It drives
  `suspect_stall`/`confirmed_retry_loop`. Failed or null/unknown-outcome tool results
  never refresh it - `last_tool_outcome` is the bounded enum
  `successful|failed|unknown` (null when there is no tool evidence), and only a
  successful completion sets `last_tool_completed_at`; `live:false` successes anchor
  age by their genuine event ts but manufacture no NOW progress; retracted-branch
  successes are dropped by the adapter. The step clock is recomputed from each poll's
  active-branch snapshot, never carried over from the previous one.
- `last_progress_at` moves ONLY on a confirmed structured checkpoint (below). Nothing
  else sets it.
- Artifact diffs (sha256+size, <=1MiB/file) are candidate signals only, surfaced as
  `artifacts_changed`; unreadable or oversized files become `artifact_unverifiable`
  uncertainty, not success. There is no code-growth-only progress detector.

### Structured checkpoints (producer attestation, not truth)

`{schema_version:1,task,attempt,session_id,candidate,checkpoint_id,completed_at,kind,
verified:true}` with kind `runtime_scenario|review_checkpoint|artifact_checkpoint`.
Confirmation REQUIRES a positively bound session id AND a configured non-null
candidate - until both exist the verdict is the diagnostic `unbound_identity`
(checkpoint issue, never a silent skip); file existence alone never confirms.
Identity must match exactly (task/attempt/session_id/candidate); `completed_at` must
be aware UTC (naive rejected), strictly `<= now` (no future grace), and not older
than the `registered_at` baseline - violations are reason `timestamp`. Same id or
older ts is a replay and ignored; a confirmed checkpoint is monotonic across
restarts and attempts. The persisted checkpoint is re-validated against the current
identity on every poll: a positive mismatch retracts it
(`persisted:foreign_identity` in `checkpoint_issues`, no longer anchoring
`last_progress_at`), and a record from a past attempt may persist only as
`checkpoint_historical: true` - never a confirmation of the current candidate.
`verified:true` is the producer's attestation only - the watcher does not verify the
underlying claim. Checkpoint files are read-only inputs; the producer (executor or
reviewer per procedure) writes them, the watcher never does.

### Sidecar files (the ONLY writes)

The scripts write only inside `sidecar_dir` - never STATE/TODO/EVENTS, session logs, or
sources: `state.json` (baselines, adapter cursors, confirmed checkpoints, removed-task
ring <=128, transition journal <=256 metadata-only; atomic replace; corruption =>
`state_corrupt` with the file untouched, baselines kept), `snapshot.json` (`written_at`,
`config_digest`, task views; atomic), `observer.lock` (fcntl flock, non-blocking,
single writer for poll/watch, crash-safe; status/diagnose take no lock), and the
ownership marker `.watch_managed` (content `campaign_watch/1`). State and snapshot
are bounded by an explicit 32 MiB cap on BOTH read and write: a write whose
serialized form would exceed it fails with `state_capacity` and leaves the previous
state and snapshot untouched - the watcher never writes a state it cannot reload.
On poll/watch a pre-existing sidecar dir is accepted only if it carries the marker
or contains nothing but known managed files (fresh or legacy sidecar; crash-leftover
`*.tmp.<pid>` tolerated) - anything else, including the campaign root holding
unmanaged files, is `sidecar_unmanaged`; managed outputs must be regular files and
symlinks are refused (`sidecar_refused`, no-follow opens). Removed tasks
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
   scheduler. Coordinator wakeups come only from a verified wakeup mechanism - the
   bounded event watcher (Option A) or the native heartbeat (Option B) - per
   [coordinator-heartbeat.md](coordinator-heartbeat.md); in the heartbeat's preferred
   sole-writer mode the heartbeat itself runs one bounded `poll` per cycle and no
   persistent `watch` process exists. If a persistent `watch` is running, the
   heartbeat reads `status` from its fresh sample and never starts a second writer -
   the flock makes concurrent poll/watch safe but not useful, and two writers means
   misdocumented ownership.

Nothing auto-starts: the scripts run only when explicitly invoked.

### Known constraints

- `observer.lock` uses fcntl flock: POSIX only.
- The process probe is Linux-only (/proc) and works only in the same PID namespace;
  elsewhere process and activity stay `unknown`.
- Activity is asserted only from current-operation evidence: a live PID with no
  pending ask or running tool reports activity `unknown`, never `generating` - a
  live PID alone cannot prove the model is generating. `idle` is likewise not
  asserted (no known-stop signal); both stay in the vocabulary for adapters that
  can prove them.
- Checkpoint `completed_at` is strict: aware UTC, `<= now`, and not older than the
  registration baseline - there is no future grace for progress.
- Retry-loop confirmation needs adapter error fingerprints, each matching error
  counted only while inside the rolling `retry_window_seconds` (unrelated newer
  errors never freshen an old group); runtimes that never emit them can at most
  reach `suspect_stall`.
- Invalid, corrupt, stale, rotated, or truncated input fails safe to `unknown`;
  bounded parent history (removed ring <=128, journal <=256) is explicit.
- Adapter ancestry gap: an oversized/malformed row or an unprovable parent latches
  a critical gap - adapter status stays `unknown` for the rest of that file
  generation and resets only on a rebuild (log identity change or truncation),
  never by later valid rows.
- Validation status: the adapter implements the OMP session-log schema version 3
  (the format emitted by OMP 18.2.6) as a bounded, metadata-only incremental
  reader, exercised against recorded real OMP sessions and synthetic edge cases
  (oversized rows, unprovable ancestry, deep chains). No end-to-end classification
  PASS against live OMP sessions is claimed for the integrated watcher; bounded
  fail-safe behavior is the contract.

### Relationship to the attempt budget (procedural, not CLI)

The watchdog's numerical thresholds (`no_step_seconds`, `retry_window_seconds`,
`stale_seconds`) are DIAGNOSIS triggers only. The campaign's attempt budget
(`attempt_budget_seconds`, default 2100; see SKILL.md section 10 and
[state-and-recovery.md](state-and-recovery.md)) is a separate hard procedural cap
enforced by the coordinator/runtime through scoped control - never by the observer,
which never kills, nudges, or remediates. The observer has no CLI flags or config
options for budget enforcement; that enforcement is procedure, not code.
