"""omp_events — metadata-only incremental adapter for OMP v3 session JSONL.

Contract (finalized for the slice-01 observer watchdog):

Import API
----------
    from omp_events import OmpSessionAdapter

    adapter = OmpSessionAdapter(clock=time.time)          # injectable clock
    report  = adapter.poll("/path/to/session.jsonl")      # bounded incremental poll
    state   = adapter.export_state()                      # JSON-serializable
    adapter2 = OmpSessionAdapter.from_state(state)        # cursor survives reload
    adapter.snapshot()                                    # sanitized semantic view

`report` (dict): status in {"ok","backlog","fault"}; `backlog` bool;
backlog_bytes; new_bytes; events_processed; rebuilt reason or None;
session_switch; bootstrap_pending; history_replayed; new_faults (kind->count);
summary == snapshot() at poll end.  Any new fault-class observation
(missing/unreadable input, malformed/oversized rows, unknown header/version,
unknown event type or critical shape) yields status "fault": unknown is
observable, never healthy.

Persistence: state carries file identity (st_dev/st_ino) + session header
UUID + binary offset + bounded tail of the incomplete trailing line.  Polls
never rescan the whole file except after a rebuild trigger (identity change =
rotation/session switch, or same-file truncation size < offset), which is
reported as `rebuilt` and marks re-derived progress as historical
(`live: false`), never as freshly observed success.

Sanitization: retained state/output contain only structural metadata —
entry/toolCall IDs, allowlisted tool names (unknown names irreversibly
hashed), roles, stopReason, errorId, irreversible errorMessage fingerprints,
timestamps, counters.  No raw tool arguments, message content, thoughts,
error text, or cwd.

Semantics exposed (snapshot): last successful assistant event
(stopReason in {stop, toolUse} AND no errorId, live branch only, valid ts),
last completed tool result with isError distinction, pending tools
(kind "ask_waiting" vs "running"), error totals / consecutive failure streak /
bounded recent-error ring, session + observation faults, uncertainty flags.
Non-message/service events (model_usage, title, model-change, compaction,
custom) never create semantic task progress.  stopReason "error" (with
errorId/errorMessage) and "aborted" are explicit failures; tool results with
isError are completion/error observations, never success.  A success on a
branch later reported discarded (branch_summary kind
"discarded-entry-branch") is retracted.  Malformed or future timestamps are
flagged invalid and are not proof of current progress (freshness comes from
poll-time `last_append_at`).

Fail-safe decisions (conservative, documented): ancestry that cannot be
resolved within the bounded parent map counts as uncertain and does NOT
count as success; assistant messages without a recognizable stopReason are
"other" (neither success nor failure, unknown-flagged); unsupported session
version poisons the scan (lines keep being consumed for cursor health, but
no semantics); dedupe/branch structures are bounded and eviction raises an
uncertainty flag rather than guessing.

OMP v3 shape assumptions (from prior peer inspection of OMP 18.2.6; where
the peer flagged uncertainty — branch_summary nesting, custom event naming —
parsing is tolerant over a small set of candidate locations and unrecognized
shapes surface as unknown, not silence).
"""

from __future__ import annotations

import base64
import hashlib
import json
import os
import re
import stat
import time
from datetime import datetime, timezone

__all__ = ["OmpSessionAdapter"]

SUPPORTED_VERSIONS = {3, "3"}
SERVICE_EVENT_TYPES = {
    "model_usage", "title", "compaction", "model-change", "model_change",
}
NON_PROGRESS_ROLES = {"user", "system", "developer", "tool", "summary"}
ASK_TOOL_NAMES = {
    "ask", "ask_user", "askuser", "ask_user_question",
    "user_prompt", "prompt_user", "interrogate_user",
}
_SAFE_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.\-]{0,63}$")
_SAFE_SMALL = re.compile(r"^[A-Za-z0-9_.\-]{1,64}$")
_SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.\-]{0,127}$")
_MAX_ANCESTRY_DEPTH = 64

DEFAULT_LIMITS = {
    "max_read_bytes": 1 << 20,   # bytes read per poll
    "max_row_bytes": 1 << 16,    # any single JSONL row larger than this -> skip
    "max_events_per_poll": 2000, # complete rows parsed per poll
    "seen_cap": 4096,            # dedupe entry ids retained
    "entries_cap": 4096,         # parent-chain map retained
    "discarded_cap": 1024,       # discarded branch roots retained
    "success_ring": 256,         # successes kept for discard retraction
    "pending_cap": 256,          # concurrently pending tool calls
    "recent_errors": 8,          # recent error ring length
    "allowed_skew": 300.0,       # seconds of future timestamp tolerance
}


