"""Spec Scope Verifier."""
from pathlib import Path
import sys
import ast
import argparse

def verify_edit(allowed_files: list[str], target_file: str, code_content: str) -> tuple[bool, str]:
    if target_file not in allowed_files:
        return False, f"SCOPE VIOLATION: '{target_file}' is not in allowed files {allowed_files}."
    try:
        ast.parse(code_content, filename=target_file)
    except SyntaxError as e:
        return False, f"AST SYNTAX ERROR: {e}"
    return True, "OK"

if __name__ == "__main__":
    print("Spec Scope Verifier active.")
