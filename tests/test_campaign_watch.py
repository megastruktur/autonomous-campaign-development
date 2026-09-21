"""Tests for campaign_watch — unit classifier + subprocess CLI.

All fixtures are SYNTHETIC schema-shaped rows authored for these tests.
Sensitive-looking strings are invented markers proving the watcher never
retains raw payloads in sidecars or output. No real transcripts used.
"""

import json
import os
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from datetime import datetime, timezone

SCRIPTS = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "skills", "autonomous-campaign-development", "scripts")
sys.path.insert(0, SCRIPTS)

import campaign_watch as cw  # noqa: E402

WATCH = os.path.join(SCRIPTS, "campaign_watch.py")
T0 = 1_700_000_000.0
SECRET_CONTENT = "SYNTHETIC-WATCH-MARKER-message-content"
SECRET_ERROR = "SYNTHETIC-WATCH-MARKER-provider-error-text"


def iso(t):
    return datetime.fromtimestamp(t, tz=timezone.utc).isoformat()


def snap_base():
    return {
        "session": {"header_id": "sess-1", "version": 3},
        "session_fault": None, "file": {"dev": 1, "ino": 2}, "offset": 100,
        "bootstrap_pending": False,
        "last_success": None, "last_tool": None, "pending_tools": [],
        "consecutive_failures": 0,
        "error_totals": {"assistant_error": 0, "assistant_aborted": 0,
                         "tool_error": 0},
        "recent_errors": [], "counters": {}, "faults": {},
        "faults_recent": [], "uncertainty": {},
        "observation": {"last_poll_at": T0 + 10, "last_append_at": T0 + 5,
                        "polls": 1},
    }


def success(eid, ts, live=True, ts_valid=True):
    return {"entry_id": eid, "ts": ts, "ts_valid": ts_valid,
            "stop_reason": "stop", "live": live}


def aerror(fp, ts, category="assistant_error"):
    return {"category": category, "error_id": "err",
            "fingerprint": fp, "ts": ts, "ts_valid": True}


def report(status="ok", snap=None, bootstrap=False):
    return {"status": status, "bootstrap_pending": bootstrap,
            "offset": 100, "backlog_bytes": 0,
            "summary": snap if snap is not None else snap_base()}


def tcfg(**over):
    cfg = {"task": "t1", "attempt": "a1", "phase": "develop",
           "session_log": "/x/s.jsonl", "session_id": None,
           "registered_at": T0, "candidate": None,
           "checkpoint_files": [], "artifact_files": [],
           "tool_deadline_seconds": 100.0, "process": None}
    cfg.update(over)
    return cfg


def tstate(registered_at=T0, checkpoint=None, session_id="sess-1"):
    return {"registered_at": registered_at, "checkpoint": checkpoint,
            "session_id": session_id}


TH = {"no_step_seconds": 600.0, "retry_window_seconds": 600.0,
      "repeat_error_count": 3}
NOW = T0 + 1000.0


def classify(snapshot, rep=None, ts=None, cfg=None, proc=None, now=NOW):
    return cw.classify_task(cfg or tcfg(), ts or tstate(), snapshot,
                            rep or report(snap=snapshot), proc, now, TH)


