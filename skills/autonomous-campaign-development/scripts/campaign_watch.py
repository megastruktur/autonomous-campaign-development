#!/usr/bin/env python3
"""campaign_watch — read-only progress watchdog over omp_events adapter metadata.

CLI (all outputs one JSON line; errors -> {"v":1,"kind":"error","error":CODE},
exit 2, no tracebacks/paths/secrets):
  poll    --config PATH            one bounded sample, updates sidecars
  watch   --config PATH            poll loop: change lines + heartbeat (<=1024B)
  status  --config PATH [--task T] cached snapshot, stale check, ALWAYS <=1024B
  diagnose --config PATH [--task T] cached detail, <=4096B

Config (schema_version 1):
{"schema_version":1,"sidecar_dir":"/abs/.watch",
 "poll_seconds":30,"heartbeat_seconds":300,"stale_seconds":120,
 "no_step_seconds":600,"retry_window_seconds":600,"repeat_error_count":3,
 "tasks":[{"task":"t1","attempt":"a1","phase":"develop",
   "session_log":"/abs/f.jsonl","session_id":"uuid|null",
   "registered_at":"ISO UTC","candidate":"opaque|null",
   "checkpoint_files":[],"artifact_files":[],
   "tool_deadline_seconds":1800,
   "process":null|{"pid":int,"start_ticks":int,"boot_id":str}}]}
Intervals are positive floats <=86400 (fractional allowed). Max 64 tasks.
Error codes: config_unreadable, config_invalid, state_corrupt,
state_capacity, no_snapshot, config_changed, observer_locked,
sidecar_unmanaged, sidecar_refused, task_unknown, internal.

Sidecar files (only writes; NEVER session logs/sources/STATE/TODO/EVENTS):
  state.json    persistent baselines/adapter cursors/checkpoints (atomic,
                read AND write bounded by MAX_STATE_BYTES=32MiB; write
                breach -> state_capacity, old files untouched)
  snapshot.json last classified views + config digest (atomic, same bound)
  observer.lock fcntl flock single writer (poll/watch); status read-only
  .watch_managed ownership marker; a pre-existing sidecar dir holding
                anything but known managed files -> sidecar_unmanaged
Config inputs (config file, session_log, checkpoint/artifact allowlist)
must never alias managed outputs or live inside the sidecar dir; managed
outputs are never symlinks (no-follow open, symlink -> sidecar_refused).

Health: ok/degraded/suspect_stall/confirmed_retry_loop/unknown.
Activity: generating/tool_running/waiting_input/idle/exited/unknown.
Limitations: process identity only on Linux /proc (else unknown, never
exited); inaccessible /proc (EACCES/hidepid) -> unknown, ONLY ENOENT or
boot/ticks mismatch -> exited; a live PID alone never yields activity
"generating" (unknown without pending ask/running tool evidence);
confirmed_retry_loop needs >=repeat_error_count same NON-NULL assistant
error fingerprint after last useful step, EACH within the rolling retry
window (unrelated newer errors never freshen an old group); adapter
uncertainty flags hold health at unknown (adapter_uncertain) until actual
adapter recovery; tool completion is success ONLY when is_error IS false
(null/failed never refresh the step clock; successful current-branch
completions count as useful steps); checkpoint confirmation requires a
positively bound session id AND configured non-null candidate (else
unbound_identity), exact identity match, aware-UTC completed_at <= now
(no future grace) and >= registration baseline; checkpoint trust is
producer attestation (verified flag), not proof; artifact diffs are
candidate signals, never progress. Excess tasks, relative paths,
duplicate ids, unsafe values -> config_invalid (never silently ignored).
"""

from __future__ import annotations

import argparse
import errno
import fcntl
import hashlib
import json
import math
import os
import re
import signal
import stat
import sys
import time
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from omp_events import OmpSessionAdapter  # noqa: E402

STATUS_CAP = 1024          # status/heartbeat line incl newline, UTF-8 bytes
DIAG_CAP = 4096            # diagnose/poll line incl newline
MAX_TASKS = 64             # practical bound; state writes are byte-capped too
MAX_STATE_BYTES = 32 << 20  # state.json/snapshot.json read AND write bound
MAX_TASK_FILES = 64
MAX_PATH = 512
ARTIFACT_MAX_BYTES = 1 << 20
CHECKPOINT_MAX_BYTES = 1 << 16
JOURNAL_CAP = 256
REMOVED_CAP = 128
SKEW = 300.0
STATE_VERSION = 1
CHECKPOINT_KINDS = {"runtime_scenario", "review_checkpoint", "artifact_checkpoint"}
MARKER_NAME = ".watch_managed"
MARKER_CONTENT = "campaign_watch/1\n"
MANAGED_FILES = ("state.json", "snapshot.json", "observer.lock", MARKER_NAME)
PID_GONE = object()  # stat_reader result: pid confirmed absent (ENOENT)
_SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.\-]{0,127}$")
_SAFE_PHASE = re.compile(r"^[A-Za-z0-9_.\-]{1,64}$")
HEALTHS = ("ok", "degraded", "suspect_stall", "confirmed_retry_loop", "unknown")


