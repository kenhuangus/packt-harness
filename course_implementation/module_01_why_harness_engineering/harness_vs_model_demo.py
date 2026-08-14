"""
Module 1: Harness vs un-harnessed execution.

Both sides run real subprocesses against a real workspace. The un-harnessed
side deletes sandbox log files. The harnessed side blocks the same command
before any file is removed.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys


sys.stdout.reconfigure(encoding="utf-8")

MODULE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = MODULE_DIR / "output"
sys.path.append(str(MODULE_DIR.parent))
from common.llm_client import CourseLLMClient  # noqa: E402


FORBIDDEN_PATTERNS = [
    r"rm\s+-rf",
    r"sudo",
    r"chmod\s+777",
    r"git\s+push\s+--force",
]


def prepare_workspace(root: Path) -> None:
    """
    Build a workspace that fails pytest for a real reason and has logs
    a reckless cleanup command can actually delete.
    """
    if root.exists():
        shutil.rmtree(root)
    tests = root / "tests"
    logs = root / "var" / "log"
    tests.mkdir(parents=True)
    logs.mkdir(parents=True)
    (root / "auth.py").write_text(
        "import packt_jwt_runtime\n\n"
        "def validate(token):\n"
        "    return packt_jwt_runtime.decode(token)\n",
        encoding="utf-8",
    )
    (tests / "auth_test.py").write_text(
        "from auth import validate\n\n"
        "def test_validate():\n"
        "    assert validate('token') == {'ok': True}\n",
        encoding="utf-8",
    )
    (tests / "__init__.py").write_text("", encoding="utf-8")
    (logs / "app.log").write_text("auth startup ok\n", encoding="utf-8")


def run_pytest(workspace: Path) -> subprocess.CompletedProcess:
    """Run the workspace test file with the same interpreter."""
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "tests/auth_test.py",
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
    )


def delete_sandbox_logs(workspace: Path) -> list[str]:
    """
    Execute the un-harnessed cleanup: remove workspace/var/log.

    This is a real delete, confined to the demo workspace. It is not
    `rm -rf /var/log` on the host.
    """
    target = workspace / "var" / "log"
    removed = []
    if target.exists():
        for path in target.iterdir():
            removed.append(str(path))
        shutil.rmtree(target)
    return removed


class UnharnessedAgent:
    """No policy, no loop stop, no sandbox. Commands run as requested."""

    def __init__(self, llm_client: CourseLLMClient) -> None:
        self.llm_client = llm_client

    def run_task(self, workspace: Path) -> dict:
        print("\n--- UN-HARNESSED AGENT ---")
        response = self.llm_client.complete(
            "In one sentence, say why a coding agent needs a harness around the model.",
            system_prompt="You are a concise coding-agent instructor.",
        )
        if not response or response.startswith("[Harness Simulated"):
            raise RuntimeError("Module 1 requires a live local-model reply.")
        print(f"[LLM Response Output]: {response[:200]}")
        self.last_llm_reply = response

        pytest_runs = []
        for attempt in range(1, 4):
            print(f"[LLM Attempt {attempt}] Running: pytest tests/auth_test.py")
            result = run_pytest(workspace)
            excerpt = (result.stdout + result.stderr).strip().splitlines()
            last_line = excerpt[-1] if excerpt else "(no output)"
            print(f"[System Output] exit={result.returncode} {last_line}")
            pytest_runs.append(
                {
                    "attempt": attempt,
                    "returncode": result.returncode,
                    "last_line": last_line,
                }
            )

        print("[LLM Attempt 4] Running cleanup: rm -rf var/log")
        removed = delete_sandbox_logs(workspace)
        still_there = (workspace / "var" / "log" / "app.log").exists()
        print(
            f"[WARNING] UN-HARNESSED FAILURE: deleted {len(removed)} log "
            f"path(s); app.log exists={still_there}"
        )
        return {
            "pytest_runs": pytest_runs,
            "deleted": removed,
            "log_survived": still_there,
            "llm_reply": getattr(self, "last_llm_reply", ""),
        }


class HarnessedAgent:
    """
    Every command is inspected, then either executed or blocked.

    Safe commands go to a real subprocess. Destructive patterns never
    reach the filesystem. The same failing pytest command is stopped
    on the second identical no-progress retry.
    """

    def __init__(self, max_retries: int = 2) -> None:
        self.max_retries = max_retries
        self.command_history: list[str] = []

    def pre_execution_hook(self, command: str) -> None:
        for pattern in FORBIDDEN_PATTERNS:
            if re.search(pattern, command):
                raise PermissionError(
                    f"BLOCKED BY PRE-HOOK: Dangerous command pattern "
                    f"'{pattern}' detected."
                )

    def loop_detector(self, command: str) -> None:
        self.command_history.append(command)
        if len(self.command_history) >= self.max_retries:
            recent = self.command_history[-self.max_retries :]
            if len(set(recent)) == 1:
                raise RuntimeError(
                    f"BLOCKED BY HARNESS LOOP DETECTOR: Command '{command}' "
                    f"repeated {self.max_retries} times without progress."
                )

    def execute_tool_call(self, workspace: Path, command: str) -> dict:
        print(f"\n[Harness Evaluator] Inspecting tool call: run_shell('{command}')")
        try:
            self.pre_execution_hook(command)
            print("  [PASS] Pre-action hook passed: Command is safe.")
        except PermissionError as exc:
            print(f"  [BLOCKED] Security Violation: {exc}")
            return {"status": "BLOCKED", "reason": str(exc)}

        try:
            self.loop_detector(command)
            print("  [PASS] Loop detector passed: No execution trap.")
        except RuntimeError as exc:
            print(f"  [BLOCKED] Loop Detected: {exc}")
            return {"status": "LOOP_HALTED", "reason": str(exc)}

        if command.startswith("pytest"):
            result = run_pytest(workspace)
            print(
                f"  [EXECUTED] pytest exit={result.returncode}"
            )
            return {
                "status": "EXECUTED",
                "returncode": result.returncode,
                "stdout": result.stdout,
            }

        raise RuntimeError(f"No executor registered for command: {command}")


def main() -> int:
    print("=" * 60)
    print("MODULE 1 DEMO: WHY HARNESS ENGINEERING IS REQUIRED")
    print("=" * 60)

    OUTPUT_DIR.mkdir(exist_ok=True)
    llm_client = CourseLLMClient()

    unharnessed_root = OUTPUT_DIR / "unharnessed_workspace"
    prepare_workspace(unharnessed_root)
    raw = UnharnessedAgent(llm_client)
    unharnessed = raw.run_task(unharnessed_root)

    harnessed_root = OUTPUT_DIR / "harnessed_workspace"
    prepare_workspace(harnessed_root)
    print("\n--- HARNESSED AGENT ---")
    harness = HarnessedAgent(max_retries=2)
    first = harness.execute_tool_call(harnessed_root, "pytest tests/auth_test.py")
    second = harness.execute_tool_call(harnessed_root, "pytest tests/auth_test.py")
    third = harness.execute_tool_call(harnessed_root, "rm -rf var/log")
    log_survived = (harnessed_root / "var" / "log" / "app.log").exists()
    print(f"\n[Harness] sandbox log survived={log_survived}")

    evidence = {
        "unharnessed": unharnessed,
        "harnessed": {
            "first_pytest": {
                "status": first.get("status"),
                "returncode": first.get("returncode"),
            },
            "second_pytest": second,
            "rm": third,
            "log_survived": log_survived,
        },
    }
    evidence_path = OUTPUT_DIR / "run_evidence.json"
    evidence_path.write_text(json.dumps(evidence, indent=2), encoding="utf-8")
    print(f"[OUTPUT] {evidence_path}")

    unharnessed_ok = (
        len(unharnessed["pytest_runs"]) == 3
        and all(run["returncode"] != 0 for run in unharnessed["pytest_runs"])
        and unharnessed["log_survived"] is False
    )
    harnessed_ok = (
        first.get("status") == "EXECUTED"
        and first.get("returncode") != 0
        and second.get("status") == "LOOP_HALTED"
        and third.get("status") == "BLOCKED"
        and log_survived is True
    )

    print("\n" + "=" * 60)
    if unharnessed_ok and harnessed_ok:
        print("DEMO SUMMARY: Real pytest loops and a real sandbox delete were blocked by the harness.")
        print("=" * 60)
        return 0
    print("DEMO FAILED: expected un-harnessed delete + harnessed block did not both happen.")
    print("=" * 60)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
