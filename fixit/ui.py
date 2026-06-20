"""
Terminal output rendering. Uses `rich` for colored boxes/tables if it's
installed, and falls back to clean plain-text output if it isn't —
fixit should never fail to run just because an optional dependency is missing.
"""

from typing import List

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text
    _HAS_RICH = True
    _console = Console()
except ImportError:
    _HAS_RICH = False
    _console = None


DIFFICULTY_COLORS = {
    "easy": "green",
    "medium": "yellow",
    "hard": "red",
    "unsupported": "bright_red",
    "unknown": "white",
}

DIFFICULTY_LABELS = {
    "easy": "EASY FIX",
    "medium": "MEDIUM",
    "hard": "HARD (slow build)",
    "unsupported": "NOT SUPPORTED ON TERMUX",
    "unknown": "UNKNOWN",
}


def print_banner():
    if _HAS_RICH:
        _console.print(Panel.fit("[bold cyan]fixit[/bold cyan] — Termux Python error fixer",
                                  border_style="cyan"))
    else:
        print("=== fixit — Termux Python error fixer ===")


def print_no_issues():
    msg = "No known Termux-specific issues detected in that output."
    if _HAS_RICH:
        _console.print(f"[green]{msg}[/green]")
    else:
        print(msg)


def print_issues(issues: List) -> None:
    if not issues:
        print_no_issues()
        return

    if _HAS_RICH:
        for i, issue in enumerate(issues, 1):
            color = DIFFICULTY_COLORS.get(issue.difficulty, "white")
            label = DIFFICULTY_LABELS.get(issue.difficulty, issue.difficulty.upper())
            body = Text()
            if issue.note:
                body.append(issue.note + "\n\n", style="dim")
            body.append("Fix:\n", style="bold")
            for line in issue.fix:
                body.append(f"  {line}\n", style="bold white on grey15" if not line.startswith("#") else "dim italic")
            _console.print(Panel(
                body,
                title=f"[{color}]{i}. {issue.title}  ·  {label}[/{color}]",
                border_style=color,
            ))
    else:
        for i, issue in enumerate(issues, 1):
            label = DIFFICULTY_LABELS.get(issue.difficulty, issue.difficulty.upper())
            print(f"\n[{i}] {issue.title}  ({label})")
            if issue.note:
                print(f"    {issue.note}")
            print("    Fix:")
            for line in issue.fix:
                print(f"      {line}")


def print_scan_table(rows: List[dict]) -> None:
    """rows: list of dicts with keys: package, status, pkg_equivalent, difficulty"""
    if _HAS_RICH:
        table = Table(title="Termux Compatibility Scan")
        table.add_column("Package")
        table.add_column("Status")
        table.add_column("Termux Fix")
        table.add_column("Difficulty")
        for row in rows:
            color = DIFFICULTY_COLORS.get(row["difficulty"], "white")
            table.add_row(
                row["package"],
                row["status"],
                row["pkg_equivalent"] or "-",
                f"[{color}]{row['difficulty']}[/{color}]",
            )
        _console.print(table)
    else:
        print("\nPackage           Status        Termux Fix              Difficulty")
        print("-" * 70)
        for row in rows:
            print(f"{row['package']:<17} {row['status']:<13} {(row['pkg_equivalent'] or '-'):<24} {row['difficulty']}")
