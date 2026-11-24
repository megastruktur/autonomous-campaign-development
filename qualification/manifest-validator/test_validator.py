"""Synthetic, isolated contract fixtures; none represents a real provider review."""

from contextlib import ExitStack, redirect_stderr, redirect_stdout
from copy import deepcopy
from dataclasses import FrozenInstanceError, replace
import hashlib
import io
import json
import os
from pathlib import Path
import socket
import subprocess
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from validator import ExpectedIdentity, ValidatedManifest, ValidationError, validate_manifest


SRC = "/source/files/0/after"
TEST = "/source/files/1/after"
COV = "/review/coverage/files/0"
EVIDENCE = (
    ("/provenance/source_receipt", "evidence/source.txt", b"SYNTHETIC source provenance v1\n"),
    ("/provenance/diff", "evidence/diff.txt", b"SYNTHETIC two untracked additions v1\n"),
    ("/review/evidence/raw_output", "evidence/raw.json", b'{"schema_version":3,"summary":"synthetic fixture only","verdict":"pass","findings":[]}\n'),
    ("/review/evidence/provider_trace", "evidence/trace.txt", b"SYNTHETIC provider stop; tool-src and tool-test full reads\n"),
    ("/review/evidence/coverage_reconciliation", "evidence/coverage.txt", b"SYNTHETIC external coverage reconciliation v1\n"),
    ("/review/evidence/guard_receipt", "evidence/guards.txt", b"SYNTHETIC unchanged source config hooks v1\n"),
    ("/review/evidence/qualification_receipt", "evidence/qualification.txt", b"SYNTHETIC qualification receipt; not actual readiness\n"),
)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def get(packet, pointer):
    node = packet
    for part in pointer.strip("/").split("/") if pointer else ():
        node = node[int(part)] if isinstance(node, list) else node[part]
    return node


def put(packet, pointer, value):
    parent, key = pointer.rsplit("/", 1)
    node = get(packet, parent)
    node[int(key) if isinstance(node, list) else key] = value


