# Coordinator Wakeups: the Native Heartbeat Contract

The observer only reports; something must reliably re-enter the coordinator session so
the report turns into coordinator action. This reference defines the ONLY sanctioned
wakeup mechanism and its verification standard. Root cause background:
incident 2026-09-22 (`plans/watcher-incident-2026-09-22/REPORT.md` in the source repo).

## The mechanism (verified against installed Hermes source)

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

## What is explicitly forbidden as a wakeup mechanism

Each of these caused or enabled the 2026-09-22 incident:

- **`notify:true` on a persistent background process** - installed Hermes maps boolean
  `notify` to notify-on-COMPLETION (`tools/terminal_tool.py:1311-1338`). A
  12-hour loop that prints alerts to stdout keeps running and notifies nothing while
  alive. Persistent stdout is not a wakeup.
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

## Establishing and verifying (required before claiming autonomous monitoring)

Campaign START - and adoption of an already-running campaign - MUST establish AND
verify the heartbeat BEFORE the coordinator claims autonomous monitoring. "Set" alone
proves nothing.

1. Discover the exact current session (the one that will own coordination) and confirm
   it is the campaign's execution session.
2. `/heartbeat status` - confirm no pre-existing heartbeat, or one that is explicitly
   this campaign's; a foreign heartbeat means escalate or isolate, never overwrite.
3. Set it: `/heartbeat every 5m <instruction as above>`.
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
7. Prove stop control: `/heartbeat pause` (or `clear`), confirm via `/heartbeat
   status`, and confirm no further tick fires after one full interval.

Receipt standard: a duty receipt counts only with the observer's own fresh timestamp
or the concrete action taken - the heartbeat's armed status or `fire_count` alone is
NOT proof. Until steps 1-7 pass, the campaign is NOT under autonomous monitoring and
must be described as such.

## Stop conditions

Clear (`/heartbeat clear`) or pause the heartbeat when the campaign reaches
`completed`, a needs-user pause, or any state where coordinator action waits on the
user: no endless idle cycles burning tokens. Never leave stale resume commands in the
heartbeat instruction after a pause - a paused campaign's heartbeat, if resumed by the
user, must re-validate state (per
[state-and-recovery.md](state-and-recovery.md)) rather than blindly continue.

## Missing heartbeat capability

If the coordinator's runtime has no verified native heartbeat: the campaign is NOT
autonomous - say so. Temporary fallback: explicit bounded foreground waiting/polling
by the coordinator inside a turn (with a declared deadline), or the user re-prompting.
Never claim a schedule is installed when it is not, and never substitute the forbidden
mechanisms above. Bootstrap/migration tooling from other lanes is out of scope here
until independently verified; this skill's contract is the native heartbeat.
