# Module 10: Closing Principles & Production Readiness Audit

## Overview
This module provides an automated Production Readiness Audit Suite verifying that a project satisfies all 5 core criteria of Harness Engineering.

## The 4 Core Principles
1. **Predictability Over Randomness**: Standardize environment & memory files (`CLAUDE.md` / `AGENTS.md`).
2. **Reduce Ambiguity**: Use executable specs (`SPEC.md`) instead of natural language prompts.
3. **Automate Checks**: Replace human vigilance with deterministic hooks, AST parsers, & tests.
4. **Optimize for Trust**: Prioritize auditability, safety, and correctness over raw speed.

## The 5 Audit Criteria
- [ ] 1. Memory files present (`CLAUDE.md` / `AGENTS.md`).
- [ ] 2. `PreToolUse` hooks active for dangerous commands.
- [ ] 3. Automated test runner integrated into agent loop.
- [ ] 4. MCP tool permissions scoped appropriately.
- [ ] 5. Multi-agent role division configured for complex tasks.
