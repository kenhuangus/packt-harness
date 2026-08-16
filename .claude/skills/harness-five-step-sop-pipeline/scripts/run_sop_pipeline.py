"""5-Step SOP Pipeline CLI Runner."""
from __future__ import annotations

from pathlib import Path
import subprocess
import sys


def main() -> int:
    here = Path(__file__).resolve()
    if ".claude" in here.parts:
        repo_root = here.parents[4]
    else:
        repo_root = here.parents[5]
    script_path = repo_root / "course_implementation" / "module_09_practical_workflow_pattern" / "five_step_sop_pipeline.py"
    res = subprocess.run([sys.executable, str(script_path)])
    return res.returncode


if __name__ == "__main__":
    sys.exit(main())