class ConfigError(Exception):
    """Safe config/usage failure; str(self) is a stable public code."""


def _dumps(obj):
    return json.dumps(obj, separators=(",", ":"), sort_keys=True)


def _emit(obj):
    sys.stdout.write(_dumps(obj) + "\n")
    sys.stdout.flush()


def _fail(code):
    _emit({"v": 1, "kind": "error", "error": code})
    return 2


def _parse_iso(raw, now=None, allow_future=False):
    """ISO-8601 -> epoch float or None. Future rejected unless allowed."""
    if not isinstance(raw, str) or not raw:
        return None
    try:
        dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    ts = dt.timestamp()
    if ts < 0:
        return None
    if not allow_future and now is not None and ts > now + SKEW:
        return None
    return ts


def _iso(ts):
    if ts is None:
        return None
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()


def _atomic_write(path, text):
    """Atomic replace; refuses symlink/non-regular targets (no follow)."""
    if os.path.islink(path) or (os.path.lexists(path)
                                and not os.path.isfile(path)):
        raise ConfigError("sidecar_refused")
    tmp = path + ".tmp.%d" % os.getpid()
    flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC | getattr(os, "O_NOFOLLOW", 0)
    try:
        fd = os.open(tmp, flags, 0o600)
    except OSError as e:
        raise ConfigError("sidecar_refused" if e.errno == errno.ELOOP
                          else "internal")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(text)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def _read_json(path, cap):
    """Bounded JSON read of a REGULAR file (no symlinks); dict or None."""
    try:
        st = os.lstat(path)
        if not stat.S_ISREG(st.st_mode) or st.st_size > cap:
            return None
        with open(path, "r", encoding="utf-8") as f:
            raw = f.read(cap + 1)
        if len(raw.encode("utf-8")) > cap:  # actual bytes, not stat alone
            return None
        data = json.loads(raw)
        return data if isinstance(data, dict) else None
    except (OSError, ValueError):
        return None


def _num(cfg, key, lo, hi):
    v = cfg.get(key)
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        raise ConfigError("config_invalid")
    if not (lo < float(v) <= hi):
        raise ConfigError("config_invalid")
    return float(v)


def _file_list(raw, root):
    """Validated absolute file allowlist under campaign root (no symlinks)."""
    if raw is None:
        return []
    if not isinstance(raw, list) or len(raw) > MAX_TASK_FILES:
        raise ConfigError("config_invalid")
    out = []
    for p in raw:
        if (not isinstance(p, str) or len(p) > MAX_PATH
                or not os.path.isabs(p)):
            raise ConfigError("config_invalid")
        real = os.path.realpath(p)
        if real != os.path.abspath(p) or not real.startswith(root + os.sep):
            raise ConfigError("config_invalid")  # symlink/outside-scope
        out.append(real)
    return out


def _proc_spec(raw):
    if raw is None:
        return None
    if not isinstance(raw, dict):
        raise ConfigError("config_invalid")
    pid, ticks, boot = raw.get("pid"), raw.get("start_ticks"), raw.get("boot_id")
    if (isinstance(pid, bool) or not isinstance(pid, int) or pid <= 0
            or isinstance(ticks, bool) or not isinstance(ticks, int)
            or ticks < 0 or not isinstance(boot, str)
            or not _SAFE_ID.match(boot)):
        raise ConfigError("config_invalid")
    return {"pid": pid, "start_ticks": ticks, "boot_id": boot}


def load_config(path, now=None):
    """Strict-validated config; raises ConfigError('config_invalid')."""
    try:
        st = os.lstat(path)
        if not stat.S_ISREG(st.st_mode) or st.st_size > (1 << 20):
            raise ConfigError("config_unreadable")
        with open(path, "r", encoding="utf-8") as f:
            raw = f.read((1 << 20) + 1)
        if len(raw.encode("utf-8")) > (1 << 20):
            raise ConfigError("config_unreadable")
        cfg = json.loads(raw)
    except ConfigError:
        raise
    except (OSError, ValueError):
        raise ConfigError("config_unreadable")
    if not isinstance(cfg, dict) or cfg.get("schema_version") != 1:
        raise ConfigError("config_invalid")
    sidecar = cfg.get("sidecar_dir")
    if (not isinstance(sidecar, str) or len(sidecar) > MAX_PATH
            or not os.path.isabs(sidecar)):
        raise ConfigError("config_invalid")
    sidecar = os.path.realpath(sidecar)
    root = os.path.dirname(sidecar)  # campaign root: scope for allowlists
    out = {
        "sidecar_dir": sidecar, "root": root,
        "poll_seconds": _num(cfg, "poll_seconds", 0, 86400),
        "heartbeat_seconds": _num(cfg, "heartbeat_seconds", 0, 86400),
        "stale_seconds": _num(cfg, "stale_seconds", 0, 86400),
        "no_step_seconds": _num(cfg, "no_step_seconds", 0, 86400),
        "retry_window_seconds": _num(cfg, "retry_window_seconds", 0, 86400),
    }
    rec = cfg.get("repeat_error_count")
    if isinstance(rec, bool) or not isinstance(rec, int) or not 1 <= rec <= 100:
        raise ConfigError("config_invalid")
    out["repeat_error_count"] = rec
    tasks = cfg.get("tasks")
    if not isinstance(tasks, list) or not tasks or len(tasks) > MAX_TASKS:
        raise ConfigError("config_invalid")  # excess rejected, never ignored
    out["tasks"] = [_task_cfg(t, root, now) for t in tasks]
    ids = [t["task"] for t in out["tasks"]]
    if len(set(ids)) != len(ids):
        raise ConfigError("config_invalid")
    _alias_check(out, os.path.realpath(path))
    return out


