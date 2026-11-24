"""Read-only consistency checker for externally pinned manifest-evidence v1.

Success is not independent review or product acceptance. The caller must supply
a private quiescent snapshot and independently reconcile raw review evidence.
"""

from dataclasses import dataclass
import errno
import hashlib
import json
import math
import os
from pathlib import Path
import re
import stat
import unicodedata


@dataclass(frozen=True)
class ExpectedIdentity:
    manifest_sha256: str
    repository_id: str
    source_revision: str
    scenario_id: str
    scenario_revision: str


@dataclass(frozen=True)
class ValidatedManifest:
    manifest_sha256: str
    repository_id: str
    source_revision: str
    scenario_id: str
    scenario_revision: str
    file_count: int
    evidence_count: int


class ValidationError(ValueError):
    def __init__(self, code: str, field: str, message: str):
        self.code = code
        self.field = field
        self.message = message
        super().__init__(f"{code} {field}: {message}")


_MANIFEST_LIMIT = 1048576
_FILE_LIMIT = 16777216
_TOTAL_LIMIT = 67108864
_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:/@+-]{0,199}")
_SHA = re.compile(r"[0-9a-f]{64}")
_OID = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})")
_SEGMENT = re.compile(r"[A-Za-z0-9_.-]+")


def _fail(code, field, message):
    raise ValidationError(code, field or "/", message)


def _pointer(parent, key):
    return parent + "/" + str(key).replace("~", "~0").replace("/", "~1")


def _path(value, field):
    if not isinstance(value, str) or not value or len(value) > 512:
        _fail("E_PATH", field, "expected a bounded relative POSIX path")
    parts = value.split("/")
    if len(parts) > 32 or any(
        part in (".", "..") or _SEGMENT.fullmatch(part) is None for part in parts
    ):
        _fail("E_PATH", field, "unsafe or unsupported path")


_BLOB = {"path": "path", "sha256": "sha", "size_bytes": "count"}
_EVIDENCE_BLOB = {**_BLOB, "size_bytes": ("integer", 1, _FILE_LIMIT)}
_SOURCE_FILE = {
    "path": "path", "role": ("enum", ("source", "test", "dependency")),
    "origin": ("enum", ("tracked", "untracked", "required_ignored")),
    "before": ("nullable", _BLOB), "after": ("nullable", _BLOB),
}
_RANGE = {
    "start_line": ("integer", 1, _FILE_LIMIT),
    "end_line": ("integer", 1, _FILE_LIMIT), "tool_id": "id", "sha256": "sha",
}
_COVERED = {
    "path": "path", "sha256": "sha", "total_lines": "count",
    "empty_tool_id": ("nullable", "id"), "ranges": ("array", _RANGE, 4096),
}
_BINDING = {
    "repository_id": "id", "source_revision": "id",
    "scenario_id": "id", "scenario_revision": "id",
}
_SCHEMA = {
    "schema_version": ("integer", 1, 1),
    "packet_kind": ("enum", ("manifest-evidence",)),
    "source": {
        "repository_id": "id", "revision": "id", "base_revision": "oid",
        "tip_revision": ("nullable", "oid"),
        "snapshot_kind": ("enum", ("uncommitted", "unborn")),
        "inventory_complete": "bool", "files": ("array", _SOURCE_FILE, 128),
        "renames": ("array", {"from": "path", "to": "path"}, None),
    },
    "scenario": {"id": "id", "revision": "id"},
    "provenance": {"source_receipt": _EVIDENCE_BLOB, "diff": _EVIDENCE_BLOB},
    "review": {
        "engine": ("enum", ("roborev",)), "engine_version": "id",
        "execution_engine": ("enum", ("omp",)), "execution_engine_version": "id",
        "model": "id", "run_id": "id", "author_id": "id", "reviewer_id": "id",
        "verdict": ("nullable", ("enum", ("PASS", "FAIL", "INCONCLUSIVE", "INVALIDATED"))),
        "bound_to": _BINDING,
        "completion": {
            "status": ("enum", ("complete", "partial", "failed", "skipped", "unknown")),
            "exit_code": ("nullable", ("integer", -255, 255)),
            "provider_stop_reason": ("nullable", "id"),
            "provider_error": ("nullable", "text"),
            "tool_errors": ("array", "text", None), "truncated": "bool",
        },
        "evidence": {
            "raw_output": _EVIDENCE_BLOB, "provider_trace": _EVIDENCE_BLOB,
            "coverage_reconciliation": _EVIDENCE_BLOB, "guard_receipt": _EVIDENCE_BLOB,
            "qualification_receipt": _EVIDENCE_BLOB,
        },
        "coverage": {"complete": "bool", "files": ("array", _COVERED, 256)},
        "findings": ("array", {
            "id": "id", "severity": ("enum", ("critical", "high", "medium", "low")),
        }, 128),
    },
}


