"""
Module 4: Guardrails and Deterministic Hooks
Enforces the 4-layer control architecture:
1. System Rules (Prompt guidelines)
2. Tool Schemas (Argument typing & JSON schema)
3. Pre/Post Interceptors & Claude Code Event Hooks
4. OS Sandboxing & Path Isolation
"""

import os
import re
import ast
import json
from datetime import datetime, timezone

class ClaudeCodeHookInterceptor:
    """Interceptors for Claude Code native event hooks (pre-tool-use, post-tool-use)."""
    def __init__(self):
        self.blocked_flags = ["--dangerously-skip-permissions", "-y", "--force-all"]

    def intercept_pre_tool_use(self, tool_name: str, tool_args: dict) -> tuple[bool, str]:
        command = tool_args.get("command", "")
        for flag in self.blocked_flags:
            if flag in command:
                return False, f"CLI Flag '{flag}' is strictly prohibited by Enterprise Security Policy!"
        return True, "Pre-tool-use check passed."

class GuardrailsEngine:
    def __init__(self, workspace_root: str):
        self.workspace_root = os.path.abspath(workspace_root)
        self.claude_interceptor = ClaudeCodeHookInterceptor()
        self.dangerous_patterns = [
            r"rm\s+-rf",
            r"sudo\s+",
            r"chmod\s+777",
            r"git\s+push\s+.*--force",
            r"mkfs",
            r"dd\s+if="
        ]

    def intercept_shell_command(self, command: str) -> tuple[bool, str]:
        for pattern in self.dangerous_patterns:
            if re.search(pattern, command, re.IGNORECASE):
                return False, f"CRITICAL SECURITY BLOCK: Command matches dangerous pattern '{pattern}'"
        return True, "Shell command permitted."

    def audit_ast_and_secrets(self, file_path: str, code_content: str) -> tuple[bool, list]:
        issues = []
        try:
            ast.parse(code_content)
        except SyntaxError as e:
            issues.append(f"AST Syntax Error on line {e.lineno}: {e.msg}")
            return False, issues

        secret_pattern = r"(sk-proj-[A-Za-z0-9_\-]{20,}|AKIA[0-9A-Z]{16})"
        if re.search(secret_pattern, code_content):
            issues.append("SECURITY CRITICAL: Hardcoded API secret key detected!")

        if issues:
            return False, issues
        return True, ["AST syntax valid. Zero secret leaks detected."]

    def enforce_path_sandbox(self, target_path: str) -> tuple[bool, str]:
        abs_target = os.path.abspath(target_path)
        if not abs_target.startswith(self.workspace_root):
            return False, f"SANDBOX VIOLATION: Target path '{target_path}' resides outside workspace '{self.workspace_root}'"
        return True, "Path sandbox check passed."

if __name__ == "__main__":
    engine = GuardrailsEngine(os.path.abspath("."))
    print("Guardrails Engine & Claude Code Native Interceptor loaded.")
    
    ok, msg = engine.claude_interceptor.intercept_pre_tool_use("Bash", {"command": "claude --dangerously-skip-permissions"})
    print("Pre-Tool-Use Test:", ok, "|", msg)