class ClassifyTests(unittest.TestCase):

    def test_ok_fresh_step(self):
        s = snap_base()
        s["last_success"] = success("e1", T0 + 900)
        v = classify(s)
        self.assertEqual((v["health"], v["activity"]), ("ok", "unknown"))
        self.assertEqual(v["last_successful_response_at"], T0 + 900)

    def test_degraded_errors_with_recent_step(self):
        s = snap_base()
        s["last_success"] = success("e1", T0 + 900)
        s["recent_errors"] = [aerror("fp1", T0 + 950)]
        v = classify(s)
        self.assertEqual(v["health"], "degraded")

    def test_suspect_stall_old_step(self):
        s = snap_base()
        s["last_success"] = success("e1", T0 + 100)  # 900s > 600 budget
        v = classify(s)
        self.assertEqual((v["health"], v["reason"]),
                         ("suspect_stall", "no_step_timeout"))

    def test_no_events_ever_baseline_from_registration(self):
        v = classify(snap_base())  # registered T0, now T0+1000
        self.assertEqual(v["health"], "suspect_stall")
        self.assertIsNone(v["last_successful_response_at"])

    def test_pending_ask_is_waiting_not_stall(self):
        s = snap_base()
        s["pending_tools"] = [{"tool_call_id": "c1", "kind": "ask_waiting",
                               "started": True, "ts": T0, "ts_valid": True,
                               "entry_id": "e9"}]
        v = classify(s)
        self.assertEqual((v["health"], v["activity"]), ("ok", "waiting_input"))

    def test_tool_within_deadline_not_stall(self):
        s = snap_base()
        s["last_success"] = success("e1", T0)
        s["pending_tools"] = [{"tool_call_id": "c1", "kind": "running",
                               "started": True, "ts": T0 + 950,
                               "ts_valid": True, "entry_id": "e9"}]
        v = classify(s)
        self.assertEqual((v["health"], v["activity"]), ("ok", "tool_running"))

    def test_tool_deadline_expired_stall_even_pid_alive(self):
        s = snap_base()
        s["last_success"] = success("e1", T0)
        s["pending_tools"] = [{"tool_call_id": "c1", "kind": "running",
                               "started": True, "ts": T0 + 100,
                               "ts_valid": True, "entry_id": "e9"}]
        v = classify(s, proc="alive")
        self.assertEqual(v["health"], "suspect_stall")

    def test_confirmed_retry_loop_same_fingerprint(self):
        s = snap_base()
        s["last_success"] = success("e1", T0)
        s["recent_errors"] = [aerror("fp9", T0 + 800 + i) for i in range(3)]
        v = classify(s)
        self.assertEqual(v["health"], "confirmed_retry_loop")
        self.assertEqual(v["retry_fingerprint_count"], 3)

    def test_null_fingerprints_never_confirm(self):
        s = snap_base()  # aborted/tool_error carry no fingerprint
        s["recent_errors"] = [aerror(None, T0 + 900 + i, cat)
                              for i, cat in enumerate(
                                  ["assistant_aborted", "tool_error",
                                   "assistant_aborted"])]
        v = classify(s)
        self.assertEqual(v["health"], "suspect_stall")

    def test_errors_outside_retry_window_not_confirmed(self):
        s = snap_base()
        s["last_success"] = success("e1", T0 - 5000)
        s["recent_errors"] = [aerror("fp9", T0 - 4000 + i) for i in range(3)]
        v = classify(s)  # latest error 5000s ago > 600s window
        self.assertEqual(v["health"], "suspect_stall")

    def test_adapter_fault_backlog_bootstrap_unknown(self):
        for st, boot in (("fault", False), ("backlog", False), ("ok", True)):
            v = classify(snap_base(), rep=report(status=st, bootstrap=boot))
            self.assertEqual(v["health"], "unknown", (st, boot))

    def test_session_mismatch_unknown(self):
        s = snap_base()
        s["session"] = {"header_id": "other", "version": 3}
        s["last_success"] = success("e1", T0 + 900)
        v = classify(s)
        self.assertEqual((v["health"], v["reason"]),
                         ("unknown", "session_changed"))

    def test_historical_live_false_uses_event_ts_no_now_progress(self):
        s = snap_base()
        s["last_success"] = success("e1", T0 - 5000, live=False)
        v = classify(s)
        self.assertEqual(v["last_successful_response_at"], T0 - 5000)
        self.assertEqual(v["health"], "suspect_stall")

    def test_retracted_success_anchor_registration(self):
        s = snap_base()  # adapter already retracted: last_success None
        v = classify(s, ts=tstate(registered_at=T0 - 5000))
        self.assertEqual(v["health"], "suspect_stall")

    def test_failed_tool_not_useful_step(self):
        s = snap_base()
        s["last_tool"] = {"tool_call_id": "c1", "name": "Write",
                          "name_class": "tool", "is_error": True,
                          "ts": T0 + 990, "ts_valid": True}
        v = classify(s)
        self.assertIsNone(v["last_tool_completed_at"])
        self.assertEqual(v["health"], "suspect_stall")

    def test_activity_precedence_and_unknown(self):
        s = snap_base()
        s["pending_tools"] = [
            {"tool_call_id": "c1", "kind": "running", "started": True,
             "ts": NOW, "ts_valid": True, "entry_id": "e1"},
            {"tool_call_id": "c2", "kind": "ask_waiting", "started": True,
             "ts": NOW, "ts_valid": True, "entry_id": "e2"}]
        self.assertEqual(classify(s, proc="alive")["activity"], "waiting_input")
        self.assertEqual(classify(snap_base(), proc="alive")["activity"],
                         "generating")
        self.assertEqual(classify(snap_base(), proc="exited")["activity"],
                         "exited")


