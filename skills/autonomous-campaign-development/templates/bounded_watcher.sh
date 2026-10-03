#!/usr/bin/env bash
# bounded_watcher.sh - Bounded event-driven coordinator wakeup (Option A).
#
# Part of the autonomous-campaign-development skill (v1.2.0). The COORDINATOR
# spawns this script as a background process with completion notification
# (Hermes: terminal(command="...", background=true, notify=true)). Installed
# Hermes maps boolean notify to notify-on-COMPLETION, so this script is a
# wakeup ONLY because it always EXITS: on the first coordinator-actionable
# event, or when the slice budget expires. A loop that never exits notifies
# nothing (incident 2026-09-22). The coordinator decides whether to spawn the
# next slice; at completed/paused/needs-user states it spawns nothing
# (auto-stop: no daemon, no idle token burn, no heartbeat cleanup needed).
#
# Event contract (exactly one JSON line <=1024 bytes on stdout as the last
# output; human-readable progress goes to stderr):
#   NEW_COMMIT    exit 0  a watched worktree HEAD moved (rev-list --count
#                         changed from the baseline taken at spawn)
#   SILENCE_NUDGE exit 0  a watched session JSONL has been quiet for more than
#                         WATCHER_SILENCE_SECONDS (default 1500s = 25m); the
#                         watcher sent ONE bounded status nudge to the pinned
#                         terminal (a scoped steer per SKILL.md section 10)
#                         and exits so the coordinator regains control
#   SLICE_TIMEOUT exit 0  the polling window elapsed with no event: a
#                         scheduled coordinator check-in
#   TERMINATED    exit 0  the watcher received SIGINT/SIGTERM (cancelled)
#   WORKER_EXIT   exit 3  a pinned agent terminal handle vanished from
#                         `terminal list` (agent exited or crashed)
#   ERROR         exit 2  the watcher cannot do its job: pinned terminal list
#                         unavailable on MAX_FAILS consecutive polls, a
#                         worktree unreadable on MAX_FAILS consecutive polls,
#                         a malformed WATCHER_WATCHED item, or lock trouble
#
# Because completion notification fires on ANY exit, a crash of this script
# still wakes the coordinator (visible as a nonzero exit + stderr tail). The
# one unnotified failure mode: the Orca terminal PROCESS hosting this watcher
# dies. That kills the wakeup channel without an exit event - the same
# dead-owner honesty rule as the heartbeat option applies: monitoring is down,
# say so; never claim coverage you cannot prove.
#
# Configuration (environment variables; defaults in parentheses):
#   WATCHER_WATCHED         REQUIRED for commit/silence/exit detection. Items
#                           separated by spaces; each item is
#                           "<worktree-path>|<session.jsonl-path>|<terminal-handle>".
#                           Use "-" for a field you do not want monitored, e.g.
#                           "/repo/.wt/T1-feat|/repo/.omp/sessions/t1.jsonl|term_abc"
#                           or "/repo/.wt/T2-fix|-|-". Paths must not contain
#                           spaces. An empty value runs a pure SLICE_TIMEOUT
#                           window (scheduled periodic check-ins).
#   WATCHER_POLL_INTERVAL   seconds between checks (20)
#   WATCHER_SLICE_BUDGET    total seconds before SLICE_TIMEOUT (900). Set this
#                           to your worst-case acceptable check-in gap. A
#                           session silent before spawn trips SILENCE_NUDGE on
#                           the first poll; a worker that goes quiet mid-slice
#                           is caught when the age crosses the threshold, so
#                           keep WATCHER_SLICE_BUDGET > WATCHER_SILENCE_SECONDS
#                           if mid-silence wakeups matter for the campaign.
#   WATCHER_SILENCE_SECONDS session-JSONL quiet threshold (1500 = 25m)
#   WATCHER_NUDGE_TEXT      the single bounded status nudge text (default below)
#   WATCHER_LOCK            optional lock file; a second watcher instance with
#                           the same lock exits ERROR instead of double-nudging
#   ORCA_CLI_COMMAND        Orca executable (default "orca-ide"; inside Orca
#                           terminals "orca", dev checkouts "orca-dev")
#
# Identity rules (bind the coordinator to these, not just the script): pin
# handles discovered FRESH via `orca-ide terminal list --json` at spawn time
# (handle AND incarnation AND worktree AND agentIdentity = the expected agent,
# connected, not orphaned) and re-verify at every respawn - handles and
# incarnations are recycled. The silence nudge sends only to a handle that was
# present in the same poll's fresh listing. Full contract:
# references/coordinator-heartbeat.md in the skill.