def _alias_check(cfg, cfg_real):
    """Inputs/config must never alias managed outputs or the sidecar dir.

    All paths are already realpath-resolved, so symlinks cannot bypass.
    """
    sidecar = cfg["sidecar_dir"]
    managed = {os.path.join(sidecar, n) for n in MANAGED_FILES}

    def _bad(p):
        return p in managed or p == sidecar or p.startswith(sidecar + os.sep)

    if _bad(cfg_real):
        raise ConfigError("config_invalid")
    for t in cfg["tasks"]:
        paths = ([t["session_log"]] + t["checkpoint_files"]
                 + t["artifact_files"])
        if any(_bad(p) for p in paths):
            raise ConfigError("config_invalid")


def prepare_sidecar(cfg):
    """Create/validate sidecar BEFORE any lock/write.

    A pre-existing dir is managed iff it carries a valid ownership marker,
    or holds only known managed files (fresh/legacy sidecar). Anything else
    (e.g. sidecar_dir == campaign root with unmanaged files) is refused.
    """
    d = cfg["sidecar_dir"]
    os.makedirs(d, exist_ok=True)
    known = set(MANAGED_FILES)
    for name in MANAGED_FILES:
        if os.path.islink(os.path.join(d, name)):
            raise ConfigError("sidecar_refused")
    marker = os.path.join(d, MARKER_NAME)
    if os.path.lexists(marker):
        try:
            with open(marker, "r", encoding="utf-8") as f:
                ok = f.read(len(MARKER_CONTENT) + 1) == MARKER_CONTENT
        except OSError:
            ok = False
        if not ok or not os.path.isfile(marker):
            raise ConfigError("sidecar_unmanaged")
    else:
        extra = [e for e in os.listdir(d)
                 if e not in known
                 and e.split(".tmp.")[0] not in known]
        if extra:
            raise ConfigError("sidecar_unmanaged")
        _atomic_write(marker, MARKER_CONTENT)


def _task_cfg(raw, root, now):
    if not isinstance(raw, dict):
        raise ConfigError("config_invalid")
    tid, att = raw.get("task"), raw.get("attempt")
    if (not isinstance(tid, str) or not _SAFE_ID.match(tid)
            or not isinstance(att, str) or not _SAFE_ID.match(att)):
        raise ConfigError("config_invalid")
    phase = raw.get("phase")
    if phase is not None and (not isinstance(phase, str)
                              or not _SAFE_PHASE.match(phase)):
        raise ConfigError("config_invalid")
    log = raw.get("session_log")
    if (not isinstance(log, str) or len(log) > MAX_PATH
            or not os.path.isabs(log)):
        raise ConfigError("config_invalid")
    sid = raw.get("session_id")
    if sid is not None and (not isinstance(sid, str) or not _SAFE_ID.match(sid)):
        raise ConfigError("config_invalid")
    cand = raw.get("candidate")
    if cand is not None and (not isinstance(cand, str) or len(cand) > 256):
        raise ConfigError("config_invalid")
    reg = _parse_iso(raw.get("registered_at"), now, allow_future=False)
    if reg is None:
        raise ConfigError("config_invalid")
    return {
        "task": tid, "attempt": att, "phase": phase,
        "session_log": os.path.realpath(log), "session_id": sid,
        "registered_at": reg, "candidate": cand,
        "checkpoint_files": _file_list(raw.get("checkpoint_files"), root),
        "artifact_files": _file_list(raw.get("artifact_files"), root),
        "tool_deadline_seconds": _num(raw, "tool_deadline_seconds", 0, 604800),
        "process": _proc_spec(raw.get("process")),
    }


def _read_boot_id():
    try:
        with open("/proc/sys/kernel/random/boot_id", "r") as f:
            return f.read().strip()
    except OSError:
        return None


