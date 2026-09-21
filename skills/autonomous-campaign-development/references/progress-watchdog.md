# Progress Semantics and the Optional Watchdog

Liveness wording is strict here because weak wording has caused false health calls:
transport or process activity, model responses, and task completion are three different
things. This reference defines what counts as each, and the planned contract of the
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

## Planned observer CLI (contract pending final alignment)

Two Python 3 standard-library-only scripts ship with this skill (release 1.1.0):
`scripts/omp_events.py`, a metadata-only incremental OMP session-JSONL adapter, and
`scripts/campaign_watch.py`, the deterministic watcher CLI. Documented command surface:
`poll --config PATH` (one bounded sample), `watch --config PATH` (30s local polls, 300s
periodic heartbeat, transitions reported immediately), `status --config PATH [--task ID]`
(reads the snapshot; output is one JSON object of at most 1024 UTF-8 bytes),
`diagnose --config PATH [--task ID]` (separately bounded). These flags are the planned
contract; the exact final flag set and the config file schema are validated against the
implementation before release - do not script against undocumented flags or fields.

The config file (future `templates/WATCH.json`) expresses, per watched task: task and
attempt identity, session identity, phase, session log path, optional trusted process
identity, scoped checkpoint paths with deadlines, and thresholds. The template is
deliberately deferred until the schema is aligned with `scripts/campaign_watch.py`;
hand-writing configs against an unpublished schema is prohibited.
