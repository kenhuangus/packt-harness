# Harness Skills Labs

These labs are designed to run against your own repository, not this course repository. Bring your real project and apply each skill there. You will feel each constraint where it actually matters.  
Exception: Lab 07 starts in this repo to confirm MCP wiring, then moves back to your own repo.

## Shared prerequisites

- Python 3.13 installed and available as `python`.
- Clone this repo somewhere local so you can run its skill scripts.
- From this repo root, install editable dependencies once:

```bash
pip install -e .
```

- If a lab step needs live generation, run a local model at `http://127.0.0.1:8000/v1`.
- If your local model is down, use this fallback for generation steps only:

```bash
export HARNESS_ALLOW_SIMULATED_LLM=1
```

- Labs that do not need generation call that out so you know you are not blocked.

## Lab index

| Lab | Skill | Module | Sheet |
|---|---|---|---|
| 01 | `harness-interception-loop-detector` | [module_01_why_harness_engineering](https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_01_why_harness_engineering) | [`lab-01-interception-loop-detector.md`](./lab-01-interception-loop-detector.md) |
| 02 | `harness-core-stack-sandbox` | [module_02_core_harness_stack](https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_02_core_harness_stack) | [`lab-02-core-stack-sandbox.md`](./lab-02-core-stack-sandbox.md) |
| 03 | `harness-spec-driven-development` | [module_03_spec_driven_development](https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_03_spec_driven_development) | [`lab-03-spec-driven-development.md`](./lab-03-spec-driven-development.md) |
| 04 | `harness-guardrails-and-hooks` | [module_04_guardrails_and_hooks](https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_04_guardrails_and_hooks) | [`lab-04-guardrails-and-hooks.md`](./lab-04-guardrails-and-hooks.md) |
| 05 | `harness-permission-escalation-gateway` | [module_05_break_and_qna](https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_05_break_and_qna) | [`lab-05-permission-escalation-gateway.md`](./lab-05-permission-escalation-gateway.md) |
| 06 | `harness-tda-reliability-pipeline` | [module_06_tests_as_reliability_layer](https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_06_tests_as_reliability_layer) | [`lab-06-tda-reliability-pipeline.md`](./lab-06-tda-reliability-pipeline.md) |
| 07 | `harness-mcp-and-plugins` | [module_07_skills_plugins_mcp](https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_07_skills_plugins_mcp) | [`lab-07-mcp-and-plugins.md`](./lab-07-mcp-and-plugins.md) |
| 08 | `harness-compound-multi-agent-worktrees` | [module_08_compound_engineering](https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_08_compound_engineering) | [`lab-08-compound-multi-agent-worktrees.md`](./lab-08-compound-multi-agent-worktrees.md) |
| 09 | `harness-five-step-sop-pipeline` | [module_09_practical_workflow_pattern](https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_09_practical_workflow_pattern) | [`lab-09-five-step-sop-pipeline.md`](./lab-09-five-step-sop-pipeline.md) |
| 10 | `harness-production-readiness-auditor` | [module_10_closing_and_principles](https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_10_closing_and_principles) | [`lab-10-production-readiness-auditor.md`](./lab-10-production-readiness-auditor.md) |

## Running order

- Lab 01 — feel the failure
- Labs 02-05 — constrain
- Lab 06 — verify
- Lab 07 — extend
- Labs 08-09 — scale
- Lab 10 — certify