def _schema(value, shape, field="", counters=None):
    if counters is None:
        counters = {"ranges": 0}
    if isinstance(shape, dict):
        if not isinstance(value, dict):
            _fail("E_SCHEMA", field, "expected an object")
        for key in shape:
            if key not in value:
                _fail("E_SCHEMA", _pointer(field, key), "required member is missing")
        for key in value:
            if key not in shape:
                _fail("E_SCHEMA", _pointer(field, key), "unexpected member")
        for key, child in shape.items():
            _schema(value[key], child, _pointer(field, key), counters)
        return
    if isinstance(shape, tuple):
        kind = shape[0]
        if kind == "nullable":
            if value is not None:
                _schema(value, shape[1], field, counters)
            return
        if kind == "array":
            if not isinstance(value, list):
                _fail("E_SCHEMA", field, "expected an array")
            if shape[2] is not None and len(value) > shape[2]:
                _fail("E_LIMIT", field, "array count exceeds admission limit")
            if shape[1] is _RANGE:
                counters["ranges"] += len(value)
                if counters["ranges"] > 4096:
                    _fail("E_LIMIT", field, "total coverage range limit exceeded")
            for index, child in enumerate(value):
                _schema(child, shape[1], _pointer(field, index), counters)
            return
        if kind == "enum":
            if not isinstance(value, str) or value not in shape[1]:
                _fail("E_SCHEMA", field, "unsupported literal value")
            return
        if type(value) is not int:
            _fail("E_SCHEMA", field, "expected an integer")
        if value < shape[1] or value > shape[2]:
            code = "E_LIMIT" if shape[2] == _FILE_LIMIT and value > shape[2] else "E_SCHEMA"
            _fail(code, field, "integer outside admitted range")
        return
    if shape == "path":
        _path(value, field)
    elif shape == "count":
        _schema(value, ("integer", 0, _FILE_LIMIT), field, counters)
    elif shape == "bool":
        if type(value) is not bool:
            _fail("E_SCHEMA", field, "expected a boolean")
    elif shape == "text":
        if (not isinstance(value, str) or not 1 <= len(value) <= 4096
                or any((unicodedata.category(char) in ("Cc", "Cs"))
                       and char not in "\n\t" for char in value)):
            _fail("E_SCHEMA", field, "expected bounded text without controls")
    else:
        pattern = {"id": _ID, "sha": _SHA, "oid": _OID}[shape]
        if not isinstance(value, str) or pattern.fullmatch(value) is None:
            _fail("E_SCHEMA", field, "invalid identifier or digest")


def _platform():
    if (any(not getattr(os, flag, 0) for flag in ("O_DIRECTORY", "O_NOFOLLOW", "O_NONBLOCK"))
            or os.open not in os.supports_dir_fd or os.stat not in os.supports_dir_fd
            or os.stat not in os.supports_follow_symlinks):
        _fail("E_PLATFORM", "/", "descriptor-relative no-follow access is unavailable")


def _root_open(root):
    if not isinstance(root, Path) or not root.is_absolute():
        _fail("E_ROOT", "/root", "root must be an explicit absolute directory")
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | getattr(os, "O_CLOEXEC", 0)
    fd = None
    try:
        fd = os.open("/", flags)
        for part in root.parts[1:]:
            child = os.open(part, flags, dir_fd=fd)
            os.close(fd)
            fd = child
        return fd
    except (OSError, ValueError):
        if fd is not None:
            os.close(fd)
        _fail("E_ROOT", "/root", "root is unavailable or contains a symlink")


def _open_component(name, flags, parent, field):
    try:
        return os.open(name, flags, dir_fd=parent)
    except OSError as exc:
        # Linux can report ENOTDIR rather than ELOOP for O_DIRECTORY symlinks.
        if exc.errno in (errno.ELOOP, errno.ENOTDIR):
            try:
                symlink = stat.S_ISLNK(os.stat(name, dir_fd=parent, follow_symlinks=False).st_mode)
            except OSError:
                symlink = exc.errno == errno.ELOOP
            if symlink:
                _fail("E_PATH", field, "symlink traversal is forbidden")
        if exc.errno == errno.ENOENT:
            _fail("E_MISSING", field, "required file is absent")
        _fail("E_IO", field, "required file cannot be opened")


