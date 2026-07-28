# Module 2: Core Harness Stack & System Architecture

## Overview
This module implements the 5 fundamental pillars of a production AI coding harness.

## The 5 Pillars
1. **Instructions & Repo Conventions**: `CLAUDE.md` and `AGENTS.md` persistent memory standards.
2. **Scoped Tools & Permissions**: Least-privilege tool access with path sandboxing.
3. **Hooks & Policy Engine**: `PreToolUse` security checks and `PostToolUse` AST linting.
4. **Automated Testing Loop**: Automatic test suite execution feeding tracebacks back to the LLM.
5. **Observability & Event Tracing**: Structured JSONL audit logging of all tool calls and diffs.

## Memory Standards (`CLAUDE.md` vs `AGENTS.md`)
- `CLAUDE.md`: Claude Code repository instructions; subdirectory files can add more specific guidance.
- `AGENTS.md`: Repository instructions for tools that support the `AGENTS.md` convention.
- **Symlink Pattern**: `ln -s AGENTS.md CLAUDE.md` exposes the same instructions under both filenames without duplication.
