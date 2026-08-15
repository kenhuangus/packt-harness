"""5-Gate Production Harness Auditor CLI."""
import sys
from pathlib import Path

def run_audit(target_dir: str):
    root = Path(target_dir)
    mem_ok = (root / "CLAUDE.md").is_file() and (root / "AGENTS.md").is_file()
    print(f"Memory Files Gate: {'PASS' if mem_ok else 'FAIL'}")

if __name__ == "__main__":
    run_audit(".")
