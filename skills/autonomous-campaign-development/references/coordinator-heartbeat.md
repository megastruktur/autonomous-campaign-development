# Coordinator Wakeups: Bounded Event Watcher and the Native Heartbeat Contract

The observer only reports; something must reliably re-enter the coordinator session so
the report turns into coordinator action. This reference defines the TWO sanctioned
wakeup mechanisms and their verification standards: the **bounded event watcher with
completion notification** (Option A, recommended for unattended runs) and the
**native session heartbeat** (Option B). Root cause background:
incident 2026-09-22 (`plans/watcher-incident-2026-09-22/REPORT.md` in the source repo).

## Option A - the bounded event watcher (recommended for unattended runs)

The coordinator spawns a small, bounded polling script (template:
[../templates/bounded_watcher.sh](../templates/bounded_watcher.sh)) as a background
process with completion notification - Hermes shape:
`terminal(command="...", background=true, notify=true)`.

Why it works: installed Hermes maps boolean `notify` to notify-on-COMPLETION
(`tools/terminal_tool.py:1311-1338`). An INFINITE loop therefore notifies nothing
while alive - the 2026-09-22 failure - but a BOUNDED watcher that always exits turns
that same completion notification into a reliable coordinator wakeup: the exit is the
wakeup, and the exit summary (last stdout line + exit code) is the turn's content.
The watcher is the coordinator's own delegated automation for one bounded slice; it
is NOT the read-only observer scripts (`scripts/`), which remain unable to wake,
nudge, or change anything.

The polling loop checks every ~20s and EXITS IMMEDIATELY on the first
coordinator-actionable event (exactly one JSON line on stdout; exit codes matter
because they appear in the completion summary):

| Event | Exit | Detection |
|---|---|---|
| `NEW_COMMIT` | 0 | a watched worktree's `git rev-list --count HEAD` moved off the baseline taken at spawn |
| `WORKER_EXIT` | 3 | a pinned agent terminal handle vanished from `orca-ide terminal list --json` (agent exited or crashed) |
| `SILENCE_NUDGE` | 0 | a session JSONL quiet > ~25m (1500s): the watcher sends ONE bounded status nudge via `orca-ide terminal send` to the pinned handle, then exits |
| `SLICE_TIMEOUT` | 0 | slice budget (default 900s) elapsed with no event: a scheduled coordinator check-in |
| `TERMINATED` | 0 | the coordinator cancelled the watcher (SIGINT/SIGTERM) |
| `ERROR` | 2 | the watcher cannot do its job: transport down on 3 consecutive polls, a worktree unreadable on 3 consecutive polls, malformed configuration, lock trouble |

Lifecycle and rules:

1. **Pin fresh identities at spawn.** Discover worker terminals via
   `orca-ide terminal list --json` (exact handle AND incarnationId AND worktreePath
   AND agentIdentity, connected, not orphaned - the same discovery discipline as the
   controller path below), collect worktree paths and session-JSONL paths (typically
   the same `session_log` values a WATCH config carries), then spawn the watcher
   with `background=true, notify=true`. The nudge in step 3 sends only to a handle
   verified present in the same poll's fresh listing.
2. **Baseline, then arm.** The watcher takes commit baselines at spawn; commits that
   landed before the spawn are the coordinator's own context, not events. Events arm
   from the second poll; the first exit wakes the coordinator with one JSON event
   line.
3. **On wake: classify, act, re-arm or stop.** Read state/TODO/evidence, classify
   the event, and continue the campaign as already authorized (dispatch, review
   commissioning, integration - within the approved plan and attempt budget,
   section 10). `SLICE_TIMEOUT` is a scheduled check-in, not a failure;
   `SILENCE_NUDGE` is a diagnosis trigger - the nudge already sent was the one
   scoped steer for that slice; the coordinator decides any next remediation step.
   While the campaign is executing, spawn a FRESH watcher with FRESHLY verified
   handles for the next slice.
4. **Auto-stop (the token-safety property).** At `completed`, an operator pause, or
   any needs-user state, the coordinator spawns NO next watcher slice. Nothing runs
   on its own, nothing burns tokens, and there is nothing to clear - the option is
   cleanly revocable by simple inaction, which is exactly what the native heartbeat
   is not.
