"""5-Gate Production Harness Auditor CLI."""
from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys


def find_repo_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / "pyproject.toml").is_file() or (candidate / ".git").exists():
            return candidate
    raise RuntimeError("repository root not found from " + str(start))


def run_audit(target_dir: str = ".") -> int:
    repo_root = find_repo_root(Path(__file__).resolve().parent)
    script_path = repo_root / "course_implementation" / "module_10_closing_and_principles" / "production_harness_audit.py"
    target_path = Path(target_dir).resolve()
    if target_dir == ".":
        target_path = repo_root
    res = subprocess.run([sys.executable, str(script_path), str(target_path)])
    return res.returncode


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run the 5-gate production readiness audit against a project."
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=".",
        help="project directory to audit (default: this repository root)",
    )
    sys.exit(run_audit(parser.parse_args().target))