def _read_starttime(pid):
    """/proc/<pid>/stat starttime (field 22), PID_GONE if absent, else None.

    None means INACCESSIBLE (EACCES/hidepid/malformed) -> never `exited`.
    """
    try:
        with open("/proc/%d/stat" % pid, "r") as f:
            data = f.read()
        rest = data[data.rindex(")") + 2:].split()
        return int(rest[19])
    except FileNotFoundError:
        return PID_GONE
    except (OSError, ValueError, IndexError):
        return None


def process_verdict(spec, boot_reader=_read_boot_id,
                    stat_reader=_read_starttime, platform=sys.platform):
    """alive|exited|unknown. Unknown on unsupported platform/inaccessible.

    `exited` requires positive evidence: boot_id mismatch (recorded identity
    predates this boot), stat_reader returning PID_GONE (ENOENT), or a
    readable stat whose starttime differs (PID reuse). None from stat_reader
    (inaccessible) is ALWAYS unknown. Boot/ticks evidence assumes the
    recorded identity shares this PID namespace; generation cannot be
    proven from `alive`, only matched.
    """
    if spec is None:
        return None
    if not platform.startswith("linux"):
        return "unknown"
    boot = boot_reader()
    if boot is None:
        return "unknown"
    if boot != spec["boot_id"]:
        return "exited"  # recorded identity predates current boot
    try:
        ticks = stat_reader(spec["pid"])
    except OSError:
        return "unknown"  # inaccessible: EACCES/hidepid, never exited
    if ticks is None:
        return "unknown"
    if ticks is PID_GONE:
        return "exited"  # pid confirmed absent
    return "alive" if ticks == spec["start_ticks"] else "exited"  # reuse


def _hash_file(path):
    """sha256+size for a bounded REGULAR artifact, or None (unverifiable)."""
    try:
        st = os.lstat(path)
        if not stat.S_ISREG(st.st_mode) or st.st_size > ARTIFACT_MAX_BYTES:
            return None
        h = hashlib.sha256()
        total = 0
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                total += len(chunk)
                if total > ARTIFACT_MAX_BYTES:  # actual bytes, not stat alone
                    return None
                h.update(chunk)
        return {"sha256": h.hexdigest(), "size": total}
    except OSError:
        return None


def artifact_signals(files, prev):
    """Return ({path: sig}, changed_basenames, unverifiable_basenames)."""
    sigs, changed, bad = {}, [], []
    for p in files:
        sig = _hash_file(p)
        if sig is None:
            bad.append(os.path.basename(p))
            continue
        sigs[p] = sig
        if prev.get(p) != sig:
            changed.append(os.path.basename(p))
    return sigs, sorted(changed), sorted(bad)


def _parse_iso_strict(raw, now):
    """Aware-UTC ISO-8601 -> epoch, or None. Naive/future rejected (no grace)."""
    if not isinstance(raw, str) or not raw:
        return None
    try:
        dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return None
    if dt.tzinfo is None:
        return None  # naive timestamps are not acceptable progress evidence
    ts = dt.timestamp()
    if ts < 0 or ts > now:
        return None  # strict: no future grace for progress
    return ts


def read_checkpoint(path, tcfg, bound_session, confirmed, now, baseline=None):
    """Validate semantic checkpoint file.

    Returns (record|None, reason). Confirmation REQUIRES a positively bound
    session id AND a configured non-null candidate; until both exist the
    verdict is `unbound_identity` (never a skipped/existence check). Identity
    comparisons are exact. `completed_at` must be aware UTC, <= now (no
    future grace), and not older than the registration baseline.
    """
    data = _read_json(path, CHECKPOINT_MAX_BYTES)
    if data is None:
        return None, "unreadable"
    if data.get("schema_version") != 1:
        return None, "shape"
    if data.get("task") != tcfg["task"] or data.get("attempt") != tcfg["attempt"]:
        return None, "mismatch"
    if not bound_session or tcfg["candidate"] is None:
        return None, "unbound_identity"
    if (data.get("session_id") != bound_session
            or data.get("candidate") != tcfg["candidate"]):
        return None, "mismatch"
    cid, kind = data.get("checkpoint_id"), data.get("kind")
    if (not isinstance(cid, str) or not _SAFE_ID.match(cid)
            or kind not in CHECKPOINT_KINDS or data.get("verified") is not True):
        return None, "shape"
    ts = _parse_iso_strict(data.get("completed_at"), now)
    if ts is None:
        return None, "timestamp"  # malformed, naive, or future
    floor = baseline if baseline is not None else tcfg["registered_at"]
    if ts < floor:
        return None, "timestamp"  # predates registration: not this attempt
    if confirmed and (cid == confirmed["checkpoint_id"]
                      or ts <= confirmed["completed_at"]):
        return None, "replay"  # never count repeats/touches as new
    return {"checkpoint_id": cid, "completed_at": ts, "kind": kind,
            "task": tcfg["task"], "attempt": tcfg["attempt"],
            "session_id": bound_session,
            "candidate": tcfg["candidate"]}, ""


