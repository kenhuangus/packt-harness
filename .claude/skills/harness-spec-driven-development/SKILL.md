---
name: harness-spec-driven-development
description: Enforces immutable SPEC.md contracts by bounding agent edits strictly
  to allowed_files, rejecting out-of-scope non-goals, and verifying AST syntax before
  accepting code modifications. Trigger when scoping feature tasks, preventing architectural
  drift, or validating code against specifications.
version: 1.0.0
author: Harness Engineering Team
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Harness Spec-Driven Development

## Overview
Converts Markdown specification contracts (SPEC.md) into machine-enforceable write boundaries that eliminate architectural drift and invalid AST syntax.

## Structure & Progressive Disclosure
- `scripts/`: Executable helper and verification tools.
- `references/`: Detailed specifications, guides, and architectural rules.
- `assets/`: Configuration templates and machine-readable schemas.

## When to Use
- When authoring or verifying feature specifications (`SPEC.md`).
- When bounding agent writes strictly to `allowed_files` and protecting `forbidden_files`.
- When pre-validating code syntax with Python `ast.parse()` before applying disk edits.

## Required Inputs
- Specification file path (`SPEC.md`).
- Target file path to edit.
- Proposed code implementation string.

## Instructions
1. Parse `SPEC.md` using the schema in `assets/spec_schema.json` (Goal, Allowed Files, Forbidden Files, Non-Goals).
2. Run `python scripts/verify_spec_scope.py` to assert the target file is permitted.
3. Execute `ast.parse(code_content)` to catch syntax errors before writing to disk.
4. Reject edits modifying forbidden files or implementing explicitly declared non-goals.
5. Consult `references/sdd-contract-guide.md` for specification best practices.

## Output Format
Always format output adhering to this structure:
```json
{
  "valid": true,
  "target_file": "src/calculator.py",
  "ast_syntax_valid": true,
  "scope_verdict": "ALLOWED",
  "violations": []
}
```

## Examples
### Verifying Edit Scope & AST Syntax
```python
import ast

code = "def add(a: int, b: int) -> int:\n    return a + b"
tree = ast.parse(code)
print("AST parsed successfully!")
```

## Key Implementation Links (GitHub)
- [https://github.com/kenhuangus/packt-harness/tree/main/.claude/skills/harness-spec-driven-development/](https://github.com/kenhuangus/packt-harness/tree/main/.claude/skills/harness-spec-driven-development/)
- [https://github.com/kenhuangus/packt-harness/blob/main/.claude/skills/harness-spec-driven-development/SKILL.md](https://github.com/kenhuangus/packt-harness/blob/main/.claude/skills/harness-spec-driven-development/SKILL.md)
- [https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_03_spec_driven_development/](https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_03_spec_driven_development/)
