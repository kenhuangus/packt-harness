# Module 4 Run Results

The required Python 3.13 interpreter resolves to
`C:\Users\kenhu\AppData\Local\Programs\Python\Python313\python.exe`, but the
managed verification environment denied executing it:

```text
> python --version
Access is denied.
EXIT=1
```

The following is literal output from a secondary smoke run with the accessible
Python 3.12.12 interpreter. It is useful evidence, but it is not a substitute
for the required Python 3.13 verification.

```text
Python 3.12.12
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
  [PASS] Inside path allowed: Path sandbox check passed for 'C:\Users\kenhu\packt\harness\course_implementation\module_04_guardrails_and_hooks\examples\output.py'.
  [PASS] Sibling-prefix path rejected: SANDBOX VIOLATION: Target path 'C:\Users\kenhu\packt\harness\course_implementation\module_04_guardrails_and_hooks-outside\escape.py' resides outside workspace 'C:\Users\kenhu\packt\harness\course_implementation\module_04_guardrails_and_hooks'

============================================================
MODULE 4 DEMO COMPLETE: ALL EXPECTED CONTROLS VERIFIED!
============================================================
```

Direct hook smoke results:

```text
{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"defer","permissionDecisionReason":"No dangerous command pattern matched; normal permissions still apply."}}
SAFE_EXIT=0
{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"Blocked dangerous Bash command: recursive forced deletion (matched '\\brm\\s+-rf\\b')."}}
DANGER_EXIT=0
Bash guard input error: Expecting value: line 1 column 1 (char 0)
MALFORMED_EXIT=2
```