def _metadata(info):
    return (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns, info.st_ctime_ns)


def _read_file(root_fd, path, field, limit, *, declared=None, digest=None):
    parent = root_fd
    leaf = None
    flags = os.O_RDONLY | os.O_NOFOLLOW | getattr(os, "O_CLOEXEC", 0)
    try:
        for part in path.split("/")[:-1]:
            child = _open_component(part, flags | os.O_DIRECTORY, parent, field)
            if parent != root_fd:
                os.close(parent)
            parent = child
        leaf = _open_component(path.split("/")[-1], flags | os.O_NONBLOCK, parent, field)
        before = os.fstat(leaf)
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
            _fail("E_IO", field, "leaf must be a regular single-link file")
        if before.st_size > limit:
            _fail("E_LIMIT", field, "file exceeds admitted byte limit")
        data = bytearray()
        while True:
            chunk = os.read(leaf, min(65536, limit + 1 - len(data)))
            if not chunk:
                break
            data.extend(chunk)
            if len(data) > limit:
                _fail("E_LIMIT", field, "file exceeds admitted byte limit")
        after = os.fstat(leaf)
        if _metadata(before) != _metadata(after):
            _fail("E_FILE_CHANGED", field, "file metadata changed during read")
        if declared is not None and len(data) != declared:
            _fail("E_SIZE", field.rsplit("/", 1)[0] + "/size_bytes", "file size differs from declaration")
        if digest is not None and hashlib.sha256(data).hexdigest() != digest:
            _fail("E_HASH", field.rsplit("/", 1)[0] + "/sha256", "file hash differs from declaration")
        return data
    except OSError:
        _fail("E_IO", field, "required file cannot be read")
    finally:
        if leaf is not None:
            os.close(leaf)
        if parent != root_fd:
            os.close(parent)


def _parse(data):
    try:
        text = data.decode("utf-8")
    except UnicodeError:
        _fail("E_JSON", "/", "manifest is not strict UTF-8")
    if text.startswith("\ufeff"):
        _fail("E_JSON", "/", "manifest BOM is forbidden")
    depth = 0
    quoted = escaped = False
    for char in text:
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
        elif char == '"':
            quoted = True
        elif char in "[{":
            depth += 1
            if depth > 32:
                _fail("E_LIMIT", "/", "JSON nesting limit exceeded")
        elif char in "]}":
            depth -= 1

    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                # Escape controls and bound attacker-controlled diagnostic text.
                label = json.dumps(key[:80], ensure_ascii=True)
                _fail("E_JSON", "/", f"duplicate JSON key {label}")
            result[key] = value
        return result

    def nonfinite(_value):
        _fail("E_JSON", "/", "nonfinite JSON number")

    def real(value):
        number = float(value)
        if not math.isfinite(number):
            nonfinite(value)
        return number

    try:
        return json.loads(text, object_pairs_hook=pairs, parse_constant=nonfinite, parse_float=real)
    except ValidationError:
        raise
    except (ValueError, UnicodeError, OverflowError):
        _fail("E_JSON", "/", "invalid JSON")
    except RecursionError:
        _fail("E_LIMIT", "/", "JSON nesting limit exceeded")


