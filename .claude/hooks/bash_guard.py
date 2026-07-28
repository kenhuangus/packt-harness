#!/usr/bin/env python3
"""Claude Code PreToolUse guard for dangerous Bash commands."""

import json
import re
import sys


DANGEROUS_PATTERNS = [
    (r"\brm\s+-rf\b", "recursive forced deletion"),
    (r"\bsudo(?:\s|$)", "privilege escalation"),
    (r"\bchmod\s+777\b", "world-writable permissions"),
    (r"\bgit\s+push\b[^\n]*(?:--force(?:-with-lease)?|-f)\b", "forced Git push"),
    (r"\bmkfs(?:\.[A-Za-z0-9_-]+)?\b", "filesystem formatting"),
    (r"\bdd\s+[^\n]*\bif=", "raw device copy"),
]


def permission_output(decision: str, reason: str) -> dict:
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": decision,
            "permissionDecisionReason": reason,
        }
    }


def evaluate(payload: dict) -> dict:
    if payload.get("hook_event_name") != "PreToolUse":
        raise ValueError("bash_guard.py only accepts PreToolUse input.")

    tool_name = payload.get("tool_name")
    if tool_name != "Bash":
        return permission_output(
            "defer", f"No Bash-specific decision applies to tool '{tool_name}'."
        )

    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict):
        raise ValueError("PreToolUse Bash input requires object tool_input.")
    command = tool_input.get("command")
    if not isinstance(command, str):
        raise ValueError("tool_input.command must be a string.")

    for pattern, description in DANGEROUS_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            return permission_output(
                "deny",
                f"Blocked dangerous Bash command: {description} "
                f"(matched {pattern!r}).",
            )

    return permission_output(
        "defer",
        "No dangerous command pattern matched; normal permissions still apply.",
    )


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        if not isinstance(payload, dict):
            raise ValueError("Hook input must be a JSON object.")
        output = evaluate(payload)
    except (json.JSONDecodeError, TypeError, ValueError) as exc:
        print(f"Bash guard input error: {exc}", file=sys.stderr)
        return 2

    json.dump(output, sys.stdout, separators=(",", ":"))
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
