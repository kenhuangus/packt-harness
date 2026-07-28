# Module 2: Core Harness Stack & System Architecture

## Overview
This module implements the 5 fundamental pillars of a production AI coding harness.

## The 5 Pillars
1. **Instructions & Repo Conventions**: `CLAUDE.md` and `AGENTS.md` persistent memory standards.
2. **Scoped Tools & Permissions**: Least-privilege tool access with path sandboxing.
3. **Hooks & Policy Engine**: Pre-action security checks & post-action AST linting.
4. **Automated Testing Loop**: Automatic test suite execution feeding tracebacks back to the LLM.
5. **Observability & Event Tracing**: Structured JSONL audit logging of all tool calls and diffs.

## Memory Standards (`CLAUDE.md` vs `AGENTS.md`)
- `CLAUDE.md`: Anthropic Claude Code session brief with cascading subdirectory resolution.
- `AGENTS.md`: Universal open standard supported across Cursor, Copilot, and Aider.
- **Symlink Pattern**: `ln -s AGENTS.md CLAUDE.md` ensures cross-tool compatibility without duplication.
