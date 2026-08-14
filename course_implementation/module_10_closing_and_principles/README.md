# Module 10: Closing Principles and Audit

## What this module teaches

The course closes on four principles and a five-check audit that
inspects **this repository**, not a slide.

### Four principles

1. **Predictability over randomness** — `CLAUDE.md` / `AGENTS.md` so
   every session starts from the same rules.
2. **Reduce ambiguity** — `SPEC.md` instead of a paragraph prompt.
3. **Automate checks** — hooks, AST, tests. Do not rely on the model
   remembering the policy.
4. **Optimize for trust** — every `[PASS]` must be backed by a check
   the process actually ran.

### Five audit checks

The auditor walks a target directory (default: this repo root) and
prints a reason string for each check.

| Check | Evidence it looks for |
| --- | --- |
| 1. Memory files | Regular files `CLAUDE.md` and/or `AGENTS.md` |
| 2. Pre-execution hooks | `.claude/settings.json` has PascalCase `PreToolUse` whose command points at a file that exists |
| 3. Automated test runner | `run_all_modules.py` parses as Python; `pytest --version` works |
| 4. MCP scoped tools | Module 7 Python files declare at least one `@tool` and one `@resource` (AST) |
| 5. Multi-agent roles | `.claude/agents/*.md` have documented frontmatter (`name`, `description`, optional `tools` / `isolation`) |

A failed check lowers the score. The process still exits 0 so a partial
project can be audited. Against an empty directory the score is 0/5.

## Files

| Path | Role |
| --- | --- |
| `C:\Users\kenhu\packt-harness\course_implementation\module_10_closing_and_principles\production_harness_audit.py` | Auditor |
| `C:\Users\kenhu\packt-harness\CLAUDE.md` | Check 1 |
| `C:\Users\kenhu\packt-harness\AGENTS.md` | Check 1 |
| `C:\Users\kenhu\packt-harness\.claude\settings.json` | Check 2 |
| `C:\Users\kenhu\packt-harness\.claude\hooks\bash_guard.py` | Check 2 hook file |
| `C:\Users\kenhu\packt-harness\run_all_modules.py` | Check 3 |
| `C:\Users\kenhu\packt-harness\course_implementation\module_07_skills_plugins_mcp\mcp_server_demo.py` | Check 4 AST source |
| `C:\Users\kenhu\packt-harness\.claude\agents\spec-reviewer.md` | Check 5 |
| `C:\Users\kenhu\packt-harness\course_implementation\module_10_closing_and_principles\RUN_RESULTS.md` | Last captured stdout |

No extra output file. The audit prints to stdout.

## How to run

Audit this repository (default target = two directories up from the script):

```powershell
C:\Users\kenhu\AppData\Local\Programs\Python\Python313\python.exe C:\Users\kenhu\packt-harness\course_implementation\module_10_closing_and_principles\production_harness_audit.py
```

Audit some other project:

```powershell
C:\Users\kenhu\AppData\Local\Programs\Python\Python313\python.exe C:\Users\kenhu\packt-harness\course_implementation\module_10_closing_and_principles\production_harness_audit.py C:\path\to\other\repo
```

## Output file and evidence

- **Stdout** (exit 0), score 5/5 against this repo.
- **Recorded copy:** `C:\Users\kenhu\packt-harness\course_implementation\module_10_closing_and_principles\RUN_RESULTS.md`

Captured on this machine, 2026-08-14:

```text
Target Project Path: C:\Users\kenhu\packt-harness

  [PASS] Check 1: Memory files -> found regular file(s): CLAUDE.md, AGENTS.md
  [PASS] Check 2: Pre-execution hooks -> PreToolUse matcher 'Bash' runs existing hook file C:\Users\kenhu\packt-harness\.claude\hooks\bash_guard.py
  [PASS] Check 3: Automated test runner -> run_all_modules.py is valid Python; pytest 9.1.1
  [PASS] Check 4: MCP scoped tools/resources -> AST declarations found: tools=['query_database_record']; resources=['app_settings']
  [PASS] Check 5: Multi-agent role definitions -> validated 1 subagent definition(s): spec-reviewer.md

AUDIT SUMMARY: 5/5 Checks Passed (100% Production Readiness Score)
STATUS: ALL AUDITED READINESS CHECKS PASSED.
```

## Annotated code

```python
class ProductionHarnessAuditor:
    """
    Each check returns (passed, reason). A failed check lowers the
    score; the process still exits 0. The reason string is the evidence.
    """

    def check_memory_files(self):
        # Regular files CLAUDE.md / AGENTS.md under the target root.

    def check_pre_execution_hooks(self):
        # Parse .claude/settings.json. Require matcher + type=command
        # whose expanded path is an existing file.

    def check_test_runner(self):
        # ast.parse(run_all_modules.py) and subprocess pytest --version.

    def check_mcp_scoped_tools(self):
        # Walk module 7 *.py and collect @tool / @resource function names.

    def check_multi_agent_roles(self):
        # Parse YAML-ish frontmatter. name and description required.
        # isolation, if present, must be the string 'worktree'.
```