class ProcessTests(unittest.TestCase):

    def _self_spec(self):
        with open("/proc/self/stat") as f:
            data = f.read()
        ticks = int(data[data.rindex(")") + 2:].split()[19])
        with open("/proc/sys/kernel/random/boot_id") as f:
            boot = f.read().strip()
        return {"pid": os.getpid(), "start_ticks": ticks, "boot_id": boot}

    def test_alive_real_process(self):
        self.assertEqual(cw.process_verdict(self._self_spec()), "alive")

    def test_pid_reuse_wrong_ticks_exited_not_alive(self):
        spec = self._self_spec()
        spec["start_ticks"] += 1  # fabricated identity must not pass
        self.assertEqual(cw.process_verdict(spec), "exited")

    def test_missing_pid_exited(self):
        spec = self._self_spec()
        spec["pid"] = 99999999
        self.assertEqual(cw.process_verdict(spec), "exited")

    def test_previous_boot_exited(self):
        spec = self._self_spec()
        spec["boot_id"] = "00000000-0000-0000-0000-000000000000"
        self.assertEqual(cw.process_verdict(spec), "exited")

    def test_unsupported_platform_unknown(self):
        self.assertEqual(cw.process_verdict(self._self_spec(),
                                            platform="darwin"), "unknown")

    def test_inaccessible_proc_unknown(self):
        self.assertEqual(cw.process_verdict(
            self._self_spec(), boot_reader=lambda: None), "unknown")