def _fp(text: str) -> str:
    """Irreversible fingerprint (sha256/16 hex) of a sensitive string."""
    return hashlib.sha256(text.encode("utf-8", "replace")).hexdigest()[:16]


def _classify_tool_name(raw):
    """Return (name_class, safe_display). Unknown/unsafe names are hashed."""
    if isinstance(raw, str) and _SAFE_NAME.match(raw):
        return ("ask" if raw.lower() in ASK_TOOL_NAMES else "tool"), raw
    if isinstance(raw, str):
        return "unknown", "name:" + _fp(raw)
    return "unknown", "name:" + _fp(repr(type(raw).__name__))


def _parse_ts(raw, now, allowed_skew):
    """Return (epoch_or_None, valid, reason). Future/malformed -> invalid."""
    if not isinstance(raw, str) or not raw:
        return None, False, "malformed"
    try:
        dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return None, False, "malformed"
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    ts = dt.timestamp()
    if ts < 0:
        return None, False, "malformed"
    if ts > now + allowed_skew:
        return ts, False, "future"
    return ts, True, ""


def _walk_for(container, key, depth=2):
    """Tolerant lookup of `key` in container and nested details/data dicts."""
    if not isinstance(container, dict):
        return None
    if key in container:
        return container[key]
    if depth <= 0:
        return None
    for sub in (container.get("details"), container.get("data")):
        if isinstance(sub, dict):
            found = _walk_for(sub, key, depth - 1)
            if found is not None:
                return found
    return None

_TSTATE_VERSION = 1