def _relations(packet, expected, manifest_path):
    source, scenario, review = packet["source"], packet["scenario"], packet["review"]
    identities = (
        (source["repository_id"], expected.repository_id, "/source/repository_id"),
        (source["revision"], expected.source_revision, "/source/revision"),
        (scenario["id"], expected.scenario_id, "/scenario/id"),
        (scenario["revision"], expected.scenario_revision, "/scenario/revision"),
    )
    for actual, wanted, field in identities:
        if actual != wanted:
            _fail("E_IDENTITY", field, "identity differs from trusted expectation")
    for key, (actual, _, _) in zip(_BINDING, identities):
        if review["bound_to"][key] != actual:
            _fail("E_IDENTITY", "/review/bound_to/" + key, "review binding is stale")
    if (source["snapshot_kind"] == "unborn") != (source["tip_revision"] is None):
        _fail("E_PROVENANCE", "/source/tip_revision", "tip contradicts snapshot kind")
    if not source["inventory_complete"]:
        _fail("E_PROVENANCE", "/source/inventory_complete", "inventory is incomplete")
    if not source["files"]:
        _fail("E_PROVENANCE", "/source/files", "source inventory is empty")
    logical, required, before_paths, after_paths = {}, {}, set(), set()
    live_source = False
    for index, entry in enumerate(source["files"]):
        field = f"/source/files/{index}"
        if entry["path"] in logical:
            _fail("E_PROVENANCE", field + "/path", "duplicate logical source path")
        logical[entry["path"]] = entry
        if entry["before"] is None and entry["after"] is None:
            _fail("E_PROVENANCE", field + "/after", "entry has no preserved bytes")
        if entry["origin"] != "tracked" and entry["before"] is not None:
            _fail("E_PROVENANCE", field + "/before", "untracked input cannot have a baseline")
        live_source |= entry["role"] == "source" and entry["after"] is not None
        for side, seen in (("before", before_paths), ("after", after_paths)):
            blob = entry[side]
            if blob is None:
                continue
            pointer = field + "/" + side
            path = blob["path"]
            if path in required and required[path][0] != blob:
                _fail("E_PROVENANCE", pointer + "/path", "conflicting blob definitions")
            if path in seen:
                _fail("E_PATH", pointer + "/path", "logical files share a blob role")
            if path == manifest_path:
                _fail("E_PATH", pointer + "/path", "manifest cannot be a source blob")
            seen.add(path)
            required.setdefault(path, (blob, pointer))
            if len(required) > 256:
                _fail("E_LIMIT", "/source/files", "too many distinct source blobs")
    if not live_source:
        _fail("E_PROVENANCE", "/source/files", "no surviving source entry")
    endpoints = set()
    for index, rename in enumerate(source["renames"]):
        field = f"/source/renames/{index}"
        for key, side in (("from", "before"), ("to", "after")):
            name = rename[key]
            if name in endpoints:
                _fail("E_PROVENANCE", field + "/" + key, "rename endpoint is reused")
            endpoints.add(name)
            entry = logical.get(name)
            other = "after" if side == "before" else "before"
            if entry is None or entry[side] is None or entry[other] is not None:
                _fail("E_PROVENANCE", field + "/" + key, "rename endpoint has wrong shape")
    evidence = []
    occupied = set(required) | {manifest_path}
    for section, members in (("/provenance", packet["provenance"]), ("/review/evidence", review["evidence"])):
        shape = _SCHEMA["provenance"] if section == "/provenance" else _SCHEMA["review"]["evidence"]
        for key in shape:
            blob = members[key]
            pointer = section + "/" + key
            if blob["path"] in occupied:
                _fail("E_PATH", pointer + "/path", "evidence path collides with another role")
            occupied.add(blob["path"])
            evidence.append((blob, pointer))
    total = 0
    for blob, pointer in list(required.values()) + evidence:
        total += blob["size_bytes"]
        if total > _TOTAL_LIMIT:
            _fail("E_LIMIT", pointer + "/size_bytes", "aggregate byte limit exceeded")
    return required, evidence


def _review(review, required):
    if review["verdict"] != "PASS":
        _fail("E_REVIEW", "/review/verdict", "explicit PASS is required")
    if review["reviewer_id"] == review["author_id"]:
        _fail("E_REVIEW", "/review/reviewer_id", "author cannot be reviewer")
    completion = review["completion"]
    for key, wanted in (("status", "complete"), ("exit_code", 0), ("provider_stop_reason", "stop"),
                        ("provider_error", None), ("tool_errors", []), ("truncated", False)):
        if completion[key] != wanted:
            _fail("E_REVIEW", "/review/completion/" + key, "review did not complete without errors")
    ids = set()
    for index, finding in enumerate(review["findings"]):
        field = f"/review/findings/{index}"
        if finding["id"] in ids:
            _fail("E_SCHEMA", field + "/id", "duplicate finding ID")
        ids.add(finding["id"])
        if finding["severity"] != "low":
            _fail("E_REVIEW", field + "/severity", "blocking finding remains")
    coverage = review["coverage"]
    if not coverage["complete"]:
        _fail("E_COVERAGE", "/review/coverage/complete", "coverage is incomplete")
    if not coverage["files"]:
        _fail("E_COVERAGE", "/review/coverage/files", "coverage is empty")
    rows = {}
    for index, row in enumerate(coverage["files"]):
        field = f"/review/coverage/files/{index}"
        path = row["path"]
        if path in rows or path not in required:
            _fail("E_COVERAGE", field + "/path", "duplicate or unexpected coverage row")
        rows[path] = (row, field)
        if row["sha256"] != required[path][0]["sha256"]:
            _fail("E_COVERAGE", field + "/sha256", "coverage digest differs from required blob")
        if row["total_lines"] == 0:
            if row["empty_tool_id"] is None:
                _fail("E_COVERAGE", field + "/empty_tool_id", "empty file needs an explicit EOF observation")
            if row["ranges"]:
                _fail("E_COVERAGE", field + "/ranges", "empty file has line ranges")
        else:
            if row["empty_tool_id"] is not None:
                _fail("E_COVERAGE", field + "/empty_tool_id", "nonempty file cannot use EOF-only coverage")
            next_line = 1
            for position, span in enumerate(row["ranges"]):
                base = field + f"/ranges/{position}"
                if span["start_line"] != next_line:
                    _fail("E_COVERAGE", base + "/start_line", "coverage is not contiguous and ascending")
                if span["end_line"] < span["start_line"] or span["end_line"] > row["total_lines"]:
                    _fail("E_COVERAGE", base + "/end_line", "invalid coverage end line")
                next_line = span["end_line"] + 1
            if next_line != row["total_lines"] + 1:
                _fail("E_COVERAGE", field + "/ranges", "coverage does not reach EOF")
    if rows.keys() != required.keys():
        _fail("E_COVERAGE", "/review/coverage/files", "required coverage row is missing")
    return rows


