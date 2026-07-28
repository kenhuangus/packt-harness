# Repository Guidelines for AI Coding Agents

## Architecture Overview
- Core Harness Engine: `core_harness_stack.py`
- Test Runner: `pytest`
- Memory File: `AGENTS.md` (Symlinked to `CLAUDE.md`)

## Code Style & Rules
- Language: Python 3.10+
- Type Hints: Required on all public functions.
- Error Handling: Explicit exceptions; never swallow errors.

## Build & Test Commands
- Run Unit Tests: `pytest tests/`
- Run Static Analysis: `python core_harness_stack.py`
