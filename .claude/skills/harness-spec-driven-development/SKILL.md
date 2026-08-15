---
name: harness-spec-driven-development
description: Parses and enforces immutable SPEC.md contracts, bounding agent writes strictly to allowed files, blocking non-goals, and validating AST syntax before accepting code changes. Use when scoping features, preventing architectural drift, or validating code proposals against specifications.
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Spec-Driven Development (SDD) Enforcer (Module 3 Skill)

This skill replaces open-ended natural language prompt drift with deterministic `SPEC.md` contract verification, ensuring agent code modifications stay bounded to authorized files and explicit goals.

## When to Use
- Before generating code for any feature or refactoring task.
- When validating that an agent edit only touches files listed under `Allowed Files` and avoids `Forbidden Files`.
- When filtering diff proposals against `Non-Goals` (e.g. rejecting database connections in stateless units).
- When verifying that generated Python code passes AST syntax parsing before saving.

## How to Use
1. **Define the Specification Contract (`SPEC.md`)**:
   Include `Allowed Files`, `Forbidden Files`, `Non-Goals`, and `Acceptance Criteria`.

2. **Scope Verification & Non-Goal Filtering**:
   ```python
   relative = _normalized(target_file)
   if relative not in allowed_files or relative in forbidden_files:
       raise PermissionError(f"SCOPE VIOLATION: '{relative}' outside allowed scope {allowed_files}.")

   lowered = code.lower()
   for non_goal in non_goals:
       if non_goal.lower() in lowered:
           raise PermissionError(f"NON-GOAL VIOLATION: code contains non-goal '{non_goal}'.")

   ast.parse(code, filename=target_file)
   dest.write_text(code, encoding="utf-8")
   ```

3. **Verification**:
   ```bash
   python course_implementation/module_03_spec_driven_development/spec_driven_verifier.py
   ```

## Key Files & Implementation
- `course_implementation/module_03_spec_driven_development/spec_driven_verifier.py`
- `course_implementation/module_03_spec_driven_development/SPEC.md`
