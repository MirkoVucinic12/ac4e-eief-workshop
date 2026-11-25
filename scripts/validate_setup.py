#!/usr/bin/env python3
"""Validate the workshop setup without modifying the project.

The script reports missing optional coding-assistant command lines as INFO.
A Cursor participant does not need ``claude`` or ``codex`` installed, and the
reverse. Desktop apps cannot be verified here.
"""

from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIN_PYTHON = (3, 10)
OPTIONAL_COMMANDS = frozenset(
    {"claude", "codex", "cursor", "cursor-agent", "agent", "code"}
)
OPTIONAL_PACKAGES = frozenset({"mcp-python", "httpx"})

REQUIRED_PATHS = [
    ROOT / "START_HERE.md",
    ROOT / "SETUP.md",
    ROOT / "AGENTS.md",
    ROOT / "examples" / "card-krueger-toy" / "data" / "toy_fast_food.csv",
    ROOT / "examples" / "card-krueger-toy" / "src" / "did_analysis.py",
    ROOT / ".claude" / "skills" / "replication-checker" / "SKILL.md",
]


@dataclass
class CheckResult:
    """One setup check and a human-readable detail line."""

    label: str
    status: str
    detail: str


def run_version(label: str, command: list[str], required: bool = True) -> CheckResult:
    """Run a ``--version``-style command and classify the outcome."""
    executable = shutil.which(command[0])
    if executable is None:
        status = "MISSING" if required else "INFO"
        detail = f"{command[0]} not found"
        return CheckResult(label, status, detail)

    try:
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except Exception as exc:  # pragma: no cover - diagnostic path
        return CheckResult(label, "WARN", f"{command[0]} exists but failed: {exc}")

    output = (completed.stdout or completed.stderr).strip().splitlines()
    detail = output[0] if output else f"{command[0]} found at {executable}"
    status = "OK" if completed.returncode == 0 else "WARN"
    return CheckResult(label, status, detail)


def check_python_version() -> CheckResult:
    """Require Python 3.10 or newer."""
    version = sys.version.split()[0]
    if sys.version_info < MIN_PYTHON:
        minimum = ".".join(str(part) for part in MIN_PYTHON)
        return CheckResult(
            "python",
            "MISSING",
            f"{version} is below the workshop minimum ({minimum})",
        )
    return CheckResult("python", "OK", version)


def check_python_package(
    module_name: str,
    label: str,
    required: bool = True,
) -> CheckResult:
    """Check whether a Python module is importable in this interpreter."""
    if importlib.util.find_spec(module_name) is None:
        status = "MISSING" if required else "INFO"
        return CheckResult(label, status, f"Python package '{module_name}' not installed")
    return CheckResult(label, "OK", f"Python package '{module_name}' importable")


def check_course_paths() -> CheckResult:
    """Confirm the clone contains the files the eight hours need."""
    missing = [path.relative_to(ROOT) for path in REQUIRED_PATHS if not path.exists()]
    if missing:
        joined = ", ".join(str(path) for path in missing)
        return CheckResult("course_files", "MISSING", f"missing paths: {joined}")
    return CheckResult("course_files", "OK", "core workshop paths present")


def _is_optional(check: CheckResult) -> bool:
    """Return True when a missing result is allowed for this workshop."""
    return check.label in OPTIONAL_COMMANDS or check.label in OPTIONAL_PACKAGES


def main() -> int:
    """Print setup checks and return 1 if a required item is missing."""
    checks = [
        check_course_paths(),
        check_python_version(),
        run_version("git", ["git", "--version"]),
        run_version("code", ["code", "--version"], required=False),
        run_version("claude", ["claude", "--version"], required=False),
        run_version("codex", ["codex", "--version"], required=False),
        run_version("cursor", ["cursor", "--version"], required=False),
        run_version("cursor-agent", ["cursor-agent", "--version"], required=False),
        run_version("agent", ["agent", "--version"], required=False),
        check_python_package("pandas", "pandas"),
        check_python_package("numpy", "numpy"),
        check_python_package("pytest", "pytest"),
        check_python_package("httpx", "httpx", required=False),
        check_python_package("mcp", "mcp-python", required=False),
    ]

    for check in checks:
        print(f"{check.status}: {check.label} - {check.detail}")

    required_failures = [
        check for check in checks if check.status == "MISSING" and not _is_optional(check)
    ]
    if required_failures:
        print("\nSetup is incomplete. Revisit SETUP.md for the missing required items.")
        return 1

    print(
        "\nINFO: desktop-app - Claude Code, Codex, Cursor, and VS Code "
        "extensions cannot be verified here. Open the app on this repository "
        "folder and run one read-only prompt from SETUP.md."
    )
    print(
        "\nINFO: next - with the virtual environment active, run:\n"
        "  python3 -m pytest examples/card-krueger-toy/tests examples/mini-economics/tests"
    )
    print("\nSetup check complete. Optional assistant command lines may still need sign-in.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
