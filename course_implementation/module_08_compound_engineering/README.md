# Module 8: Compound Engineering & Multi-Agent Teams

## Overview
This module implements multi-agent role specialization, git worktree isolation, and recursive self-improvement loops.

## Architecture & Subagent Roles
1. **Planner Agent** (Architect): Read-only context access; analyzes requirements & generates task plans.
2. **Implementer Agent** (Coder): Executes file edits within strict workspace boundaries or git worktrees (`git worktree add`).
3. **Reviewer Agent** (Auditor): Independent subagent running static analysis, AST linters, and spec checks.
4. **Recursive Self-Improvement Loop**: Telemetry logging (`telemetry.jsonl`) feeding continuous rule updates to `CLAUDE.md`.
