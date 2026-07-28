"""
Module 2: Core Harness Stack & System Architecture
Demonstrates the 5 pillars of a production AI coding harness:
1. Memory Files (CLAUDE.md / AGENTS.md)
2. Scoped Tools & Path Sandboxing
3. Deterministic Hooks & Policy Engine
4. Context Token Budgeting & Compacting
5. JSONL Tracing & Observability
"""

import ast
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

class ContextTokenBudgeter:
    """Manages token allocation and compacts long context windows to prevent amnesia."""
    def __init__(self, max_tokens=128000):
        self.max_tokens = max_tokens
        self.allocations = {
            'memory': int(max_tokens * 0.20),
            'spec': int(max_tokens * 0.20),
            'workspace': int(max_tokens * 0.50),
            'output_buffer': int(max_tokens * 0.10)
        }
        
    def estimate_tokens(self, text: str) -> int:
        # Standard token estimation: ~1.33 tokens per word
        words = text.split()
        return int(len(words) * 1.33)
        
    def compact_output(self, raw_output: str, max_lines=20) -> str:
        lines = raw_output.splitlines()
        if len(lines) <= max_lines:
            return raw_output
        header = lines[:5]
        footer = lines[-15:]
        omitted_count = len(lines) - 20
        return "\n".join(header) + f"\n\n... [HARNESS COMPACTION: Omitted {omitted_count} lines of compiler stdout] ...\n\n" + "\n".join(footer)

class CoreHarnessStack:
    def __init__(self, workspace_root: str):
        self.workspace_root = os.path.abspath(workspace_root)
        self.audit_log_path = os.path.join(self.workspace_root, "events.jsonl")
        self.budgeter = ContextTokenBudgeter()

    def log_event(self, event_type: str, details: dict):
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "details": details
        }
        with open(self.audit_log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(payload) + "\n")

    def validate_tool_permission(self, tool_name: str, target_path: str = None) -> bool:
        allowed_tools = ["read_file", "write_file", "run_test", "list_dir"]
        if tool_name not in allowed_tools:
            self.log_event("PERMISSION_DENIED", {"reason": f"Tool '{tool_name}' not in allowed tool set."})
            return False

        if target_path:
            abs_target = os.path.abspath(target_path)
            if not abs_target.startswith(self.workspace_root):
                self.log_event("PATH_TRAVERSAL_BLOCKED", {"path": target_path, "workspace": self.workspace_root})
                return False

        self.log_event("PERMISSION_GRANTED", {"tool": tool_name, "path": target_path})
        return True

    def run_post_edit_hook(self, file_path: str, code_content: str) -> bool:
        if "sk-proj-" in code_content:
            self.log_event("SECURITY_VIOLATION", {"file": file_path, "issue": "Hardcoded OpenAI secret key detected!"})
            return False

        if not code_content.strip():
            self.log_event("QUALITY_VIOLATION", {"file": file_path, "issue": "Empty code edit proposal."})
            return False

        self.log_event("HOOK_PASS", {"file": file_path, "status": "Post-edit checks passed."})
        return True