def _text_coverage(data, row, field, blob_field):
    try:
        data.decode("utf-8")
    except UnicodeError:
        _fail("E_TEXT", blob_field + "/path", "required text is not UTF-8")
    if b"\x00" in data:
        _fail("E_TEXT", blob_field + "/path", "required text contains NUL")
    lines = data.count(b"\n") + bool(data and not data.endswith(b"\n"))
    if lines != row["total_lines"]:
        _fail("E_COVERAGE", field + "/total_lines", "line count differs from raw bytes")
    offset, line = 0, 0
    for index, span in enumerate(row["ranges"]):
        start = offset
        while line < span["end_line"]:
            end = data.find(b"\n", offset)
            offset = len(data) if end < 0 else end + 1
            line += 1
        if hashlib.sha256(memoryview(data)[start:offset]).hexdigest() != span["sha256"]:
            _fail("E_COVERAGE", field + f"/ranges/{index}/sha256", "range hash differs from raw bytes")


def validate_manifest(root: Path, manifest_path: str, *, expected: ExpectedIdentity) -> ValidatedManifest:
    """Validate one pinned packet without writing, importing, or executing it."""
    for key, pattern in (("manifest_sha256", _SHA), ("repository_id", _ID),
                         ("source_revision", _ID), ("scenario_id", _ID), ("scenario_revision", _ID)):
        value = getattr(expected, key, None) if isinstance(expected, ExpectedIdentity) else None
        if not isinstance(value, str) or pattern.fullmatch(value) is None:
            _fail("E_EXPECTED", "/expected/" + key, "trusted expectation is required and must be valid")
    _platform()
    _path(manifest_path, "/manifest_path")
    root_fd = _root_open(root)
    try:
        data = _read_file(root_fd, manifest_path, "/manifest_path", _MANIFEST_LIMIT)
        if hashlib.sha256(data).hexdigest() != expected.manifest_sha256:
            _fail("E_MANIFEST_HASH", "/manifest_path", "manifest differs from the trusted pin")
        packet = _parse(data)
        _schema(packet, _SCHEMA)
        required, evidence = _relations(packet, expected, manifest_path)
        rows = _review(packet["review"], required)
        actual_total = 0
        for path, (blob, field) in required.items():
            content = _read_file(root_fd, path, field + "/path", min(_FILE_LIMIT, _TOTAL_LIMIT - actual_total),
                                 declared=blob["size_bytes"], digest=blob["sha256"])
            actual_total += len(content)
            row, coverage_field = rows[path]
            _text_coverage(content, row, coverage_field, field)
        for blob, field in evidence:
            content = _read_file(root_fd, blob["path"], field + "/path", min(_FILE_LIMIT, _TOTAL_LIMIT - actual_total),
                                 declared=blob["size_bytes"], digest=blob["sha256"])
            actual_total += len(content)
        return ValidatedManifest(expected.manifest_sha256, expected.repository_id, expected.source_revision,
                                 expected.scenario_id, expected.scenario_revision, len(required), len(evidence))
    finally:
        os.close(root_fd)
