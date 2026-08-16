"""5-Gate Production Harness Auditor CLI."""
from __future__ import annotations

from pathlib import Path
import subprocess
import sys


def run_audit(target_dir: str = ".") -> int:
    here = Path(__file__).resolve()
    if ".claude" in here.parts:
        repo_root = here.parents[4]
    else:
        repo_root = here.parents[5]
    script_path = repo_root / "course_implementation" / "module_10_closing_and_principles" / "production_harness_audit.py"
    target_path = Path(target_dir).resolve()
    if target_dir == ".":
        target_path = repo_root
    res = subprocess.run([sys.executable, str(script_path), str(target_path)])
    return res.returncode


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    sys.exit(run_audit(target))
