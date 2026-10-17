# Module 2: Core Harness Stack

## What this module teaches

A production coding harness is five pillars, not a better prompt.

| Pillar | What it is in this repo |
| --- | --- |
| 1. Instructions and repo conventions | `AGENTS.md` loaded by byte count before any tool runs |
| 2. Scoped tools and permissions | Allow-list `read_file`, `write_file`, `run_test`, `list_dir` plus a workspace prefix sandbox |
| 3. Hooks and policy | Pre-write secret/empty checks; post-write `ast.parse` |
| 4. Token budget | 20/20/50/10 split of a 128k window; head/tail log compaction |
| 5. Observability / tracing | Harness-owned `EventLogger` spans in `events.jsonl` (same pattern as LangSmith / Langfuse) |

`CLAUDE.md` is Claude Code's repository memory file. `AGENTS.md` is the
same idea for tools that follow the AGENTS.md convention. This module's
committed memory file is
[AGENTS.md](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_02_core_harness_stack/AGENTS.md).

The live workspace is still a temp directory. After the checks, the
harness copies `events.jsonl`, `sample_module.py`, and the compacted
compiler log into
[course_implementation/module_02_core_harness_stack/output/](https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_02_core_harness_stack/output/).
Path checks use `Path.resolve().is_relative_to()`, not a string prefix.

## Pillar 5 lab focus: harness-owned tracing

Slide 12 (Pillars 4 & 5) uses **this module** as the lab demo. Pillar 5 is
**not** vendor session dumps. The harness is the system of record:

1. **`CoreHarnessStack.log_event`** appends one JSON object per line to
   `events.jsonl` with ISO UTC `timestamp`, `event_type`, `session_id`, and
   `details` (tool name, path, allow/deny, latency hints, token fields when known).
2. **Every permission, hook, write, and test outcome** emits a span before the
   next step continues — so the audit trail is complete even when a path is blocked.
3. **Industry backends:** the same span shape can be mirrored to
   [LangSmith](https://docs.smith.langchain.com/) or
   [Langfuse](https://langfuse.com/docs) for UI dashboards, latency/token charts,
   and eval datasets. Start with local `events.jsonl`; export when you need a UI.

Schema reference:
[event_schema.json](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_02_core_harness_stack/skills/harness-core-stack-sandbox/assets/event_schema.json).

## Files

| Path | Role |
| --- | --- |
| [core_harness_stack.py](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_02_core_harness_stack/core_harness_stack.py) | Five-pillar demo + EventLogger |
| [AGENTS.md](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_02_core_harness_stack/AGENTS.md) | Pillar 1 memory file |
| [sample_module.py](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_02_core_harness_stack/sample_module.py) | Older sample; not written by the current demo |
| [events.jsonl](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_02_core_harness_stack/events.jsonl) | Last copied harness audit log (from the demo run) |
| [output/events.jsonl](https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_02_core_harness_stack/output) | Recorded copy after each successful run |
| [RUN_RESULTS.md](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_02_core_harness_stack/RUN_RESULTS.md) | Last captured stdout |

## How to run

Run from the repository root, using the project virtualenv
(`python -m venv .venv` then `.venv\Scripts\Activate.ps1`, then
`pip install -e .` — see the [root README](../../README.md#setup)):

```powershell
python course_implementation/module_02_core_harness_stack/core_harness_stack.py
```

Requires `pytest` on that interpreter (`python -m pip install pytest`).
Without it the test pillar exits 1 instead of printing `[PASS]`.

After the run, open `output/events.jsonl` and confirm you see spans such as
`PERMISSION_GRANTED`, `WRITE_FILE_SUCCESS`, `RUN_TEST_SUCCESS`, and
`PATH_TRAVERSAL_BLOCKED` / `HARNESS_ERROR`.

## Output file and evidence

- **Stdout** (exit 0).
- **Live audit log (ephemeral):** `%TEMP%\module_02_harness_<random>\events.jsonl`
- **Recorded copy:** [output/events.jsonl](https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_02_core_harness_stack/output) and [RUN_RESULTS.md](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_02_core_harness_stack/RUN_RESULTS.md)

Example stdout excerpt:

```text
[Pillar 1 - Memory] Loaded persistent guidelines from 'AGENTS.md' (...)
Allocations: {'memory': 25600, 'spec': 25600, 'workspace': 64000, 'output_buffer': 12800}

>>> HARNESS EXECUTION TASK: write_file <<<
[Pillar 2 - Permission] Tool 'write_file' and path '...' validated.
[Pillar 3 - Pre-Hook] Code safety inspection passed.
[Pillar 3 - Post-Hook] Running AST static analysis on 'sample_module.py'...
  [PASS] AST syntax valid.
[Pillar 5 - Trace] EventLogger span 'WRITE_FILE_SUCCESS' -> events.jsonl

>>> HARNESS EXECUTION TASK: run_test <<<
  [PASS] pytest exited with code 0.
[Pillar 5 - Trace] EventLogger span 'RUN_TEST_SUCCESS' -> events.jsonl

>>> HARNESS EXECUTION TASK: write_file <<<
[FAIL] HARNESS ERROR: Path Traversal Blocked: ...
[Pillar 5 - Observability] Local EventLogger trail ready. Mirror spans to LangSmith or Langfuse for UI dashboards / evals.
```

The last `[FAIL] HARNESS ERROR` line is the expected sandbox rejection.
The process still exits 0 because the block is the demonstration.

## Annotated code

```python
class CoreHarnessStack:
    """
    workspace_root is the only directory write_file may touch. Every
    permission decision and hook result is appended via EventLogger to
    events.jsonl inside that workspace as one JSON object per line
    (same span pattern you later send to LangSmith or Langfuse).
    """

    def validate_tool_permission(self, tool_name, target_path=None) -> bool:
        # Pillar 2: unknown tool names are denied. A target outside
        # workspace_root (Path.is_relative_to) is path traversal.
        ...

    def run_post_edit_hook(self, file_path, code_content) -> bool:
        # Pillar 3: reject hardcoded sk-proj- keys and empty edits
        # before the file is written. Syntax is checked later with ast.parse.
        ...

    def log_event(self, event_type, details):
        # Pillar 5: append-only EventLogger span. Never overwrite previous lines.
        ...
```
