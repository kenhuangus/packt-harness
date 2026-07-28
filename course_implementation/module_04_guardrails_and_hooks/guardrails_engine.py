"""
Module 4: Guardrails and Deterministic Hooks

Enforces the 4-layer control architecture:
1. System rules (prompt guidelines)
2. Tool schemas (argument typing and JSON Schema)
3. PreToolUse/PostToolUse hooks
4. OS sandboxing and path isolation
"""

import ast
import json
from pathlib import Path
import re
import sys
from typing import TextIO


class ClaudeCodeHookInterceptor:
    """Model the documented Claude Code command-hook input/output contract."""

    PRE_TOOL_USE = "PreToolUse"
    POST_TOOL_USE = "PostToolUse"
    PERMISSION_DECISIONS = {"allow", "deny", "ask", "defer"}

    def __init__(self) -> None:
        self.blocked_flags = [
            "--dangerously-skip-permissions",
            "-y",
            "--force-all",
        ]

    def intercept_pre_tool_use(
        self, tool_name: str, tool_input: dict
    ) -> tuple[bool, str]:
        """Evaluate a PreToolUse payload before a tool executes."""
        command = tool_input.get("command", "")
        if tool_name != "Bash":
            return True, f"No Bash policy applies to tool '{tool_name}'."
        for flag in self.blocked_flags:
            if flag in command:
                return (
                    False,
                    f"CLI flag '{flag}' is prohibited by enterprise policy.",
                )
        return True, "PreToolUse check passed."

    @classmethod
    def permission_output(
        cls,
        decision: str,
        reason: str,
        updated_input: dict | None = None,
    ) -> dict:
        """Build the structured exit-0 output for a PreToolUse decision."""
        if decision not in cls.PERMISSION_DECISIONS:
            raise ValueError(
                "permissionDecision must be allow, deny, ask, or defer."
            )
        specific_output = {
            "hookEventName": cls.PRE_TOOL_USE,
            "permissionDecision": decision,
            "permissionDecisionReason": reason,
        }
        if updated_input is not None:
            specific_output["updatedInput"] = updated_input
        return {"hookSpecificOutput": specific_output}

    def process_hook_payload(self, payload: dict) -> dict:
        """Process JSON received on stdin and return structured stdout JSON."""
        event_name = payload.get("hook_event_name")
        if event_name not in {self.PRE_TOOL_USE, self.POST_TOOL_USE}:
            raise ValueError(
                "hook_event_name must be PreToolUse or PostToolUse."
            )

        if event_name == self.POST_TOOL_USE:
            return {
                "continue": True,
                "systemMessage": "PostToolUse observation completed.",
            }

        tool_input = payload.get("tool_input")
        if not isinstance(tool_input, dict):
            raise ValueError("PreToolUse payload requires object tool_input.")
        allowed, reason = self.intercept_pre_tool_use(
            payload.get("tool_name", ""), tool_input
        )
        decision = "allow" if allowed else "deny"
        return self.permission_output(decision, reason)

    def run_stdio(
        self,
        stdin: TextIO = sys.stdin,
        stdout: TextIO = sys.stdout,
        stderr: TextIO = sys.stderr,
    ) -> int:
        """
        Read hook JSON from stdin.

        Exit 0 writes structured JSON. Exit 2 blocks the tool and writes the
        blocking error to stderr; stdout is ignored by Claude Code in that case.
        """
        try:
            payload = json.load(stdin)
            if not isinstance(payload, dict):
                raise ValueError("Hook input must be a JSON object.")
            output = self.process_hook_payload(payload)
        except (json.JSONDecodeError, TypeError, ValueError) as exc:
            print(f"Hook input error: {exc}", file=stderr)
            return 2

        json.dump(output, stdout)
        stdout.write("\n")
        return 0


