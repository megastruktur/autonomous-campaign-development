"""Validate a pinned local evidence packet; VALID is not product acceptance.

Run with --help for the seven required explicit inputs. No packet values supply
expectations, imports, executable actions, or configuration defaults.
"""

# Bootstrap from interpreter-owned paths before any filesystem-resolved import.
# The interpreter, its preloaded modules and this installation are trusted;
# packet cwd/PYTHONPATH entries are not. Restore the caller's path on every exit.
import sys


class _TrustedImports:
    def __enter__(self):
        self.previous = sys.path
        sys.path = [
            sys._stdlib_dir,
            f"{sys.base_exec_prefix}/{sys.platlibdir}/python{sys.version_info.major}."
            f"{sys.version_info.minor}/lib-dynload",
        ]

    def __exit__(self, *exc):
        sys.path = self.previous


with _TrustedImports():
    import argparse
    import importlib.util
    from pathlib import Path

    # Never resolve the sibling by an ambient name (including sys.modules).
    _spec = importlib.util.spec_from_file_location(
        __name__ + "._validator", Path(__file__).with_name("validator.py"),
    )
    _validator = importlib.util.module_from_spec(_spec)
    sys.modules[_spec.name] = _validator
    try:
        _spec.loader.exec_module(_validator)
    except BaseException:
        del sys.modules[_spec.name]
        raise
    ExpectedIdentity = _validator.ExpectedIdentity
    ValidationError = _validator.ValidationError
    validate_manifest = _validator.validate_manifest


class _ParserExit(Exception):
    def __init__(self, status):
        self.status = status


class _Parser(argparse.ArgumentParser):
    def exit(self, status=0, message=None):
        if message:
            self._print_message(message, sys.stderr)
        raise _ParserExit(status)


class _Once(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if getattr(namespace, self.dest) is not None:
            parser.error(f"argument {option_string}: must be supplied exactly once")
        setattr(namespace, self.dest, values)


def _one_line(text):
    # JSON member names can contain controls even though valid paths cannot.
    return "".join(char if char.isprintable() else f"\\u{ord(char):04x}" for char in text)


def main(argv: list[str] | None = None) -> int:
    """Return 0 valid, 1 invalid packet, 2 usage error, or 3 internal failure."""
    # argparse/help and validator dependencies may import stdlib lazily too.
    with _TrustedImports():
        return _main(argv)


def _main(argv):
    try:
        parser = _Parser(
            prog="cli.py", allow_abbrev=False,
            description="Check a pinned local packet for consistency, not product acceptance.",
        )
        for option, metavar, help_text in (
            ("--root", "ABSOLUTE_PACKET_ROOT", "absolute, non-symlink packet directory"),
            ("--manifest", "PATH", "manifest path relative to root"),
            ("--expect-manifest-sha256", "SHA256", "independently pinned manifest digest"),
            ("--expect-repository", "REPOSITORY_ID", "trusted repository identity"),
            ("--expect-source", "SOURCE_REVISION", "trusted source revision"),
            ("--expect-scenario", "SCENARIO_ID", "trusted scenario identity"),
            ("--expect-scenario-revision", "SCENARIO_REVISION", "trusted scenario revision"),
        ):
            parser.add_argument(option, required=True, action=_Once, metavar=metavar, help=help_text)
        # Help exits during parsing, so reject repeats before that first action.
        argv = sys.argv[1:] if argv is None else argv
        help_count = 0
        for token in argv:
            if token == "--":
                break
            if token == "--help":
                help_count += 1
            elif token.startswith("-h") and not token[1:].strip("h"):
                help_count += len(token) - 1
            if help_count > 1:
                parser.error("argument -h/--help: must be supplied exactly once")
        args = parser.parse_args(argv)
        expected = ExpectedIdentity(
            manifest_sha256=args.expect_manifest_sha256,
            repository_id=args.expect_repository,
            source_revision=args.expect_source,
            scenario_id=args.expect_scenario,
            scenario_revision=args.expect_scenario_revision,
        )
        result = validate_manifest(Path(args.root), args.manifest, expected=expected)
        line = f"VALID files={result.file_count} evidence={result.evidence_count} manifest={result.manifest_sha256}"
    except _ParserExit as exc:
        return exc.status
    except ValidationError as exc:
        print(f"ERROR {exc.code} {_one_line(exc.field)}: {_one_line(exc.message)}", file=sys.stderr)
        return 1
    except Exception:
        print("ERROR E_INTERNAL /: internal validator failure", file=sys.stderr)
        return 3
    print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