set -u -o pipefail

POLL_INTERVAL="${WATCHER_POLL_INTERVAL:-20}"
SLICE_BUDGET="${WATCHER_SLICE_BUDGET:-900}"
SILENCE_SECONDS="${WATCHER_SILENCE_SECONDS:-1500}"
NUDGE_TEXT="${WATCHER_NUDGE_TEXT:-Status check (bounded watcher): reply with a one-line progress status for your current task, per the campaign procedure.}"
ORCA_BIN="${ORCA_CLI_COMMAND:-orca-ide}"
WATCHED="${WATCHER_WATCHED:-}"
LOCK="${WATCHER_LOCK:-}"

MAX_FAILS=3  # consecutive failed polls of one target before ERROR

log() { printf '%s %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$*" >&2; }

# emit EVENT TASK DETAIL: one bounded JSON line on stdout, then stop.
emit() {
  python3 - "$1" "$2" "$3" <<'PY'
import json, sys, time
event, task, detail = sys.argv[1], sys.argv[2], sys.argv[3]
line = json.dumps({"v": 1, "kind": "watcher_event", "event": event,
                   "task": task, "detail": detail[:400], "at": int(time.time())})
print(line, flush=True)
PY
}

finish() {
  local code=0
  case "$1" in
    WORKER_EXIT) code=3 ;;
    ERROR) code=2 ;;
  esac
  emit "$@"
  exit "$code"
}

trap 'finish TERMINATED "watcher" "received SIGINT/SIGTERM; coordinator cancelled the slice"' INT TERM

# Single-instance guard (optional). flock is util-linux; POSIX-only like the
# observer's own lock.
if [[ -n "$LOCK" ]]; then
  if ! : > "$LOCK" 2>/dev/null; then
    finish ERROR "watcher" "lock file unusable: $LOCK"
  fi
  exec 9>"$LOCK"
  if ! flock -n 9; then
    finish ERROR "watcher" "another watcher instance already holds $LOCK"
  fi
fi

