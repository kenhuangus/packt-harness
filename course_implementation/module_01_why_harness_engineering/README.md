# Module 1: Why Harness Engineering

## What this module teaches

A strong model is not a reliable coding agent. Reliability comes from the
deterministic scaffolding around the model.

**Agent = Model + Harness**

The demo runs the same task two ways against real workspaces under
`output\`:

1. **Un-harnessed runner** — actually runs `pytest` three times (the test
   imports a missing module, so pytest exits 2) and then deletes
   `output\unharnessed_workspace\var\log\app.log`.
2. **Harnessed runner** — runs pytest once, blocks the second identical
   call, and refuses `rm -rf` so
   `output\harnessed_workspace\var\log\app.log` still exists.

Three failure modes are made visible:

| Failure mode | What happens without a harness | What the harness does |
| --- | --- | --- |
| Execution loop | Same `pytest` command retried after the same `ModuleNotFoundError` | Loop detector blocks the second identical call |
| Dangerous mutation | `rm -rf /var/log/*` is executed as typed | Pre-hook matches `rm\s+-rf` and denies it |
| Context decay | The runner never inspects *why* the test failed | The harness at least refuses to repeat a stall |

The LLM client at
[llm_client.py](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/common/llm_client.py)
is used. If `http://127.0.0.1:8000/v1` is down, the client prints a simulated
string and the harness checks still run.

## Files

| Path | Role |
| --- | --- |
| [harness_vs_model_demo.py](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_01_why_harness_engineering/harness_vs_model_demo.py) | Runnable demo |
| [RUN_RESULTS.md](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_01_why_harness_engineering/RUN_RESULTS.md) | Last captured stdout |
| [README.md](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_01_why_harness_engineering/README.md) | This file |

Output files:

- [run_evidence.json](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_01_why_harness_engineering/output/run_evidence.json)
- [course_implementation/module_01_why_harness_engineering/output/unharnessed_workspace/](https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_01_why_harness_engineering/output/unharnessed_workspace/)
- [course_implementation/module_01_why_harness_engineering/output/harnessed_workspace/](https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_01_why_harness_engineering/output/harnessed_workspace/)

## How to run

Use the Python 3.13 interpreter and the absolute script path. Working
directory does not matter; the script locates `common\llm_client.py` from
its own file path.

```powershell
C:\Users\kenhu\AppData\Local\Programs\Python\Python313\python.exe C:\Users\kenhu\packt-harness\course_implementation\module_01_why_harness_engineering\harness_vs_model_demo.py
```

Or run every module from the repository root:

```powershell
C:\Users\kenhu\AppData\Local\Programs\Python\Python313\python.exe C:\Users\kenhu\packt-harness\run_all_modules.py
```

## Output file and evidence

- **Stdout** from the command above (exit 0).
- **Recorded copy:** [RUN_RESULTS.md](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_01_why_harness_engineering/RUN_RESULTS.md)

Captured on this machine, 2026-08-14:

```text
============================================================
MODULE 1 DEMO: WHY HARNESS ENGINEERING IS REQUIRED
============================================================
[LLM Client] Configured LLM client with model 'default-harness-model' | Endpoint: 'http://127.0.0.1:8000/v1'

--- UN-HARNESSED AGENT SIMULATION ---
[LLM Response Output]: [Harness Simulated Output for prompt: Fix auth test failures...
[LLM Attempt 1] Trying command: pytest tests/auth_test.py
[System Output] Error: ModuleNotFoundError: No module named 'jwt'
...
[LLM Attempt 4] Trying dangerous cleanup command: rm -rf /var/log/*
[WARNING] UN-HARNESSED FAILURE: Unsanitized dangerous command executed!

--- HARNESSED AGENT SIMULATION ---
[Harness Evaluator] Inspecting tool call: run_shell('pytest tests/auth_test.py')
  ✓ Pre-action hook passed: Command is safe.
  ✓ Loop detector passed: No execution trap.
[Harness Evaluator] Inspecting tool call: run_shell('pytest tests/auth_test.py')
  ❌ Loop Detected: BLOCKED BY HARNESS LOOP DETECTOR: Command 'pytest tests/auth_test.py' repeated 2 times without progress.
[Harness Evaluator] Inspecting tool call: run_shell('rm -rf /var/log/*')
  ❌ Security Violation: BLOCKED BY PRE-HOOK: Dangerous command pattern 'rm\s+-rf' detected.
```

## Annotated code

The full file is
[harness_vs_model_demo.py](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_01_why_harness_engineering/harness_vs_model_demo.py).
Each block is commented in the source. The two classes:

```python
class UnharnessedAgentSimulator:
    """
    Simulate a raw model runner with no policy, no sandbox, and no loop stop.

    Everything after the LLM call is scripted so the failure modes are
    reproducible. The point is not that a particular model always does this;
    it is that nothing in this runner would stop it if it did.
    """

    def run_task(self, prompt):
        # Call the model. The return value is printed but never inspected
        # for command safety, so a dangerous suggestion would still run.
        response = self.llm_client.complete(prompt, ...)

        # Failure mode 1: the same pytest command is retried three times
        # against the same ModuleNotFoundError. No loop detector exists.
        # Failure mode 2: a destructive cleanup command is executed as typed.
        print("[LLM Attempt 4] Trying dangerous cleanup command: rm -rf /var/log/*")


class HarnessedAgentRunner:
    """
    Two deterministic gates sit in front of execution:
    - pre_execution_hook: regex deny-list for destructive shell patterns
    - loop_detector: halt when the same command repeats without progress
    """

    def execute_tool_call(self, tool_name, command):
        # Gate 1: deny-list check before anything is recorded as executed.
        self.pre_execution_hook(command)
        # Gate 2: identical-retry detector. The first pytest call passes;
        # the second identical call is halted when max_retries == 2.
        self.loop_detector(command)
```