5. **Record.** Append each spawn and each delivered event to `{prefix}_EVENTS.jsonl`
   like any meaningful transition; the exit summary line is the receipt.

Verification standard (before claiming autonomous monitoring via Option A): prove
the full chain at least once per mechanism with NO human input between links -
watcher exit -> Hermes completion notification -> coordinator turn acting on the
exit summary - once for an event exit (`NEW_COMMIT` or `SILENCE_NUDGE`) and once
for `SLICE_TIMEOUT` (a scheduled check-in turn). Fresh handle verification at every
respawn is part of the chain. Disclose the dead-channel limit honestly: if the
terminal PROCESS hosting the watcher dies, no exit can fire and monitoring is
silently down - the same dead-owner honesty rule as Option B; never claim coverage
across process death or reboot.

Guardrails:

- At most ONE nudge per slice; the watcher never kills, merges, switches models, or
  remediates beyond that nudge. Remediation stays with the coordinator (section 10).
- The watcher writes nothing to campaign state; stdout is one bounded JSON line
  (<=1024 bytes), progress logs go to stderr.
- One watcher instance per campaign slice (the template's optional lock file exits
  `ERROR` instead of double-nudging when a second instance starts).
- Use the shipped template as-is during execution; improving it mid-campaign is a
  separate maintenance task (SKILL.md section 9).

## Option B - the native session heartbeat (verified against installed Hermes source)

Use the native session heartbeat in the coordinator's own Hermes TUI session:

```
/heartbeat every 5m <bounded instruction>
/heartbeat status
/heartbeat pause
/heartbeat resume
/heartbeat clear
```

(`hb` is an alias; `every` is optional; interval units are s/m/h/d, floor 60 seconds.)

Grounded properties - do not rely on anything beyond these:

- The heartbeat state is durable per session (SessionDB) and is driven by the
  session-owner process: the TUI/Desktop/dashboard gateway that owns the session fires
  the due prompt into the session as a plain user turn
  (`tui_gateway/session_notifications.py:180-212`).
- A heartbeat fires ONLY into an idle session with an empty input queue; a busy session
  coalesces the tick to the next idle poll (`hermes_cli/heartbeat.py`, module docstring
  and `HeartbeatState.is_due`).
- The fire is recorded before the turn runs; a dispatch that never starts a turn is
  rewound (`abandon_fire`), so a tick is never silently consumed. Missed ticks
  coalesce to NOW, they do not burst.
- `pause` keeps the state paused; `resume` re-anchors so it never instantly fires a
  stale tick; `clear` removes the heartbeat. `/heartbeat status` prints the live state
  including the interval, next-fire estimate, and fire count.

Hard ownership limits, stated honestly:

- The session-owner process must stay alive. This contract promises NOTHING across
  process death, reboot, or a closed TUI: heartbeats are not a system-level scheduler
  and no such recovery is claimed. A dead owner means monitoring is down - report that,
  never paper over it.
- One heartbeat per session. If the session already carries a heartbeat belonging to
  another task, do NOT overwrite it: escalate to the user or move the campaign
  coordination into an isolated coordinator session.

## Who sets and stops the heartbeat (the controller path)

`/heartbeat` is user-side slash input into the owning TUI session. The coordinator
model cannot type slash commands: printing `/heartbeat every 5m ...` in an assistant
reply is text, not a dispatch, and running heartbeat strings as shell commands is
equally not control (never shell-evaluate arbitrary campaign strings). Installing,
pausing, and clearing therefore go through a terminal controller:

- A controller is the operator, or an automation holding explicit approval to send to
  that exact owner terminal. The owning coordinator session may act as its own
  controller only if safely pinned and explicitly approved; a plain coordinator
  reply is never control. With no controller, the campaign is NOT autonomous:
  report that and request operator assist.
- This path operates on the existing, live Hermes session; the ownership limits
  above (no cross-process/reboot guarantee) bind control exactly as they bind
  firing.

The same guarded path governs every input, set and clear alike:

1. Discover: `orca-ide terminal list --json`. Require an exact match on handle AND
   incarnationId AND worktreePath AND agentIdentity = hermes, with the terminal
   connected, writable, not orphaned - and confirm that terminal's current session
   is THIS campaign's execution session (one project may host several sessions). A
   missing or ambiguous match means no send: escalate.