if __name__ == "__main__":
    print("=" * 72)
    print("MODULE 2 DEMO: CORE HARNESS STACK (5 PILLARS)")
    print("=" * 72)

    module_dir = os.path.dirname(os.path.abspath(__file__))
    memory_path = os.path.join(module_dir, "AGENTS.md")
    try:
        with open(memory_path, "rb") as memory_file:
            memory_bytes = memory_file.read()
    except OSError as exc:
        print(f"[FAIL] Could not load persistent guidelines: {exc}")
        raise SystemExit(1)

    print(
        "[Pillar 1 - Memory] Loaded persistent guidelines from "
        f"'AGENTS.md' ({len(memory_bytes)} bytes)"
    )

    with tempfile.TemporaryDirectory(prefix="module_02_harness_") as workspace:
        harness = CoreHarnessStack(workspace)
        print("Allocations:", harness.budgeter.allocations)

        print("\n>>> HARNESS EXECUTION TASK: write_file <<<")
        sample_path = os.path.join(workspace, "sample_module.py")
        permission_granted = harness.validate_tool_permission("write_file", sample_path)
        if not permission_granted:
            print("[FAIL] Permission validation unexpectedly rejected sample_module.py.")
            raise SystemExit(1)
        print(
            "[Pillar 2 - Permission] Tool 'write_file' and path "
            f"'{sample_path}' validated."
        )

        sample_code = "def add(left: int, right: int) -> int:\n    return left + right\n"
        hook_passed = harness.run_post_edit_hook(sample_path, sample_code)
        if not hook_passed:
            print("[FAIL] Code safety inspection unexpectedly rejected safe code.")
            raise SystemExit(1)
        print("[Pillar 3 - Pre-Hook] Code safety inspection passed.")

        try:
            with open(sample_path, "w", encoding="utf-8") as sample_file:
                sample_file.write(sample_code)
            print(
                "[Pillar 3 - Post-Hook] Running AST static analysis on "
                "'sample_module.py'..."
            )
            with open(sample_path, "r", encoding="utf-8") as sample_file:
                ast.parse(sample_file.read(), filename=sample_path)
        except (OSError, SyntaxError) as exc:
            print(f"[FAIL] AST static analysis failed: {exc}")
            raise SystemExit(1)
        print("  [PASS] AST syntax valid.")

        harness.log_event("WRITE_FILE_SUCCESS", {"path": sample_path})
        try:
            with open(harness.audit_log_path, "r", encoding="utf-8") as audit_file:
                last_event = json.loads(audit_file.readlines()[-1])
        except (OSError, IndexError, json.JSONDecodeError) as exc:
            print(f"[FAIL] Could not verify the write trace event: {exc}")
            raise SystemExit(1)
        if last_event.get("event_type") != "WRITE_FILE_SUCCESS":
            print("[FAIL] WRITE_FILE_SUCCESS was not the final audit event.")
            raise SystemExit(1)
        print("[Pillar 5 - Trace] Logged 'WRITE_FILE_SUCCESS' to JSONL audit file.")

        print("\n>>> HARNESS EXECUTION TASK: run_test <<<")
        permission_granted = harness.validate_tool_permission("run_test")
        if not permission_granted:
            print("[FAIL] Permission validation unexpectedly rejected run_test.")
            raise SystemExit(1)
        print("[Pillar 2 - Permission] Tool 'run_test' and path 'None' validated.")

        test_path = os.path.join(workspace, "test_sample_module.py")
        test_code = (
            "from sample_module import add\n\n"
            "def test_add() -> None:\n"
            "    assert add(2, 3) == 5\n"
        )
        try:
            with open(test_path, "w", encoding="utf-8") as test_file:
                test_file.write(test_code)
            print("[Pillar 4 - Test Runner] Executing test suite: pytest")
            test_result = subprocess.run(
                [sys.executable, "-m", "pytest", "-q", test_path],
                cwd=workspace,
                capture_output=True,
                text=True,
                timeout=60,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            print(f"[FAIL] pytest could not be executed: {exc}")
            raise SystemExit(1)

        if test_result.returncode != 0:
            output = (test_result.stdout + test_result.stderr).strip()
            if "No module named pytest" in output:
                print("[SKIPPED] pytest is not installed for this interpreter.")
            else:
                print(f"[FAIL] pytest exited with code {test_result.returncode}.")
                if output:
                    print(output)
            raise SystemExit(1)
        print(f"  [PASS] pytest exited with code {test_result.returncode}.")

        harness.log_event(
            "RUN_TEST_SUCCESS",
            {"runner": "pytest", "returncode": test_result.returncode},
        )
        try:
            with open(harness.audit_log_path, "r", encoding="utf-8") as audit_file:
                last_event = json.loads(audit_file.readlines()[-1])
        except (OSError, IndexError, json.JSONDecodeError) as exc:
            print(f"[FAIL] Could not verify the test trace event: {exc}")
            raise SystemExit(1)
        if last_event.get("event_type") != "RUN_TEST_SUCCESS":
            print("[FAIL] RUN_TEST_SUCCESS was not the final audit event.")
            raise SystemExit(1)
        print("[Pillar 5 - Trace] Logged 'RUN_TEST_SUCCESS' to JSONL audit file.")

        print("\n>>> HARNESS EXECUTION TASK: write_file <<<")
        traversal_target = os.path.join(
            workspace, os.pardir, os.pardir, "forbidden.py"
        )
        traversal_allowed = harness.validate_tool_permission(
            "write_file", traversal_target
        )
        try:
            with open(harness.audit_log_path, "r", encoding="utf-8") as audit_file:
                rejection_event = json.loads(audit_file.readlines()[-1])
        except (OSError, IndexError, json.JSONDecodeError) as exc:
            print(f"[FAIL] Could not verify the path rejection event: {exc}")
            raise SystemExit(1)
        rejection_logged = (
            rejection_event.get("event_type") == "PATH_TRAVERSAL_BLOCKED"
        )
        if traversal_allowed or not rejection_logged:
            print("[FAIL] The sandbox did not produce the expected path rejection.")
            raise SystemExit(1)

        harness.log_event(
            "HARNESS_ERROR",
            {
                "reason": "Path Traversal Blocked",
                "path": traversal_target,
            },
        )
        try:
            with open(harness.audit_log_path, "r", encoding="utf-8") as audit_file:
                last_event = json.loads(audit_file.readlines()[-1])
        except (OSError, IndexError, json.JSONDecodeError) as exc:
            print(f"[FAIL] Could not verify the harness error trace: {exc}")
            raise SystemExit(1)
        if last_event.get("event_type") != "HARNESS_ERROR":
            print("[FAIL] HARNESS_ERROR was not the final audit event.")
            raise SystemExit(1)
        print("[Pillar 5 - Trace] Logged 'HARNESS_ERROR' to JSONL audit file.")
        print(
            "[FAIL] HARNESS ERROR: Path Traversal Blocked: Target "
            f"'{traversal_target}' is outside workspace '{workspace}'"
        )

    print("\nMODULE 2 DEMO COMPLETE: All 5 Pillars Executed & Logged!")
