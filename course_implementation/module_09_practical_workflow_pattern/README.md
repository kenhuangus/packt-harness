# Module 9: Practical Workflow Pattern (5-Step SOP)

## Overview
This module demonstrates the 5-Step Standard Operating Procedure (SOP) for reliable AI agent software execution.

## The 5-Step Pipeline
1. **Step 1: Spec First** - Draft & validate `SPEC.md` requirements.
2. **Step 2: Constrained Execution** - Run agent inside sandboxed workspace with scoped permissions.
3. **Step 3: Deterministic Checks** - Run `PreToolUse`/`PostToolUse` hooks, AST static analysis, and linters.
4. **Step 4: Test Verification** - Execute automated unit & integration test suites.
5. **Step 5: Human Review** - Perform developer sanity check & merge clean PR diff.
