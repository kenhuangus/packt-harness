# Module 2: Core Harness Stack

## What this module teaches

A production coding harness is five pillars, not a better prompt.

| Pillar | What it is in this repo |
| --- | --- |
| 1. Instructions and repo conventions | `AGENTS.md` loaded by byte count before any tool runs |
| 2. Scoped tools and permissions | Allow-list `read_file`, `write_file`, `run_test`, `list_dir` plus a workspace prefix sandbox |
| 3. Hooks and policy | Pre-write secret/empty checks; post-write `ast.parse` |
| 4. Token budget | 20/20/50/10 split of a 128k window; head/tail log compaction |
| 5. Observability | One JSON object per line in `events.jsonl` |

`CLAUDE.md` is Claude Code's repository memory file. `AGENTS.md` is the
same idea for tools that follow the AGENTS.md convention. This module's
committed memory file is
`C:\Users\kenhu\packt-harness\course_implementation\module_02_core_harness_stack\AGENTS.md`.

The demo writes into a `TemporaryDirectory` under
`C:\Users\kenhu\AppData\Local\Temp\module_02_harness_*`. The committed
`events.jsonl` next to this README is leftover from an older run that
wrote into the module directory. The current code does not update that
file. Durable evidence is stdout and `RUN_RESULTS.md`.

## Files

| Path | Role |
| --- | --- |
| `C:\Users\kenhu\packt-harness\course_implementation\module_02_core_harness_stack\core_harness_stack.py` | Five-pillar demo |
| `C:\Users\kenhu\packt-harness\course_implementation\module_02_core_harness_stack\AGENTS.md` | Pillar 1 memory file |
| `C:\Users\kenhu\packt-harness\course_implementation\module_02_core_harness_stack\sample_module.py` | Older sample; not written by the current demo |
| `C:\Users\kenhu\packt-harness\course_implementation\module_02_core_harness_stack\events.jsonl` | Historical leftover, not the live audit log |
| `C:\Users\kenhu\packt-harness\course_implementation\module_02_core_harness_stack\RUN_RESULTS.md` | Last captured stdout |

## How to run

```powershell
C:\Users\kenhu\AppData\Local\Programs\Python\Python313\python.exe C:\Users\kenhu\packt-harness\course_implementation\module_02_core_harness_stack\core_harness_stack.py
```

Requires `pytest` on that interpreter (`python -m pip install pytest`).
Without it the test pillar exits 1 instead of printing `[PASS]`.

## Output file and evidence

- **Stdout** (exit 0).
- **Live audit log (ephemeral):** `C:\Users\kenhu\AppData\Local\Temp\module_02_harness_<random>\events.jsonl`
- **Recorded copy:** `C:\Users\kenhu\packt-harness\course_implementation\module_02_core_harness_stack\RUN_RESULTS.md`

Captured on this machine, 2026-08-14:

```text
[Pillar 1 - Memory] Loaded persistent guidelines from 'AGENTS.md' (482 bytes)
Allocations: {'memory': 25600, 'spec': 25600, 'workspace': 64000, 'output_buffer': 12800}

>>> HARNESS EXECUTION TASK: write_file <<<
[Pillar 2 - Permission] Tool 'write_file' and path 'C:\Users\kenhu\AppData\Local\Temp\module_02_harness_0gg2cx8v\sample_module.py' validated.
[Pillar 3 - Pre-Hook] Code safety inspection passed.
[Pillar 3 - Post-Hook] Running AST static analysis on 'sample_module.py'...
  [PASS] AST syntax valid.
[Pillar 5 - Trace] Logged 'WRITE_FILE_SUCCESS' to JSONL audit file.

>>> HARNESS EXECUTION TASK: run_test <<<
  [PASS] pytest exited with code 0.
[Pillar 5 - Trace] Logged 'RUN_TEST_SUCCESS' to JSONL audit file.

>>> HARNESS EXECUTION TASK: write_file <<<
[FAIL] HARNESS ERROR: Path Traversal Blocked: Target 'C:\Users\kenhu\AppData\Local\Temp\module_02_harness_0gg2cx8v\..\..\forbidden.py' is outside workspace 'C:\Users\kenhu\AppData\Local\Temp\module_02_harness_0gg2cx8v'
```

The last `[FAIL] HARNESS ERROR` line is the expected sandbox rejection.
The process still exits 0 because the block is the demonstration.

## Annotated code

```python
class CoreHarnessStack:
    """
    workspace_root is the only directory write_file may touch. Every
    permission decision and hook result is appended to events.jsonl
    inside that workspace as one JSON object per line.
    """

    def validate_tool_permission(self, tool_name, target_path=None) -> bool:
        # Pillar 2: unknown tool names are denied. A target whose
        # abspath does not start with workspace_root is path traversal.
        ...

    def run_post_edit_hook(self, file_path, code_content) -> bool:
        # Pillar 3: reject hardcoded sk-proj- keys and empty edits
        # before the file is written. Syntax is checked later with ast.parse.
        ...

    def log_event(self, event_type, details):
        # Pillar 5: append-only JSONL. Never overwrite previous lines.
        ...
```
