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

`report` (dict): status in {"ok","backlog","fault","unknown"}; `backlog` bool;
backlog_bytes; new_bytes; events_processed; rebuilt reason or None;
session_switch; bootstrap_pending; history_replayed; new_faults (kind->count);
summary == snapshot() at poll end.  Any new fault-class observation
(missing/unreadable input, malformed/oversized rows, unknown header/version,
unknown event type or critical shape) yields status "fault": unknown is
observable, never healthy.  Once a critical gap is latched for this file
generation (oversized/malformed skipped record, or a parent that cannot be
resolved), otherwise-healthy polls report status "unknown" — never a plain
"ok" — until an explicit rebuild (rotation/truncation) starts a new
generation.

Persistence (state format 2): state carries file identity (st_dev/st_ino) +
session header UUID + the consumed binary offset and bounded structural
metadata.  Raw line tails are NEVER persisted in any encoding — the offset
already excludes the incomplete trailing row, which is re-read from the
file after reload.  Older formats are refused with an explicit
incompatibility error (no silent reset).  Polls never rescan the whole
file except after a rebuild trigger (identity change = rotation/session
switch, or same-file truncation size < offset), which is reported as
`rebuilt` and marks re-derived progress as historical (`live: false`),
never as freshly observed success.

Active-branch semantics: the adapter tracks the current active chain
explicitly (head = latest entry; linear appends extend it, any other
parent recomputes the chain from the new entry).  Only entries reachable
from the current head count as live.  Siblings that leave the head's
ancestry — branch switches, tree navigation, discarded branches — have
their last_success / last_tool / pending projections retracted; there is
no passive all-nondiscarded-siblings-are-active fallback.  A row replayed
under a discarded root never becomes the active head.  The retained chain
is bounded by entries_cap (default 4096, far above observed real session
depths of ~300) with cycle detection; ancestry beyond the retained bound
is explicitly "uncertain" (documented unknown), never guessed live.

Sanitization: retained state/output contain only structural metadata —
entry/toolCall IDs, allowlisted tool names (unknown names irreversibly
hashed), roles, stopReason, errorId, irreversible errorMessage fingerprints,
timestamps, counters.  No raw tool arguments, message content, thoughts,
error text, or cwd.

Semantics exposed (snapshot): last successful assistant event
(stopReason in {stop, toolUse} AND no errorId, live branch only, valid ts),
last completed tool result (isError true => error observation; false =>
clean completion; missing/wrong-typed => explicitly unknown, NEVER a
success signal), pending tools (kind "ask_waiting" vs "running"), error
totals / consecutive failure streak / bounded recent-error ring, session +
observation faults, uncertainty flags.  Non-message/service events
(model_usage, title, model_change, compaction, custom, envelopeless title
rows) never create semantic task progress.  stopReason "error" (with
errorId/errorMessage) and "aborted" are explicit failures; toolCalls on a
failed/aborted assistant never register pendings (no eternally running
tasks).  A success on a branch later discarded or switched away from is
retracted.

Timestamp contract: a success with a malformed or future timestamp NEVER
updates last_success (observable only via counters.success_invalid_ts and
an invalid_timestamp fault).  The occurrence timestamp from the log is
recorded for age computation, but freshness of the step clock comes ONLY
from poll-time observation.last_append_at, which is refreshed exclusively
by newly appended bytes — never by replayed history.  A historical
successful event remains valid past evidence (last_success, live:false
during bootstrap replay); it is not "freshly completed now".

Watcher status contract: poll() "status" reflects THIS poll only —
"fault" means at least one new fault-class observation occurred during
this poll (see new_faults); it does not mean the session is permanently
broken.  Persistent uncertainty (unknown shapes seen, ancestry beyond the
retained bound, evictions, pending overflow) lives in
summary.uncertainty / summary.faults and survives across polls.  A
watcher should alert on persistent uncertainty/uncertain ancestry and on
repeated fault polls, and treat a lone fault poll followed by "ok" as a
recovered transient.

