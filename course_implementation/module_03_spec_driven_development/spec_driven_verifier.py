"""
Module 3: Spec-driven verifier that writes and tests a real JWT module.

The spec at SPEC.md is parsed, in-scope files are written, out-of-scope
writes are refused, and pytest is run against a real HS256 implementation.
"""

from __future__ import annotations

import ast
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time


sys.stdout.reconfigure(encoding="utf-8")

MODULE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = MODULE_DIR / "output"
sys.path.append(str(MODULE_DIR.parent))
from common.jwt_tools import (  # noqa: E402
    auth_validator_source,
    encode_jwt,
    test_auth_source,
    validate_jwt,
)
from common.llm_client import CourseLLMClient  # noqa: E402


class SpecVerifier:
    """Parse SPEC.md and enforce file scope plus non-goal keywords."""

    def __init__(self, spec_path: Path, workspace: Path) -> None:
        self.spec_path = spec_path
        self.workspace = workspace
        self.allowed_files: list[str] = []
        self.forbidden_files: list[str] = []
        self.non_goals: list[str] = []
        self.llm_client = CourseLLMClient()
        self.parse_spec()

    def parse_spec(self) -> None:
        content = self.spec_path.read_text(encoding="utf-8")

        allowed_line = re.search(r"Allowed Files:\s*(.+)$", content, re.MULTILINE)
        if allowed_line:
            self.allowed_files = re.findall(r"`([^`]+)`", allowed_line.group(1))

        forbidden_line = re.search(r"Forbidden Files:\s*(.+)$", content, re.MULTILINE)
        if forbidden_line:
            self.forbidden_files = re.findall(r"`([^`]+)`", forbidden_line.group(1))

        non_goals_match = re.search(
            r"^## 3\. Explicit Non-Goals\s*$(?P<body>.*?)(?=^##\s|\Z)",
            content,
            re.MULTILINE | re.DOTALL,
        )
        if non_goals_match:
            self.non_goals = [
                line.removeprefix("-").strip()
                for line in non_goals_match.group("body").splitlines()
                if line.strip().startswith("-")
            ]

        print("[Spec Verifier] Parsed SPEC.md:")
        print(f"  Allowed Files Scope: {self.allowed_files}")
        print(f"  Forbidden Files: {self.forbidden_files}")
        print(f"  Explicit Non-Goals: {self.non_goals}")
        if not self.allowed_files or not self.non_goals:
            raise ValueError("SPEC.md did not yield allowed files and non-goals.")

    def _normalized(self, target_file: str) -> str:
        return Path(target_file).as_posix().lstrip("./")

    def attempt_write(self, target_file: str, code: str) -> tuple[bool, str]:
        """
        Write only when the relative path is allowed and the body does
        not implement a listed non-goal. Returns (written, reason).
        """
        print(f"\n[Spec Verifier] Auditing proposed write to '{target_file}'...")
        relative = self._normalized(target_file)
        dest = (self.workspace / relative).resolve()

        if relative not in self.allowed_files or relative in self.forbidden_files:
            print(
                f"  [BLOCKED] SCOPE VIOLATION: '{relative}' is outside "
                f"allowed spec scope {self.allowed_files}."
            )
            return False, "SCOPE_VIOLATION"

        if not dest.is_relative_to(self.workspace.resolve()):
            print(f"  [BLOCKED] PATH VIOLATION: '{dest}' escapes the workspace.")
            return False, "PATH_VIOLATION"

        lowered = code.lower()
        if "database" in lowered or "connect_db" in lowered or "oauth2" in lowered:
            print(
                "  [BLOCKED] NON-GOAL VIOLATION: diff mentions database "
                "or OAuth2 refresh logic."
            )
            return False, "NON_GOAL_VIOLATION"

        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(code, encoding="utf-8")
        ast.parse(code, filename=str(dest))
        print(f"  [PASS] Wrote {dest} ({dest.stat().st_size} bytes).")
        return True, str(dest)


def run_pytest(workspace: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "tests/test_auth.py",
            "-q",
            "--tb=short",
            "-p",
            "no:cacheprovider",
        ],
        cwd=workspace,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )


def main() -> int:
    print("=" * 60)
    print("MODULE 3 DEMO: SPEC-DRIVEN DEVELOPMENT VERIFIER")
    print("=" * 60)

    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir()

    spec_path = MODULE_DIR / "SPEC.md"
    verifier = SpecVerifier(spec_path, OUTPUT_DIR)
    verifier.llm_client.complete("Generate auth_validator.py according to SPEC.md")

    wrote_impl, impl_reason = verifier.attempt_write(
        "auth_validator.py", auth_validator_source()
    )
    refused_db, db_reason = verifier.attempt_write(
        "database.py", "def connect_db():\n    pass\n"
    )
    refused_nongoal, nongoal_reason = verifier.attempt_write(
        "auth_validator.py",
        "import database\n\ndef validate_jwt(token):\n    return database.connect_db()\n",
    )
    wrote_tests, test_reason = verifier.attempt_write(
        "tests/test_auth.py", test_auth_source()
    )

    db_absent = not (OUTPUT_DIR / "database.py").exists()
    impl_intact = "import database" not in (
        (OUTPUT_DIR / "auth_validator.py").read_text(encoding="utf-8")
        if wrote_impl
        else ""
    )

    print("\n[Spec Verifier] Running real pytest against the written module...")
    pytest_result = run_pytest(OUTPUT_DIR)
    pytest_output = (pytest_result.stdout + pytest_result.stderr).strip()
    print(pytest_output)
    pytest_ok = pytest_result.returncode == 0 and "passed" in pytest_output

    sys.path.insert(0, str(OUTPUT_DIR))
    from auth_validator import validate_jwt as disk_validate  # type: ignore  # noqa: E402

    live_token = encode_jwt({"user_id": "123", "roles": ["user"], "exp": time.time() + 60})
    live_result = disk_validate(live_token)
    expired_token = encode_jwt({"user_id": "123", "exp": time.time() - 30})
    expired_result = disk_validate(expired_token)
    print(f"\n[Live call] valid token -> {live_result}")
    print(f"[Live call] expired token -> {expired_result}")

    evidence = {
        "allowed_files": verifier.allowed_files,
        "wrote_impl": wrote_impl,
        "impl_path": impl_reason,
        "refused_database": (not refused_db) and db_absent,
        "refused_nongoal": (not refused_nongoal) and impl_intact,
        "wrote_tests": wrote_tests,
        "pytest_returncode": pytest_result.returncode,
        "pytest_output": pytest_output,
        "live_valid": live_result,
        "live_expired": expired_result,
    }
    evidence_path = OUTPUT_DIR / "run_evidence.json"
    evidence_path.write_text(json.dumps(evidence, indent=2), encoding="utf-8")
    print(f"[OUTPUT] {evidence_path}")

    ok = (
        wrote_impl
        and wrote_tests
        and db_absent
        and impl_intact
        and pytest_ok
        and live_result.get("valid") is True
        and live_result.get("user_id") == "123"
        and expired_result.get("error") == "EXPIRED"
    )

    print("\n" + "=" * 60)
    if ok:
        print("MODULE 3 DEMO COMPLETE: Real JWT module written and tested.")
        print("=" * 60)
        return 0
    print("MODULE 3 DEMO FAILED: spec write, pytest, or live JWT check failed.")
    print("=" * 60)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
