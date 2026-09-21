"""Unit tests for omp_events.OmpSessionAdapter.

All fixtures are SYNTHETIC — schema-shaped rows authored for these tests,
not captured from any real user session.  No real tool arguments, message
content, or error text are checked in; the sensitive-looking strings below
are invented markers used to prove the adapter never retains raw payloads.
"""

import json
import os
import sys
import tempfile
import unittest
from datetime import datetime, timezone

sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "skills",
        "autonomous-campaign-development",
        "scripts",
    ),
)

from omp_events import OmpSessionAdapter  # noqa: E402

T0 = 1_700_000_000.0
SECRET_CONTENT = "SYNTHETIC-MARKER-message-content"
SECRET_ARG = "SYNTHETIC-MARKER-tool-argument"
SECRET_ERROR = (
    "500 litellm.APIConnectionError: BedrockException - "
    "Response payload is not completed"
)
SECRET_CWD = "/synthetic/cwd/path"


def iso(t):
    return datetime.fromtimestamp(t, tz=timezone.utc).isoformat()


class Clock:
    """Injectable deterministic clock (no sleeps anywhere)."""

    def __init__(self, t=T0 + 3600):
        self.now = t

    def __call__(self):
        return self.now

    def advance(self, dt):
        self.now += dt


def row(eid, parent, t, typ, **body):
    ev = {"id": eid, "parentId": parent, "timestamp": t, "type": typ}
    ev.update(body)
    return ev


def header(eid="e0", t=None, version=3, parent=None):
    return row(eid, parent, t or iso(T0), "session", version=version, cwd=SECRET_CWD)


def assistant(eid, parent, t=None, stop="stop", content=None, **extra):
    msg = {"role": "assistant", "stopReason": stop, "content": content or []}
    msg.update(extra)
    return row(eid, parent, t or iso(T0 + 1), "message", message=msg)


def tool_call_part(tcid, name="Write"):
    return {"type": "toolCall", "id": tcid, "name": name,
            "arguments": {"payload": SECRET_ARG}}


def tool_result(eid, parent, tcid, t=None, name="Write", is_error=False):
    return row(eid, parent, t or iso(T0 + 2), "message", message={
        "role": "toolResult", "toolCallId": tcid, "toolName": name,
        "isError": is_error, "content": SECRET_CONTENT,
    })


def tool_start(eid, parent, tcid, t=None):
    return row(eid, parent, t or iso(T0 + 2), "custom",
               name="tool_execution_start", data={"toolCallId": tcid})


def branch_discard(eid, parent, target, t=None, variant="flat"):
    t = t or iso(T0 + 3)
    if variant == "flat":
        return row(eid, parent, t, "branch_summary",
                   details={"kind": "discarded-entry-branch", "discardedEntryId": target})
    if variant == "nested":
        return row(eid, parent, t, "branch_summary",
                   data={"details": {"kind": "discarded-entry-branch",
                                     "discardedEntryId": target}})
    return row(eid, parent, t, "branch_summary",
               details={"details": {"kind": "discarded-entry-branch",
                                    "discardedEntryId": target}})


def write_rows(path, rows, mode="w"):
    with open(path, mode) as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")



