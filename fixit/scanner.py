"""
Scans a requirements.txt (or any list of pip package specs) and reports
which packages are known to be problematic on Termux, before you even
try to install them.
"""

import re
from typing import List

from . import packages

_SPEC_SPLIT = re.compile(r"[<>=!~;\[\s]")


def parse_requirement_line(line: str):
    """Extract the bare package name from a requirements.txt line."""
    line = line.strip()
    if not line or line.startswith("#") or line.startswith("-"):
        return None
    name = _SPEC_SPLIT.split(line)[0].strip()
    return name or None


def scan_requirements(lines: List[str]) -> List[dict]:
    rows = []
    for line in lines:
        name = parse_requirement_line(line)
        if not name:
            continue
        info = packages.lookup(name)
        if info is None:
            rows.append({
                "package": name,
                "status": "OK (likely fine)",
                "pkg_equivalent": None,
                "difficulty": "easy",
            })
        elif info["difficulty"] == "unsupported":
            rows.append({
                "package": name,
                "status": "WILL FAIL",
                "pkg_equivalent": info["pkg"],
                "difficulty": info["difficulty"],
            })
        else:
            rows.append({
                "package": name,
                "status": "NEEDS PKG INSTALL",
                "pkg_equivalent": info["pkg"],
                "difficulty": info["difficulty"],
            })
    return rows