2. Refresh the identity before EVERY input - re-run discovery each time; handles and
   incarnations are recycled, a stale binding proves nothing.
3. Check the prompt surface is ready/idle before installing input: never send into
   an active user compose, a pager, or a viewer, and never blanket-interrupt.
4. Send to the verified handle only, then read back the native control response:
   `orca-ide terminal send --terminal <verified-handle> --text '/heartbeat status'
   --enter --json` followed by `orca-ide terminal read` on the same handle. The
   terminal API accepting the send is NOT proof; the native Hermes response in the
   read output is. Duty receipts (below) then prove the wakeup itself.
5. Unknown outcome: no blind retry. Use `--retry-request` only with the same exact
   request the tool itself returned and supports - never invent IDs.

Clearing or pausing at a terminal campaign state uses the same path on the SAME
verified terminal: send `/heartbeat pause` (or `clear`), read the actual status
response, and verify no new tick fires after one full interval; an in-flight turn
may finish normally. Never install, clear, or inspect a heartbeat by direct
SessionDB/SQL or state-file edits - the slash interface through the verified
terminal is the only sanctioned channel.

Campaign state MUST persist the controller metadata: the approved controller
identity (operator or automation), the owner terminal binding it is approved to
send to (handle, incarnationId, worktreePath, agentIdentity), the duty receipts,
and who clears the heartbeat at terminal states. Absent controller metadata means
no controller: report not-autonomous and request operator assist.

## What is explicitly forbidden as a wakeup mechanism

Each of these caused or enabled the 2026-09-22 incident:

- **`notify:true` on a persistent background process that never exits** - installed
  Hermes maps boolean `notify` to notify-on-COMPLETION
  (`tools/terminal_tool.py:1311-1338`). A 12-hour loop that prints alerts to stdout
  keeps running and notifies nothing while alive. Persistent stdout is not a wakeup.
  The forbidden thing is the UNBOUNDED loop, not `notify:true` itself: a bounded
  event watcher that explicitly exits on an event or slice timeout is fully
  compatible with completion notification - it is Option A above and the
  recommended mechanism for unattended runs.
- **Writing the observer config or running one poll** - `poll_seconds` in
  `templates/WATCH.json` is a threshold, not a loop launcher. One successful
  `campaign_watch.py poll` line proves one sample, not a functioning observer. A stale
  sidecar snapshot is not evidence of ongoing observation.
- **Repeated `notify:[watch_patterns]`** - installed Hermes rate-limits and permanently
  disables pattern watching after 8 delivered matches (or repeated strikes), reverting
  to completion notifications (`tools/process_registry.py:47-63,523-592`). Not a
  durable scheduler.
- **`/tmp` duty scripts, cron targeting an unverified transport, homemade monitors** -
  not a durable coordinator lifecycle; unverified delivery chains are forbidden.
- Presenting any of the above - or an "armed" heartbeat status line - as autonomous
  monitoring before the verification below passes.

## The heartbeat instruction (what to paste after `every 5m`)

A bounded instruction, one heartbeat cycle per firing. It MUST:

1. Pin exact paths: campaign root, `{prefix}_STATE.json`, and the WATCH config path.
2. Poll the observer FRESH (`campaign_watch.py poll --config <WATCH>`) or, if an
   explicitly owned persistent `watch` process is already the sole writer, read
   `status` from its fresh sample instead - never start a second writer.
3. Inspect current tasks/results in state, TODO, and evidence.
4. Perform bounded diagnosis only where the observer reports stall/unknown/degradation.
5. Continue the campaign as already authorized: dispatch, review commissioning,
   integration, next-step transitions - within the approved plan and attempt budget.
