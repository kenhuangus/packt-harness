---
name: harness-core-stack-sandbox
description: 'Enforces the 5 core harness pillars: CLAUDE.md/AGENTS.md memory, least-privilege
  tool allowlists, Path.is_relative_to() sandboxing, post-edit secret scanning, token
  budgeting, and append-only event tracing. Trigger when sandboxing agent tools, enforcing
  workspace boundaries, or establishing events.jsonl audit trails.'
version: 1.0.0
author: Harness Engineering Team
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Harness Core Stack & Sandbox

## Overview
Implements the 5 core architectural harness pillars (Memory, Sandboxing, Hooks, Budgeting, Tracing) to wrap LLM tool calls in strict deterministic safety guarantees.

## Structure & Progressive Disclosure
- `scripts/`: Executable helper and verification tools.
- `references/`: Detailed specifications, guides, and architectural rules.
- `assets/`: Configuration templates and machine-readable schemas.

## When to Use
- When configuring workspace memory guidelines (`CLAUDE.md`, `AGENTS.md`).
- When restricting file write operations strictly within workspace boundaries via `Path.resolve().is_relative_to()`.
- When scanning code edits for hardcoded API keys and secrets before saving.
- When recording immutable audit events in `events.jsonl`.

## Required Inputs
- Workspace root directory path.
- Target file path and proposed edit contents.
- Tool invocation name and arguments.

## Instructions
Run all commands from the repository root.
1. Verify memory files (`CLAUDE.md`, `AGENTS.md`) exist at workspace root.
2. Validate tool requests against `assets/allowed_tools.json`; reject any unlisted tools.
3. Run `python .claude/skills/harness-core-stack-sandbox/scripts/validate_sandbox.py --workspace "." --path "<target>"` to ensure path containment.
4. Scan file contents against secret patterns in `references/secret-patterns.md` (OpenAI, AWS, GitHub tokens).
5. Append an ISO UTC timestamped record to `events.jsonl` matching `assets/event_schema.json`.

## Output Format
Always format output adhering to this structure:
```json
{
  "status": "APPROVED | REJECTED",
  "pillar_checks": {
    "memory_present": true,
    "path_sandboxed": true,
    "secret_scan_clean": true,
    "budget_ok": true
  },
  "event_id": "evt_20260815_001"
}
```

## Examples
### Validating Path Containment
```python
from pathlib import Path

workspace = Path("/app/project").resolve()
target = Path("/app/project/src/index.py").resolve()

assert target.is_relative_to(workspace), "Path containment violation!"
```

## Key Implementation Links (GitHub)
- [https://github.com/kenhuangus/packt-harness/tree/main/.claude/skills/harness-core-stack-sandbox/](https://github.com/kenhuangus/packt-harness/tree/main/.claude/skills/harness-core-stack-sandbox/)
- [https://github.com/kenhuangus/packt-harness/blob/main/.claude/skills/harness-core-stack-sandbox/SKILL.md](https://github.com/kenhuangus/packt-harness/blob/main/.claude/skills/harness-core-stack-sandbox/SKILL.md)
- [https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_02_core_harness_stack/](https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_02_core_harness_stack/)
