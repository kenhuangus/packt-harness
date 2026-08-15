---
name: harness-interception-loop-detector
description: Intercepts destructive shell commands (rm -rf, sudo, chmod 777) and detects
  repeating retry execution loops to prevent token waste and data loss. Trigger when
  running automated agent loops, auditing shell commands, or debugging stuck test-fix
  iterations.
version: 1.0.0
author: Harness Engineering Team
allowed-tools: Bash, Read, Grep
---

# Harness Interception & Loop Detector

## Overview
Provides deterministic pre-execution command auditing and sliding-window loop detection for agent shell tools, ensuring safe and bounded execution.

## Structure & Progressive Disclosure
- `scripts/`: Executable helper and verification tools.
- `references/`: Detailed specifications, guides, and architectural rules.
- `assets/`: Configuration templates and machine-readable schemas.

## When to Use
- When the user asks to "audit agent commands", "prevent destructive bash executions", or "detect infinite retry loops".
- When running autonomous agent test-and-repair loops that risk entering repetitive failure cycles.
- When validating shell commands against prohibited command patterns.

## Required Inputs
- Target shell command string to evaluate.
- Sliding window history buffer of recently executed commands.
- Maximum allowed identical retry threshold (default: 2).

## Instructions
1. Execute `python scripts/intercept_command.py --command "<cmd>"` or inspect `assets/forbidden_patterns.json`.
2. Scan the command string against prohibited regex patterns (`rm -rf`, `sudo`, `chmod 777`, `drop database`).
3. Check command history: if the exact same command failed $\ge 2$ consecutive times without code changes, trigger the loop circuit breaker.
4. If unsafe or looped, block execution immediately and provide actionable remediation guidance prompting the agent to change strategy.
5. Consult `references/destructive-command-patterns.md` and `references/loop-detection-guide.md` for policy standards.

## Output Format
Always format output adhering to this structure:
```json
{
  "verdict": "ALLOW | BLOCK",
  "risk_level": "LOW | MEDIUM | HIGH | CRITICAL",
  "reason": "Clear explanation of block reason or validation confirmation",
  "loop_detected": false
}
```

## Examples
### Intercepting a Dangerous Shell Command
```python
from scripts.intercept_command import check_command

verdict, reason = check_command("rm -rf /tmp/data")
print(f"Verdict: {verdict}, Reason: {reason}")
# Output: Verdict: False, Reason: BLOCKED: Destructive pattern '\brm\s+-[rR][fF]\b' detected.
```

## Key Implementation Links (GitHub)
- [https://github.com/kenhuangus/packt-harness/tree/main/.claude/skills/harness-interception-loop-detector/](https://github.com/kenhuangus/packt-harness/tree/main/.claude/skills/harness-interception-loop-detector/)
- [https://github.com/kenhuangus/packt-harness/blob/main/.claude/skills/harness-interception-loop-detector/SKILL.md](https://github.com/kenhuangus/packt-harness/blob/main/.claude/skills/harness-interception-loop-detector/SKILL.md)
- [https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_01_why_harness_engineering/](https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_01_why_harness_engineering/)
