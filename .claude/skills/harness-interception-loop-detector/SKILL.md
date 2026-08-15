---
name: harness-interception-loop-detector
description: Intercepts destructive shell commands and breaks repeating execution retry loops before token waste or data loss occurs. Use when running untrusted or automated agent command loops, auditing shell tool calls, or debugging stuck test-fix iterations.
allowed-tools: Bash, Read, Grep
---

# Harness Interception & Loop Detector (Module 1 Skill)

This skill provides deterministic protection against common LLM execution failure modes: destructive shell execution (e.g. `rm -rf`, `sudo`, `chmod 777`) and zero-progress retry loops.

## When to Use
- When evaluating or running proposed agent shell commands in automated environments.
- When an agent is repeatedly executing failing commands or tests without recovering.
- When establishing a circuit breaker to prevent token depletion and filesystem corruption.

## How to Use
1. **Pre-Execution Regex Interception**:
   Inspect proposed command strings against forbidden patterns before subprocess spawn:
   ```python
   FORBIDDEN_PATTERNS = [
       r"\brm\s+-[rR][fF]\b",
       r"\bsudo\b",
       r"\bchmod\s+777\b",
       r"\bdrop\s+database\b",
   ]
   for pattern in FORBIDDEN_PATTERNS:
       if re.search(pattern, command):
           raise PermissionError(f"BLOCKED BY PRE-HOOK: Dangerous command '{pattern}' detected.")
   ```

2. **Sliding-Window Loop Detection**:
   Maintain a sliding history of the last $N$ commands. If the last $N$ commands are identical, halt execution:
   ```python
   command_history.append(command)
   if len(command_history) >= max_retries:
       recent = command_history[-max_retries:]
       if len(set(recent)) == 1:
           raise RuntimeError(f"LOOP DETECTOR: Command '{command}' repeated {max_retries}x without progress.")
   ```

3. **Verification**:
   Execute the module verification demo:
   ```bash
   python course_implementation/module_01_why_harness_engineering/harness_vs_model_demo.py
   ```

## Key Files & Implementation
- `course_implementation/module_01_why_harness_engineering/harness_vs_model_demo.py`
- `course_implementation/module_01_why_harness_engineering/README.md`
