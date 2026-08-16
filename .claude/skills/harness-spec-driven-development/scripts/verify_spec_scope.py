"""Spec Scope Verifier."""
from __future__ import annotations

import argparse
import ast
from pathlib import Path
import sys


def verify_edit(allowed_files: list[str], target_file: str, code_content: str) -> tuple[bool, str]:
    if target_file not in allowed_files:
        return False, f"SCOPE VIOLATION: '{target_file}' is not in allowed files {allowed_files}."
    try:
        ast.parse(code_content, filename=target_file)
    except SyntaxError as e:
        return False, f"AST SYNTAX ERROR: {e}"
    return True, "OK"


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify code edit against spec scope")
    parser.add_argument("--allowed", nargs="+", default=["auth_validator.py", "tests/test_auth.py"])
    parser.add_argument("--file", default="auth_validator.py")
    parser.add_argument("--content", default="def validate_jwt(t):\n    return {'valid': True}\n")
    args = parser.parse_args()

    ok, reason = verify_edit(args.allowed, args.file, args.content)
    print(f"[{'PASS' if ok else 'FAIL'}] {reason}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
