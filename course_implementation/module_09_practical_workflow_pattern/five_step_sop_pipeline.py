"""
Module 9: A real five-step specification-to-review workflow.

Every reported result in this demonstration comes from work performed during
the current run. Temporary implementation and test files are always cleaned up.
"""

from __future__ import annotations

import difflib
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile


sys.stdout.reconfigure(encoding="utf-8")

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
MODULE_03_DIR = (
    REPOSITORY_ROOT
    / "course_implementation"
    / "module_03_spec_driven_development"
)
MODULE_04_DIR = (
    REPOSITORY_ROOT
    / "course_implementation"
    / "module_04_guardrails_and_hooks"
)
sys.path.insert(0, str(MODULE_04_DIR))

from guardrails_engine import GuardrailsEngine  # noqa: E402

COMMON_DIR = REPOSITORY_ROOT / "course_implementation" / "common"
sys.path.insert(0, str(COMMON_DIR.parent))
from common.jwt_tools import auth_validator_source, test_auth_source  # noqa: E402


def print_check(label: str, passed: bool, detail: str) -> bool:
    """Print only the result supplied by a check that has already run."""
    status = "PASS" if passed else "FAIL"
    print(f"  [{status}] {label}: {detail}")
    return passed


def parse_spec(spec_path: Path) -> tuple[list[str], list[str]]:
    """
    Step 1 helper: read the committed module 3 SPEC.md.

    Allowed files are the backtick-quoted names on the Allowed Files
    line. Non-goals are the dash list under heading 3. Either field
    empty is a hard error so the pipeline cannot claim a parse it
    did not perform.
    """
    content = spec_path.read_text(encoding="utf-8")

    allowed_line = re.search(
        r"^\s*-\s*Allowed Files:\s*(.+)$", content, re.MULTILINE
    )
    if allowed_line is None:
        raise ValueError("SPEC.md has no 'Allowed Files' declaration.")
    allowed_files = re.findall(r"`([^`]+)`", allowed_line.group(1))
    if not allowed_files:
        allowed_files = [
            item.strip()
            for item in allowed_line.group(1).split(",")
            if item.strip()
        ]

    non_goals_match = re.search(
        r"^## 3\. Explicit Non-Goals\s*$"
        r"(?P<body>.*?)"
        r"(?=^##\s|\Z)",
        content,
        re.MULTILINE | re.DOTALL,
    )
    if non_goals_match is None:
        raise ValueError("SPEC.md has no 'Explicit Non-Goals' section.")
    non_goals = [
        line.removeprefix("-").strip()
        for line in non_goals_match.group("body").splitlines()
        if line.strip().startswith("-")
    ]

    if not allowed_files or not non_goals:
        raise ValueError("SPEC.md scope or non-goals parsed as empty.")
    return allowed_files, non_goals


class ScopeEnforcer:
    """
    Step 2: allow writes only to the exact relative paths in the spec.

    database.py is rejected even though the workspace is writable.
    Paths that resolve outside the temp workspace are also rejected.
    """

    def __init__(self, workspace: Path, allowed_files: list[str]) -> None:
        self.workspace = workspace.resolve()
        self.allowed_files = {
            Path(item).as_posix().lstrip("./") for item in allowed_files
        }

    def attempt_write(
        self, relative_path: str, content: str
    ) -> tuple[bool, str]:
        normalized = Path(relative_path).as_posix().lstrip("./")
        target = (self.workspace / normalized).resolve()
        if normalized not in self.allowed_files:
            return False, f"'{normalized}' is not in the allowed file scope."
        if not target.is_relative_to(self.workspace):
            return False, f"'{normalized}' resolves outside the workspace."

        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return True, f"Wrote allowed file '{normalized}'."


