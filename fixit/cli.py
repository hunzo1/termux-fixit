"""
fixit — CLI entry point.

Usage:
    python script.py 2>&1 | fixit
    fixit --file traceback.txt
    fixit scan requirements.txt
    fixit lookup numpy
"""

import argparse
import sys

from . import detectors, scanner, ui
from . import packages as pkgdb

__version__ = "1.0.0"


def _read_stdin_or_file(file_arg: str) -> str:
    if file_arg:
        with open(file_arg, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    if sys.stdin.isatty():
        return ""
    return sys.stdin.read()


def cmd_fix(args) -> int:
    text = _read_stdin_or_file(args.file)
    if not text.strip():
        print("No input received. Pipe a traceback in, e.g.:\n  python script.py 2>&1 | fixit")
        return 1

    ui.print_banner()
    issues = detectors.analyze(text)
    ui.print_issues(issues)
    return 0 if issues else 0


def cmd_scan(args) -> int:
    try:
        with open(args.requirements, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except OSError as e:
        print(f"Couldn't read {args.requirements}: {e}")
        return 1

    ui.print_banner()
    rows = scanner.scan_requirements(lines)
    ui.print_scan_table(rows)

    broken = [r for r in rows if r["difficulty"] in ("hard", "unsupported")]
    if broken:
        print(f"\n{len(broken)} package(s) likely to cause real trouble on Termux. "
              f"Run 'fixit lookup <package>' for details on any of them.")
    return 0


def cmd_lookup(args) -> int:
    info = pkgdb.lookup(args.package)
    ui.print_banner()
    if not info:
        print(f"'{args.package}' isn't in the known problem-package list — it likely installs fine with plain pip.")
        return 0

    print(f"\nPackage: {args.package}")
    print(f"Difficulty: {info['difficulty']}")
    print(f"Why it breaks: {info['note']}")
    print("Fix:")
    for line in info["fix"]:
        print(f"  {line}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="fixit",
        description="Fix Python errors that are specific to running on Termux/Android.",
    )
    parser.add_argument("--version", action="version", version=f"fixit {__version__}")
    sub = parser.add_subparsers(dest="command")

    fix_parser = sub.add_parser("fix", help="Analyze a traceback (default if piped input is given)")
    fix_parser.add_argument("--file", help="Read traceback from a file instead of stdin")
    fix_parser.set_defaults(func=cmd_fix)

    scan_parser = sub.add_parser("scan", help="Scan a requirements.txt for Termux compatibility")
    scan_parser.add_argument("requirements", help="Path to requirements.txt")
    scan_parser.set_defaults(func=cmd_scan)

    lookup_parser = sub.add_parser("lookup", help="Look up a single package by name")
    lookup_parser.add_argument("package", help="pip package name, e.g. numpy")
    lookup_parser.set_defaults(func=cmd_lookup)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    # No subcommand given: behave like `fixit fix` so piping "just works".
    if args.command is None:
        args.file = None
        return sys.exit(cmd_fix(args))

    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