class Base(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = os.path.join(self.tmp.name, "session.jsonl")
        self.clock = Clock()

    def adapter(self, **kw):
        return OmpSessionAdapter(clock=self.clock, **kw)

    @staticmethod
    def dump(adapter, report):
        return json.dumps({"state": adapter.export_state(), "report": report})


class TestProgressSemantics(Base):

    def test_success_recorded_with_live_flag_after_bootstrap(self):
        write_rows(self.path, [header(), assistant("e1", "e0", stop="stop")])
        a = self.adapter()
        rep = a.poll(self.path)
        self.assertEqual(rep["status"], "ok")
        self.assertFalse(rep["new_faults"])
        ls = rep["summary"]["last_success"]
        self.assertEqual(ls["entry_id"], "e1")
        self.assertTrue(ls["ts_valid"])
        self.assertFalse(ls["live"])  # history, not freshly observed
        self.assertTrue(rep["history_replayed"])
        self.assertFalse(rep["bootstrap_pending"])
        # a later append is observed live
        self.clock.advance(60)
        write_rows(self.path, [assistant("e2", "e1", t=iso(T0 + 61))], mode="a")
        rep = a.poll(self.path)
        self.assertEqual(rep["summary"]["last_success"]["entry_id"], "e2")
        self.assertTrue(rep["summary"]["last_success"]["live"])
        self.assertEqual(
            rep["summary"]["observation"]["last_append_at"], self.clock.now)

    def test_partial_trailing_line_retained_then_completed(self):
        good = json.dumps(header()) + "\n" + json.dumps(
            assistant("e1", "e0", stop="stop")) + "\n"
        tail_row = json.dumps(assistant("e2", "e1", stop="stop"))
        with open(self.path, "w") as f:
            f.write(good + tail_row[: len(tail_row) // 2])
        a = self.adapter()
        rep = a.poll(self.path)
        self.assertEqual(rep["status"], "ok")
        self.assertEqual(rep["summary"]["last_success"]["entry_id"], "e1")
        self.assertGreater(rep["tail_bytes"], 0)
        self.assertEqual(rep["offset"], len(good))  # not advanced into partial
        with open(self.path, "a") as f:
            f.write(tail_row[len(tail_row) // 2:] + "\n")
        rep = a.poll(self.path)
        self.assertEqual(rep["summary"]["last_success"]["entry_id"], "e2")
        self.assertEqual(rep["summary"]["counters"]["events"], 3)
        self.assertEqual(rep["summary"]["counters"]["duplicates"], 0)
        self.assertEqual(rep["offset"], os.path.getsize(self.path))

    def test_provider_error_incident_shape(self):
        rows = [header()]
        parent = "e0"
        for i in (1, 2):  # two complete error records with a partial toolCall
            rows.append(assistant(
                "e%d" % i, parent, stop="error", errorId=135168,
                errorMessage=SECRET_ERROR,
                content=[tool_call_part("tc%d" % i, "Write")]))
            rows.append(tool_result("t%d" % i, "e%d" % i, "tc%d" % i,
                                    is_error=True))
            parent = "t%d" % i
        write_rows(self.path, rows)
        a = self.adapter()
        rep = a.poll(self.path)
        s = rep["summary"]
        self.assertIsNone(s["last_success"])
        self.assertEqual(s["error_totals"]["assistant_error"], 2)
        self.assertEqual(s["error_totals"]["tool_error"], 2)
        self.assertEqual(s["consecutive_failures"], 4)
        self.assertEqual(s["counters"]["failed_assistant"], 2)
        self.assertEqual(s["counters"]["tool_results_error"], 2)
        self.assertEqual(s["last_tool"]["tool_call_id"], "tc2")
        self.assertTrue(s["last_tool"]["is_error"])
        self.assertEqual(len(s["pending_tools"]), 0)
        self.assertTrue(all(
            e["category"] in ("assistant_error", "tool_error")
            and "fingerprint" in e for e in s["recent_errors"]))

    def test_aborted_and_usage_only_never_success(self):
        write_rows(self.path, [
            header(),
            assistant("e1", "e0", stop="aborted", completedAt=iso(T0 + 5),
                      usage={"inputTokens": 10, "outputTokens": 0}),
            row("e2", "e1", iso(T0 + 6), "model_usage",
                usage={"inputTokens": 10, "outputTokens": 0}),
            row("e3", "e1", iso(T0 + 7), "title", title="SYNTHETIC title"),
            row("e4", "e1", iso(T0 + 8), "compaction"),
        ])
        rep = self.adapter().poll(self.path)
        s = rep["summary"]
        self.assertIsNone(s["last_success"])
        self.assertEqual(s["error_totals"]["assistant_aborted"], 1)
        self.assertEqual(s["counters"]["service_events"], 3)
        self.assertEqual(s["counters"]["successful_assistant"], 0)

    def test_failure_streak_resets_on_success(self):
        write_rows(self.path, [
            header(),
            assistant("e1", "e0", stop="error", errorId=1,
                      errorMessage=SECRET_ERROR),
            assistant("e2", "e1", stop="error", errorId=1,
                      errorMessage=SECRET_ERROR),
            assistant("e3", "e2", stop="stop"),
            assistant("e4", "e3", stop="aborted"),
        ])
        s = self.adapter().poll(self.path)["summary"]
        self.assertEqual(s["consecutive_failures"], 1)
        self.assertEqual(s["counters"]["failed_assistant"], 3)
        self.assertEqual(s["counters"]["successful_assistant"], 1)

    def test_tool_lifecycle_ask_vs_running(self):
        write_rows(self.path, [
            header(),
            assistant("e1", "e0", stop="toolUse",
                      content=[tool_call_part("tc-ask", "ask_user")]),
            assistant("e2", "e1", stop="toolUse",
                      content=[tool_call_part("tc-write", "Write")]),
            tool_start("e3", "e2", "tc-write"),
        ])
        s = self.adapter().poll(self.path)["summary"]
        kinds = {p["tool_call_id"]: p["kind"] for p in s["pending_tools"]}
        self.assertEqual(kinds["tc-ask"], "ask_waiting")
        self.assertEqual(kinds["tc-write"], "running")
        started = {p["tool_call_id"]: p["started"] for p in s["pending_tools"]}
        self.assertFalse(started["tc-ask"])
        self.assertTrue(started["tc-write"])
        # successful toolUse assistant counts as progress; tool completion
        write_rows(self.path, [
            tool_result("e4", "e3", "tc-write"),
            tool_result("e5", "e4", "tc-ask", name="ask_user"),
        ], mode="a")
        s = self.adapter().poll(self.path)["summary"]
        self.assertEqual(s["pending_tools"], [])
        self.assertEqual(s["last_tool"]["tool_call_id"], "tc-ask")
        self.assertFalse(s["last_tool"]["is_error"])
        self.assertEqual(s["counters"]["tool_results"], 2)
        # a failed result completes without ever being success
        write_rows(self.path, [assistant("e6", "e5", stop="toolUse",
                                         content=[tool_call_part("tc-x")]),
                               tool_result("e7", "e6", "tc-x", is_error=True)],
                   mode="a")
        s = self.adapter().poll(self.path)["summary"]
        self.assertTrue(s["last_tool"]["is_error"])
        self.assertEqual(s["error_totals"]["tool_error"], 1)

class TestBranchesAndDedupe(Base):

    def test_discarded_branch_retraction_all_variants(self):
        for variant in ("flat", "nested", "deep"):
            with self.subTest(variant=variant):
                path = os.path.join(self.tmp.name, "v-%s.jsonl" % variant)
                write_rows(path, [
                    header(),
                    assistant("e1", "e0", stop="stop"),
                    assistant("e2", "e1", stop="stop"),
                    branch_discard("b", "e2", "e2", variant=variant),
                ])
                s = self.adapter().poll(path)["summary"]
                self.assertEqual(s["last_success"]["entry_id"], "e1")
                self.assertEqual(s["counters"]["successful_assistant"], 1)
                self.assertEqual(s["counters"]["discarded_success_retracted"], 1)

    def test_replayed_discarded_entries_do_not_inflate(self):
        write_rows(self.path, [
            header(),
            assistant("e1", "e0", stop="stop"),
            assistant("e2", "e1", stop="stop"),
            branch_discard("b", "e2", "e2"),
        ])
        a = self.adapter()
        a.poll(self.path)
        # replay of the discarded subtree, incl. an exact duplicate row
        write_rows(self.path, [
            assistant("e3", "e2", stop="stop"),
            assistant("e2", "e1", stop="stop"),
        ], mode="a")
        s = a.poll(self.path)["summary"]
        self.assertEqual(s["counters"]["successful_assistant"], 1)
        self.assertEqual(s["counters"]["discarded_branch_events"], 1)
        self.assertEqual(s["counters"]["duplicates"], 1)
        self.assertEqual(s["last_success"]["entry_id"], "e1")


class TestFaultsAndRobustness(Base):

    def test_missing_file_is_fault_then_recovers(self):
        a = self.adapter()
        rep = a.poll(self.path)
        self.assertEqual(rep["status"], "fault")
        self.assertIn("input_missing", rep["new_faults"])
        self.assertIsNone(rep["file"])
        write_rows(self.path, [header(), assistant("e1", "e0", stop="stop")])
        rep = a.poll(self.path)
        self.assertEqual(rep["status"], "ok")
        self.assertEqual(rep["summary"]["last_success"]["entry_id"], "e1")

    def test_unreadable_input_is_fault(self):
        rep = self.adapter().poll(self.tmp.name)  # a directory, not a file
        self.assertEqual(rep["status"], "fault")
        self.assertIn("input_unreadable", rep["new_faults"])

    def test_unsupported_version_poisons_scan(self):
        write_rows(self.path, [
            header(version=99),
            assistant("e1", "e0", stop="stop"),
        ])
        rep = self.adapter().poll(self.path)
        self.assertEqual(rep["status"], "fault")
        self.assertIn("unsupported_version", rep["new_faults"])
        s = rep["summary"]
        self.assertIsNone(s["session"])
        self.assertEqual(s["session_fault"], "unsupported_version")
        self.assertIsNone(s["last_success"])
        self.assertEqual(s["counters"]["skipped_schema_fault"], 1)

    def test_missing_and_string_version_header_accepted(self):
        write_rows(self.path, [header()])
        self.assertEqual(self.adapter().poll(self.path)["status"], "ok")
        path2 = os.path.join(self.tmp.name, "strver.jsonl")
        write_rows(path2, [row("e0", None, iso(T0), "session", version="3")])
        self.assertEqual(self.adapter().poll(path2)["status"], "ok")

    def test_missing_header_is_fault(self):
        write_rows(self.path, [assistant("e1", "e0", stop="stop")])
        rep = self.adapter().poll(self.path)
        self.assertEqual(rep["status"], "fault")
        self.assertIn("message_before_header", rep["new_faults"])
        self.assertIsNone(rep["summary"]["last_success"])

    def test_malformed_rows_skipped_next_processed(self):
        good = json.dumps(header()) + "\n"
        with open(self.path, "w") as f:
            f.write(good)
            f.write("{not json at all\n")
            f.write("[1,2,3]\n")
            f.write(json.dumps(
                assistant("e1", "e0", stop="stop")) + "\n")
        rep = self.adapter().poll(self.path)
        self.assertEqual(rep["status"], "fault")
        self.assertEqual(rep["new_faults"].get("malformed_row"), 2)
        self.assertEqual(rep["summary"]["last_success"]["entry_id"], "e1")

    def test_unknown_event_type_and_shapes_are_observable(self):
        write_rows(self.path, [
            header(),
            row("e1", "e0", iso(T0 + 1), "time_travel"),
            row("e2", "e0", iso(T0 + 2), "message", message={"role": "strange"}),
        ])
        rep = self.adapter().poll(self.path)
        self.assertEqual(rep["status"], "fault")
        self.assertIn("unknown_event_type", rep["new_faults"])
        self.assertIn("unknown_shape", rep["new_faults"])
        self.assertTrue(rep["summary"]["uncertainty"]["unknown_seen"])

    def test_oversized_row_skipped_without_unbounded_buffer(self):
        huge = json.dumps(row("h1", "e0", iso(T0 + 1), "title",
                              blob="x" * 5000))
        with open(self.path, "w") as f:
            f.write(json.dumps(header()) + "\n")
            f.write(huge + "\n")
            f.write(json.dumps(
                assistant("e1", "e0", stop="stop")) + "\n")
        a = self.adapter(max_row_bytes=512)
        rep = a.poll(self.path)
        self.assertEqual(rep["status"], "fault")
        self.assertGreaterEqual(rep["new_faults"].get("oversized_row", 0), 1)
        self.assertEqual(rep["summary"]["last_success"]["entry_id"], "e1")
        self.assertLessEqual(rep["tail_bytes"], 512)
        self.assertEqual(rep["offset"], os.path.getsize(self.path))

    def test_unterminated_oversized_tail_dropped_safely(self):
        with open(self.path, "w") as f:
            f.write(json.dumps(header()) + "\n")
            f.write("x" * 1000)  # partial row, never newline-terminated
        a = self.adapter(max_row_bytes=256)
        rep = a.poll(self.path)
        self.assertEqual(rep["status"], "fault")
        self.assertIn("oversized_row", rep["new_faults"])
        self.assertEqual(rep["tail_bytes"], 0)
        with open(self.path, "a") as f:
            f.write("\n" + json.dumps(
                assistant("e1", "e0", stop="stop")) + "\n")
        rep = a.poll(self.path)
        self.assertEqual(rep["summary"]["last_success"]["entry_id"], "e1")
        self.assertEqual(rep["offset"], os.path.getsize(self.path))

class TestBoundedReadsAndBacklog(Base):

    def test_byte_budget_reports_backlog_and_catches_up_once(self):
        rows = [header()]
        parent = "e0"
        for i in range(1, 9):
            rows.append(assistant("e%d" % i, parent, t=iso(T0 + i)))
            parent = "e%d" % i
        write_rows(self.path, rows)
        a = self.adapter(max_read_bytes=120)
        total = 0
        polls = 0
        while True:
            rep = a.poll(self.path)
            total += rep["events_processed"]
            polls += 1
            if not rep["backlog"]:
                break
            self.assertLess(polls, 50)
        self.assertEqual(total, len(rows))  # each row processed exactly once
        self.assertEqual(rep["summary"]["counters"]["duplicates"], 0)
        self.assertEqual(rep["summary"]["counters"]["successful_assistant"], 8)
        self.assertEqual(rep["offset"], os.path.getsize(self.path))

    def test_event_budget_caps_and_leftover_processed_next_poll(self):
        write_rows(self.path, [
            header(),
            assistant("e1", "e0", stop="stop"),
            assistant("e2", "e1", stop="stop"),
            assistant("e3", "e2", stop="stop"),
        ])
        a = self.adapter(max_events_per_poll=2)
        rep1 = a.poll(self.path)
        self.assertEqual(rep1["events_processed"], 2)
        self.assertTrue(rep1["backlog"])
        rep2 = a.poll(self.path)
        self.assertEqual(rep2["events_processed"], 2)
        self.assertFalse(rep2["backlog"])
        self.assertEqual(rep2["summary"]["counters"]["events"], 4)
        self.assertEqual(rep2["summary"]["last_success"]["entry_id"], "e3")


class TestCursorLifecycle(Base):

    def test_state_reload_continues_without_rescan(self):
        with open(self.path, "w") as f:
            f.write(json.dumps(header()) + "\n")
            f.write(json.dumps(assistant("e1", "e0", stop="stop")) + "\n")
            f.write(json.dumps(assistant("e2", "e1"))[:30])  # partial
        a = self.adapter()
        rep = a.poll(self.path)
        self.assertGreater(rep["tail_bytes"], 0)
        state = json.loads(json.dumps(a.export_state()))
        b = OmpSessionAdapter.from_state(state, clock=self.clock)
        with open(self.path, "a") as f:
            f.write(json.dumps(assistant("e2", "e1", stop="stop"))[30:] + "\n")
            f.write(json.dumps(assistant("e3", "e2", stop="stop")) + "\n")
        rep = b.poll(self.path)
        self.assertEqual(rep["events_processed"], 2)  # no replay of e0/e1
        self.assertEqual(rep["summary"]["counters"]["duplicates"], 0)
        self.assertEqual(rep["summary"]["last_success"]["entry_id"], "e3")
        self.assertEqual(rep["offset"], os.path.getsize(self.path))

    def test_truncation_rebuild_without_manufactured_progress(self):
        write_rows(self.path, [
            header(),
            assistant("e1", "e0", stop="stop"),
        ])
        a = self.adapter()
        a.poll(self.path)  # bootstrap over history
        write_rows(self.path, [assistant("e2", "e1", stop="stop")], mode="a")
        a.poll(self.path)
        self.assertTrue(a.snapshot()["last_success"]["live"])
        write_rows(self.path, [header(), assistant("e1", "e0", stop="stop")])
        self.clock.advance(30)
        rep = a.poll(self.path)
        self.assertEqual(rep["rebuilt"], "truncation")
        self.assertTrue(rep["history_replayed"])
        s = rep["summary"]
        self.assertEqual(s["counters"]["successful_assistant"], 1)
        self.assertFalse(s["last_success"]["live"])  # history, not live proof

    def test_rotation_same_session_replays_history_flagged(self):
        write_rows(self.path, [header(), assistant("e1", "e0", stop="stop")])
        a = self.adapter()
        a.poll(self.path)
        write_rows(self.path, [assistant("e2", "e1", stop="stop")], mode="a")
        a.poll(self.path)
        self.assertTrue(a.snapshot()["last_success"]["live"])
        rotated = os.path.join(self.tmp.name, "rotated.jsonl")
        write_rows(rotated, [
            header(),
            assistant("e1", "e0", stop="stop"),
            assistant("e2", "e1", stop="stop"),
        ])
        self.clock.advance(30)
        rep = a.poll(rotated)
        self.assertEqual(rep["rebuilt"], "rotation")
        self.assertFalse(rep["session_switch"])
        self.assertFalse(rep["summary"]["last_success"]["live"])
        self.assertEqual(rep["summary"]["counters"]["successful_assistant"], 2)

    def test_rotation_different_session_resets_semantics(self):
        write_rows(self.path, [
            header("e0"),
            assistant("e1", "e0", stop="error", errorId=7,
                      errorMessage=SECRET_ERROR),
        ])
        a = self.adapter()
        a.poll(self.path)
        other = os.path.join(self.tmp.name, "other.jsonl")
        write_rows(other, [header("f0"), assistant("f1", "f0", stop="stop")])
        rep = a.poll(other)
        self.assertEqual(rep["rebuilt"], "rotation")
        self.assertTrue(rep["session_switch"])
        s = rep["summary"]
        self.assertEqual(s["error_totals"]["assistant_error"], 0)
        self.assertEqual(s["counters"]["successful_assistant"], 1)
        self.assertEqual(s["session"]["header_id"], "f0")


class TestTimestampsAndSanitization(Base):

    def test_malformed_and_future_timestamps_not_progress_proof(self):
        write_rows(self.path, [
            header(),
            assistant("e1", "e0", t="not-a-timestamp", stop="stop"),
        ])
        s = self.adapter().poll(self.path)["summary"]
        ls = s["last_success"]
        self.assertEqual(ls["entry_id"], "e1")
        self.assertFalse(ls["ts_valid"])
        self.assertIsNone(ls["ts"])
        path2 = os.path.join(self.tmp.name, "future.jsonl")
        future = self.clock.now + 3600
        write_rows(path2, [
            header(),
            assistant("e1", "e0", t=iso(future), stop="stop"),
        ])
        rep = self.adapter().poll(path2)
        ls = rep["summary"]["last_success"]
        self.assertFalse(ls["ts_valid"])  # future ts flagged, not trusted
        self.assertIn("invalid_timestamp", rep["new_faults"])
        # freshness signal comes from poll-time observation, not the bad ts
        self.assertEqual(
            rep["summary"]["observation"]["last_append_at"], self.clock.now)

    def test_no_raw_sensitive_material_in_state_or_report(self):
        write_rows(self.path, [
            header(),
            row("u1", "e0", iso(T0 + 1), "message",
                message={"role": "user", "content": SECRET_CONTENT}),
            assistant("e1", "u1", stop="error", errorId=135168,
                      errorMessage=SECRET_ERROR,
                      content=[tool_call_part("tc1"),
                               {"type": "text", "text": SECRET_CONTENT}]),
            tool_result("t1", "e1", "tc1", is_error=True),
            row("ti", "t1", iso(T0 + 3), "title", title=SECRET_CONTENT),
        ])
        a = self.adapter()
        rep = a.poll(self.path)
        blob = self.dump(a, rep)
        for marker in (SECRET_CONTENT, SECRET_ARG, SECRET_ERROR, SECRET_CWD,
                       "/synthetic"):
            self.assertNotIn(marker, blob)
        # fingerprint of the error message is retained instead
        import hashlib
        fp = hashlib.sha256(SECRET_ERROR.encode()).hexdigest()[:16]
        self.assertIn(fp, blob)
        self.assertIn("135168", blob)  # structural errorId survives

    def test_unsafe_tool_names_hashed(self):
        weird = "drop table users;-- SECRET_ARG"
        write_rows(self.path, [
            header(),
            assistant("e1", "e0", stop="toolUse",
                      content=[tool_call_part("tc1", weird)]),
        ])
        s = self.adapter().poll(self.path)["summary"]
        pending = s["pending_tools"][0]
        self.assertEqual(pending["name_class"], "unknown")
        self.assertTrue(pending["name"].startswith("name:"))
        self.assertNotIn("SECRET", json.dumps(s))
        self.assertNotIn("drop table", json.dumps(s))