# Parse WATCHER_WATCHED into parallel arrays: WTS / LOGS / HANDLES.
declare -a WTS=() LOGS=() HANDLES=()
if [[ -n "$WATCHED" ]]; then
  read -r -a _items <<< "$WATCHED"
  for item in "${_items[@]}"; do
    wt="${item%%|*}"
    rest="${item#*|}"
    jsonl="${rest%%|*}"
    handle="${rest#*|}"
    _stripped="${item//|/}"
    npipes=$(( ${#item} - ${#_stripped} ))
    if (( npipes != 2 )) || [[ -z "$wt" || -z "$jsonl" || -z "$handle" ]]; then
      finish ERROR "watcher" "malformed WATCHER_WATCHED item (need wt|jsonl|handle): $item"
    fi
    WTS+=("$wt"); LOGS+=("$jsonl"); HANDLES+=("$handle")
  done
fi

HAVE_HANDLES=0
for h in "${HANDLES[@]}"; do
  [[ "$h" != "-" ]] && HAVE_HANDLES=1
done

declare -A WT_BASELINE=() WT_FAILS=() LOG_FAILS=()
TRANSPORT_FAILS=0

# A pinned terminal handle that vanished from the fresh listing means the
# agent terminal exited or crashed. Presence is checked as a fixed string in
# the JSON listing: schema-agnostic on purpose. Refining this check is a
# maintenance task (SKILL.md section 9), never a mid-campaign edit.
check_terminals() {
  local listing h
  listing="$("$ORCA_BIN" terminal list --json 2>/dev/null)" || return 1
  [[ -n "$listing" ]] || return 1
  for h in "${HANDLES[@]}"; do
    [[ "$h" == "-" ]] && continue
    if ! grep -qF -- "$h" <<< "$listing"; then
      finish WORKER_EXIT "$h" "pinned terminal handle no longer present in terminal list"
    fi
  done
  return 0
}

# NEW_COMMIT: any watched worktree HEAD moved. The baseline is the first
# successful sample AFTER spawn; a commit that landed between the
# coordinator's last look and the spawn is the coordinator's own context, not
# an event. Any count change (forward or reset) fires.
check_commits() {
  local idx wt count
  for idx in "${!WTS[@]}"; do
    wt="${WTS[$idx]}"
    if ! count="$(git -C "$wt" rev-list --count HEAD 2>/dev/null)"; then
      WT_FAILS[$idx]=$(( ${WT_FAILS[$idx]:-0} + 1 ))
      log "git unreadable in $wt (fail ${WT_FAILS[$idx]}/$MAX_FAILS)"
      if (( WT_FAILS[$idx] >= MAX_FAILS )); then
        finish ERROR "$wt" "git rev-list failed ${WT_FAILS[$idx]} consecutive polls (worktree gone?)"
      fi
      continue
    fi
    WT_FAILS[$idx]=0
    if [[ -z "${WT_BASELINE[$idx]:-}" ]]; then
      WT_BASELINE[$idx]="$count"
      log "baseline $wt HEAD commits=$count"
    elif [[ "$count" != "${WT_BASELINE[$idx]}" ]]; then
      finish NEW_COMMIT "$wt" "rev-list --count HEAD ${WT_BASELINE[$idx]} -> $count"
    fi
  done
}

# SILENCE_NUDGE: JSONL mtime older than the threshold means no session writes
# for that long. jsonl mtime age is transport evidence, not progress evidence
# (progress-watchdog.md); it only ever triggers a diagnosis nudge, never a
# verdict. At most ONE nudge per slice, then this watcher exits so the
# coordinator - not the script - decides the next remediation step.
check_silence() {
  local idx logpath handle age mtime detail
  for idx in "${!LOGS[@]}"; do
    logpath="${LOGS[$idx]}"
    [[ "$logpath" == "-" ]] && continue
    if ! mtime="$(stat -c %Y "$logpath" 2>/dev/null)"; then
      LOG_FAILS[$idx]=$(( ${LOG_FAILS[$idx]:-0} + 1 ))
      log "session jsonl unreadable: $logpath (fail ${LOG_FAILS[$idx]}/$MAX_FAILS)"
      if (( LOG_FAILS[$idx] >= MAX_FAILS )); then
        finish ERROR "$logpath" "session jsonl unreadable ${LOG_FAILS[$idx]} consecutive polls (wrong path?)"
      fi
      continue
    fi
    LOG_FAILS[$idx]=0
    age=$(( $(date +%s) - mtime ))
    if (( age > SILENCE_SECONDS )); then
      handle="${HANDLES[$idx]}"
      detail="session jsonl quiet for ${age}s > ${SILENCE_SECONDS}s"
      if [[ "$handle" != "-" ]]; then
        if "$ORCA_BIN" terminal send --terminal "$handle" --text "$NUDGE_TEXT" --enter --json >/dev/null 2>&1; then
          detail+="; one bounded nudge sent to $handle"
        else
          detail+="; nudge send to $handle FAILED (coordinator must verify delivery)"
        fi
      else
        detail+="; no pinned terminal to nudge"
      fi
      finish SILENCE_NUDGE "$logpath" "$detail"
    fi
  done
}

deadline=$(( $(date +%s) + SLICE_BUDGET ))
log "watcher started: interval=${POLL_INTERVAL}s budget=${SLICE_BUDGET}s silence>${SILENCE_SECONDS}s targets=${#WTS[@]} handles_pinned=$HAVE_HANDLES"

# First iteration captures baselines; events arm from the second poll onward.
while :; do
  now="$(date +%s)"
  if (( now >= deadline )); then
    finish SLICE_TIMEOUT "campaign" "no event within ${SLICE_BUDGET}s; scheduled coordinator check-in due"
  fi

  if (( HAVE_HANDLES )); then
    if check_terminals; then
      TRANSPORT_FAILS=0
    else
      TRANSPORT_FAILS=$(( TRANSPORT_FAILS + 1 ))
      log "terminal list unavailable (fail $TRANSPORT_FAILS/$MAX_FAILS)"
      if (( TRANSPORT_FAILS >= MAX_FAILS )); then
        finish ERROR "$ORCA_BIN" "terminal list failed $TRANSPORT_FAILS consecutive polls (transport down?)"
      fi
    fi
  fi

  check_commits
  check_silence

  sleep_for="$POLL_INTERVAL"
  remaining=$(( deadline - now ))
  (( remaining < sleep_for )) && sleep_for="$remaining"
  (( sleep_for > 0 )) && sleep "$sleep_for"
done
