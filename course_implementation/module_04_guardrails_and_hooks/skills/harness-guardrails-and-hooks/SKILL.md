---
name: harness-guardrails-and-hooks
description: Implements Claude Code PascalCase PreToolUse and PostToolUse deterministic hook interceptors to block dangerous CLI flags, parse AST syntax, and prevent multi-vendor credential leaks. Use when configuring .claude/settings.json hooks or auditing pre/post tool execution policies.
allowed-tools: Read, Write, Glob, Grep
---

# Deterministic Guardrails & Hook Interceptors (Module 4 Skill)

This skill implements enterprise defense-in-depth across the 4 control layers (System Prompt, Tool Schemas, Pre/Post Hooks, and OS Sandbox), conforming to Claude Code's PascalCase hook event standards.

## When to Use
- When configuring `.claude/settings.json` with PreToolUse and PostToolUse hook handlers.
- When blocking CLI flags that attempt to bypass user permissions (`--dangerously-skip-permissions`, `-y`, `--force-all`).
- When returning structured JSON permission decisions (`allow`, `deny`, `ask`, `defer`).
- When auditing code for hardcoded vendor secrets (OpenAI `sk-proj-`, Anthropic `sk-ant-`, AWS `AKIA`).

## How to Use
1. **PreToolUse Shell Interception**:
   ```python
   def intercept_pre_tool_use(tool_name: str, tool_input: dict) -> dict:
       command = tool_input.get("command", "")
       if tool_name == "Bash":
           for flag in ["--dangerously-skip-permissions", "-y", "--force-all"]:
               if flag in command:
                   return {"hookSpecificOutput": {
                       "hookEventName": "PreToolUse",
                       "permissionDecision": "deny",
                       "permissionDecisionReason": f"Prohibited CLI flag '{flag}'."
                   }}
       return {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "allow"}}
   ```

2. **Post-Tool Static & AST Audit**:
   ```python
   ast.parse(code_content, filename=file_path)
   if re.search(r"(sk-proj-[A-Za-z0-9_\-]{20,}|AKIA[0-9A-Z]{16})", code_content):
       raise ValueError("SECURITY CRITICAL: Hardcoded API secret key detected!")
   ```

3. **Verification**:
   ```bash
   python course_implementation/module_04_guardrails_and_hooks/guardrails_engine.py
   ```

## Key Files & Implementation (GitHub Links)
- [https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_04_guardrails_and_hooks/guardrails_engine.py](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_04_guardrails_and_hooks/guardrails_engine.py)
- [https://github.com/kenhuangus/packt-harness/blob/main/.claude/settings.json](https://github.com/kenhuangus/packt-harness/blob/main/.claude/settings.json)
- [https://github.com/kenhuangus/packt-harness/blob/main/.claude/skills/harness-guardrails-and-hooks/SKILL.md](https://github.com/kenhuangus/packt-harness/blob/main/.claude/skills/harness-guardrails-and-hooks/SKILL.md)
