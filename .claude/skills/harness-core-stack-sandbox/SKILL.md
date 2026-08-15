---
name: harness-core-stack-sandbox
description: Enforces least-privilege tool allowlists, path sandboxing via is_relative_to(), post-edit secret scanning, context token budgeting, and append-only event tracing. Use when sandboxing agent tool invocations, setting up file system isolation, or establishing audit trails in events.jsonl.
allowed-tools: Read, Write, Glob, Grep
---

# Core Harness Stack & Sandboxing (Module 2 Skill)

This skill implements the 5 foundational pillars of an enterprise coding agent harness: Persistent Memory (`CLAUDE.md`), Scoped Tool Allowlisting, Deterministic Hooks, Context Token Budgeting, and Observability Tracing.

## When to Use
- When sandboxing agent file access to prevent directory traversal (`../`) and unauthorized workspace escapes.
- When restricting tool execution to an explicit allowlist.
- When scanning generated source code for API key leaks (`sk-proj-`, `AKIA`) before writing to disk.
- When compacting large command/build outputs to prevent prompt context bloat.

## How to Use
1. **Tool Permission & Path Sandboxing**:
   ```python
   allowed_tools = ["read_file", "write_file", "run_test", "list_dir"]
   if tool_name not in allowed_tools:
       log_event("PERMISSION_DENIED", {"tool": tool_name})
       return False

   workspace = Path(workspace_root).resolve()
   abs_target = Path(target_path).resolve()
   if not abs_target.is_relative_to(workspace):
       log_event("PATH_TRAVERSAL_BLOCKED", {"path": str(abs_target)})
       return False
   ```

2. **Post-Edit Secret Leak Inspection**:
   ```python
   if "sk-proj-" in code_content or "AKIA" in code_content:
       log_event("SECURITY_VIOLATION", {"file": file_path, "issue": "Hardcoded secret key detected!"})
       return False
   ```

3. **Event Tracing**:
   Write all decisions with ISO UTC timestamps to `events.jsonl`.

4. **Verification**:
   ```bash
   python course_implementation/module_02_core_harness_stack/core_harness_stack.py
   ```

## Key Files & Implementation
- `course_implementation/module_02_core_harness_stack/core_harness_stack.py`
- `CLAUDE.md`, `AGENTS.md`
