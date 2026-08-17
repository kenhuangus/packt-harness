"""5-Step SOP Pipeline CLI Runner."""
from __future__ import annotations

from pathlib import Path
import subprocess
import sys


def find_repo_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / "pyproject.toml").is_file() or (candidate / ".git").exists():
            return candidate
    raise RuntimeError("repository root not found from " + str(start))


def main() -> int:
    repo_root = find_repo_root(Path(__file__).resolve().parent)
    script_path = repo_root / "course_implementation" / "module_09_practical_workflow_pattern" / "five_step_sop_pipeline.py"
    res = subprocess.run([sys.executable, str(script_path)])
    return res.returncode


if __name__ == "__main__":
    sys.exit(main())