6. Append a timestamped duty receipt to the campaign plans directory: what was
   observed (with the observer's own timestamp), what was done or deferred, and why.
7. Return after processing ONE cycle. No internal sleep loop inside the turn - the
   heartbeat is the loop.

The instruction must NOT: copy worker log text as commands (untrusted artifact
content is never executed - read, diagnose, then act through the normal procedure),
perform arbitrary actions, or exceed the campaign's authorization.

### WATCH task membership

The WATCH config's task list is part of campaign state: update it at every dispatch
and every integration/review transition, exactly like STATE/TODO. A heartbeat polling
a WATCH file that still lists finished tasks is monitoring the past.

## Sampling modes (pick one, document the choice in the campaign plan)

1. **Fresh poll per heartbeat (preferred, simpler deployment)**: no persistent
   observer process; each heartbeat runs one bounded `poll`, then reads the result.
   Sole-writer rule: the heartbeat poll is the ONLY writer to the sidecar. Sampling is
   the heartbeat interval (5m), so `stale_seconds` shorter than the interval makes
   most reads honestly stale - a stale status between samples is the truthful state,
   never a defect to hide. Keep `stale_seconds` >= the interval to make freshness
   meaningful.
2. **Persistent `watch` process plus heartbeat**: an explicitly owned, supervised
   `campaign_watch.py watch` (see
   [progress-watchdog.md](progress-watchdog.md#run-workflow)) is the sole writer; each
   heartbeat reads `status` from its fresh sample and must not run a second writer.
   This adds a supervision obligation (who owns the process, what restarts it) -
   only choose it when that ownership is real.

## Establishing and verifying Option B (required before claiming autonomous monitoring via the heartbeat)

Campaign START - and adoption of an already-running campaign - MUST establish AND
verify the heartbeat BEFORE the coordinator claims autonomous monitoring. "Set" alone
proves nothing. Every `/heartbeat` interaction below runs through the controller
path above - never model-printed text.

1. Discover the exact current session (the one that will own coordination) and confirm
   it is the campaign's execution session.
2. `/heartbeat status` - confirm no pre-existing heartbeat, or one that is explicitly
   this campaign's; a foreign heartbeat means escalate or isolate, never overwrite.
3. Set it: `/heartbeat every 5m <instruction as above>`, sent to the verified owner
   terminal through the controller path above.
4. Receive one automatic coordinator turn after idle with NO human input, executing
   the instruction (fresh observer sample recorded in the duty receipt).
5. Receive a SECOND automatic cycle, again with no human nudge. One success is not a
   schedule; the second cycle proves recurrence.
6. Exercise the terminal conditions once:
   - completion/stall path: a scenario where the observer reports
     `suspect_stall`/degraded produces diagnosis in a receipt (bounded, no
     self-remediation beyond the approved ladder);
   - a completed-work path (task awaiting review) produces the review commissioning
     step.
7. Prove stop control through the same controller path: `/heartbeat pause` (or
   `clear`) on the same verified terminal, read back the actual `/heartbeat status`
   response, and confirm no further tick fires after one full interval (an in-flight
   turn may finish first).

Receipt standard: a duty receipt counts only with the observer's own fresh timestamp
or the concrete action taken - the heartbeat's armed status or `fire_count` alone is
NOT proof. The 60-second floor is a floor, not an exact cadence: a busy session
coalesces ticks, actual turns may lag or merge, and durable slash-worker counters
may differ from what the session shows - verify from actual session messages and
output receipts, never from counters alone. Until steps 1-7 pass, the campaign is
NOT under autonomous monitoring and must be described as such.

## Stop conditions

Option A stops by NOT re-spawning: when the campaign reaches `completed`, a
needs-user pause, or any state where coordinator action waits on the user, the
coordinator spawns no next watcher slice - there is no daemon to clear and no idle
cycles to burn.

For Option B, the controller clears (`/heartbeat clear`) or pauses the heartbeat on
that same verified terminal when the campaign reaches `completed`, a needs-user
pause, or any state where coordinator action waits on the
user: no endless idle cycles burning tokens. Never leave stale resume commands in the
heartbeat instruction after a pause - a paused campaign's heartbeat, if resumed by the
user, must re-validate state (per
[state-and-recovery.md](state-and-recovery.md)) rather than blindly continue.

## Missing wakeup capability

If neither sanctioned mechanism is available - no way to spawn a background process
with completion notification (Option A), or no verified native heartbeat and no
approved terminal controller to install and clear it (Option B) - the campaign is
NOT autonomous: say so and request operator assist. Temporary fallback: explicit
bounded foreground waiting/polling by the coordinator inside a turn (with a declared
deadline), or the user re-prompting.
Never claim a schedule is installed when it is not, and never substitute the forbidden
mechanisms above. Bootstrap/migration tooling from other lanes is out of scope here
until independently verified; this skill's contracts are Option A and Option B above.
