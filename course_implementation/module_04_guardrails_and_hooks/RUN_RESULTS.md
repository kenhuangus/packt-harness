# Module 4 Run Results

Captured 2026-08-14 on this machine from an actual process.

```text
> C:\Users\kenhu\AppData\Local\Programs\Python\Python313\python.exe C:\Users\kenhu\packt-harness\course_implementation\module_04_guardrails_and_hooks\guardrails_engine.py
cwd = C:\Users\kenhu\packt-harness\course_implementation\module_04_guardrails_and_hooks
============================================================
MODULE 4 DEMO: PRODUCTION GUARDRAILS & CLAUDE CODE HOOKS
============================================================

[Claude Code Hook Contract]
  [PASS] Safe PreToolUse command allowed: PreToolUse check passed.
  [PASS] Dangerous PreToolUse command denied: CLI flag '--dangerously-skip-permissions' is prohibited by enterprise policy.
  [PASS] Structured deny JSON: {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": "CLI flag '--dangerously-skip-permissions' is prohibited by enterprise policy."}}

[Shell Command Guardrail]
  [PASS] Safe shell command allowed: Shell command permitted.
  [PASS] Dangerous shell command blocked: CRITICAL SECURITY BLOCK: Command matches dangerous pattern 'rm\s+-rf'

[AST and Secret Scan]
  [PASS] Valid code accepted: AST syntax valid. Zero secret leaks detected.
  [PASS] Hardcoded secret rejected: SECURITY CRITICAL: Hardcoded API secret key detected!
  [PASS] Invalid syntax rejected: AST Syntax Error on line 1: invalid syntax

[Resolved Path Sandbox]
  [PASS] Inside path allowed: Path sandbox check passed for 'C:\Users\kenhu\packt-harness\course_implementation\module_04_guardrails_and_hooks\examples\output.py'.
  [PASS] Sibling-prefix path rejected: SANDBOX VIOLATION: Target path 'C:\Users\kenhu\packt-harness\course_implementation\module_04_guardrails_and_hooks-outside\escape.py' resides outside workspace 'C:\Users\kenhu\packt-harness\course_implementation\module_04_guardrails_and_hooks'

============================================================
MODULE 4 DEMO COMPLETE: ALL EXPECTED CONTROLS VERIFIED!
============================================================
```

Exit code: 0