class CheckpointTests(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = os.path.join(self.tmp.name, "camp")
        os.makedirs(os.path.join(self.root, ".watch"))
        self.path = os.path.join(self.root, "cp.json")

    def _write(self, **over):
        doc = {"schema_version": 1, "task": "t1", "attempt": "a1",
               "session_id": "sess-1", "candidate": "cand",
               "checkpoint_id": "cp1", "completed_at": iso(T0 + 500),
               "kind": "review_checkpoint", "verified": True}
        doc.update(over)
        with open(self.path, "w") as f:
            json.dump(doc, f)

    def _read(self, confirmed=None, cfg=None):
        return cw.read_checkpoint(self.path, cfg or tcfg(candidate="cand"),
                                  "sess-1", confirmed, NOW)

    def test_valid_confirm(self):
        rec, why = self._write() or self._read()
        self.assertEqual(why, "")
        self.assertEqual(rec["checkpoint_id"], "cp1")

    def test_replay_same_id_rejected(self):
        self._write()
        confirmed = {"checkpoint_id": "cp1", "completed_at": T0 + 500,
                     "kind": "review_checkpoint"}
        rec, why = self._read(confirmed=confirmed)
        self.assertEqual((rec, why), (None, "replay"))

    def test_older_checkpoint_not_monotonic(self):
        self._write()
        confirmed = {"checkpoint_id": "cp9", "completed_at": T0 + 900,
                     "kind": "review_checkpoint"}
        rec, why = self._read(confirmed=confirmed)
        self.assertEqual((rec, why), (None, "replay"))

    def test_future_timestamp_rejected(self):
        self._write(completed_at=iso(NOW + 99999), checkpoint_id="cp2")
        rec, why = self._read()
        self.assertEqual((rec, why), (None, "timestamp"))

    def test_mismatch_task_attempt_session_candidate(self):
        for kw in ({"task": "t2"}, {"attempt": "a9"}, {"session_id": "s9"},
                   {"candidate": "other"}):
            self._write(**kw)
            rec, why = self._read()
            self.assertEqual((rec, why), (None, "mismatch"), kw)

    def test_unverified_and_unknown_kind_rejected(self):
        self._write(verified=False)
        self.assertEqual(self._read()[1], "shape")
        self._write(kind="mystery")
        self.assertEqual(self._read()[1], "shape")


class ArtifactTests(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.p = os.path.join(self.tmp.name, "out.bin")

    def test_change_and_unverifiable_signals(self):
        with open(self.p, "wb") as f:
            f.write(b"v1")
        sigs, changed, bad = cw.artifact_signals([self.p], {})
        self.assertEqual((changed, bad), (["out.bin"], []))
        sigs2, changed2, bad2 = cw.artifact_signals([self.p], sigs)
        self.assertEqual((changed2, bad2), ([], []))  # stable
        with open(self.p, "wb") as f:
            f.write(b"v2")
        _, changed3, _ = cw.artifact_signals([self.p], sigs2)
        self.assertEqual(changed3, ["out.bin"])
        missing = os.path.join(self.tmp.name, "gone.bin")
        _, _, bad4 = cw.artifact_signals([missing], {})
        self.assertEqual(bad4, ["gone.bin"])  # uncertainty, not success


class ConfigTests(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = os.path.join(self.tmp.name, "camp")
        os.makedirs(os.path.join(self.root, ".watch"))

    def _cfg(self, **over):
        cfg = {"schema_version": 1,
               "sidecar_dir": os.path.join(self.root, ".watch"),
               "poll_seconds": 0.1, "heartbeat_seconds": 0.2,
               "stale_seconds": 120, "no_step_seconds": 600,
               "retry_window_seconds": 600, "repeat_error_count": 3,
               "tasks": [dict(tcfg(task="t1",
                                   session_log=os.path.join(self.root, "s.jsonl"),
                                   registered_at=iso(T0)))]}
        cfg.update(over)
        path = os.path.join(self.root, "cfg.json")
        with open(path, "w") as f:
            json.dump(cfg, f)
        return path

    def test_fractional_intervals_accepted(self):
        cfg = cw.load_config(self._cfg(), now=NOW)
        self.assertEqual(cfg["poll_seconds"], 0.1)

    def _invalid(self, **over):
        with self.assertRaises(cw.ConfigError):
            cw.load_config(self._cfg(**over), now=NOW)

    def test_duplicate_ids_rejected(self):
        t = dict(tcfg(session_log=os.path.join(self.root, "s.jsonl"),
                      registered_at=iso(T0)))
        self._invalid(tasks=[t, dict(t)])

    def test_relative_session_log_rejected(self):
        self._invalid(tasks=[dict(tcfg(session_log="rel.jsonl",
                                       registered_at=iso(T0)))])

    def test_excess_tasks_rejected_not_ignored(self):
        tasks = [dict(tcfg(task="task-%d" % i,
                           session_log=os.path.join(self.root, "s.jsonl"),
                           registered_at=iso(T0)))
                 for i in range(cw.MAX_TASKS + 1)]
        self._invalid(tasks=tasks)

    def test_bad_interval_and_version_rejected(self):
        self._invalid(poll_seconds=0)
        self._invalid(poll_seconds=-1)
        self._invalid(schema_version=2)

    def test_symlink_outside_scope_file_rejected(self):
        outside = os.path.join(self.tmp.name, "outside.txt")
        with open(outside, "w") as f:
            f.write("x")
        link = os.path.join(self.root, "link.txt")
        os.symlink(outside, link)
        t = dict(tcfg(session_log=os.path.join(self.root, "s.jsonl"),
                      registered_at=iso(T0), checkpoint_files=[link]))
        self._invalid(tasks=[t])


class BoundedLineTests(unittest.TestCase):

    def _views(self, n):
        return [{"task": "task-%03d" % i, "health": "ok",
                 "activity": "unknown"} for i in range(n)]

    def test_status_always_within_cap_with_omitted(self):
        line = cw.status_line("status", self._views(cw.MAX_TASKS), NOW, False)
        raw = line.encode("utf-8")
        self.assertLessEqual(len(raw), cw.STATUS_CAP)
        obj = json.loads(line)  # never broken/truncated JSON
        self.assertEqual(obj["omitted"] + len(obj["tasks"]), cw.MAX_TASKS)
        self.assertEqual(obj["counts"], {"ok": cw.MAX_TASKS})
        self.assertEqual([t["t"] for t in obj["tasks"]],
                         sorted(t["t"] for t in obj["tasks"]))

    def test_diagnose_cap(self):
        views = [dict(v, extra="x" * 100) for v in self._views(100)]
        line = cw.detail_line("diagnose", views, NOW, False)
        self.assertLessEqual(len(line.encode("utf-8")), cw.DIAG_CAP)
        self.assertTrue(json.loads(line))

    def test_stale_marks_health_unknown(self):
        obj = json.loads(cw.status_line("status", self._views(3), NOW, True))
        self.assertTrue(obj["stale"])
        self.assertEqual(obj["counts"], {"unknown": 3})


def row(eid, parent, t, typ, **body):
    ev = {"id": eid, "parentId": parent, "timestamp": t, "type": typ}
    ev.update(body)
    return ev


def hdr(eid="e0", t=None):
    return row(eid, None, t or iso(time.time() - 60), "session",
               version=3, cwd="/synthetic/cwd")


def asst(eid, parent, t=None, stop="stop", **extra):
    msg = {"role": "assistant", "stopReason": stop,
           "content": [{"type": "text", "text": SECRET_CONTENT}]}
    msg.update(extra)
    return row(eid, parent, t or iso(time.time() - 50), "message", message=msg)


def write_rows(path, rows, mode="w"):
    with open(path, mode) as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")


class CliBase(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = os.path.join(self.tmp.name, "camp")
        self.sidecar = os.path.join(self.root, ".watch")
        os.makedirs(self.sidecar)
        self.log = os.path.join(self.root, "s.jsonl")

    def config(self, tasks, **over):
        cfg = {"schema_version": 1, "sidecar_dir": self.sidecar,
               "poll_seconds": 0.2, "heartbeat_seconds": 0.4,
               "stale_seconds": 1.0, "no_step_seconds": 600,
               "retry_window_seconds": 600, "repeat_error_count": 3,
               "tasks": tasks}
        cfg.update(over)
        self._cfg_n = getattr(self, "_cfg_n", 0) + 1
        path = os.path.join(self.root, "cfg-%d.json" % self._cfg_n)
        with open(path, "w") as f:
            json.dump(cfg, f)
        return path

    def task(self, tid="t1", log=None, **over):
        t = {"task": tid, "attempt": "a1", "phase": "develop",
             "session_log": log or self.log, "session_id": None,
             "registered_at": iso(time.time()), "candidate": None,
             "checkpoint_files": [], "artifact_files": [],
             "tool_deadline_seconds": 1800, "process": None}
        t.update(over)
        return t

    def run_cli(self, *argv, timeout=30):
        return subprocess.run([sys.executable, WATCH, *argv],
                              capture_output=True, text=True, timeout=timeout)


class CliPollTests(CliBase):

    def poll(self, cfg_path, **kw):
        return self.run_cli("poll", "--config", cfg_path, **kw)

    def test_poll_end_to_end_ok_and_privacy(self):
        write_rows(self.log, [hdr(), asst("e1", "e0")])
        cfg = self.config([self.task()])
        r = self.poll(cfg)
        self.assertEqual(r.returncode, 0, r.stderr)
        out = json.loads(r.stdout)
        self.assertEqual(out["kind"], "poll")
        (v,) = out["tasks"]
        self.assertEqual(v["health"], "ok")
        # privacy: invented markers never reach output or sidecars
        blob = r.stdout + r.stderr
        for name in os.listdir(self.sidecar):
            with open(os.path.join(self.sidecar, name), "rb") as f:
                blob += f.read().decode("utf-8", "replace")
        self.assertNotIn(SECRET_CONTENT, blob)
        self.assertNotIn(self.tmp.name, blob)  # no host paths either

    def test_poll_missing_log_unknown_not_healthy(self):
        cfg = self.config([self.task()])
        r = self.poll(cfg)
        self.assertEqual(r.returncode, 0, r.stderr)
        (v,) = json.loads(r.stdout)["tasks"]
        self.assertEqual(v["health"], "unknown")

    def test_status_and_diagnose_caps(self):
        logs = []
        tasks = []
        for i in range(30):
            log = os.path.join(self.root, "s%d.jsonl" % i)
            write_rows(log, [hdr(), asst("e1", "e0")])
            logs.append(log)
            tasks.append(self.task("task-%02d" % i, log=log))
        cfg = self.config(tasks)
        self.assertEqual(self.poll(cfg).returncode, 0)
        r = self.run_cli("status", "--config", cfg)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertLessEqual(len(r.stdout.encode()), cw.STATUS_CAP)
        obj = json.loads(r.stdout)
        self.assertEqual(obj["omitted"] + len(obj["tasks"]), 30)
        r = self.run_cli("diagnose", "--config", cfg)
        self.assertLessEqual(len(r.stdout.encode()), cw.DIAG_CAP)
        r = self.run_cli("diagnose", "--config", cfg, "--task", "task-03")
        one = json.loads(r.stdout)
        self.assertEqual([t["task"] for t in one["tasks"]], ["task-03"])
        self.assertIn("last_successful_response_at", one["tasks"][0])
        r = self.run_cli("status", "--config", cfg, "--task", "nope")
        self.assertNotEqual(r.returncode, 0)
        self.assertEqual(json.loads(r.stdout)["error"], "task_unknown")

    def test_stale_snapshot_unknown(self):
        write_rows(self.log, [hdr(), asst("e1", "e0")])
        cfg = self.config([self.task()], stale_seconds=0.3)
        self.assertEqual(self.poll(cfg).returncode, 0)
        time.sleep(0.5)  # let snapshot go stale
        obj = json.loads(self.run_cli("status", "--config", cfg).stdout)
        self.assertTrue(obj["stale"])
        self.assertEqual(obj["counts"], {"unknown": 1})

    def test_status_before_any_poll(self):
        cfg = self.config([self.task()])
        r = self.run_cli("status", "--config", cfg)
        self.assertEqual(json.loads(r.stdout)["error"], "no_snapshot")
        self.assertNotEqual(r.returncode, 0)


class CliDurabilityTests(CliBase):

    def _state(self):
        with open(os.path.join(self.sidecar, "state.json")) as f:
            return json.load(f)

    def _poll(self, cfg):
        r = self.run_cli("poll", "--config", cfg)
        self.assertEqual(r.returncode, 0, r.stderr)
        return json.loads(r.stdout)

    def test_corrupt_state_failsafe_preserves_file(self):
        write_rows(self.log, [hdr(), asst("e1", "e0")])
        cfg = self.config([self.task()])
        self._poll(cfg)
        spath = os.path.join(self.sidecar, "state.json")
        with open(spath, "w") as f:
            f.write("{not json")
        r = self.run_cli("poll", "--config", cfg)
        self.assertNotEqual(r.returncode, 0)
        self.assertEqual(json.loads(r.stdout)["error"], "state_corrupt")
        with open(spath) as f:  # untouched: baseline never silently reset
            self.assertEqual(f.read(), "{not json")

    def test_invalid_config_safe_error(self):
        path = os.path.join(self.root, "bad.json")
        with open(path, "w") as f:
            json.dump({"schema_version": 1, "sidecar_dir": "relative"}, f)
        r = self.run_cli("poll", "--config", path)
        self.assertNotEqual(r.returncode, 0)
        obj = json.loads(r.stdout)
        self.assertEqual(obj["error"], "config_invalid")
        self.assertNotIn(self.tmp.name, r.stdout + r.stderr)
        self.assertNotIn("Traceback", r.stderr)

    def test_restart_preserves_registration_baseline(self):
        write_rows(self.log, [hdr()])  # no events: baseline = registered_at
        old_reg = iso(time.time() - 5000)
        cfg = self.config([self.task(registered_at=old_reg)],
                          no_step_seconds=600)
        out = self._poll(cfg)
        self.assertEqual(out["tasks"][0]["health"], "suspect_stall")
        st = self._state()["tasks"]["t1"]
        self.assertLess(st["registered_at"], time.time() - 4000)
        cfg2 = self.config([self.task(registered_at=iso(time.time()))],
                           no_step_seconds=600)
        out2 = self._poll(cfg2)  # config re-registration cannot mint new age
        self.assertEqual(out2["tasks"][0]["health"], "suspect_stall")
        self.assertEqual(self._state()["tasks"]["t1"]["registered_at"],
                         st["registered_at"])

    def test_new_attempt_keeps_baseline_rebinds_session(self):
        write_rows(self.log, [hdr()])
        cfg = self.config([self.task()], no_step_seconds=0.5)
        self._poll(cfg)
        st1 = self._state()["tasks"]["t1"]
        time.sleep(0.7)
        cfg2 = self.config([self.task(attempt="a2")], no_step_seconds=0.5)
        out = self._poll(cfg2)  # attempt label must not reset no-step age
        self.assertEqual(out["tasks"][0]["health"], "suspect_stall")
        st2 = self._state()["tasks"]["t1"]
        self.assertEqual(st2["registered_at"], st1["registered_at"])
        self.assertEqual(st2["attempt"], "a2")

    def test_session_binding_captured_then_mismatch(self):
        write_rows(self.log, [hdr(), asst("e1", "e0")])
        cfg = self.config([self.task()])
        self._poll(cfg)
        self.assertEqual(self._state()["tasks"]["t1"]["session_id"], "e0")
        # rotate: new inode + new session header under same path
        os.remove(self.log)
        write_rows(self.log, [hdr("z9"), asst("z1", "z9")])
        out = self._poll(cfg)
        self.assertEqual(out["tasks"][0]["health"], "unknown")
        self.assertEqual(out["tasks"][0]["reason"], "session_changed")

    def test_removed_task_pruned_and_resumed(self):
        write_rows(self.log, [hdr()])
        cfg = self.config([self.task()], no_step_seconds=0.5)
        self._poll(cfg)
        reg = self._state()["tasks"]["t1"]["registered_at"]
        cfg2 = self.config([self.task("other",
                                      log=os.path.join(self.root, "o.jsonl"))])
        self._poll(cfg2)
        st = self._state()
        self.assertNotIn("t1", st["tasks"])
        self.assertEqual(st["removed"][0]["task"], "t1")
        time.sleep(0.7)
        out = self._poll(cfg)  # re-added: resume old baseline
        self.assertEqual(out["tasks"][0]["health"], "suspect_stall")
        self.assertEqual(self._state()["tasks"]["t1"]["registered_at"], reg)

    def test_config_change_requires_repoll(self):
        write_rows(self.log, [hdr(), asst("e1", "e0")])
        cfg = self.config([self.task()])
        self._poll(cfg)
        cfg2 = self.config([self.task()], stale_seconds=999)
        r = self.run_cli("status", "--config", cfg2)
        self.assertEqual(json.loads(r.stdout)["error"], "config_changed")

    def test_single_writer_lock(self):
        write_rows(self.log, [hdr()])
        cfg = self.config([self.task()])
        fd = os.open(os.path.join(self.sidecar, "observer.lock"),
                     os.O_CREAT | os.O_RDWR)
        import fcntl
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        try:
            r = self.run_cli("poll", "--config", cfg)
            self.assertEqual(json.loads(r.stdout)["error"], "observer_locked")
        finally:
            os.close(fd)


class CliIntegrationTests(CliBase):

    def _poll(self, cfg):
        r = self.run_cli("poll", "--config", cfg)
        self.assertEqual(r.returncode, 0, r.stderr)
        return json.loads(r.stdout)

    def test_healthy_recovery_after_errors(self):
        write_rows(self.log, [hdr(), asst("e1", "e0"),
                              asst("e2", "e1", stop="error", errorId="e500",
                                   errorMessage=SECRET_ERROR)])
        cfg = self.config([self.task()])
        out = self._poll(cfg)
        self.assertEqual(out["tasks"][0]["health"], "degraded")
        write_rows(self.log, [asst("e3", "e2")], mode="a")
        out = self._poll(cfg)  # fresh useful step after errors -> ok
        v = out["tasks"][0]
        self.assertEqual(v["health"], "ok")
        self.assertNotIn(SECRET_ERROR, json.dumps(out))

    def test_checkpoint_confirm_and_replay_via_cli(self):
        cp = os.path.join(self.root, "cp.json")
        doc = {"schema_version": 1, "task": "t1", "attempt": "a1",
               "session_id": "e0", "candidate": None,
               "checkpoint_id": "cp1", "completed_at": iso(time.time()),
               "kind": "runtime_scenario", "verified": True}
        write_rows(self.log, [hdr(), asst("e1", "e0")])
        with open(cp, "w") as f:
            json.dump(doc, f)
        cfg = self.config([self.task(checkpoint_files=[cp])])
        v = self._poll(cfg)["tasks"][0]
        self.assertEqual(v["checkpoint_id"], "cp1")
        progress = v["last_progress_at"]
        self.assertIsNotNone(progress)
        doc["completed_at"] = iso(time.time() + 10)  # touch: same id
        with open(cp, "w") as f:
            json.dump(doc, f)
        v = self._poll(cfg)["tasks"][0]
        self.assertEqual(v["last_progress_at"], progress)  # no replay
        doc.update(checkpoint_id="cp2")
        with open(cp, "w") as f:
            json.dump(doc, f)
        v = self._poll(cfg)["tasks"][0]
        self.assertEqual(v["checkpoint_id"], "cp2")

    def test_watch_loop_change_and_heartbeat(self):
        import select
        write_rows(self.log, [hdr(), asst("e1", "e0")])
        cfg = self.config([self.task()])
        proc = subprocess.Popen([sys.executable, WATCH, "watch",
                                 "--config", cfg],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, text=True)
        lines = []

        def read_line(timeout):
            ready, _, _ = select.select([proc.stdout], [], [], timeout)
            if not ready:
                return None
            line = proc.stdout.readline()
            if line:
                lines.append(line)
            return line

        try:
            deadline = time.time() + 15
            initial = False
            while time.time() < deadline and not initial:
                line = read_line(0.5)
                if line and json.loads(line).get("kind") == "poll":
                    initial = True
            self.assertTrue(initial, lines)
            # only now inject a failure: transition must be observed live
            write_rows(self.log, [asst("e2", "e1", stop="error",
                                       errorId="e500",
                                       errorMessage=SECRET_ERROR)], mode="a")
            saw_change = saw_heartbeat = False
            while time.time() < deadline and not (saw_change and saw_heartbeat):
                line = read_line(1.0)
                if not line:
                    continue
                obj = json.loads(line)
                saw_change |= obj.get("kind") == "change"
                saw_heartbeat |= obj.get("kind") == "heartbeat"
            self.assertTrue(saw_change, lines)
            self.assertTrue(saw_heartbeat, lines)
            for line in lines:
                self.assertNotIn(SECRET_ERROR, line)
                if json.loads(line).get("kind") == "heartbeat":
                    self.assertLessEqual(len(line.encode()), cw.STATUS_CAP)
        finally:
            proc.send_signal(signal.SIGTERM)  # only the test process
            rc = proc.wait(timeout=10)
        self.assertEqual(rc, 0, proc.stderr.read())


if __name__ == "__main__":
    unittest.main()
