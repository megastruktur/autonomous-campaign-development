"""CLI contract tests on synthetic packets, never real review acceptance."""

from contextlib import ExitStack, redirect_stderr, redirect_stdout
import io
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import cli
from test_validator import EVIDENCE, Packet, put


CLI = Path(__file__).with_name("cli.py").resolve()
OPTIONS = (
    "--root", "--manifest", "--expect-manifest-sha256", "--expect-repository",
    "--expect-source", "--expect-scenario", "--expect-scenario-revision",
)


def arguments(root, expected):
    values = (
        str(root), "manifest.json", expected.manifest_sha256, expected.repository_id,
        expected.source_revision, expected.scenario_id, expected.scenario_revision,
    )
    return [token for pair in zip(OPTIONS, values) for token in pair]


def tree_bytes(root):
    return {str(path.relative_to(root)): path.read_bytes()
            for path in root.rglob("*") if path.is_file()}


class CliTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix="manifest-cli-")
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.packet = Packet(self.root)
        self.expected = self.packet.pin()
        self.argv = arguments(self.root, self.expected)

    def process(self, argv, **kwargs):
        return subprocess.run(
            [sys.executable, "-B", str(CLI), *argv], capture_output=True,
            text=True, timeout=10, **kwargs,
        )

    def invoke(self, argv):
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            code = cli.main(argv)
        return code, stdout.getvalue(), stderr.getvalue()

    def assert_valid(self, code, stdout, stderr, expected=None, count=2):
        expected = expected or self.expected
        self.assertEqual(code, 0)
        self.assertEqual(stdout, f"VALID files={count} evidence=7 manifest={expected.manifest_sha256}\n")
        self.assertEqual(stderr, "")

    def assert_invalid(self, code, stdout, stderr, error, field):
        self.assertEqual(code, 1)
        self.assertEqual(stdout, "")
        self.assertTrue(stderr.startswith(f"ERROR {error} {field}: "), stderr)
        self.assertEqual(len(stderr.splitlines()), 1)
        self.assertNotIn("Traceback", stderr)

    def assert_usage(self, code, stdout, stderr, option):
        self.assertEqual(code, 2)
        self.assertEqual(stdout, "")
        self.assertIn("usage:", stderr)
        self.assertIn("error:", stderr)
        self.assertIn(option, stderr)
        self.assertNotIn("E_INTERNAL", stderr)

    def test_real_process_valid_and_read_only(self):
        before = tree_bytes(self.root)
        result = self.process(self.argv)
        self.assert_valid(result.returncode, result.stdout, result.stderr)
        self.assertEqual(tree_bytes(self.root), before)

    def test_real_process_optional_equals_syntax_and_reordered_options(self):
        argv = [f"{self.argv[i]}={self.argv[i + 1]}" for i in range(0, len(self.argv), 2)]
        result = self.process(list(reversed(argv)))
        self.assert_valid(result.returncode, result.stdout, result.stderr)

    def test_real_process_missing_files(self):
        targets = [("manifest.json", "/manifest_path"),
                   ("candidate/src/pilot.py", "/source/files/0/after/path"),
                   ("candidate/tests/test_pilot.py", "/source/files/1/after/path")]
        targets += [(path, pointer + "/path") for pointer, path, _ in EVIDENCE]
        for path, field in targets:
            with self.subTest(path=path), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                packet = Packet(root)
                argv = arguments(root, packet.pin())
                (root / path).unlink()
                before = tree_bytes(root)
                result = self.process(argv)
                self.assert_invalid(result.returncode, result.stdout, result.stderr, "E_MISSING", field)
                self.assertEqual(tree_bytes(root), before)

    def test_real_process_stale_external_identities(self):
        fields = {
            "--expect-repository": "/source/repository_id",
            "--expect-source": "/source/revision",
            "--expect-scenario": "/scenario/id",
            "--expect-scenario-revision": "/scenario/revision",
        }
        for option, field in fields.items():
            with self.subTest(option=option):
                argv = self.argv.copy()
                argv[argv.index(option) + 1] = "stale"
                result = self.process(argv)
                self.assert_invalid(result.returncode, result.stdout, result.stderr, "E_IDENTITY", field)

    def test_real_process_semantic_mutants_with_new_pins(self):
        mutations = [
            ("/review/bound_to/source_revision", "stale", "E_IDENTITY"),
            ("/review/bound_to/scenario_revision", "stale", "E_IDENTITY"),
            ("/review/verdict", "FAIL", "E_REVIEW"),
            ("/review/verdict", "INCONCLUSIVE", "E_REVIEW"),
            ("/review/verdict", "INVALIDATED", "E_REVIEW"),
            ("/review/verdict", None, "E_REVIEW"),
            ("/review/verdict", "pass", "E_SCHEMA"),
            ("/review/completion/status", "partial", "E_REVIEW"),
            ("/review/completion/exit_code", 1, "E_REVIEW"),
            ("/review/completion/provider_stop_reason", "end_turn", "E_REVIEW"),
            ("/review/completion/provider_error", "synthetic failure", "E_REVIEW"),
            ("/review/completion/tool_errors", ["synthetic failure"], "E_REVIEW"),
            ("/review/completion/truncated", True, "E_REVIEW"),
            ("/review/coverage/complete", False, "E_COVERAGE"),
            ("/review/coverage/files", [], "E_COVERAGE"),
            ("/source/files/0/after/path", "../outside.py", "E_PATH"),
        ]
        for pointer, value, error in mutations:
            with self.subTest(pointer=pointer, value=value), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                packet = Packet(root)
                put(packet.data, pointer, value)
                argv = arguments(root, packet.pin())
                before = tree_bytes(root)
                result = self.process(argv)
                self.assert_invalid(result.returncode, result.stdout, result.stderr, error, pointer)
                self.assertEqual(tree_bytes(root), before)

    def test_real_process_coverage_omission(self):
        self.packet.data["review"]["coverage"]["files"].pop()
        result = self.process(arguments(self.root, self.packet.pin()))
        self.assert_invalid(result.returncode, result.stdout, result.stderr,
                            "E_COVERAGE", "/review/coverage/files")

    def test_real_process_manifest_drift_keeps_original_pin(self):
        manifest = self.root / "manifest.json"
        manifest.write_bytes(manifest.read_bytes() + b" ")
        result = self.process(self.argv)
        self.assert_invalid(result.returncode, result.stdout, result.stderr,
                            "E_MANIFEST_HASH", "/manifest_path")

    def test_real_process_source_baseline_and_evidence_byte_drift(self):
        targets = [("candidate/src/pilot.py", "/source/files/0/after/sha256"),
                   ("baseline/src/pilot.py", "/source/files/0/before/sha256")]
        targets += [(path, pointer + "/sha256") for pointer, path, _ in EVIDENCE]
        for path, field in targets:
            with self.subTest(path=path), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                packet = Packet(root)
                packet.baseline()
                argv = arguments(root, packet.pin())
                target = root / path
                data = target.read_bytes()
                target.write_bytes(bytes([data[0] ^ 1]) + data[1:])
                result = self.process(argv)
                self.assert_invalid(result.returncode, result.stdout, result.stderr, "E_HASH", field)

    def test_real_process_missing_required_options(self):
        for index, option in enumerate(OPTIONS):
            with self.subTest(option=option):
                argv = self.argv[:2 * index] + self.argv[2 * index + 2:]
                result = self.process(argv)
                self.assert_usage(result.returncode, result.stdout, result.stderr, option)

    def test_real_process_duplicate_options_including_equals(self):
        for index, option in enumerate(OPTIONS):
            for equal in (False, True):
                with self.subTest(option=option, equal=equal):
                    value = self.argv[2 * index + 1]
                    extra = [f"{option}={value}"] if equal else [option, value]
                    result = self.process(self.argv + extra)
                    self.assert_usage(result.returncode, result.stdout, result.stderr, option)

    def test_real_process_missing_option_values(self):
        for index, option in enumerate(OPTIONS):
            with self.subTest(option=option):
                argv = self.argv[:2 * index + 1] + self.argv[2 * index + 2:]
                result = self.process(argv)
                self.assert_usage(result.returncode, result.stdout, result.stderr, option)

    def test_real_process_unknown_abbreviated_and_positional_arguments(self):
        for extra in (["--unknown", "value"], ["--roo", str(self.root)],
                      ["--expect-scenario-rev", "v1"], ["unexpected"], ["--", "unexpected"]):
            with self.subTest(extra=extra):
                result = self.process(self.argv + extra)
                self.assert_usage(result.returncode, result.stdout, result.stderr, extra[-1])

    def test_real_process_help_and_help_without_inputs(self):
        for argv in (["--help"], ["--root", str(self.root / "absent"), "--help"]):
            with self.subTest(argv=argv):
                result = self.process(argv)
                self.assertEqual(result.returncode, 0)
                self.assertEqual(result.stderr, "")
                self.assertIn("usage:", result.stdout)
                for option in OPTIONS:
                    self.assertIn(option, result.stdout)

    def test_help_aliases_reject_duplicates_without_packet_access_or_imports(self):
        for module in ("validator", "argparse"):
            marker = self.root / f"executed-{module}"
            (self.root / f"{module}.py").write_text(
                f"open({str(marker)!r}, 'w').write('executed')\n"
                f"raise RuntimeError('packet {module} import')\n"
            )
        before = tree_bytes(self.root)
        # A trusted startup hook observes the actual script, not a replacement main.
        # Any descriptor traversal or packet file open makes the stream/code fail.
        with tempfile.TemporaryDirectory(prefix="cli-help-audit-") as directory:
            (Path(directory) / "sitecustomize.py").write_text(
                "import sys\n"
                "def audit(event, args):\n"
                "    if event == 'open':\n"
                "        path, mode, flags = args\n"
                f"        if flags & {os.O_DIRECTORY} or (isinstance(path, str) and "
                f"(path == {str(self.root)!r} or path.startswith({str(self.root) + '/'!r}))):\n"
                "            raise AssertionError('unexpected packet access')\n"
                "sys.addaudithook(audit)\n"
            )
            environment = dict(os.environ, PYTHONPATH=os.pathsep.join(
                (directory, str(self.root), str(CLI.parent))))
            program = (
                "import sys; original_path = sys.path; original_entries = sys.path.copy(); "
                "import cli; assert sys.path is original_path and sys.path == original_entries; "
                "code = cli.main(sys.argv[1:]); "
                "assert sys.path is original_path and sys.path == original_entries; "
                "raise SystemExit(code)"
            )
            cases = [([alias], 0) for alias in ("-h", "--help")]
            cases += [([first, second], 2) for first in ("-h", "--help")
                      for second in ("-h", "--help")]
            cases += [(["-hh"], 2), (["-hhh"], 2), (["--help", "-hh"], 2),
                      (["--help", "--", "-h", "--help"], 0)]
            for route in ("direct", "imported"):
                command = ([sys.executable, "-B", str(CLI)] if route == "direct"
                           else [sys.executable, "-B", "-c", program])
                for help_args, expected_code in cases:
                    for full_inputs in (False, True):
                        with self.subTest(route=route, help_args=help_args,
                                          full_inputs=full_inputs):
                            argv = (self.argv if full_inputs else []) + help_args
                            result = subprocess.run(
                                command + argv, cwd=self.root, env=environment,
                                capture_output=True, text=True, timeout=10,
                            )
                            if expected_code == 2:
                                self.assert_usage(result.returncode, result.stdout,
                                                  result.stderr, "--help")
                                self.assertIn("exactly once", result.stderr)
                            else:
                                self.assertEqual(result.returncode, 0)
                                self.assertEqual(result.stderr, "")
                                for option in OPTIONS:
                                    self.assertIn(option, result.stdout)
                            self.assertEqual(tree_bytes(self.root), before)
                            for module in ("validator", "argparse"):
                                self.assertFalse((self.root / f"executed-{module}").exists())

    def test_imported_main_matches_process_and_is_reentrant(self):
        for argv in (self.argv, self.argv, self.argv[:-2], self.argv + ["--root", ""],
                     ["--help"], self.argv):
            with self.subTest(argv=argv):
                process = self.process(argv)
                self.assertEqual(self.invoke(argv), (process.returncode, process.stdout, process.stderr))
        (self.root / "candidate/src/pilot.py").unlink()
        process = self.process(self.argv)
        self.assertEqual(self.invoke(self.argv), (process.returncode, process.stdout, process.stderr))

    def test_syntax_and_help_do_not_access_packet(self):
        cases = [([], 2), (["--help"], 0), (self.argv + ["unexpected"], 2),
                 (self.argv + ["--manifest", "manifest.json"], 2),
                 (self.argv + ["--roo", str(self.root)], 2), (self.argv[:-1], 2)]
        for argv, expected_code in cases:
            with self.subTest(argv=argv), patch("os.open", side_effect=AssertionError("packet access")) as opened:
                code, stdout, stderr = self.invoke(argv)
                self.assertEqual(code, expected_code)
                opened.assert_not_called()
                self.assertNotIn("E_INTERNAL", stderr)
                if expected_code == 2:
                    self.assertEqual(stdout, "")

    def test_main_none_uses_process_argv_not_environment_defaults(self):
        with patch.object(sys, "argv", [str(CLI), *self.argv]):
            self.assert_valid(*self.invoke(None))
        with patch.dict(os.environ, {"ROOT": str(self.root), "MANIFEST": "manifest.json",
                                    "EXPECT_SOURCE": "fixture-source-v1"}):
            self.assert_usage(*self.invoke([]), "--root")

    def test_unexpected_internal_failure_is_not_validation_failure(self):
        for error in (RuntimeError("private packet content"), ValueError("secret"),
                      OSError("private host path")):
            with self.subTest(error=type(error).__name__), patch("cli.validate_manifest", side_effect=error):
                self.assertEqual(self.invoke(self.argv),
                                 (3, "", "ERROR E_INTERNAL /: internal validator failure\n"))

    def test_expected_identity_errors_are_not_usage_or_internal_errors(self):
        for option, field in (("--expect-manifest-sha256", "/expected/manifest_sha256"),
                              ("--expect-source", "/expected/source_revision")):
            with self.subTest(option=option):
                argv = self.argv.copy()
                argv[argv.index(option) + 1] = ""
                self.assert_invalid(*self.invoke(argv), "E_EXPECTED", field)

    def test_control_characters_in_field_stay_on_one_diagnostic_line(self):
        self.packet.data["bad\nfield\x1b"] = "opaque"
        result = self.process(arguments(self.root, self.packet.pin()))
        self.assert_invalid(result.returncode, result.stdout, result.stderr,
                            "E_SCHEMA", "/bad\\u000afield\\u001b")

    def test_packet_cwd_and_pythonpath_cannot_supply_validator(self):
        marker = self.root / "executed"
        payload = f"from pathlib import Path\nPath({str(marker)!r}).write_text('executed')\nraise RuntimeError('packet import')\n"
        for name in ("validator.py", "cli.py"):
            (self.root / name).write_text(payload)
        self.packet.source_bytes(payload.encode())
        expected = self.packet.pin()
        environment = dict(os.environ, PYTHONPATH=str(self.root))
        before = tree_bytes(self.root)
        result = self.process(arguments(self.root, expected), cwd=self.root, env=environment)
        self.assert_valid(result.returncode, result.stdout, result.stderr, expected)
        self.assertFalse(marker.exists())
        self.assertEqual(tree_bytes(self.root), before)

    def test_imported_main_packet_cwd_cannot_supply_validator(self):
        marker = self.root / "executed-validator"
        (self.root / "validator.py").write_text(
            f"open({str(marker)!r}, 'w').write('executed')\n"
            "raise RuntimeError('packet validator import')\n"
        )
        environment = dict(os.environ, PYTHONPATH=str(CLI.parent))
        program = (
            "import sys; original_path = sys.path; original_entries = sys.path.copy(); "
            "import cli; assert sys.path is original_path and sys.path == original_entries; "
            "code = cli.main(); "
            "assert sys.path is original_path and sys.path == original_entries; "
            "raise SystemExit(code)"
        )
        before = tree_bytes(self.root)
        for stale in (False, True):
            with self.subTest(stale=stale):
                argv = self.argv.copy()
                if stale:
                    argv[argv.index("--expect-source") + 1] = "stale"
                result = subprocess.run(
                    [sys.executable, "-B", "-c", program, *argv],
                    cwd=self.root, env=environment, capture_output=True,
                    text=True, timeout=10,
                )
                if stale:
                    self.assert_invalid(result.returncode, result.stdout, result.stderr,
                                        "E_IDENTITY", "/source/revision")
                else:
                    self.assert_valid(result.returncode, result.stdout, result.stderr)
                self.assertFalse(marker.exists())
                self.assertEqual(tree_bytes(self.root), before)

    def test_direct_script_packet_pythonpath_cannot_supply_stdlib(self):
        marker = self.root / "executed-argparse"
        (self.root / "argparse.py").write_text(
            f"open({str(marker)!r}, 'w').write('executed')\n"
            "raise RuntimeError('packet argparse import')\n"
        )
        environment = dict(os.environ, PYTHONPATH=str(self.root))
        before = tree_bytes(self.root)
        for kind in ("valid", "stale", "help", "syntax"):
            with self.subTest(kind=kind):
                argv = self.argv.copy()
                if kind == "stale":
                    argv[argv.index("--expect-source") + 1] = "stale"
                elif kind == "help":
                    argv = ["--root", str(self.root / "absent"), "--help"]
                elif kind == "syntax":
                    argv += ["--roo", str(self.root)]
                result = self.process(argv, cwd=self.root, env=environment)
                if kind == "valid":
                    self.assert_valid(result.returncode, result.stdout, result.stderr)
                elif kind == "stale":
                    self.assert_invalid(result.returncode, result.stdout, result.stderr,
                                        "E_IDENTITY", "/source/revision")
                elif kind == "help":
                    self.assertEqual(result.returncode, 0)
                    self.assertEqual(result.stderr, "")
                    for option in OPTIONS:
                        self.assertIn(option, result.stdout)
                else:
                    self.assert_usage(result.returncode, result.stdout, result.stderr, "--roo")
                self.assertFalse(marker.exists())
                self.assertEqual(tree_bytes(self.root), before)

    def test_import_is_silent_and_does_not_run_validation(self):
        program = (
            "import sys; from unittest.mock import patch; "
            f"sys.path.insert(0, {str(CLI.parent)!r}); "
            "opened = patch('os.open', side_effect=AssertionError('import packet access')); "
            "guard = opened.start(); import cli; guard.assert_not_called()"
        )
        result = subprocess.run([sys.executable, "-B", "-c", program],
                                capture_output=True, text=True, timeout=10, cwd=self.root)
        self.assertEqual((result.returncode, result.stdout, result.stderr), (0, "", ""))

    def test_imported_main_has_no_execution_network_or_packet_write(self):
        before = tree_bytes(self.root)
        with ExitStack() as stack:
            guards = [stack.enter_context(patch(name, side_effect=AssertionError(name)))
                      for name in ("subprocess.Popen", "socket.socket", "os.system")]
            self.assert_valid(*self.invoke(self.argv))
            invalid = self.argv.copy()
            invalid[invalid.index("--expect-source") + 1] = "stale"
            self.assert_invalid(*self.invoke(invalid), "E_IDENTITY", "/source/revision")
            for guard in guards:
                guard.assert_not_called()
        self.assertEqual(tree_bytes(self.root), before)


if __name__ == "__main__":
    unittest.main()
