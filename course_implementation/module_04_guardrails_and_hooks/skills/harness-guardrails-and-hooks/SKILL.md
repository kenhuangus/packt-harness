---
name: harness-guardrails-and-hooks
description: Implements Claude Code PascalCase PreToolUse and PostToolUse hook interceptors
  in .claude/settings.json to block dangerous CLI flags, parse AST syntax, and prevent
  multi-vendor credential leaks. Trigger when configuring Claude Code hooks, securing
  shell executions, or auditing pre/post tool policies.
version: 1.0.0
author: Harness Engineering Team
allowed-tools: Read, Write, Glob, Grep
---

# Harness Guardrails & Hooks

## Overview
Provides deterministic PreToolUse and PostToolUse hook handlers configured inside `.claude/settings.json` to enforce execution safety and prevent credential leaks.

## Structure & Progressive Disclosure
- `scripts/`: Executable helper and verification tools.
- `references/`: Detailed specifications, guides, and architectural rules.
- `assets/`: Configuration templates and machine-readable schemas.

## When to Use
- When configuring Claude Code hooks in `.claude/settings.json`.
- When intercepting shell tool calls before execution to block hazardous flags (`--dangerously-skip-permissions`, `-y`).
- When inspecting tool outputs post-execution to redact secrets or validate AST syntax.

## Required Inputs
- Claude Code hook JSON payload delivered via stdin.
- Tool name (`Bash`, `Write`, `Edit`) and argument dictionary.

## Instructions
1. Register hook commands in `.claude/settings.json` following `assets/settings-hooks-template.json`.
2. In PreToolUse (`scripts/hook_pre_tool_use.py`), inspect incoming tool arguments for dangerous flags.
3. Return JSON response containing `hookSpecificOutput` with `permissionDecision: allow | deny | ask`.
4. In PostToolUse, verify modified files for valid AST syntax and absence of credential leaks.
5. Consult `references/claude-code-hooks-spec.md` for hook lifecycle specifications.

## Output Format
Always format output adhering to this structure:
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Prohibited CLI flag '--dangerously-skip-permissions' detected."
  }
}
```

## Examples
### PascalCase Hook JSON Response
```python
import json

response = {
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "allow"
    }
}
print(json.dumps(response))
```

## Key Implementation Links (GitHub)
- [https://github.com/kenhuangus/packt-harness/tree/main/.claude/skills/harness-guardrails-and-hooks/](https://github.com/kenhuangus/packt-harness/tree/main/.claude/skills/harness-guardrails-and-hooks/)
- [https://github.com/kenhuangus/packt-harness/blob/main/.claude/skills/harness-guardrails-and-hooks/SKILL.md](https://github.com/kenhuangus/packt-harness/blob/main/.claude/skills/harness-guardrails-and-hooks/SKILL.md)
- [https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_04_guardrails_and_hooks/](https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_04_guardrails_and_hooks/)
