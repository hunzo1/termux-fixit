"""
Detects known error patterns in pasted/piped traceback text and produces
structured Issue objects describing the problem and the fix.
"""

import re
from dataclasses import dataclass, field
from typing import List, Optional

from . import packages


@dataclass
class Issue:
    kind: str                      # short machine-readable category
    title: str                     # human-readable one-liner
    package: Optional[str] = None  # pip package name involved, if any
    note: str = ""                 # why this happens on Termux
    fix: List[str] = field(default_factory=list)
    difficulty: str = "unknown"    # easy | medium | hard | unsupported | unknown


# --- Regex patterns for each known error type -----------------------------

RE_MODULE_NOT_FOUND = re.compile(r"ModuleNotFoundError:\s*No module named ['\"]([A-Za-z0-9_.\-]+)['\"]")
RE_IMPORT_ERROR_NAMED = re.compile(r"ImportError:\s*No module named ['\"]?([A-Za-z0-9_.\-]+)['\"]?")
RE_EXTERNALLY_MANAGED = re.compile(r"externally-managed-environment")
RE_FAILED_WHEEL = re.compile(r"Failed building wheel for ([A-Za-z0-9_.\-]+)")
RE_BUILD_CMD_FAILED = re.compile(r"error: command '([^']+)' failed")
RE_MISSING_SO = re.compile(r"(lib[A-Za-z0-9_\-]+\.so(?:\.\d+)?)[:]?\s*cannot open shared object file")
RE_NO_MATCHING_DIST = re.compile(r"No matching distribution found for ([A-Za-z0-9_.\-]+)")
RE_PERMISSION_DENIED = re.compile(r"PermissionError:.*Permission denied")
RE_GCC_MISSING = re.compile(r"(gcc|cc1|clang)[:]?\s*(not found|command not found)")


def _pkg_name_from_module(module_name: str) -> str:
    """Strip submodule paths like 'numpy.core' -> 'numpy', and fix common import-name mismatches."""
    base = module_name.split(".")[0].lower()
    aliases = {
        "cv2": "opencv-python",
        "pil": "pillow",
        "yaml": "pyyaml",
        "zmq": "pyzmq",
        "sklearn": "scikit-learn",
        "bs4": "beautifulsoup4",
    }
    return aliases.get(base, base)


def _issue_from_pkg_lookup(module_name: str, kind: str, title_fmt: str) -> Issue:
    pkg_name = _pkg_name_from_module(module_name)
    info = packages.lookup(pkg_name)
    if info:
        return Issue(
            kind=kind,
            title=title_fmt.format(module_name),
            package=pkg_name,
            note=info["note"],
            fix=info["fix"] if info["fix"] else [f"pip install {pkg_name}"],
            difficulty=info["difficulty"],
        )
    # Unknown package: fall back to a generic but still useful suggestion.
    return Issue(
        kind=kind,
        title=title_fmt.format(module_name),
        package=pkg_name,
        note="Not in the known Termux problem-package list — it likely installs fine with plain pip.",
        fix=[f"pip install {pkg_name}", f"# If that fails: pkg search {pkg_name}"],
        difficulty="unknown",
    )


def analyze(text: str) -> List[Issue]:
    """Scan traceback/error text and return a list of detected Issues, most relevant first."""
    issues: List[Issue] = []
    seen_kinds = set()

    for match in RE_MODULE_NOT_FOUND.finditer(text):
        issues.append(_issue_from_pkg_lookup(match.group(1), "module_not_found",
                                              "Missing module: '{}'"))

    for match in RE_IMPORT_ERROR_NAMED.finditer(text):
        issues.append(_issue_from_pkg_lookup(match.group(1), "import_error",
                                              "Import error for: '{}'"))

    if RE_EXTERNALLY_MANAGED.search(text) and "externally_managed" not in seen_kinds:
        seen_kinds.add("externally_managed")
        issues.append(Issue(
            kind="externally_managed",
            title="pip refuses to install: externally-managed-environment",
            note="Newer Termux Python builds protect the system environment from plain pip installs.",
            fix=[
                "pip install --break-system-packages <package>",
                "# Or, cleaner: create a venv first:",
                "python -m venv ~/venv && source ~/venv/bin/activate",
            ],
            difficulty="easy",
        ))

    for match in RE_FAILED_WHEEL.finditer(text):
        pkg_name = match.group(1).lower()
        info = packages.lookup(pkg_name)
        if info:
            issues.append(Issue(
                kind="build_failed",
                title=f"Wheel build failed for '{pkg_name}'",
                package=pkg_name,
                note=info["note"],
                fix=info["fix"],
                difficulty=info["difficulty"],
            ))
        else:
            issues.append(Issue(
                kind="build_failed",
                title=f"Wheel build failed for '{pkg_name}'",
                package=pkg_name,
                note="This package needs to compile native code and something in that chain is missing.",
                fix=[
                    "pkg install build-essential",
                    f"pip install {pkg_name}",
                    f"# If it still fails: pkg search {pkg_name}",
                ],
                difficulty="unknown",
            ))

    for match in RE_MISSING_SO.finditer(text):
        lib = match.group(1)
        pkg_for_lib = packages.lookup_so(lib)
        if pkg_for_lib:
            issues.append(Issue(
                kind="missing_so",
                title=f"Missing shared library: {lib}",
                note="A compiled extension needs this native library and it isn't installed.",
                fix=[f"pkg install {pkg_for_lib}"],
                difficulty="easy",
            ))
        else:
            issues.append(Issue(
                kind="missing_so",
                title=f"Missing shared library: {lib}",
                note="Couldn't map this library to a known Termux package automatically.",
                fix=[f"pkg search {lib.replace('.so', '')}"],
                difficulty="unknown",
            ))

    if RE_GCC_MISSING.search(text) and "no_compiler" not in seen_kinds:
        seen_kinds.add("no_compiler")
        issues.append(Issue(
            kind="no_compiler",
            title="No C compiler available",
            note="A package needs to compile native code but Termux has no compiler installed yet.",
            fix=["pkg install build-essential"],
            difficulty="easy",
        ))

    for match in RE_NO_MATCHING_DIST.finditer(text):
        pkg_name = match.group(1).lower()
        issues.append(Issue(
            kind="no_matching_dist",
            title=f"No matching distribution for '{pkg_name}'",
            package=pkg_name,
            note="Either the package name is wrong, or there's no wheel for this Python/arch combo.",
            fix=[
                f"pip index versions {pkg_name}",
                f"pkg search {pkg_name}",
            ],
            difficulty="unknown",
        ))

    if RE_PERMISSION_DENIED.search(text) and "permission" not in seen_kinds:
        seen_kinds.add("permission")
        issues.append(Issue(
            kind="permission",
            title="Permission denied",
            note="Termux's storage sandboxing or pip's target directory permissions are blocking the write.",
            fix=[
                "termux-setup-storage   # if writing to shared storage",
                "pip install --user <package>   # if writing to site-packages",
            ],
            difficulty="easy",
        ))

    return issues
