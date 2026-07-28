# Module 4: Guardrails & Deterministic Hooks

## Overview

This module implements a four-layer defense-in-depth architecture for coding
agents:

1. Prompt system rules
2. Typed tool argument schemas
3. Deterministic `PreToolUse` and `PostToolUse` hooks
4. Resolved-path sandboxing

## Claude Code Hook Contract

Claude Code sends a JSON object to command hooks on stdin. Tool events include
`hook_event_name`, `tool_name`, and `tool_input`. Hook event names are
case-sensitive PascalCase; the events used here are `PreToolUse` and
`PostToolUse`.

For `PreToolUse`, an exit-code-0 hook can return a structured decision:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "permissionDecisionReason": "Policy check passed."
  }
}
```

The valid permission decisions are `allow`, `deny`, `ask`, and `defer`. Exit
code 2 is the blocking-error path: Claude Code receives stderr and ignores
stdout. Other nonzero exit codes are non-blocking errors.

## Runnable Bash Guard

The repository-level `.claude/settings.json` registers
`.claude/hooks/bash_guard.py` for `PreToolUse` events whose tool name matches
`Bash`. It uses `${CLAUDE_PROJECT_DIR}` so the path is stable regardless of the
current working directory.

You can exercise the hook directly in PowerShell:

```powershell
'{"hook_event_name":"PreToolUse","tool_name":"Bash","tool_input":{"command":"pytest"}}' |
  python .claude/hooks/bash_guard.py

'{"hook_event_name":"PreToolUse","tool_name":"Bash","tool_input":{"command":"rm -rf /"}}' |
  python .claude/hooks/bash_guard.py
```

The first input returns `defer`, leaving normal Claude Code permissions in
force. The second returns a structured `deny`.

## Path and Content Guardrails

`guardrails_engine.py` retains the teaching layers for dangerous-command
matching, Python AST parsing, and common secret formats. Its path sandbox uses
`Path.resolve()` followed by `Path.is_relative_to()`. That rejects `..`
traversal and sibling paths with a shared string prefix on both Windows and
POSIX.

Run the complete demonstration from the repository root:

```powershell
python course_implementation/module_04_guardrails_and_hooks/guardrails_engine.py
```