class Packet:
    def __init__(self, root):
        self.root = root
        self.data = {
            "schema_version": 1, "packet_kind": "manifest-evidence",
            "source": {
                "repository_id": "fixture-repo", "revision": "fixture-source-v1",
                "base_revision": "a" * 40, "tip_revision": None,
                "snapshot_kind": "unborn", "inventory_complete": True,
                "files": [], "renames": [],
            },
            "scenario": {"id": "fixture-scenario", "revision": "v1"},
            "provenance": {},
            "review": {
                "engine": "roborev", "engine_version": "0.75.0", "execution_engine": "omp",
                "execution_engine_version": "19.1.1", "model": "fixture-model",
                "run_id": "fixture-review-v1", "author_id": "fixture-author",
                "reviewer_id": "fixture-reviewer", "verdict": "PASS",
                "bound_to": {
                    "repository_id": "fixture-repo", "source_revision": "fixture-source-v1",
                    "scenario_id": "fixture-scenario", "scenario_revision": "v1",
                },
                "completion": {
                    "status": "complete", "exit_code": 0, "provider_stop_reason": "stop",
                    "provider_error": None, "tool_errors": [], "truncated": False,
                },
                "evidence": {}, "coverage": {"complete": True, "files": []}, "findings": [],
            },
        }
        for logical, path, role, data, tool in (
            ("src/pilot.py", "candidate/src/pilot.py", "source", b"value = 1\n", "tool-src"),
            ("tests/test_pilot.py", "candidate/tests/test_pilot.py", "test", b"assert 1 == 1\n", "tool-test"),
        ):
            blob = self.blob(path, data)
            self.data["source"]["files"].append({
                "path": logical, "role": role, "origin": "untracked", "before": None, "after": blob,
            })
            self.cover(blob, tool=tool)
        for pointer, path, data in EVIDENCE:
            put(self.data, pointer, self.blob(path, data))

    def blob(self, path, data):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        return {"path": path, "sha256": sha(data), "size_bytes": len(data)}

    def cover(self, blob, *, tool="tool-read", spans=None):
        data = (self.root / blob["path"]).read_bytes()
        lines = data.split(b"\n")
        if lines[-1] == b"":
            lines.pop()
        count = len(lines)
        # Split only at LF, retaining CR as ordinary bytes.
        chunks = [line + b"\n" for line in data.split(b"\n")[:-1]]
        if data and not data.endswith(b"\n"):
            chunks.append(data.rsplit(b"\n", 1)[-1])
        ranges = []
        for start, end in spans if spans is not None else ([(1, count)] if count else []):
            ranges.append({"start_line": start, "end_line": end, "tool_id": tool,
                           "sha256": sha(b"".join(chunks[start - 1:end]))})
        row = {"path": blob["path"], "sha256": blob["sha256"], "total_lines": count,
               "empty_tool_id": tool if not count else None, "ranges": ranges}
        rows = self.data["review"]["coverage"]["files"]
        for index, old in enumerate(rows):
            if old["path"] == blob["path"]:
                rows[index] = row
                break
        else:
            rows.append(row)
        return row

    def source_bytes(self, data, index=0, spans=None):
        entry = self.data["source"]["files"][index]
        entry["after"] = self.blob(entry["after"]["path"], data)
        return self.cover(entry["after"], spans=spans)

    def baseline(self):
        source = self.data["source"]
        source["snapshot_kind"], source["tip_revision"] = "uncommitted", "b" * 40
        entry = source["files"][0]
        entry["origin"] = "tracked"
        entry["before"] = self.blob("baseline/src/pilot.py", b"value = 0\n")
        self.cover(entry["before"])
        return entry["before"]

    def rename(self):
        old = {"path": "src/old.py", "role": "source", "origin": "tracked",
               "before": self.blob("baseline/src/old.py", b"old = True\n"), "after": None}
        self.data["source"]["files"].append(old)
        self.cover(old["before"])
        self.data["source"]["renames"] = [{"from": "src/old.py", "to": "src/pilot.py"}]

    def pin(self, raw=None):
        if raw is None:
            raw = (json.dumps(self.data, sort_keys=True, ensure_ascii=True, separators=(",", ":")) + "\n").encode()
        (self.root / "manifest.json").write_bytes(raw)
        return ExpectedIdentity(sha(raw), "fixture-repo", "fixture-source-v1", "fixture-scenario", "v1")

    def validate(self):
        return validate_manifest(self.root, "manifest.json", expected=self.pin())


class ValidatorTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.packet = Packet(self.root)

    def error(self, code, field, *, expected=None, root=None, manifest="manifest.json"):
        if expected is None:
            expected = self.packet.pin()
        with self.assertRaises(ValidationError) as caught:
            validate_manifest(self.root if root is None else root, manifest, expected=expected)
        self.assertEqual((caught.exception.code, caught.exception.field), (code, field))
        self.assertNotIn(str(self.root), caught.exception.message)
        return caught.exception

    def mutants(self, cases):
        original = deepcopy(self.packet.data)
        for pointer, value, code, field in cases:
            with self.subTest(pointer=pointer, value=value):
                self.packet.data = deepcopy(original)
                put(self.packet.data, pointer, value)
                self.error(code, field or pointer)
        self.packet.data = original

    def tree(self):
        return {str(path.relative_to(self.root)): path.read_bytes()
                for path in self.root.rglob("*") if path.is_file()}

    def test_v01_deterministic_identity_frozen_result_no_writes(self):
        expected = self.packet.pin()
        before = self.tree()
        result = validate_manifest(self.root, "manifest.json", expected=expected)
        self.assertEqual(result, ValidatedManifest(expected.manifest_sha256, "fixture-repo",
                         "fixture-source-v1", "fixture-scenario", "v1", 2, 7))
        self.assertEqual(before, self.tree())
        with self.assertRaises(FrozenInstanceError):
            result.file_count = 8
        with tempfile.TemporaryDirectory() as other:
            fixture = Packet(Path(other))
            self.assertEqual(fixture.pin(), expected)
            self.assertEqual((Path(other) / "manifest.json").read_bytes(), before["manifest.json"])

    def test_v02_baseline_and_identical_context(self):
        self.packet.baseline()
        entry = self.packet.data["source"]["files"][1]
        entry["origin"], entry["before"] = "tracked", deepcopy(entry["after"])
        self.assertEqual(self.packet.validate().file_count, 3)

    def test_v03_edited_rename(self):
        self.packet.rename()
        self.assertEqual(self.packet.validate().file_count, 3)

    def test_v04_raw_newlines_and_multiranges(self):
        row = self.packet.source_bytes(b"one\r\ntwo\rthree\nfour", spans=[(1, 1), (2, 3)])
        row["ranges"][1]["tool_id"] = "different-tool"
        self.assertEqual(self.packet.validate().file_count, 2)

    def test_v05_empty_file_requires_coverage(self):
        self.packet.source_bytes(b"", index=1)
        self.assertEqual(self.packet.validate().file_count, 2)
        self.packet.data["review"]["coverage"]["files"].pop()
        self.error("E_COVERAGE", "/review/coverage/files")

    def test_v06_findings(self):
        self.packet.data["review"]["findings"] = [{"id": "f1", "severity": "low"}]
        self.assertEqual(self.packet.validate().evidence_count, 7)
        self.mutants([("/review/findings/0/severity", severity, "E_REVIEW", None)
                      for severity in ("medium", "high", "critical")])

    def test_j01_strict_json_and_depth_before_payload_access(self):
        for raw, code in ((b"{", "E_JSON"), (b"\xff", "E_JSON"), (b"\xef\xbb\xbf{}", "E_JSON"),
                          (b'{"x":1,"x":2}', "E_JSON"), (b"NaN", "E_JSON"),
                          (b"Infinity", "E_JSON"), (b"-Infinity", "E_JSON"), (b"1e9999", "E_JSON"),
                          (b"[" * 33 + b"0" + b"]" * 33, "E_LIMIT")):
            with self.subTest(raw=raw[:40]):
                expected = self.packet.pin(raw)
                with patch("os.read", wraps=os.read) as reader:
                    self.error(code, "/", expected=expected)
                    self.assertLessEqual(reader.call_count, 2)
        error = self.error("E_JSON", "/", expected=self.packet.pin(b'{"known":0,"known":1}'))
        self.assertIn("known", error.message)

    def test_j02_all_object_kinds_missing_extra_and_wrong_container(self):
        self.packet.rename()
        self.packet.data["review"]["findings"] = [{"id": "f1", "severity": "low"}]
        original = deepcopy(self.packet.data)
        objects = ("", "/source", "/source/files/0", SRC, "/source/renames/0", "/scenario",
                   "/provenance", "/provenance/source_receipt", "/review", "/review/bound_to", "/review/completion",
                   "/review/evidence", "/review/coverage", COV, COV + "/ranges/0", "/review/findings/0")
        for pointer in objects:
            for kind in ("missing", "extra", "null", "array"):
                with self.subTest(pointer=pointer, kind=kind):
                    self.packet.data = deepcopy(original)
                    obj = get(self.packet.data, pointer)
                    key = next(iter(obj))
                    if kind == "missing":
                        del obj[key]
                        obj["extra"] = True
                        field = pointer + "/" + key
                    elif kind == "extra":
                        obj["a/b~c"] = True
                        field = pointer + "/a~1b~0c"
                    else:
                        replacement = None if kind == "null" else []
                        if pointer:
                            put(self.packet.data, pointer, replacement)
                        else:
                            self.packet.data = replacement
                        field = pointer or "/"
                    code = "E_PROVENANCE" if pointer == SRC and kind == "null" else "E_SCHEMA"
                    self.error(code, field)
        self.packet.data = original
        self.mutants([(p, None, "E_SCHEMA", None) for p in
                      ("/source/files", "/source/renames", "/review/findings", "/review/completion/tool_errors",
                       "/review/coverage/files", COV + "/ranges", "/source/revision", "/source/inventory_complete")])

    def test_j03_integer_types_hashes_enums_and_text(self):
        pointers = ("/schema_version", SRC + "/size_bytes", "/provenance/diff/size_bytes",
                    "/review/completion/exit_code", COV + "/total_lines",
                    COV + "/ranges/0/start_line", COV + "/ranges/0/end_line")
        cases = [(p, v, "E_SCHEMA", None) for p in pointers for v in (True, 1.0)]
        cases += [(p, v, "E_SCHEMA", None) for p in (SRC + "/sha256", "/source/base_revision")
                  for v in ("A" * 64, "abc", None)]
        cases += [("/schema_version", 2, "E_SCHEMA", None), ("/review/engine", "ocr", "E_SCHEMA", None),
                  ("/source/files/0/role", "other", "E_SCHEMA", None),
                  ("/review/completion/provider_error", "bad\x00", "E_SCHEMA", None),
                  ("/review/completion/provider_error", "\ud800", "E_SCHEMA", None),
                  ("/review/model", "has space", "E_SCHEMA", None)]
        self.mutants(cases)

    def test_i01_expected_identities_required(self):
        expected = self.packet.pin()
        for key in expected.__dataclass_fields__:
            for value in (None, "", "bad value", True):
                with self.subTest(key=key, value=value):
                    self.error("E_EXPECTED", "/expected/" + key, expected=replace(expected, **{key: value}))
        self.error("E_EXPECTED", "/expected/manifest_sha256", expected={})

    def test_i02_i03_identity_binding(self):
        expected = self.packet.pin()
        for key, field in (("repository_id", "/source/repository_id"), ("source_revision", "/source/revision"),
                           ("scenario_id", "/scenario/id"), ("scenario_revision", "/scenario/revision")):
            with self.subTest(key=key):
                self.error("E_IDENTITY", field, expected=replace(expected, **{key: "different"}))
        self.mutants([("/review/bound_to/" + key, "stale", "E_IDENTITY", None)
                      for key in self.packet.data["review"]["bound_to"]])

    def test_i04_pinned_bytes_cannot_drop_obligation(self):
        expected = self.packet.pin()
        manifest = self.root / "manifest.json"
        manifest.write_bytes(manifest.read_bytes() + b" ")
        self.error("E_MANIFEST_HASH", "/manifest_path", expected=expected)
        self.packet.data["source"]["files"].pop()
        self.packet.data["review"]["coverage"]["files"].pop()
        self.packet.pin()
        self.error("E_MANIFEST_HASH", "/manifest_path", expected=expected)

    def test_p01_p02_source_relations(self):
        source = self.packet.data["source"]
        self.mutants([
            ("/source/files", [], "E_PROVENANCE", None),
            ("/source/inventory_complete", False, "E_PROVENANCE", None),
            ("/source/files/0/role", "test", "E_PROVENANCE", "/source/files"),
            ("/source/files/1/path", source["files"][0]["path"], "E_PROVENANCE", None),
            (SRC, None, "E_PROVENANCE", None),
            ("/source/files/0/before", deepcopy(source["files"][0]["after"]), "E_PROVENANCE", None),
            ("/source/tip_revision", "a" * 40, "E_PROVENANCE", None),
            ("/source/snapshot_kind", "uncommitted", "E_PROVENANCE", "/source/tip_revision"),
        ])
        self.packet.data["source"]["files"][0]["origin"] = "required_ignored"
        self.assertEqual(self.packet.validate().file_count, 2)

    def test_p03_rename_relations(self):
        self.packet.rename()
        rename = deepcopy(self.packet.data["source"]["renames"][0])
        self.mutants([
            ("/source/renames/0/from", "absent.py", "E_PROVENANCE", None),
            ("/source/renames/0/from", "tests/test_pilot.py", "E_PROVENANCE", None),
            ("/source/renames/0/to", "src/old.py", "E_PROVENANCE", None),
            ("/source/renames", [rename, rename], "E_PROVENANCE", "/source/renames/1/from"),
        ])

    def test_p04_blob_conflicts_and_roles(self):
        self.packet.baseline()
        after = deepcopy(get(self.packet.data, SRC))
        conflict = {**after, "sha256": "0" * 64}
        self.mutants([
            (TEST, conflict, "E_PROVENANCE", TEST + "/path"),
            (TEST, after, "E_PATH", TEST + "/path"),
            (SRC + "/path", "manifest.json", "E_PATH", None),
            ("/provenance/diff/path", after["path"], "E_PATH", None),
            ("/provenance/diff/path", "manifest.json", "E_PATH", None),
            ("/review/evidence/raw_output/path", "evidence/diff.txt", "E_PATH", None),
        ])

    def test_r01_r02_r03_r04_review_and_completion(self):
        cases = [("/review/verdict", v, "E_REVIEW", None) for v in ("FAIL", "INCONCLUSIVE", "INVALIDATED", None)]
        cases += [("/review/verdict", v, "E_SCHEMA", None) for v in ("pass", "unknown")]
        prefix = "/review/completion/"
        cases += [(prefix + "status", v, "E_REVIEW", None) for v in ("partial", "failed", "skipped", "unknown")]
        cases += [(prefix + "exit_code", v, "E_REVIEW", None) for v in (None, 1, -1)]
        cases += [(prefix + "provider_stop_reason", v, "E_REVIEW", None) for v in (None, "end_turn", "length")]
        cases += [(prefix + "provider_error", "failure", "E_REVIEW", None),
                  (prefix + "tool_errors", ["read failed"], "E_REVIEW", None),
                  (prefix + "truncated", True, "E_REVIEW", None),
                  ("/review/reviewer_id", "fixture-author", "E_REVIEW", None),
                  ("/review/findings", [{"id": "x", "severity": "other"}], "E_SCHEMA", "/review/findings/0/severity"),
                  ("/review/findings", [{"id": "x", "severity": "low"}] * 2, "E_SCHEMA", "/review/findings/1/id")]
        self.mutants(cases)

    def test_c01_coverage_set(self):
        rows = deepcopy(self.packet.data["review"]["coverage"]["files"])
        self.mutants([
            ("/review/coverage/complete", False, "E_COVERAGE", None),
            ("/review/coverage/files", [], "E_COVERAGE", None),
            ("/review/coverage/files", rows[:1], "E_COVERAGE", None),
            ("/review/coverage/files", rows + [rows[0]], "E_COVERAGE", "/review/coverage/files/2/path"),
            (COV + "/path", "extra.txt", "E_COVERAGE", None),
        ])

    def test_c02_c03_range_and_eof_contract(self):
        self.packet.source_bytes(b"one\ntwo\nthree", spans=[(1, 1), (2, 3)])
        self.mutants([
            (COV + "/sha256", "0" * 64, "E_COVERAGE", None),
            (COV + "/total_lines", 4, "E_COVERAGE", COV + "/ranges"),
            (COV + "/ranges/0/start_line", 2, "E_COVERAGE", None),
            (COV + "/ranges/1/start_line", 1, "E_COVERAGE", None),
            (COV + "/ranges/1/start_line", 3, "E_COVERAGE", None),
            (COV + "/ranges/1/end_line", 1, "E_COVERAGE", None),
            (COV + "/ranges/1/end_line", 4, "E_COVERAGE", None),
            (COV + "/ranges/0/sha256", "0" * 64, "E_COVERAGE", None),
            (COV + "/ranges/0/tool_id", None, "E_SCHEMA", None),
            (COV + "/empty_tool_id", "eof", "E_COVERAGE", None),
        ])
        row = self.packet.source_bytes(b"one\ntwo\n")
        row["total_lines"] = 1
        row["ranges"][0]["end_line"] = 1
        self.error("E_COVERAGE", COV + "/total_lines")
        self.packet.source_bytes(b"")
        self.mutants([(COV + "/empty_tool_id", None, "E_COVERAGE", None),
                      (COV + "/ranges", [{"start_line": 1, "end_line": 1, "tool_id": "x", "sha256": "0" * 64}],
                       "E_COVERAGE", None)])

    def test_c04_required_text(self):
        for raw in (b"\xff\n", b"nul\x00\n"):
            with self.subTest(raw=raw):
                self.packet.source_bytes(raw)
                self.error("E_TEXT", SRC + "/path")

    def test_f01_missing_every_required_file(self):
        baseline = self.packet.baseline()
        expected = self.packet.pin()
        cases = [("manifest.json", "/manifest_path"),
                 ("candidate/src/pilot.py", SRC + "/path"),
                 (baseline["path"], "/source/files/0/before/path")]
        cases += [(path, pointer + "/path") for pointer, path, _ in EVIDENCE]
        for path, field in cases:
            with self.subTest(path=path):
                target = self.root / path
                data = target.read_bytes()
                target.unlink()
                self.error("E_MISSING", field, expected=expected)
                target.write_bytes(data)

    def test_f02_f03_drift_sizes_and_empty_evidence(self):
        baseline = self.packet.baseline()
        expected = self.packet.pin()
        cases = [("candidate/src/pilot.py", SRC), (baseline["path"], "/source/files/0/before")]
        cases += [(path, pointer) for pointer, path, _ in EVIDENCE]
        for path, pointer in cases:
            with self.subTest(path=path):
                target = self.root / path
                data = target.read_bytes()
                target.write_bytes(b"X" + data[1:])
                self.error("E_HASH", pointer + "/sha256", expected=expected)
                target.write_bytes(data + b"X")
                self.error("E_SIZE", pointer + "/size_bytes", expected=expected)
                target.write_bytes(data)
        self.mutants([(pointer + "/size_bytes", 0, "E_SCHEMA", None) for pointer, _, _ in EVIDENCE])

    def test_s01_lexical_paths_before_open(self):
        paths = ("/etc/passwd", "../sentinel", "a/../b", "a//b", "a\\b", "C:/file", "//server/file",
                 "percent%20name", "a\x00b", "a\nb", "", "a" * 513, "/".join(["a"] * 33), "é", "a/.")
        for value in paths:
            with self.subTest(value=value):
                expected = self.packet.pin()
                self.error("E_PATH", "/manifest_path", manifest=value, expected=expected)
        self.mutants([(SRC + "/path", value, "E_PATH", None) for value in paths])
        # A bad later lexical path outranks an earlier missing payload.
        (self.root / "candidate/src/pilot.py").unlink()
        put(self.packet.data, "/review/evidence/qualification_receipt/path", "../outside")
        self.error("E_PATH", "/review/evidence/qualification_receipt/path")

    def test_s02_root_and_payload_symlinks(self):
        with tempfile.TemporaryDirectory() as outside:
            sentinel = Path(outside) / "sentinel"
            sentinel.write_bytes(b"outside sentinel")
            root_link = Path(outside) / "root-link"
            root_link.symlink_to(self.root, target_is_directory=True)
            self.error("E_ROOT", "/root", root=root_link)
            self.error("E_ROOT", "/root", root=Path("relative"))
            self.error("E_ROOT", "/root", root=self.root / "absent")
            self.error("E_ROOT", "/root", root=self.root / "candidate/src/pilot.py")
            target = self.root / "candidate/src/pilot.py"
            data = target.read_bytes()
            for destination in (sentinel, Path(outside) / "missing", self.root / "evidence/source.txt"):
                with self.subTest(destination=destination.name):
                    target.unlink()
                    target.symlink_to(destination)
                    self.error("E_PATH", SRC + "/path")
            target.unlink()
            target.write_bytes(data)
            directory = self.root / "candidate/src"
            directory.rename(self.root / "preserved-src")
            directory.symlink_to(self.root / "preserved-src", target_is_directory=True)
            self.error("E_PATH", SRC + "/path")
            self.assertEqual(sentinel.read_bytes(), b"outside sentinel")

    def test_s03_nonregular_hardlink_no_block(self):
        target = self.root / "candidate/src/pilot.py"
        target.unlink()
        target.mkdir()
        self.error("E_IO", SRC + "/path")
        target.rmdir()
        os.mkfifo(target)
        self.error("E_IO", SRC + "/path")
        target.unlink()
        with socket.socket(socket.AF_UNIX) as sock:
            sock.bind(str(target))
            self.error("E_IO", SRC + "/path")
        target.unlink()
        os.link(self.root / "evidence/source.txt", target)
        self.error("E_IO", SRC + "/path")

    def test_s04_platform_and_read_denial(self):
        expected = self.packet.pin()
        for flag in ("O_NOFOLLOW", "O_DIRECTORY", "O_NONBLOCK"):
            with self.subTest(flag=flag), patch.object(os, flag, 0):
                self.error("E_PLATFORM", "/", expected=expected)
        with patch.object(os, "supports_dir_fd", set()):
            self.error("E_PLATFORM", "/", expected=expected)
        real_open = os.open

        def denied(path, flags, **kwargs):
            if path == "pilot.py":
                raise PermissionError("sensitive host text")
            return real_open(path, flags, **kwargs)

        with patch.object(os, "open", side_effect=denied) as mocked:
            with patch.object(os, "supports_dir_fd", os.supports_dir_fd | {mocked}):
                error = self.error("E_IO", SRC + "/path", expected=expected)
                self.assertNotIn("sensitive", error.message)

    def test_s05_declared_count_and_range_limits(self):
        source = deepcopy(self.packet.data["source"]["files"][0])
        row = deepcopy(self.packet.data["review"]["coverage"]["files"][0])
        span = deepcopy(row["ranges"][0])
        self.mutants([
            (SRC + "/size_bytes", 16777217, "E_LIMIT", None),
            ("/source/files", [source] * 129, "E_LIMIT", None),
            ("/review/findings", [{"id": "x", "severity": "low"}] * 129, "E_LIMIT", None),
            ("/review/coverage/files", [row] * 257, "E_LIMIT", None),
            (COV + "/ranges", [span] * 4097, "E_LIMIT", None),
            (COV + "/ranges/0/end_line", 16777217, "E_LIMIT", None),
        ])
        rows = self.packet.data["review"]["coverage"]["files"]
        rows[0]["ranges"] = [span] * 2049
        rows[1]["ranges"] = [span] * 2048
        self.error("E_LIMIT", "/review/coverage/files/1/ranges")

    def test_s05_aggregate_and_actual_limits(self):
        original = deepcopy(self.packet.data)
        for pointer in (SRC, TEST, "/provenance/source_receipt", "/provenance/diff"):
            put(self.packet.data, pointer + "/size_bytes", 16777216)
        self.error("E_LIMIT", "/review/evidence/raw_output/size_bytes")
        self.packet.data = original
        expected = self.packet.pin()
        source = self.root / "candidate/src/pilot.py"
        with source.open("wb") as stream:
            stream.truncate(16777217)
        self.error("E_LIMIT", SRC + "/path", expected=expected)
        with (self.root / "manifest.json").open("wb") as stream:
            stream.truncate(1048577)
        self.error("E_LIMIT", "/manifest_path", expected=expected)

    def test_s06_metadata_change_closes_descriptors(self):
        expected = self.packet.pin()
        target = self.root / "candidate/src/pilot.py"
        inode = target.stat().st_ino
        original = os.fstat
        calls = 0

        def changed(fd):
            nonlocal calls
            info = original(fd)
            if info.st_ino == inode:
                calls += 1
                if calls == 2:
                    fields = {key: getattr(info, key) for key in
                              ("st_dev", "st_ino", "st_size", "st_mtime_ns", "st_ctime_ns", "st_mode", "st_nlink")}
                    fields["st_mtime_ns"] += 1
                    return SimpleNamespace(**fields)
            return info

        before = set(os.listdir("/proc/self/fd"))
        with patch.object(os, "fstat", side_effect=changed):
            self.error("E_FILE_CHANGED", SRC + "/path", expected=expected)
        self.assertEqual(before, set(os.listdir("/proc/self/fd")))

    def test_reads_each_distinct_blob_once_in_contract_order(self):
        self.packet.baseline()
        entry = self.packet.data["source"]["files"][1]
        entry["origin"], entry["before"] = "tracked", deepcopy(entry["after"])
        expected = self.packet.pin()
        real_open = os.open
        leaves = []

        def observed(path, flags, **kwargs):
            if not flags & os.O_DIRECTORY:
                leaves.append(path)
            return real_open(path, flags, **kwargs)

        with patch.object(os, "open", side_effect=observed) as mocked:
            with patch.object(os, "supports_dir_fd", os.supports_dir_fd | {mocked}):
                result = validate_manifest(self.root, "manifest.json", expected=expected)
        self.assertEqual(result.file_count, 3)
        self.assertEqual(leaves, ["manifest.json", "pilot.py", "pilot.py", "test_pilot.py",
                                 "source.txt", "diff.txt", "raw.json", "trace.txt", "coverage.txt",
                                 "guards.txt", "qualification.txt"])

    def test_actual_stream_excess_is_bounded_even_if_stat_understates_size(self):
        expected = self.packet.pin()
        target = self.root / "candidate/src/pilot.py"
        inode = target.stat().st_ino
        real_stat, real_read = os.fstat, os.read
        delivered = 0

        def oversized(fd, count):
            nonlocal delivered
            if real_stat(fd).st_ino == inode:
                delivered += count
                return b"x" * count
            return real_read(fd, count)

        with patch.object(os, "read", side_effect=oversized):
            self.error("E_LIMIT", SRC + "/path", expected=expected)
        self.assertEqual(delivered, 16777217)

    def test_exact_depth_limit_and_braces_inside_json_strings(self):
        expected = self.packet.pin(b"[" * 32 + b"0" + b"]" * 32)
        self.error("E_SCHEMA", "/", expected=expected)
        put(self.packet.data, "/review/completion/provider_error", "[" * 100 + '"\\\\')
        self.error("E_REVIEW", "/review/completion/provider_error")

    def test_root_and_manifest_failures_are_structured(self):
        expected = self.packet.pin()
        self.error("E_ROOT", "/root", root=Path("/invalid\x00root"), expected=expected)
        self.error("E_ROOT", "/root", root="/not-a-path-object", expected=expected)
        manifest = self.root / "manifest.json"
        manifest.unlink()
        manifest.symlink_to(self.root / "evidence/raw.json")
        self.error("E_PATH", "/manifest_path", expected=expected)

    def test_schema_paths_all_admitted_before_review_or_payload(self):
        self.packet.data["review"]["verdict"] = "FAIL"
        put(self.packet.data, "/review/coverage/files/1/path", "../escape")
        self.error("E_PATH", "/review/coverage/files/1/path")

    def test_io_read_error_closes_descriptors_and_hides_os_text(self):
        expected = self.packet.pin()
        inode = (self.root / "candidate/src/pilot.py").stat().st_ino
        real_read = os.read

        def denied(fd, count):
            if os.fstat(fd).st_ino == inode:
                raise OSError("secret location /unrelated/private")
            return real_read(fd, count)

        before = set(os.listdir("/proc/self/fd"))
        with patch.object(os, "read", side_effect=denied):
            error = self.error("E_IO", SRC + "/path", expected=expected)
            self.assertNotIn("secret", error.message)
        self.assertEqual(before, set(os.listdir("/proc/self/fd")))

    def test_s07_s08_no_execution_printing_or_mutation(self):
        marker = self.root / "should-not-exist"
        self.packet.source_bytes(f"__import__('pathlib').Path({str(marker)!r}).touch()\n".encode())
        put(self.packet.data, "/provenance/diff", self.packet.blob("evidence/diff.txt", b"$(touch never); exec('bad')\n"))
        expected = self.packet.pin()
        before = self.tree()
        out, err = io.StringIO(), io.StringIO()
        with ExitStack() as stack:
            for target in ("subprocess.Popen", "subprocess.run", "os.system", "os.execve", "socket.socket"):
                stack.enter_context(patch(target, side_effect=AssertionError("forbidden execution")))
            stack.enter_context(redirect_stdout(out))
            stack.enter_context(redirect_stderr(err))
            self.assertEqual(validate_manifest(self.root, "manifest.json", expected=expected).file_count, 2)
            self.error("E_MANIFEST_HASH", "/manifest_path", expected=replace(expected, manifest_sha256="0" * 64))
        self.assertEqual((out.getvalue(), err.getvalue()), ("", ""))
        self.assertEqual(before, self.tree())
        self.assertFalse(marker.exists())
        self.packet.data["command"] = "touch should-not-exist"
        self.error("E_SCHEMA", "/command")
        self.assertFalse(marker.exists())


if __name__ == "__main__":
    unittest.main()