def _valid_ts(rec, now):
    """Finite event ts <= now from a ts_valid record, else None (fail closed).

    Independent of the adapter's own ts_valid verdict: unexpected types,
    non-finite, or future values never count as progress.
    """
    if not rec or not rec.get("ts_valid"):
        return None
    ts = rec.get("ts")
    if isinstance(ts, bool) or not isinstance(ts, (int, float)):
        return None
    ts = float(ts)
    if not math.isfinite(ts) or ts > now:
        return None
    return ts


def classify_task(tcfg, tstate, snap, report, proc, now, th):
    """Pure classification. Returns the per-task view (JSON-safe).

    tstate: {"registered_at","checkpoint"} persisted baseline (read-only).
    snap: adapter snapshot(); report: adapter poll() report; proc: verdict.
    """
    un = sorted(k for k, v in (snap.get("uncertainty") or {}).items() if v)
    view = {
        "task": tcfg["task"], "attempt": tcfg["attempt"],
        "phase": tcfg.get("phase"), "process": proc,
        "last_observed_at": (snap.get("observation") or {}).get("last_poll_at"),
        "last_successful_response_at": None, "last_tool_completed_at": None,
        "last_tool_outcome": None,
        "last_progress_at": (tstate.get("checkpoint") or {}).get("completed_at"),
        "pending_ask": False, "pending_tools": 0, "errors_recent": 0,
        "retry_fingerprint_count": 0, "uncertainty": un,
    }
    status, bootstrap = report.get("status"), report.get("bootstrap_pending")
    session = snap.get("session")
    bound = tstate.get("session_id")
    mismatch = bool(session and bound
                    and session.get("header_id") != bound)
    # genuine event ts only; live:false is historical but may anchor age
    step_ts = _valid_ts(snap.get("last_success"), now)
    view["last_successful_response_at"] = step_ts
    # tool outcome: is_error IS False is the ONLY success; null/failed are
    # never progress. A successful current-branch completion also counts as
    # a useful step (evidence of active work), failures/unknown never do.
    tool_step = None
    lt = snap.get("last_tool")
    if lt is not None:
        lt_ts = _valid_ts(lt, now)
        outcome = lt.get("is_error")
        if lt_ts is None or outcome not in (True, False):
            view["last_tool_outcome"] = "unknown"
        elif outcome is False:
            view["last_tool_outcome"] = "successful"
            view["last_tool_completed_at"] = lt_ts
            tool_step = lt_ts
        else:
            view["last_tool_outcome"] = "failed"  # completion, not a step
    pend = snap.get("pending_tools") or []
    asks = [p for p in pend if p.get("kind") == "ask_waiting"]
    running = [p for p in pend if p.get("kind") == "running"]
    view["pending_ask"] = bool(asks)
    view["pending_tools"] = len(pend)
    tool_ok = False
    for p in running:  # stale/off-branch/invalid pending never grants an OK
        pts = _valid_ts(p, now)
        if pts is not None and now - pts <= tcfg["tool_deadline_seconds"]:
            tool_ok = True
            break
    # ---- activity (orthogonal; conservative)
    if proc == "exited":
        activity = "exited"
    elif asks:
        activity = "waiting_input"
    elif running:
        activity = "tool_running"
    else:
        # a live PID alone never proves generation -> unknown
        activity = "unknown"
    # ---- health (step clock recomputed from THIS active-branch snapshot)
    useful = step_ts if tool_step is None else (
        tool_step if step_ts is None else max(step_ts, tool_step))
    anchor = useful if useful is not None else tstate["registered_at"]
    age = max(0.0, now - anchor)
    errs = []
    for e in snap.get("recent_errors") or []:
        ets = _valid_ts(e, now)
        if ets is not None and (useful is None or ets > useful):
            errs.append((e, ets))
    view["errors_recent"] = len(errs)
    if mismatch:
        health, reason = "unknown", "session_changed"
    elif status in ("fault", "backlog"):
        health, reason = "unknown", "adapter_" + str(status)
    elif snap.get("session_fault"):
        health, reason = "unknown", "adapter_fault"
    elif bootstrap:
        health, reason = "unknown", "adapter_bootstrap"
    elif un:
        # adapter uncertainty persists until actual recovery; a clean poll
        # after a critical unknown must NOT flip healthy on its own
        health, reason = "unknown", "adapter_uncertain"
    elif age > th["no_step_seconds"] and not asks and not tool_ok:
        # confirmed loop: SAME non-null assistant-error fingerprint, each
        # matching error INSIDE the rolling window; unrelated newer errors
        # never freshen an old group.
        fps = {}
        for e, ets in errs:  # only assistant errors carry fingerprints
            fp = e.get("fingerprint")
            if (e.get("category") == "assistant_error" and fp
                    and now - ets <= th["retry_window_seconds"]):
                fps[fp] = fps.get(fp, 0) + 1
        best = max(fps.values()) if fps else 0
        view["retry_fingerprint_count"] = best
        if best >= th["repeat_error_count"]:
            health, reason = "confirmed_retry_loop", "same_error_fingerprint"
        else:
            health, reason = "suspect_stall", "no_step_timeout"
    elif errs:
        health, reason = "degraded", "errors_with_recent_step"
    else:
        health, reason = "ok", ("step_fresh" if useful is not None
                                else "awaiting_first_step")
    if age > th["no_step_seconds"] and (asks or tool_ok) and health == "ok":
        reason = "ask_pending" if asks else "tool_within_deadline"
    view.update(health=health, activity=activity, reason=reason,
                no_step_age=round(age, 3))
    return view


