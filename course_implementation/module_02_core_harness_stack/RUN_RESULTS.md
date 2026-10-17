# Module 2 run results

Captured after the EventLogger / LangSmith-Langfuse-aligned Pillar 5 update.
`events.jsonl` was copied out of the temp workspace with `session_id` on every span.

## Command

```powershell
python course_implementation/module_02_core_harness_stack/core_harness_stack.py
```

## Notable stdout

```text
[Pillar 5 - Trace] EventLogger span 'WRITE_FILE_SUCCESS' -> events.jsonl
[Pillar 5 - Trace] EventLogger span 'RUN_TEST_SUCCESS' -> events.jsonl
[Pillar 5 - Trace] EventLogger span 'HARNESS_ERROR' -> events.jsonl
[OUTPUT] .../module_02_core_harness_stack/output/events.jsonl
[Pillar 5 - Observability] session_id=mod02-... · Local EventLogger trail ready. Mirror spans to LangSmith or Langfuse for UI dashboards / evals.
MODULE 2 DEMO COMPLETE: All 5 Pillars Executed & Logged!
```

See [README.md](README.md#pillar-5-lab-focus-harness-owned-tracing) for the slide 12 lab narrative.