Fail-safe decisions (conservative, documented): ancestry that cannot be
resolved within the bounded retained chain counts as uncertain and does
NOT count as success — a parent missing from the retained map is never
treated as a provable root, and a truncated or evicted chain is explicitly
uncertain, never live; assistant messages without a recognizable
stopReason are "other" (neither success nor failure, unknown-flagged);
unsupported session version poisons the scan (lines keep being consumed
for cursor health, but no semantics); dedupe/branch structures are bounded
and eviction raises an uncertainty flag rather than guessing.  Rows above
max_row_bytes (default 2 MiB — observed real rows reach ~150 KB) fail
closed: the payload is never parsed, sniffed, or persisted; the skipped
record latches a critical-gap uncertainty that persists for the rest of
this file generation — later valid rows never "repair" the unknown branch,
and subsequent empty polls report "unknown", not healthy.  A row whose
parentId is absent (root row, e.g. session headers) still roots normally.
Deeply nested rows that trip RecursionError count as malformed (also
latching the gap), never crash a poll.

OMP v3 shape assumptions, verified against real session logs: the first
row may be an envelopeless title row {"pad","title","type","updatedAt","v"};
session headers may omit parentId (absent == root); custom rows carry
customType + data (tool_execution_start -> data.toolCallId; session_exit);
branch_summary nesting remains tolerant over a small set of candidate
locations; unrecognized shapes surface as unknown, not silence.
"""

from __future__ import annotations

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
    # Documented non-progress service rows (observed in real OMP v3 logs:
    # model_change; title/compaction/model_usage per peer inspection;
    # thinking_level_change/service_tier_change per OMP settings events).
    "model_usage", "title", "title_change", "compaction",
    "model-change", "model_change",
    "thinking_level_change", "service_tier_change",
}
# Service rows OMP writes WITHOUT the id/parentId/timestamp envelope —
# observed: the leading title row {"pad","title","type","updatedAt","v"}.
ENVELOPELESS_SERVICE_TYPES = {"title", "title_change"}
NON_PROGRESS_ROLES = {"user", "system", "developer", "tool", "summary"}
ASK_TOOL_NAMES = {
    "ask", "ask_user", "askuser", "ask_user_question",
    "user_prompt", "prompt_user", "interrogate_user",
}
_SAFE_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.\-]{0,63}$")
_SAFE_SMALL = re.compile(r"^[A-Za-z0-9_.\-]{1,64}$")
# real OMP toolCallIds are 62-char "call_…|…" strings — '|' included
_SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.\-|]{0,127}$")

DEFAULT_LIMITS = {
    "max_read_bytes": 4 << 20,   # bytes read per poll
    "max_row_bytes": 2 << 20,    # any single JSONL row larger than this -> skip
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

_TSTATE_VERSION = 2

# (No envelope sniff for oversized rows: deliberately removed.  A skipped
# oversized/malformed record latches a critical ancestry gap — fail closed —
# instead of regex-recovering ids from an unparsed payload.)


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
        # runtime-only active chain (root..head); rebuilt from persisted
        # "head" + "entries" on load — never exported separately
        self._chain = []
        self._active_set = set()
        self._chain_truncated = False        # walk hit bound/missing/cycle
        self._chain_under_discarded = False  # chain tops a discarded root
        self.s = {
            "format": _TSTATE_VERSION,
            "session": None,            # {"header_id","version"} once header seen
            "session_fault": None,      # e.g. "unsupported_version"
            "file": None,               # {"dev","ino"}
            "offset": 0,                # consumed bytes (fully processed/skipped)
            "skip_mode": False,         # dropping bytes until next newline
            "bootstrap_pending": True,  # still scanning history this generation
            "generations": 0,
            "prev_header_id": None,
            "seen": [],                 # bounded dedupe ids (order = FIFO)
            "entries": {},              # bounded id -> parent
            "head": None,               # tip of the current active chain
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
                "pending_retracted": 0, "success_invalid_ts": 0,
            },
            "faults": {},               # kind -> cumulative count
            "faults_recent": [],        # bounded [{"kind","at"}]
            "uncertainty": {
                "dedupe_evicted": False, "entries_evicted": False,
                "ancestry_uncertain": 0, "pending_overflow": False,
                "unknown_seen": False, "ancestry_gap": False,
            },
            "observation": {"last_poll_at": None, "last_append_at": None, "polls": 0},
        }

    def export_state(self):
        """JSON-serializable persistent state (cursor + bounded metadata).

        Only the consumed offset is persisted — never raw line tails, in any
        encoding (partial_b64 from format 1 was reversible and is gone).
        The offset already excludes the unconsumed partial row, which is
        simply re-read from the file after reload.
        """
        return json.loads(json.dumps(self.s))  # detach + validate JSON-safety

    @classmethod
    def from_state(cls, state, clock=time.time, **limits):
        adapter = cls(clock=clock, **limits)
        adapter.load_state(state)
        return adapter

    def load_state(self, state):
        if not isinstance(state, dict):
            raise ValueError("incompatible state: not a dict")
        fmt = state.get("format")
        if fmt != _TSTATE_VERSION:
            raise ValueError(
                "incompatible state format %r (supported: %d); older formats "
                "may retain unsanitized raw line tails and are refused — "
                "discard and rescan from scratch" % (fmt, _TSTATE_VERSION))
        self._reset()
        self.s.update(self._validated_state(state))
        self._seen_set = set(self.s["seen"])
        self._tail = b""  # partial row re-read from the persisted offset
        self._rebuild_chain()

    def _validated_state(self, state):
        """Whitelist + type/bounds validation; corrupt state -> ValueError.

        Only known keys are retained — arbitrary loaded keys never survive.
        """
        def bad(msg):
            raise ValueError("corrupt state: " + msg)

        def is_num(x):
            return isinstance(x, (int, float)) and not isinstance(x, bool)

        def opt_str(v, what):
            if v is not None and not isinstance(v, str):
                bad("%s must be str|None" % what)
            return v

        def str_list(v, cap, what):
            if (not isinstance(v, list) or len(v) > cap
                    or not all(isinstance(x, str) for x in v)):
                bad("%s must be a list of <=%d str" % (what, cap))
            return list(v)

        def int_map(v, what, keys=None):
            if not isinstance(v, dict):
                bad("%s must be a dict" % what)
            for k, n in v.items():
                if not isinstance(k, str) or keys and k not in keys:
                    bad("%s: unknown key %r" % (what, k))
                if not isinstance(n, int) or isinstance(n, bool) or n < 0:
                    bad("%s[%r] must be a non-negative int" % (what, k))
            return dict(v)

        lim = self.lim
        out = {"format": _TSTATE_VERSION}
        sess = state.get("session")
        if sess is not None:
            if (not isinstance(sess, dict)
                    or not isinstance(sess.get("header_id"), str)
                    or not isinstance(sess.get("version"), int)):
                bad("session shape")
            out["session"] = {"header_id": sess["header_id"],
                              "version": sess["version"]}
        else:
            out["session"] = None
        out["session_fault"] = opt_str(state.get("session_fault"),
                                       "session_fault")
        f = state.get("file")
        if f is not None:
            if (not isinstance(f, dict)
                    or not isinstance(f.get("dev"), int)
                    or not isinstance(f.get("ino"), int)):
                bad("file identity shape")
            out["file"] = {"dev": f["dev"], "ino": f["ino"]}
        else:
            out["file"] = None
        off = state.get("offset")
        if not isinstance(off, int) or isinstance(off, bool) or off < 0:
            bad("offset must be a non-negative int")
        out["offset"] = off
        for flag in ("skip_mode", "bootstrap_pending"):
            if not isinstance(state.get(flag), bool):
                bad("%s must be bool" % flag)
            out[flag] = state[flag]
        gen = state.get("generations")
        if not isinstance(gen, int) or isinstance(gen, bool) or gen < 0:
            bad("generations must be a non-negative int")
        out["generations"] = gen
        out["prev_header_id"] = opt_str(state.get("prev_header_id"),
                                        "prev_header_id")
        out["seen"] = str_list(state.get("seen", []), lim["seen_cap"], "seen")
        entries = state.get("entries")
        if (not isinstance(entries, dict) or len(entries) > lim["entries_cap"]
                or not all(isinstance(k, str) for k in entries)
                or not all(v is None or isinstance(v, str)
                           for v in entries.values())):
            bad("entries must be a <=%d dict of str->str|None"
                % lim["entries_cap"])
        out["entries"] = dict(entries)
        out["head"] = opt_str(state.get("head"), "head")
        out["discarded"] = str_list(state.get("discarded", []),
                                    lim["discarded_cap"], "discarded")

        def success_rec(r, what):
            if not isinstance(r, dict):
                bad(what + " shape")
            if (not isinstance(r.get("entry_id"), str)
                    or not (r.get("ts") is None or is_num(r.get("ts")))
                    or not isinstance(r.get("ts_valid"), bool)
                    or not (r.get("stop_reason") is None
                            or isinstance(r.get("stop_reason"), str))
                    or not isinstance(r.get("live"), bool)):
                bad(what + " fields")
            return {"entry_id": r["entry_id"], "ts": r.get("ts"),
                    "ts_valid": r["ts_valid"],
                    "stop_reason": r.get("stop_reason"),
                    "live": r["live"]}

        ls = state.get("last_success")
        out["last_success"] = (success_rec(ls, "last_success")
                               if ls is not None else None)
        ring = state.get("success_ring", [])
        if not isinstance(ring, list) or len(ring) > lim["success_ring"]:
            bad("success_ring bound")
        out["success_ring"] = [success_rec(r, "success_ring") for r in ring]

        def tool_rec(r, what):
            if not isinstance(r, dict):
                bad(what + " shape")
            if (not isinstance(r.get("tool_call_id"), str)
                    or not isinstance(r.get("name"), str)
                    or r.get("name_class") not in ("ask", "tool", "unknown")
                    or not isinstance(r.get("is_error"), (bool, type(None)))
                    or not (r.get("ts") is None or is_num(r.get("ts")))
                    or not isinstance(r.get("ts_valid"), bool)
                    or not isinstance(r.get("entry_id"), str)):
                bad(what + " fields")
            return {"tool_call_id": r["tool_call_id"], "name": r["name"],
                    "name_class": r["name_class"],
                    "is_error": r.get("is_error"), "ts": r.get("ts"),
                    "ts_valid": r["ts_valid"], "entry_id": r["entry_id"]}

        lt = state.get("last_tool")
        out["last_tool"] = tool_rec(lt, "last_tool") if lt is not None else None
        pending = state.get("pending")
        if (not isinstance(pending, dict) or len(pending) > lim["pending_cap"]
                or not all(isinstance(k, str) for k in pending)):
            bad("pending bound")
        out_pending = {}
        for k, r in pending.items():
            rec = tool_rec(r, "pending")
            if rec["tool_call_id"] != k:
                bad("pending key mismatch")
            if (rec.pop("is_error") is not None
                    or not isinstance(r.get("started"), bool)
                    or r.get("kind") not in ("ask_waiting", "running")):
                bad("pending fields")
            rec["kind"] = r["kind"]
            rec["started"] = r["started"]
            out_pending[k] = rec
        out["pending"] = out_pending
        cf = state.get("consecutive_failures")
        if not isinstance(cf, int) or isinstance(cf, bool) or cf < 0:
            bad("consecutive_failures must be a non-negative int")
        out["consecutive_failures"] = cf
        out["error_totals"] = int_map(
            state.get("error_totals", {}), "error_totals",
            keys={"assistant_error", "assistant_aborted", "tool_error"})
        re_ring = state.get("recent_errors", [])
        if not isinstance(re_ring, list) or len(re_ring) > lim["recent_errors"]:
            bad("recent_errors bound")
        for r in re_ring:
            if (not isinstance(r, dict)
                    or not isinstance(r.get("category"), str)
                    or not (r.get("error_id") is None
                            or isinstance(r.get("error_id"), (str, int)))
                    or not (r.get("fingerprint") is None
                            or isinstance(r.get("fingerprint"), str))
                    or not (r.get("ts") is None or is_num(r.get("ts")))
                    or not isinstance(r.get("ts_valid"), bool)):
                bad("recent_errors fields")
        out["recent_errors"] = [dict(r) for r in re_ring]
        out["counters"] = int_map(state.get("counters", {}), "counters",
                                  keys=set(self.s["counters"]))
        out["faults"] = int_map(state.get("faults", {}), "faults")
        fr = state.get("faults_recent", [])
        if not isinstance(fr, list) or len(fr) > lim["recent_errors"]:
            bad("faults_recent bound")
        for r in fr:
            if (not isinstance(r, dict) or not isinstance(r.get("kind"), str)
                    or not (r.get("at") is None or is_num(r.get("at")))):
                bad("faults_recent fields")
        out["faults_recent"] = [dict(r) for r in fr]
        unc = state.get("uncertainty")
        if not isinstance(unc, dict):
            bad("uncertainty shape")
        out["uncertainty"] = {}
        for k, default in self.s["uncertainty"].items():
            v = unc.get(k, default)
            if isinstance(default, bool):
                if not isinstance(v, bool):
                    bad("uncertainty.%s must be bool" % k)
            elif not isinstance(v, int) or isinstance(v, bool) or v < 0:
                bad("uncertainty.%s must be a non-negative int" % k)
            out["uncertainty"][k] = v
        obs = state.get("observation")
        if (not isinstance(obs, dict)
                or not (obs.get("last_poll_at") is None
                        or is_num(obs.get("last_poll_at")))
                or not (obs.get("last_append_at") is None
                        or is_num(obs.get("last_append_at")))
                or not isinstance(obs.get("polls"), int)
                or isinstance(obs.get("polls"), bool) or obs.get("polls") < 0):
            bad("observation shape")
        out["observation"] = {"last_poll_at": obs.get("last_poll_at"),
                              "last_append_at": obs.get("last_append_at"),
                              "polls": obs["polls"]}
        return out

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

    # ------------------------------------------------------- active chain

    def _latch_gap(self):
        """Latch a critical ancestry gap for this file generation.

        Fail closed: an oversized/malformed skipped record or an
        unresolvable parent affinity keeps the adapter explicitly unknown
        (never a healthy "ok") until a rebuild starts a new generation.
        """
        u = self.s["uncertainty"]
        u["ancestry_gap"] = True
        u["unknown_seen"] = True

    _MISSING = object()

    def _walk_back(self, start):
        """Walk parent links from `start`.

        Returns (chain, truncated, under_discarded) with chain in root..start
        order.  Bounded by entries_cap with cycle detection; a discarded
        ancestor or an evicted/unknown ancestor truncates the walk — history
        beyond the retained bound is explicitly unknown, never guessed.
        """
        entries = self.s["entries"]
        discarded = set(self.s["discarded"])
        chain, visited = [], set()
        truncated = under_discarded = False
        cur = start
        while cur is not None:
            if cur in visited:
                self._fault("ancestry_cycle")
                truncated = True
                self._latch_gap()
                break
            if cur in discarded:
                under_discarded = True
                break
            visited.add(cur)
            chain.append(cur)
            if len(chain) >= self.lim["entries_cap"]:
                truncated = True
                break
            parent = entries.get(cur, self._MISSING)
            if parent is self._MISSING:
                # a missing parent is NOT a provable root: the walk (and
                # everything hanging under it) is explicitly unknown
                truncated = True
                self._latch_gap()
                break
            cur = parent
        chain.reverse()
        return chain, truncated, under_discarded

    def _set_chain(self, chain, truncated, under_discarded):
        self._chain = chain
        self._active_set = set(chain)
        self._chain_truncated = truncated
        self._chain_under_discarded = under_discarded
        self.s["head"] = chain[-1] if chain else None

    def _rebuild_chain(self):
        """Derive the runtime chain from persisted head + entries (load)."""
        head = self.s["head"]
        if head is None or head not in self.s["entries"]:
            self._set_chain([], False, False)
            return
        self._set_chain(*self._walk_back(head))

    def _advance_head(self, entry_id, parent):
        """Track the current active branch as entries stream in.

        Linear appends (parent == head) are O(1); any other parent means a
        branch switch / tree navigation and the chain is recomputed from the
        new entry.  Siblings that leave the current head's ancestry are
        retracted — there is no passive all-nondiscarded-is-active fallback.
        """
        if entry_id in self._active_set:
            return
        if parent is None:  # new root
            if entry_id not in set(self.s["discarded"]):
                self._set_chain([entry_id], False, False)
                self._retract_offbranch()
            return
        if self._chain and parent == self._chain[-1]:
            self._chain.append(entry_id)
            self._active_set.add(entry_id)
            self.s["head"] = entry_id
            if len(self._chain) > self.lim["entries_cap"]:
                self._active_set.discard(self._chain.pop(0))
                self._chain_truncated = True
                self._retract_offbranch()
            return
        chain, truncated, under_discarded = self._walk_back(entry_id)
        if under_discarded:
            # a row replayed under a discarded branch never becomes the
            # active head (and never retracts the legitimate chain)
            return
        self._set_chain(chain, truncated, under_discarded)
        self._retract_offbranch()

    def _chain_state(self, entry_id):
        """Return "live" | "retired" | "uncertain" for an entry.

        live      — on the current active chain (reachable from head);
        retired   — known sibling/discarded branch no longer on the active
                    head (definitely not live);
        uncertain — on a chain whose walk truncated (missing parent, cycle,
                    or bounded eviction), or an unknown id: explicitly
                    unknown, documented, never live.
        """
        if entry_id in self._active_set:
            if self._chain_under_discarded:
                return "retired"
            if self._chain_truncated:
                return "uncertain"
            return "live"
        if entry_id in self.s["entries"] and not self._chain_truncated:
            return "retired"
        return "uncertain"

    def _retract_offbranch(self):
        """Drop successes/pending/last_tool no longer on the active chain."""
        s = self.s
        ring = s["success_ring"]
        kept = [r for r in ring if r["entry_id"] in self._active_set]
        retracted = len(ring) - len(kept)
        if retracted:
            s["success_ring"] = kept
            c = s["counters"]
            c["successful_assistant"] = max(
                0, c["successful_assistant"] - retracted)
            c["discarded_success_retracted"] += retracted
            s["last_success"] = dict(kept[-1]) if kept else None
        pending = s["pending"]
        dead = [k for k, v in pending.items()
                if v["entry_id"] not in self._active_set]
        for k in dead:
            del pending[k]
        if dead:
            s["counters"]["pending_retracted"] += len(dead)
        lt = s["last_tool"]
        if lt is not None and lt.get("entry_id") not in self._active_set:
            s["last_tool"] = None

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

    def _note_discarded_root(self, root_id):
        d = self.s["discarded"]
        if root_id not in d:
            d.append(root_id)
            if len(d) > self.lim["discarded_cap"]:
                del d[: len(d) - self.lim["discarded_cap"]]
                self.s["uncertainty"]["entries_evicted"] = True
        # if the discarded root sits on the active chain, truncate the chain
        # at its parent: everything from the root to the old head is dead
        if root_id in self._active_set:
            idx = self._chain.index(root_id)
            self._set_chain(self._chain[:idx], self._chain_truncated, False)
        self._retract_offbranch()

    def _note_error(self, category, error_id, fingerprint, ts, ts_valid):
        s = self.s
        s["error_totals"][category] = s["error_totals"].get(category, 0) + 1
        s["consecutive_failures"] += 1
        safe_id = error_id
        if isinstance(safe_id, (dict, list)):
            # structured errorId could carry raw secrets: type fingerprint only
            safe_id = "id:" + _fp(type(safe_id).__name__)
        elif isinstance(safe_id, str) and not _SAFE_SMALL.match(safe_id):
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
            # genuinely larger than the bound: fail closed — payload never
            # parsed, sniffed, or persisted; the skipped record latches a
            # critical ancestry gap for this file generation
            self._fault("oversized_row")
            self._latch_gap()
            return
        try:
            ev = json.loads(line.decode("utf-8"))
        except (ValueError, UnicodeDecodeError, RecursionError):
            self._fault("malformed_row")
            self._latch_gap()
            return
        if not isinstance(ev, dict):
            self._fault("malformed_row")
            self._latch_gap()
            return
        etype = ev.get("type")
        if (etype in ENVELOPELESS_SERVICE_TYPES
                and "id" not in ev and "parentId" not in ev):
            # Known envelopeless service metadata (e.g. the leading title
            # row): non-progress, no fault, not deduped/chained (no id).
            self.s["counters"]["service_events"] += 1
            return
        entry_id, raw_ts = ev.get("id"), ev.get("timestamp")
        if (not isinstance(entry_id, str) or not _SAFE_ID.match(entry_id)
                or not isinstance(etype, str) or not etype):
            self._fault("unknown_shape")
            return
        # absent parentId == root row (real OMP session headers omit it)
        parent = ev.get("parentId")
        if parent is not None and not _SAFE_ID.match(parent):
            self._fault("unknown_shape")
            parent = None
        ts, ts_valid, why = _parse_ts(raw_ts, now, self.lim["allowed_skew"])
        if not ts_valid:
            self._fault("invalid_timestamp")
        if not self._note_seen(entry_id):
            self.s["counters"]["duplicates"] += 1
            return
        self._note_entry(entry_id, parent)
        self._advance_head(entry_id, parent)
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
            self._handle_tool_result(msg, entry_id, ts, ts_valid)
        elif role in NON_PROGRESS_ROLES:
            s["counters"]["service_events"] += 1  # user/system/etc: no progress
        else:
            self._fault("unknown_shape")
            self.s["uncertainty"]["unknown_seen"] = True

    def _handle_assistant(self, msg, entry_id, ts, ts_valid):
        s = self.s
        stop, err_id = msg.get("stopReason"), msg.get("errorId")
        err_msg = msg.get("errorMessage")
        # toolCalls on a failed/aborted assistant never execute — registering
        # them would create eternally running pending tasks
        failed = err_id is not None or stop in ("error", "aborted")
        if not failed:
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
            state = self._chain_state(entry_id)
            if state == "retired":
                s["counters"]["discarded_branch_events"] += 1
            elif state == "uncertain":
                s["uncertainty"]["ancestry_uncertain"] += 1
                self._fault("ancestry_uncertain")
            elif not ts_valid:
                # invalid/future ts is never proof of the last successful
                # semantic event; observable only as a counter
                s["counters"]["success_invalid_ts"] += 1
                s["consecutive_failures"] = 0
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
        if not isinstance(tcid, str) or not _SAFE_ID.match(tcid):
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

    def _handle_tool_result(self, msg, entry_id, ts, ts_valid):
        s = self.s
        tcid = msg.get("toolCallId")
        if not isinstance(tcid, str) or not _SAFE_ID.match(tcid):
            self._fault("unknown_shape")
            return
        name_class, safe_name = _classify_tool_name(msg.get("toolName"))
        is_error = msg.get("isError")
        if not isinstance(is_error, bool):
            # missing/wrong-typed isError is explicitly UNKNOWN, never a
            # success signal for the watcher
            is_error = None
            self._fault("unknown_tool_result")
            s["uncertainty"]["unknown_seen"] = True
        rec = {
            "tool_call_id": tcid, "name": safe_name, "name_class": name_class,
            "is_error": is_error, "ts": ts, "ts_valid": ts_valid,
            "entry_id": entry_id,
        }
        s["last_tool"] = rec
        s["counters"]["tool_results"] += 1
        if s["pending"].pop(tcid, None) is None:
            self._fault("unknown_tool_result_ref")
        if is_error:
            s["counters"]["tool_results_error"] += 1
            self._note_error("tool_error", None, None, ts, ts_valid)

    def _handle_custom(self, ev):
        # Verified against real OMP v3 logs: custom rows carry `customType`
        # + `data` (tool_execution_start -> data.toolCallId; session_exit).
        # Strict match only — no guessed name-only fallbacks.
        if ev.get("customType") == "tool_execution_start":
            data = ev.get("data")
            tcid = data.get("toolCallId") if isinstance(data, dict) else None
            rec = self.s["pending"].get(tcid) if isinstance(tcid, str) else None
            if rec is not None:
                rec["started"] = True
            else:
                self._fault("unknown_tool_result_ref")
        # custom events (incl. session_exit / unknown customTypes) are
        # non-progress service metadata by contract
        self.s["counters"]["service_events"] += 1

    def _handle_branch(self, ev):
        kind = _walk_for(ev, "kind")
        if kind == "discarded-entry-branch":
            root = _walk_for(ev, "discardedEntryId") or _walk_for(ev, "entryId")
            if isinstance(root, str) and _SAFE_ID.match(root):
                self._note_discarded_root(root)
            else:
                # arbitrary/unsafe root text is never retained — not even
                # hashed into a fake valid root
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
                # unterminated row already oversized: drop it, never buffer
                # or persist any of its bytes; latch the critical gap
                s["skip_mode"] = True
                self._tail = b""
                self._fault("oversized_row")
                self._latch_gap()
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
                      else "backlog" if backlog
                      else "unknown" if s["uncertainty"]["ancestry_gap"]
                      else "ok")
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