class _Lock:
    """fcntl flock single writer; crash-safe (kernel releases on death)."""

    def __init__(self, sidecar):
        self.path = os.path.join(sidecar, "observer.lock")
        self.fd = None

    def __enter__(self):
        flags = os.O_CREAT | os.O_RDWR | getattr(os, "O_NOFOLLOW", 0)
        try:
            self.fd = os.open(self.path, flags, 0o600)
        except OSError as e:
            raise ConfigError("sidecar_refused" if e.errno == errno.ELOOP
                              else "observer_locked")
        try:
            fcntl.flock(self.fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            os.close(self.fd)
            self.fd = None
            raise ConfigError("observer_locked")
        return self

    def __exit__(self, *exc):
        if self.fd is not None:
            fcntl.flock(self.fd, fcntl.LOCK_UN)
            os.close(self.fd)
        return False


class Observer:
    """Owns sidecar state, adapters, and one poll cycle."""

    def __init__(self, cfg, clock=time.time):
        self.cfg, self.clock = cfg, clock
        self.dir = cfg["sidecar_dir"]
        self.state_path = os.path.join(self.dir, "state.json")
        self.snap_path = os.path.join(self.dir, "snapshot.json")
        self.state = None
        self.digest = hashlib.sha256(_dumps({
            k: v for k, v in cfg.items() if k != "root"}).encode()).hexdigest()

    def load_state(self):
        """Corruption is fatal (fail-safe): never reset baselines silently."""
        data = _read_json(self.state_path, MAX_STATE_BYTES)
        if data is None and os.path.exists(self.state_path):
            raise ConfigError("state_corrupt")
        if data is not None and (data.get("v") != STATE_VERSION
                                 or not isinstance(data.get("tasks"), dict)):
            raise ConfigError("state_corrupt")
        self.state = data or {"v": STATE_VERSION, "tasks": {},
                              "removed": [], "journal": []}

    def save(self, views):
        """Atomic persist, byte-bound BEFORE any write.

        On bound breach nothing is written: the previous state and snapshot
        stay untouched and the caller fails with `state_capacity` (a safe,
        recoverable code), never with a self-inflicted `state_corrupt`.
        """
        state_text = _dumps(self.state)
        snap_text = _dumps({
            "v": STATE_VERSION, "written_at": self.clock(),
            "config_digest": self.digest, "tasks": views})
        if (len(state_text.encode("utf-8")) > MAX_STATE_BYTES
                or len(snap_text.encode("utf-8")) > MAX_STATE_BYTES):
            raise ConfigError("state_capacity")
        _atomic_write(self.state_path, state_text)
        _atomic_write(self.snap_path, snap_text)

    def _tstate(self, tcfg, now):
        """Task state; attempt change resets adapter/binding, never baseline."""
        tasks = self.state["tasks"]
        ts = tasks.get(tcfg["task"])
        if ts is not None and ts.get("attempt") != tcfg["attempt"]:
            ts = None  # new attempt below; baseline carried explicitly
            carry = tasks.get(tcfg["task"]) or {}
        else:
            carry = {}
        if ts is None:
            base = None
            for r in self.state["removed"]:  # resume after pruning
                if r.get("task") == tcfg["task"]:
                    base = r
                    break
            prev = carry or base or {}
            ts = {"attempt": tcfg["attempt"],
                  "registered_at": prev.get("registered_at")
                  or tcfg["registered_at"],
                  # new attempt -> rebind; resume from removed keeps binding
                  "session_id": None if carry else prev.get("session_id"),
                  "checkpoint": prev.get("checkpoint"),
                  "adapter": None, "artifacts": None}
            if base:
                self.state["removed"] = [
                    r for r in self.state["removed"]
                    if r.get("task") != tcfg["task"]]
            tasks[tcfg["task"]] = ts
        return ts

    def _prune(self, active_ids):
        """Removed tasks leave active set; baseline kept (bounded ring)."""
        tasks = self.state["tasks"]
        for tid in list(tasks):
            if tid in active_ids:
                continue
            ts = tasks.pop(tid)
            ring = self.state["removed"]
            ring = [r for r in ring if r.get("task") != tid]
            ring.append({"task": tid, "registered_at": ts["registered_at"],
                         "session_id": ts.get("session_id"),
                         "checkpoint": ts.get("checkpoint")})
            self.state["removed"] = ring[-REMOVED_CAP:]

    def poll_cycle(self):
        """One bounded sample across tasks. Returns (views, changes)."""
        cfg, now = self.cfg, self.clock()
        th = {"no_step_seconds": cfg["no_step_seconds"],
              "retry_window_seconds": cfg["retry_window_seconds"],
              "repeat_error_count": cfg["repeat_error_count"]}
        prev = {}
        old = _read_json(self.snap_path, MAX_STATE_BYTES)
        if old and old.get("config_digest") == self.digest:
            prev = {v["task"]: v for v in old.get("tasks", [])
                    if isinstance(v, dict) and "task" in v}
        views, changes = [], []
        for tcfg in cfg["tasks"]:
            ts = self._tstate(tcfg, now)
            adapter = (OmpSessionAdapter.from_state(ts["adapter"])
                       if ts.get("adapter") else OmpSessionAdapter())
            report = adapter.poll(tcfg["session_log"])
            ts["adapter"] = adapter.export_state()
            snap = report.get("summary") or {}
            session = snap.get("session")
            # binding: config-pinned wins; else capture first header
            if tcfg["session_id"]:
                ts["session_id"] = tcfg["session_id"]
            elif ts.get("session_id") is None and session:
                ts["session_id"] = session.get("header_id")
            bound = ts.get("session_id")
            cp_issues = []
            cp = ts.get("checkpoint")
            if (cp and bound and tcfg["candidate"] is not None
                    and (cp.get("session_id") != bound
                         or cp.get("candidate") != tcfg["candidate"]
                         or cp.get("task") != tcfg["task"]
                         or cp.get("attempt") != tcfg["attempt"])):
                # foreign/legacy record: identity evidence retracts it; it
                # must never anchor the progress clock forever
                ts["checkpoint"] = None
                cp_issues.append("persisted:foreign_identity")
            for path in tcfg["checkpoint_files"]:
                rec, why = read_checkpoint(path, tcfg, bound,
                                           ts.get("checkpoint"), now,
                                           baseline=ts["registered_at"])
                if rec:
                    ts["checkpoint"] = rec  # monotonic (see read_checkpoint)
                elif why not in ("", "replay"):
                    cp_issues.append(os.path.basename(path) + ":" + why)
            first_art = ts.get("artifacts") is None
            sigs, changed_art, bad_art = artifact_signals(
                tcfg["artifact_files"], ts.get("artifacts") or {})
            ts["artifacts"] = sigs
            proc = process_verdict(tcfg["process"])
            view = classify_task(tcfg, ts, snap, report, proc, now, th)
            cp_now = ts.get("checkpoint")
            view.update(
                checkpoint_id=(cp_now or {}).get("checkpoint_id"),
                # past-attempt record is explicitly historical, never a
                # confirmation of the CURRENT candidate
                checkpoint_historical=bool(
                    cp_now and cp_now.get("attempt")
                    and cp_now.get("attempt") != tcfg["attempt"]),
                artifacts_changed=[] if first_art else changed_art,
                artifact_unverifiable=bad_art, checkpoint_issues=cp_issues,
                adapter={"status": report.get("status"),
                         "offset": report.get("offset"),
                         "backlog_bytes": report.get("backlog_bytes")},
                session=(session or {}).get("header_id"))
            views.append(view)
            old_v = prev.get(tcfg["task"])
            if old_v and (old_v.get("health") != view["health"]
                          or old_v.get("activity") != view["activity"]):
                change = {"at": round(now, 3), "task": tcfg["task"],
                          "from": "%s/%s" % (old_v.get("health"),
                                             old_v.get("activity")),
                          "to": "%s/%s" % (view["health"], view["activity"]),
                          "reason": view["reason"]}
                changes.append(change)
                jr = self.state["journal"]
                jr.append(change)
                self.state["journal"] = jr[-JOURNAL_CAP:]
        self._prune({t["task"] for t in cfg["tasks"]})
        return views, changes


def _counts(views):
    c = {}
    for v in views:
        c[v["health"]] = c.get(v["health"], 0) + 1
    return c


def _bounded_line(base, entries, counts, cap):
    """JSON line <= cap bytes incl newline; stable-order prefix + omitted."""
    kept, omitted = list(entries), 0
    while True:
        obj = dict(base)
        obj["tasks"] = kept
        if counts is not None:
            obj["counts"] = counts
        obj["omitted"] = omitted
        line = _dumps(obj) + "\n"
        if len(line.encode("utf-8")) <= cap or not kept:
            return line
        kept.pop()
        omitted += 1


def _compact(v):
    return {"t": v["task"], "h": v["health"], "a": v["activity"]}


def status_line(kind, views, at, stale, cap=STATUS_CAP, single=None):
    views = sorted(views, key=lambda v: v["task"])
    if single is not None:
        views = [v for v in views if v["task"] == single]
        if not views:
            raise ConfigError("task_unknown")
    eff = views if not stale else [
        dict(v, health="unknown", reason="stale_snapshot") for v in views]
    base = {"v": 1, "kind": kind, "at": round(at, 3), "stale": bool(stale)}
    return _bounded_line(base, [_compact(v) for v in eff],
                         _counts(eff), cap)


def detail_line(kind, views, at, stale, single=None, cap=DIAG_CAP):
    views = sorted(views, key=lambda v: v["task"])
    if single is not None:
        views = [v for v in views if v["task"] == single]
        if not views:
            raise ConfigError("task_unknown")
    eff = views if not stale else [
        dict(v, health="unknown", reason="stale_snapshot") for v in views]
    base = {"v": 1, "kind": kind, "at": round(at, 3), "stale": bool(stale)}
    return _bounded_line(base, eff, None if single else _counts(eff), cap)


def change_line(change):
    return _dumps({"v": 1, "kind": "change", **change}) + "\n"


def _load_snapshot(obs):
    snap = _read_json(obs.snap_path, MAX_STATE_BYTES)
    if snap is None:
        raise ConfigError("state_corrupt" if os.path.exists(obs.snap_path)
                          else "no_snapshot")
    if snap.get("v") != STATE_VERSION or not isinstance(snap.get("tasks"), list):
        raise ConfigError("state_corrupt")
    if snap.get("config_digest") != obs.digest:
        raise ConfigError("config_changed")  # re-poll after config edits
    return snap


def _cmd_poll(args):
    cfg = load_config(args.config, now=time.time())
    prepare_sidecar(cfg)
    with _Lock(cfg["sidecar_dir"]):
        obs = Observer(cfg)
        obs.load_state()
        views, _changes = obs.poll_cycle()
        obs.save(views)
    sys.stdout.write(detail_line("poll", views, obs.clock(), False))
    return 0


def _cmd_watch(args):
    cfg = load_config(args.config, now=time.time())
    prepare_sidecar(cfg)
    stop = {"flag": False}

    def _sig(_n, _f):
        stop["flag"] = True

    signal.signal(signal.SIGTERM, _sig)
    signal.signal(signal.SIGINT, _sig)
    with _Lock(cfg["sidecar_dir"]):
        obs = Observer(cfg)
        obs.load_state()
        views, _c = obs.poll_cycle()
        obs.save(views)
        sys.stdout.write(detail_line("poll", views, obs.clock(), False))
        sys.stdout.flush()
        last_beat = obs.clock()
        while not stop["flag"]:
            deadline = obs.clock() + cfg["poll_seconds"]
            while not stop["flag"] and obs.clock() < deadline:
                time.sleep(min(0.1, deadline - obs.clock()))
            if stop["flag"]:
                break
            views, changes = obs.poll_cycle()
            obs.save(views)
            for c in changes:  # immediate transition signal
                sys.stdout.write(change_line(c))
            now = obs.clock()
            if now - last_beat >= cfg["heartbeat_seconds"]:
                last_beat = now
                sys.stdout.write(status_line("heartbeat", views, now, False))
            sys.stdout.flush()
    return 0


def _cmd_cached(args, kind, cap):
    cfg = load_config(args.config, now=time.time())
    obs = Observer(cfg)
    snap = _load_snapshot(obs)  # read-only: no lock, no writes
    now = obs.clock()
    stale = now - snap.get("written_at", 0) > cfg["stale_seconds"]
    if kind == "status":
        line = status_line("status", snap["tasks"], now, stale, cap,
                           single=args.task)
    else:
        line = detail_line("diagnose", snap["tasks"], now, stale,
                           single=args.task, cap=cap)
    sys.stdout.write(line)
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(prog="campaign_watch")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("poll", "watch", "status", "diagnose"):
        p = sub.add_parser(name)
        p.add_argument("--config", required=True)
        if name in ("status", "diagnose"):
            p.add_argument("--task", default=None)
    args = ap.parse_args(argv)
    try:
        if args.cmd == "poll":
            return _cmd_poll(args)
        if args.cmd == "watch":
            return _cmd_watch(args)
        cap = STATUS_CAP if args.cmd == "status" else DIAG_CAP
        return _cmd_cached(args, args.cmd, cap)
    except ConfigError as e:
        return _fail(str(e))
    except Exception:
        return _fail("internal")  # never traceback/paths/secrets
    return 2


if __name__ == "__main__":
    sys.exit(main())
