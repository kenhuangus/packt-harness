"""Command Interception & Loop Detection Helper Script."""
import re
import sys
import argparse

FORBIDDEN_PATTERNS = [
    r"\brm\s+-[rR][fF]\b",
    r"\bsudo\b",
    r"\bchmod\s+777\b",
    r"\bdrop\s+database\b",
]

def check_command(command: str) -> tuple[bool, str]:
    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, command):
            return False, f"BLOCKED: Destructive pattern '{pattern}' detected."
    return True, "ALLOWED"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit shell command safety")
    parser.add_argument("--command", required=True, help="Shell command to evaluate")
    args = parser.parse_args()
    allowed, reason = check_command(args.command)
    print(f"[{'PASS' if allowed else 'FAIL'}] {reason}")
    sys.exit(0 if allowed else 1)
