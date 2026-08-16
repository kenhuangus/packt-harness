"""
Module 4 Integration: Guardrails & Deterministic Hooks for Deep Research Agent.
Implements Claude Code PascalCase PreToolUse contracts, AST syntax validation,
and regex high-entropy API secret scanning.
"""

from __future__ import annotations

import ast
import re
from typing import Any


class GuardrailsEngine:
    """Enforces deterministic hooks and code/content safety guardrails."""

    def __init__(self):
        self.secret_patterns = [
            ("Anthropic API Key", re.compile(r"sk-ant-[a-zA-Z0-9_-]{20,}")),
            ("OpenAI API Key", re.compile(r"sk-[a-zA-Z0-9]{32,}")),
            ("AWS Secret Key", re.compile(r"(?i)aws_secret_access_key\s*=\s*[a-zA-Z0-9/+=]{40}")),
            ("Generic Secret", re.compile(r"(?i)(api_key|secret_token|password)\s*[:=]\s*['\"][a-zA-Z0-9_-]{16,}['\"]")),
        ]
        self.dangerous_command_patterns = [
            ("Dangerous Flag", re.compile(r"--dangerously-skip-permissions")),
            ("Force Push", re.compile(r"git\s+push\s+.*--force")),
            ("Recursive Delete", re.compile(r"rm\s+-rf\s+[/~]")),
            ("Root Escalation", re.compile(r"\bsudo\b")),
        ]

    def intercept_pre_tool_use(self, hook_input: dict[str, Any]) -> dict[str, Any]:
        """Implements Claude Code PascalCase PreToolUse JSON-RPC contract."""
        tool_name = hook_input.get("toolName", "")
        tool_input = hook_input.get("toolInput", {})

        command = tool_input.get("command", "")
        for desc, pattern in self.dangerous_command_patterns:
            if pattern.search(command):
                return {
                    "hookName": "PreToolUse",
                    "status": "DENIED",
                    "hookSpecificOutput": {
                        "permissionDecision": "deny",
                        "reason": f"Security Guardrail Block: Detected {desc} in command '{command}'",
                    },
                }

        return {
            "hookName": "PreToolUse",
            "status": "ALLOWED",
            "hookSpecificOutput": {
                "permissionDecision": "allow",
                "reason": "Tool call parameters verified by deterministic guardrails.",
            },
        }

    def scan_content_for_secrets(self, text: str) -> list[str]:
        """Scans research output or generated code for leaked API keys."""
        findings = []
        for name, pattern in self.secret_patterns:
            if pattern.search(text):
                findings.append(f"Secret Leak Guardrail: Detected {name} in content.")
        return findings

    def validate_python_ast(self, code_str: str) -> tuple[bool, str]:
        """Parses code with ast.parse to confirm syntax validity."""
        try:
            ast.parse(code_str)
            return True, "AST syntax check passed."
        except SyntaxError as e:
            return False, f"AST SyntaxError on line {e.lineno}: {e.msg}"