class OmpSessionAdapter:
    """Incremental, sanitizing, bounded adapter over one OMP v3 session file."""

    def __init__(self, clock=time.time, **limits):
        self.clock = clock
        bad = set(limits) - set(DEFAULT_LIMITS)
        if bad:
            raise ValueError("unknown limits: %s" % sorted(bad))
        self.lim = dict(DEFAULT_LIMITS)
        self.lim.update(limits)
        if (self.lim["max_read_bytes"] < 1 or self.lim["max_row_bytes"] < 2
                or self.lim["max_events_per_poll"] < 1):
            raise ValueError("limits must be positive")
        self._tail = b""
        self._reset()

    # ------------------------------------------------------------------ state

    def _reset(self):
        self._seen_set = set()
        self.s = {
            "format": _TSTATE_VERSION,
            "session": None,            # {"header_id","version"} once header seen
            "session_fault": None,      # e.g. "unsupported_version"
            "file": None,               # {"dev","ino"}
            "offset": 0,                # consumed bytes (fully processed/skipped)
            "partial_b64": "",          # bounded unconsumed tail (incl. partial line)
            "skip_mode": False,         # dropping bytes until next newline
            "bootstrap_pending": True,  # still scanning history this generation
            "generations": 0,
            "prev_header_id": None,
            "seen": [],                 # bounded dedupe ids (order = FIFO)
            "entries": {},              # bounded id -> parent
            "discarded": [],            # bounded discarded branch roots
            "last_success": None,
            "success_ring": [],
            "last_tool": None,
            "pending": {},              # toolCallId -> pending record
            "consecutive_failures": 0,
            "error_totals": {"assistant_error": 0, "assistant_aborted": 0, "tool_error": 0},
            "recent_errors": [],
            "counters": {
                "events": 0, "successful_assistant": 0, "failed_assistant": 0,
                "assistant_other": 0, "tool_results": 0, "tool_results_error": 0,
                "service_events": 0, "skipped_schema_fault": 0,
                "discarded_branch_events": 0, "discarded_success_retracted": 0,
                "duplicates": 0,
            },
            "faults": {},               # kind -> cumulative count
            "faults_recent": [],        # bounded [{"kind","at"}]
            "uncertainty": {
                "dedupe_evicted": False, "entries_evicted": False,
                "ancestry_uncertain": 0, "pending_overflow": False,
                "unknown_seen": False,
            },
            "observation": {"last_poll_at": None, "last_append_at": None, "polls": 0},
        }

    def export_state(self):
        """JSON-serializable persistent state (cursor + bounded metadata)."""
        out = json.loads(json.dumps(self.s))  # detach + validate JSON-safety
        out["partial_b64"] = base64.b64encode(self._tail).decode("ascii")
        return out

    @classmethod
    def from_state(cls, state, clock=time.time, **limits):
        adapter = cls(clock=clock, **limits)
        adapter.load_state(state)
        return adapter

    def load_state(self, state):
        if not isinstance(state, dict) or state.get("format") != _TSTATE_VERSION:
            raise ValueError("incompatible state")
        self._reset()
        self.s.update(json.loads(json.dumps(state)))
        self._seen_set = set(self.s["seen"])
        try:
            self._tail = base64.b64decode(self.s.pop("partial_b64", "") or "")
        except Exception:
            self._tail = b""
        if not isinstance(self._tail, bytes):
            self._tail = b""

    # ------------------------------------------------------------- snapshot

    def snapshot(self):
        """Sanitized semantic view for the observer (no rebuild, pure read)."""
        s = self.s
        return {
            "session": dict(s["session"]) if s["session"] else None,
            "session_fault": s["session_fault"],
            "file": dict(s["file"]) if s["file"] else None,
            "offset": s["offset"],
            "bootstrap_pending": s["bootstrap_pending"],
            "last_success": dict(s["last_success"]) if s["last_success"] else None,
            "last_tool": dict(s["last_tool"]) if s["last_tool"] else None,
            "pending_tools": [dict(v) for v in s["pending"].values()],
            "consecutive_failures": s["consecutive_failures"],
            "error_totals": dict(s["error_totals"]),
            "recent_errors": [dict(e) for e in s["recent_errors"]],
            "counters": dict(s["counters"]),
            "faults": dict(s["faults"]),
            "faults_recent": [dict(f) for f in s["faults_recent"]],
            "uncertainty": dict(s["uncertainty"]),
            "observation": dict(s["observation"]),
        }

    # ------------------------------------------------- faults and bookkeeping

    def _fault(self, kind):
        s = self.s
        s["faults"][kind] = s["faults"].get(kind, 0) + 1
        ring = s["faults_recent"]
        ring.append({"kind": kind, "at": s["observation"]["last_poll_at"]})
        del ring[: len(ring) - self.lim["recent_errors"]]
        self._new_faults[kind] = self._new_faults.get(kind, 0) + 1

    def _note_seen(self, entry_id):
        if entry_id in self._seen_set:
            return False
        seen = self.s["seen"]
        seen.append(entry_id)
        self._seen_set.add(entry_id)
        if len(seen) > self.lim["seen_cap"]:
            self._seen_set.discard(seen.pop(0))
            self.s["uncertainty"]["dedupe_evicted"] = True
        return True

    def _note_entry(self, entry_id, parent):
        entries = self.s["entries"]
        entries[entry_id] = parent
        if len(entries) > self.lim["entries_cap"]:
            oldest = next(iter(entries))
            del entries[oldest]

    def _is_live(self, entry_id):
        """Return "live" | "discarded" | "uncertain" for an entry's ancestry."""
        entries, discarded = self.s["entries"], set(self.s["discarded"])
        cur, hops = entry_id, 0
        while cur is not None and hops < _MAX_ANCESTRY_DEPTH:
            if cur in discarded:
                return "discarded"
            if cur not in entries:
                return "uncertain"  # entry/ancestor evicted: no guessing
            cur, hops = entries[cur], hops + 1
        return "uncertain" if hops >= _MAX_ANCESTRY_DEPTH else "live"

    def _record_success(self, entry_id, ts, ts_valid, stop_reason):
        s = self.s
        rec = {
            "entry_id": entry_id, "ts": ts, "ts_valid": ts_valid,
            "stop_reason": stop_reason, "live": not s["bootstrap_pending"],
        }
        ring = s["success_ring"]
        ring.append(rec)
        del ring[: len(ring) - self.lim["success_ring"]]
        s["last_success"] = dict(rec)
        s["counters"]["successful_assistant"] += 1
        s["consecutive_failures"] = 0

    def _retract_successes(self):
        """Drop successes whose ancestry now resolves to a discarded branch."""
        ring = self.s["success_ring"]
        kept = [r for r in ring if self._is_live(r["entry_id"]) != "discarded"]
        retracted = len(ring) - len(kept)
        if retracted:
            self.s["success_ring"] = kept
            c = self.s["counters"]
            c["successful_assistant"] = max(0, c["successful_assistant"] - retracted)
            c["discarded_success_retracted"] += retracted
            self.s["last_success"] = dict(kept[-1]) if kept else None

    def _note_discarded_root(self, root_id):
        d = self.s["discarded"]
        if root_id not in d:
            d.append(root_id)
            if len(d) > self.lim["discarded_cap"]:
                del d[: len(d) - self.lim["discarded_cap"]]
                self.s["uncertainty"]["entries_evicted"] = True
        self._retract_successes()

    def _note_error(self, category, error_id, fingerprint, ts, ts_valid):
        s = self.s
        s["error_totals"][category] = s["error_totals"].get(category, 0) + 1
        s["consecutive_failures"] += 1
        safe_id = error_id
        if isinstance(safe_id, str) and not _SAFE_SMALL.match(safe_id):
            safe_id = "id:" + _fp(safe_id)
        rec = {
            "category": category, "error_id": safe_id,
            "fingerprint": fingerprint, "ts": ts, "ts_valid": ts_valid,
        }
        ring = s["recent_errors"]
        ring.append(rec)
        del ring[: len(ring) - self.lim["recent_errors"]]

    # ------------------------------------------------------------ row parsing

    def _handle_line(self, line, now):
        line = line.rstrip(b"\r")
        if not line.strip():
            return
        if len(line) > self.lim["max_row_bytes"]:
            self._fault("oversized_row")
            return
        try:
            ev = json.loads(line.decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            self._fault("malformed_row")
            return
        if not isinstance(ev, dict):
            self._fault("malformed_row")
            return
        entry_id, etype, raw_ts = ev.get("id"), ev.get("type"), ev.get("timestamp")
        if (not isinstance(entry_id, str) or not _SAFE_ID.match(entry_id)
                or not isinstance(etype, str) or not etype):
            self._fault("unknown_shape")
            return
        parent = ev.get("parentId")
        if parent is not None and not _SAFE_ID.match(parent):
            self._fault("unknown_shape")
            parent = None
        if "parentId" not in ev:
            self._fault("unknown_shape")
        ts, ts_valid, why = _parse_ts(raw_ts, now, self.lim["allowed_skew"])
        if not ts_valid:
            self._fault("invalid_timestamp")
        if not self._note_seen(entry_id):
            self.s["counters"]["duplicates"] += 1
            return
        self._note_entry(entry_id, parent)
        if self.s["session_fault"]:
            self.s["counters"]["skipped_schema_fault"] += 1
            return
        self.s["counters"]["events"] += 1
        if etype == "session":
            self._handle_header(ev)
        elif etype == "message":
            self._handle_message(ev, entry_id, ts, ts_valid)
        elif etype == "branch_summary":
            self._handle_branch(ev)
        elif etype == "custom":
            self._handle_custom(ev)
        elif etype in SERVICE_EVENT_TYPES:
            self.s["counters"]["service_events"] += 1
        else:
            self._fault("unknown_event_type")
            self.s["uncertainty"]["unknown_seen"] = True

    def _handle_header(self, ev):
        s = self.s
        if s["session"] is not None or s["session_fault"]:
            self._fault("unexpected_header")
            return
        version, sid = ev.get("version"), ev.get("id")
        if (version in SUPPORTED_VERSIONS and isinstance(sid, str)
                and _SAFE_ID.match(sid)):
            s["session"] = {"header_id": sid, "version": 3}
            if s["prev_header_id"] is not None and sid != s["prev_header_id"]:
                self._switched = True
            s["prev_header_id"] = sid
        else:
            s["session_fault"] = "unsupported_version"
            self._fault("unsupported_version")
            self.s["uncertainty"]["unknown_seen"] = True

    def _handle_message(self, ev, entry_id, ts, ts_valid):
        s = self.s
        if s["session"] is None:
            self._fault("message_before_header")
            return
        msg = ev.get("message")
        if not isinstance(msg, dict):
            self._fault("unknown_shape")
            return
        role = msg.get("role")
        if role == "assistant":
            self._handle_assistant(msg, entry_id, ts, ts_valid)
        elif role == "toolResult":
            self._handle_tool_result(msg, ts, ts_valid)
        elif role in NON_PROGRESS_ROLES:
            s["counters"]["service_events"] += 1  # user/system/etc: no progress
        else:
            self._fault("unknown_shape")
            self.s["uncertainty"]["unknown_seen"] = True

    def _handle_assistant(self, msg, entry_id, ts, ts_valid):
        s = self.s
        stop, err_id = msg.get("stopReason"), msg.get("errorId")
        err_msg = msg.get("errorMessage")
        for part in self._tool_call_parts(msg):
            self._register_pending(part, entry_id, ts, ts_valid)
        if err_id is not None or stop == "error":
            fp = _fp(err_msg) if isinstance(err_msg, str) else None
            self._note_error("assistant_error", err_id, fp, ts, ts_valid)
            s["counters"]["failed_assistant"] += 1
        elif stop == "aborted":
            self._note_error("assistant_aborted", None, None, ts, ts_valid)
            s["counters"]["failed_assistant"] += 1
        elif stop in ("stop", "toolUse"):
            state = self._is_live(entry_id)
            if state == "discarded":
                s["counters"]["discarded_branch_events"] += 1
            elif state == "uncertain":
                s["uncertainty"]["ancestry_uncertain"] += 1
                self._fault("ancestry_uncertain")
            else:
                self._record_success(entry_id, ts, ts_valid, stop)
        else:
            s["counters"]["assistant_other"] += 1
            self._fault("unknown_stop_reason")
            self.s["uncertainty"]["unknown_seen"] = True

    @staticmethod
    def _tool_call_parts(msg):
        content = msg.get("content")
        if not isinstance(content, list):
            return []
        return [p for p in content
                if isinstance(p, dict) and p.get("type") == "toolCall"]

    def _register_pending(self, part, entry_id, ts, ts_valid):
        tcid = part.get("id")
        if not isinstance(tcid, str) or not tcid:
            self._fault("unknown_shape")
            return
        name_class, safe_name = _classify_tool_name(part.get("name"))
        pending = self.s["pending"]
        if len(pending) >= self.lim["pending_cap"]:
            self.s["uncertainty"]["pending_overflow"] = True
            self._fault("pending_overflow")
            return
        pending[tcid] = {
            "tool_call_id": tcid, "name": safe_name, "name_class": name_class,
            "kind": "ask_waiting" if name_class == "ask" else "running",
            "started": False, "ts": ts, "ts_valid": ts_valid, "entry_id": entry_id,
        }

    def _handle_tool_result(self, msg, ts, ts_valid):
        s = self.s
        tcid = msg.get("toolCallId")
        if not isinstance(tcid, str) or not tcid:
            self._fault("unknown_shape")
            return
        name_class, safe_name = _classify_tool_name(msg.get("toolName"))
        is_error = msg.get("isError") is True
        rec = {
            "tool_call_id": tcid, "name": safe_name, "name_class": name_class,
            "is_error": is_error, "ts": ts, "ts_valid": ts_valid,
        }
        s["last_tool"] = rec
        s["counters"]["tool_results"] += 1
        if s["pending"].pop(tcid, None) is None:
            self._fault("unknown_tool_result_ref")
        if is_error:
            s["counters"]["tool_results_error"] += 1
            self._note_error("tool_error", None, None, ts, ts_valid)

    def _handle_custom(self, ev):
        name = _walk_for(ev, "name") or _walk_for(ev, "event")
        if name == "tool_execution_start":
            tcid = _walk_for(ev, "toolCallId")
            rec = self.s["pending"].get(tcid) if isinstance(tcid, str) else None
            if rec is not None:
                rec["started"] = True
            else:
                self._fault("unknown_tool_result_ref")
            # never semantic progress: service event by contract
        self.s["counters"]["service_events"] += 1

    def _handle_branch(self, ev):
        kind = _walk_for(ev, "kind")
        if kind == "discarded-entry-branch":
            root = _walk_for(ev, "discardedEntryId") or _walk_for(ev, "entryId")
            if isinstance(root, str) and root:
                self._note_discarded_root(root)
            else:
                self._fault("branch_shape_unknown")
                self.s["uncertainty"]["unknown_seen"] = True
        else:
            self._fault("branch_shape_unknown")
            self.s["uncertainty"]["unknown_seen"] = True

    # ------------------------------------------------------------ read engine

    def _read_pass(self, f, now):
        """One bounded pass. Returns (eof, new_bytes, events, event_capped)."""
        lim, s = self.lim, self.s
        chunk_size = max(1, min(8192, lim["max_row_bytes"]))
        byte_budget = lim["max_read_bytes"]
        event_budget = lim["max_events_per_poll"]
        tail_start_len = len(self._tail)
        new_bytes = events = 0
        eof = event_capped = False
        while True:
            while True:  # consume complete lines currently buffered
                i = self._tail.find(b"\n")
                if s["skip_mode"]:
                    if i < 0:
                        self._tail = b""
                        break
                    self._tail = self._tail[i + 1:]
                    s["skip_mode"] = False
                    continue
                if i < 0:
                    break
                line, self._tail = self._tail[:i], self._tail[i + 1:]
                self._handle_line(line, now)
                events += 1
                if events >= event_budget:
                    event_capped = True
                    break
            if event_capped:
                break
            if (not s["skip_mode"] and b"\n" not in self._tail
                    and len(self._tail) > lim["max_row_bytes"]):
                # unterminated row already oversized: drop it, never buffer it
                s["skip_mode"] = True
                self._tail = b""
                self._fault("oversized_row")
                continue
            if byte_budget <= 0:
                break
            chunk = f.read(min(chunk_size, byte_budget))
            if not chunk:
                eof = True
                break
            byte_budget -= len(chunk)
            new_bytes += len(chunk)
            self._tail += chunk
        # offset advances only past fully consumed/skipped bytes; the
        # retained tail (partial line or event-capped leftover) stays excluded
        s["offset"] += tail_start_len + new_bytes - len(self._tail)
        return eof, new_bytes, events, event_capped

    def _begin_rescan(self, reason):
        keep = {
            "prev_header_id": self.s["prev_header_id"],
            "observation": self.s["observation"],
            "faults_recent": self.s["faults_recent"],
            "generations": self.s["generations"],
        }
        self._reset()
        self._tail = b""
        self.s.update(keep)
        self.s["generations"] += 1
        self._rebuilt = reason

    # ------------------------------------------------------------------- poll

    def poll(self, path):
        """One bounded incremental poll. Never rescans except after rebuild."""
        now = self.clock()
        s = self.s
        self._new_faults = {}
        self._switched = False
        self._rebuilt = None
        s["observation"]["last_poll_at"] = now
        s["observation"]["polls"] += 1
        try:
            f = open(path, "rb")
        except FileNotFoundError:
            self._fault("input_missing")
            return self._report("fault", None, 0, 0, False, False)
        except OSError:
            self._fault("input_unreadable")
            return self._report("fault", None, 0, 0, False, False)
        with f:
            try:
                fst = os.fstat(f.fileno())
            except OSError:
                self._fault("input_unreadable")
                return self._report("fault", None, 0, 0, False, False)
            if not stat.S_ISREG(fst.st_mode):
                self._fault("input_not_regular")
                return self._report("fault", None, 0, 0, False, False)
            size = fst.st_size
            fkey = {"dev": fst.st_dev, "ino": fst.st_ino}
            if s["file"] is not None:
                if s["file"] != fkey:
                    self._begin_rescan("rotation")
                    s = self.s  # _reset() swapped the state dict
                elif size < s["offset"] + len(self._tail):
                    self._begin_rescan("truncation")
                    s = self.s
            s["file"] = fkey
            try:
                f.seek(s["offset"] + len(self._tail))
            except OSError:
                self._fault("input_unreadable")
                return self._report("fault", None, 0, 0, False, False)
            history = s["bootstrap_pending"]
            eof, new_bytes, events, _capped = self._read_pass(f, now)
            if new_bytes > 0:
                s["observation"]["last_append_at"] = now
            # ground truth from fstat: anything past cursor+tail is unread;
            # complete rows still parked in the tail are also outstanding
            remaining = max(0, size - s["offset"] - len(self._tail))
            backlog = remaining > 0 or b"\n" in self._tail
            if not backlog:
                s["bootstrap_pending"] = False
            status = ("fault" if self._new_faults
                      else "backlog" if backlog else "ok")
            return self._report(status, size, new_bytes, events, backlog,
                                history)

    def _report(self, status, size, new_bytes, events, backlog, history):
        s = self.s
        info = dict(s["file"], size=size) if (s["file"] and size is not None) else None
        backlog_bytes = None
        if size is not None:
            backlog_bytes = max(0, size - s["offset"] - len(self._tail))
        return {
            "status": status,
            "at": s["observation"]["last_poll_at"],
            "poll_index": s["observation"]["polls"],
            "file": info,
            "offset": s["offset"],
            "tail_bytes": len(self._tail),
            "rebuilt": self._rebuilt,
            "session_switch": self._switched,
            "bootstrap_pending": s["bootstrap_pending"],
            "history_replayed": bool(history and (new_bytes or events)),
            "new_bytes": new_bytes,
            "events_processed": events,
            "backlog": backlog,
            "backlog_bytes": backlog_bytes,
            "new_faults": dict(self._new_faults),
            "summary": self.snapshot(),
        }