class FiveStepSOPPipeline:
    """
    Run the five SOP steps against a real spec, real guardrails, and
    a real pytest subprocess.

    Temporary files are always deleted. Human PR merge is printed as
    out-of-band so the demo does not claim it opened a pull request.
    """

    def __init__(self) -> None:
        self.spec_path = MODULE_03_DIR / "SPEC.md"
        self.results: list[bool] = []

    def record(self, label: str, passed: bool, detail: str) -> None:
        self.results.append(print_check(label, passed, detail))

    def run_pipeline(self, feature_name: str) -> int:
        print("=" * 60)
        print(f"MODULE 9 DEMO: 5-STEP SOP PIPELINE FOR '{feature_name}'")
        print("=" * 60)

        try:
            allowed_files, non_goals = parse_spec(self.spec_path)
        except (OSError, ValueError) as exc:
            print("\n[STEP 1: SPEC FIRST] Parsing SPEC.md requirements...")
            self.record("SPEC.md parsed", False, str(exc))
            return self.finish()

        print("\n[STEP 1: SPEC FIRST] Parsing SPEC.md requirements...")
        self.record(
            "SPEC.md parsed",
            True,
            f"read {self.spec_path}",
        )
        print(f"  Allowed file scope: {allowed_files}")
        print(f"  Explicit non-goals: {non_goals}")

        implementation = auth_validator_source()
        tests = test_auth_source()

        with tempfile.TemporaryDirectory(prefix="module09_pipeline_") as temp:
            workspace = Path(temp)
            enforcer = ScopeEnforcer(workspace, allowed_files)

            print(
                "\n[STEP 2: CONSTRAINED EXECUTION] "
                "Enforcing the parsed allowed-file scope..."
            )
            wrote_allowed, allowed_reason = enforcer.attempt_write(
                "auth_validator.py", implementation
            )
            allowed_exists = (workspace / "auth_validator.py").is_file()
            self.record(
                "In-scope edit",
                wrote_allowed and allowed_exists,
                allowed_reason,
            )

            wrote_forbidden, forbidden_reason = enforcer.attempt_write(
                "database.py", "def connect_db():\n    pass\n"
            )
            forbidden_absent = not (workspace / "database.py").exists()
            self.record(
                "Out-of-scope edit rejected",
                not wrote_forbidden and forbidden_absent,
                f"{forbidden_reason} File created: {not forbidden_absent}.",
            )

            print(
                "\n[STEP 3: DETERMINISTIC CHECKS] "
                "Running module 4 guardrails..."
            )
            engine = GuardrailsEngine(workspace)
            syntax_clean, syntax_messages = engine.audit_ast_and_secrets(
                "auth_validator.py", implementation
            )
            self.record(
                "AST syntax and generated-code secret scan",
                syntax_clean,
                "; ".join(syntax_messages),
            )

            secret_clean, secret_messages = engine.audit_ast_and_secrets(
                "leaked_config.py",
                'API_KEY = "sk-proj-abcdefghijklmnopqrstuvwxyz123456"\n',
            )
            self.record(
                "Secret-bearing code rejected",
                not secret_clean
                and any("secret" in item.lower() for item in secret_messages),
                "; ".join(secret_messages),
            )

            shell_allowed, shell_reason = engine.intercept_shell_command(
                "sudo rm -rf /var/config"
            )
            self.record(
                "Dangerous shell command intercepted",
                not shell_allowed,
                shell_reason,
            )

            print(
                "\n[STEP 4: TEST VERIFICATION] "
                "Running a real temporary pytest suite..."
            )
            wrote_tests, test_write_reason = enforcer.attempt_write(
                "tests/test_auth.py", tests
            )
            if not wrote_tests:
                self.record("Pytest suite", False, test_write_reason)
            else:
                environment = os.environ.copy()
                environment["PYTHONDONTWRITEBYTECODE"] = "1"
                command = [
                    sys.executable,
                    "-m",
                    "pytest",
                    str(workspace / "tests" / "test_auth.py"),
                    "-q",
                    "-p",
                    "no:cacheprovider",
                ]
                try:
                    completed = subprocess.run(
                        command,
                        cwd=workspace,
                        capture_output=True,
                        text=True,
                        encoding="utf-8",
                        errors="replace",
                        timeout=30,
                        env=environment,
                        check=False,
                    )
                except (OSError, subprocess.TimeoutExpired) as exc:
                    self.record("Pytest suite", False, str(exc))
                else:
                    output = "\n".join(
                        part.strip()
                        for part in (completed.stdout, completed.stderr)
                        if part.strip()
                    )
                    if output:
                        for line in output.splitlines():
                            print(f"    {line}")
                    passed_match = re.search(
                        r"(?P<count>\d+)\s+passed\b", output
                    )
                    failed_match = re.search(
                        r"(?P<count>\d+)\s+failed\b", output
                    )
                    passed_count = (
                        int(passed_match.group("count"))
                        if passed_match
                        else 0
                    )
                    failed_count = (
                        int(failed_match.group("count"))
                        if failed_match
                        else 0
                    )
                    pytest_ok = (
                        completed.returncode == 0
                        and passed_match is not None
                        and passed_count > 0
                        and failed_count == 0
                    )
                    self.record(
                        "Pytest suite",
                        pytest_ok,
                        f"return code {completed.returncode}; "
                        f"{passed_count} passed, {failed_count} failed.",
                    )

            print(
                "\n[STEP 5: HUMAN REVIEW] "
                "Showing the implementation actually produced..."
            )
            diff = difflib.unified_diff(
                [],
                implementation.splitlines(),
                fromfile="/dev/null",
                tofile="auth_validator.py",
                lineterm="",
            )
            diff_lines = list(diff)
            for line in diff_lines:
                print(f"  {line}")
            self.record(
                "Review diff generated",
                bool(diff_lines) and allowed_exists,
                f"{len(implementation.splitlines())} implementation lines "
                "shown from the temporary workspace.",
            )
            print(
                "  Human approval and any PR merge are out-of-band; "
                "this pipeline did not create or merge a PR."
            )

            output_dir = Path(__file__).resolve().parent / "output"
            if output_dir.exists():
                shutil.rmtree(output_dir)
            shutil.copytree(workspace, output_dir)
            print(f"  [OUTPUT] copied workspace to {output_dir}")

        return self.finish()

    def finish(self) -> int:
        print("\n" + "=" * 60)
        if self.results and all(self.results):
            print("PIPELINE COMPLETE: ALL REPORTED CHECKS EXECUTED AND PASSED")
            print("=" * 60)
            return 0
        failed = sum(not result for result in self.results)
        print(f"PIPELINE FAILED: {failed} REPORTED CHECK(S) DID NOT PASS")
        print("=" * 60)
        return 1


def main() -> int:
    pipeline = FiveStepSOPPipeline()
    return pipeline.run_pipeline("User Auth Token Validator")


if __name__ == "__main__":
    raise SystemExit(main())