class GuardrailsEngine:
    def __init__(self, workspace_root: str | Path) -> None:
        self.workspace_root = Path(workspace_root).resolve()
        self.claude_interceptor = ClaudeCodeHookInterceptor()
        self.dangerous_patterns = [
            r"rm\s+-rf",
            r"sudo\s+",
            r"chmod\s+777",
            r"git\s+push\s+.*--force",
            r"mkfs",
            r"dd\s+if=",
        ]

    def intercept_shell_command(self, command: str) -> tuple[bool, str]:
        for pattern in self.dangerous_patterns:
            if re.search(pattern, command, re.IGNORECASE):
                return (
                    False,
                    "CRITICAL SECURITY BLOCK: "
                    f"Command matches dangerous pattern '{pattern}'",
                )
        return True, "Shell command permitted."

    def audit_ast_and_secrets(
        self, file_path: str, code_content: str
    ) -> tuple[bool, list[str]]:
        issues = []
        try:
            ast.parse(code_content, filename=file_path)
        except SyntaxError as exc:
            issues.append(
                f"AST Syntax Error on line {exc.lineno}: {exc.msg}"
            )
            return False, issues

        secret_pattern = r"(sk-proj-[A-Za-z0-9_\-]{20,}|AKIA[0-9A-Z]{16})"
        if re.search(secret_pattern, code_content):
            issues.append(
                "SECURITY CRITICAL: Hardcoded API secret key detected!"
            )

        if issues:
            return False, issues
        return True, ["AST syntax valid. Zero secret leaks detected."]

    def enforce_path_sandbox(self, target_path: str | Path) -> tuple[bool, str]:
        target = Path(target_path)
        if not target.is_absolute():
            target = self.workspace_root / target
        resolved_target = target.resolve()
        if not resolved_target.is_relative_to(self.workspace_root):
            return (
                False,
                "SANDBOX VIOLATION: "
                f"Target path '{resolved_target}' resides outside workspace "
                f"'{self.workspace_root}'",
            )
        return True, f"Path sandbox check passed for '{resolved_target}'."


def print_check(label: str, passed: bool, detail: str) -> bool:
    status = "PASS" if passed else "FAIL"
    print(f"  [{status}] {label}: {detail}")
    return passed


def main() -> int:
    print("=" * 60)
    print("MODULE 4 DEMO: PRODUCTION GUARDRAILS & CLAUDE CODE HOOKS")
    print("=" * 60)

    workspace = Path(__file__).resolve().parent
    engine = GuardrailsEngine(workspace)
    checks = []

    print("\n[Claude Code Hook Contract]")
    safe, reason = engine.claude_interceptor.intercept_pre_tool_use(
        "Bash", {"command": "pytest tests/unit"}
    )
    checks.append(print_check("Safe PreToolUse command allowed", safe, reason))

    allowed, reason = engine.claude_interceptor.intercept_pre_tool_use(
        "Bash", {"command": "claude --dangerously-skip-permissions"}
    )
    checks.append(
        print_check(
            "Dangerous PreToolUse command denied",
            not allowed,
            reason,
        )
    )
    deny_output = engine.claude_interceptor.permission_output("deny", reason)
    print(f"  [PASS] Structured deny JSON: {json.dumps(deny_output)}")

    print("\n[Shell Command Guardrail]")
    allowed, reason = engine.intercept_shell_command("pytest tests/unit/")
    checks.append(print_check("Safe shell command allowed", allowed, reason))
    allowed, reason = engine.intercept_shell_command("sudo rm -rf /var/config")
    checks.append(
        print_check("Dangerous shell command blocked", not allowed, reason)
    )

    print("\n[AST and Secret Scan]")
    clean, messages = engine.audit_ast_and_secrets(
        "processor.py", "def process(value):\n    return value * 2\n"
    )
    checks.append(
        print_check("Valid code accepted", clean, "; ".join(messages))
    )
    clean, messages = engine.audit_ast_and_secrets(
        "config.py",
        'API_KEY = "sk-proj-abcdefghijklmnopqrstuvwxyz123456"\n',
    )
    checks.append(
        print_check("Hardcoded secret rejected", not clean, "; ".join(messages))
    )
    clean, messages = engine.audit_ast_and_secrets(
        "broken.py", "def broken(:\n    pass\n"
    )
    checks.append(
        print_check("Invalid syntax rejected", not clean, "; ".join(messages))
    )

    print("\n[Resolved Path Sandbox]")
    allowed, reason = engine.enforce_path_sandbox("examples/output.py")
    checks.append(print_check("Inside path allowed", allowed, reason))
    outside_path = workspace.parent / f"{workspace.name}-outside" / "escape.py"
    allowed, reason = engine.enforce_path_sandbox(outside_path)
    checks.append(
        print_check("Sibling-prefix path rejected", not allowed, reason)
    )

    print("\n" + "=" * 60)
    if all(checks):
        print("MODULE 4 DEMO COMPLETE: ALL EXPECTED CONTROLS VERIFIED!")
        print("=" * 60)
        return 0
    print("MODULE 4 DEMO FAILED: ONE OR MORE CONTROLS MISBEHAVED.")
    print("=" * 60)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
