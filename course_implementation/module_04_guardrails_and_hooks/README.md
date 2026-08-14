# Module 4: Guardrails and Hooks

## What this module teaches

Defense in depth for a coding agent is four layers. A prompt rule that
says "be careful" is layer 1. It is not enough.

| Layer | What enforces it here |
| --- | --- |
| 1. System / prompt rules | Course narrative; not executable in this file |
| 2. Typed tool arguments | `tool_input` must be an object with a string `command` |
| 3. Deterministic hooks | `PreToolUse` / `PostToolUse` JSON contract + shell regex + AST/secret scan |
| 4. Path sandbox | `Path.resolve()` then `Path.is_relative_to(workspace)` |

Claude Code sends hook JSON on stdin. Event names are case-sensitive
PascalCase (`PreToolUse`, `PostToolUse`). For `PreToolUse`, exit 0 may
return:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "..."
  }
}
```

Valid decisions: `allow`, `deny`, `ask`, `defer`. Exit 2 is blocking:
Claude Code shows stderr and ignores stdout.

The repository hook that Claude Code actually runs is
[bash_guard.py](https://github.com/kenhuangus/packt-harness/blob/main/.claude/hooks/bash_guard.py), registered
in [settings.json](https://github.com/kenhuangus/packt-harness/blob/main/.claude/settings.json) for matcher
`Bash`. The teaching engine in this module models the same contract.

## Files

| Path | Role |
| --- | --- |
| [guardrails_engine.py](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_04_guardrails_and_hooks/guardrails_engine.py) | Teaching engine + self-checks |
| [bash_guard.py](https://github.com/kenhuangus/packt-harness/blob/main/.claude/hooks/bash_guard.py) | Live Claude Code PreToolUse hook |
| [settings.json](https://github.com/kenhuangus/packt-harness/blob/main/.claude/settings.json) | Hook registration |
| [RUN_RESULTS.md](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_04_guardrails_and_hooks/RUN_RESULTS.md) | Last captured stdout |

The sandbox "inside" path
`...\module_04_guardrails_and_hooks\examples\output.py` is resolved, not
created. The demo also launches
[bash_guard.py](https://github.com/kenhuangus/packt-harness/blob/main/.claude/hooks/bash_guard.py) as a real
subprocess and writes
[hook_results.json](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_04_guardrails_and_hooks/output/hook_results.json).

## How to run

Full demo:

```powershell
C:\Users\kenhu\AppData\Local\Programs\Python\Python313\python.exe C:\Users\kenhu\packt-harness\course_implementation\module_04_guardrails_and_hooks\guardrails_engine.py
```

Live Bash hook (from the repository root). Write the JSON to a file first
so PowerShell does not eat the quotes:

```powershell
C:\Users\kenhu\AppData\Local\Programs\Python\Python313\python.exe C:\Users\kenhu\packt-harness\.claude\hooks\bash_guard.py
```

Pipe a `PreToolUse` payload into that command. Safe `pytest` returns
`defer`. `rm -rf /` returns `deny`.

## Output file and evidence

- **Stdout** (exit 0).
- **Recorded copy:** [RUN_RESULTS.md](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_04_guardrails_and_hooks/RUN_RESULTS.md)

Captured on this machine, 2026-08-14:

```text
[Claude Code Hook Contract]
  [PASS] Safe PreToolUse command allowed: PreToolUse check passed.
  [PASS] Dangerous PreToolUse command denied: CLI flag '--dangerously-skip-permissions' is prohibited by enterprise policy.
  [PASS] Structured deny JSON: {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny", ...}}

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
```

The sibling-prefix case is the important one. A string `startswith`
check would have allowed `module_04_guardrails_and_hooks-outside`.
`is_relative_to` rejects it.

## Annotated code

```python
class ClaudeCodeHookInterceptor:
    """
    Claude Code writes a JSON object to the hook's stdin. For PreToolUse,
    an exit-0 hook may return hookSpecificOutput with permissionDecision
    set to allow, deny, ask, or defer. Exit 2 is the blocking-error path.
    """

class GuardrailsEngine:
    """
    3. PreToolUse / PostToolUse plus intercept_shell_command / audit_ast_and_secrets.
    4. Path sandbox uses Path.resolve() + is_relative_to(), which rejects
       both `..` traversal and sibling directories that share a prefix.
    """

    def enforce_path_sandbox(self, target_path):
        resolved_target = Path(target_path).resolve()
        if not resolved_target.is_relative_to(self.workspace_root):
            return False, "SANDBOX VIOLATION: ..."
```
