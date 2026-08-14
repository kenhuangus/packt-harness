# Harness Engineering for AI Coding Agents (Packt Training Masterclass)

This repository supports the Packt masterclass **Build Reliable Claude Code Workflows with Guardrails and Tests**.

> **Course focus:** deterministic scaffolding, guardrails, Spec-Driven Development (SDD), the Model Context Protocol (MCP), and multi-agent workflows.

## Course architecture

| Module | Title | Key concepts and implementation |
| :--- | :--- | :--- |
| **Module 1** | Why Harness Engineering | Failure modes, context drift, loops, and unverified edits ([README](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_01_why_harness_engineering/README.md)) |
| **Module 2** | Core Harness Stack | Five pillars, repository instructions, token budgeting, and `events.jsonl` ([README](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_02_core_harness_stack/README.md)) |
| **Module 3** | Spec-Driven Development | `SPEC.md` contracts, allowed file scopes, and machine-verifiable acceptance criteria ([README](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_03_spec_driven_development/README.md)) |
| **Module 4** | Guardrails and Hooks | Layered controls, `PreToolUse` command guards, `PostToolUse` checks, and secret scanning ([README](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_04_guardrails_and_hooks/README.md)) |
| **Module 5** | Break, Q&A, and Permission Gateways | Risk-tiered approval policy and explicit confirmation for critical actions ([README](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_05_break_and_qna/README.md)) |
| **Module 6** | Tests as the Reliability Layer | Test-driven agent loops, traceback capture, and anti-regression tests ([README](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_06_tests_as_reliability_layer/README.md)) |
| **Module 7** | Skills, Plugins, and MCP | Description-driven skills; `.claude-plugin/plugin.json` bundles for skills, agents, hooks, MCP/LSP servers, and monitors; MCP over stdio or Streamable HTTP ([README](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_07_skills_plugins_mcp/README.md)) |
| **Module 8** | Compound Engineering | Planner/implementer/reviewer roles and `isolation: worktree` ([README](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_08_compound_engineering/README.md)) |
| **Module 9** | Practical Workflow SOP | A five-step pipeline combining specs, sandboxing, hooks, tests, and review ([README](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_09_practical_workflow_pattern/README.md)) |
| **Module 10** | Closing Principles and Audit | Core principles and a production-readiness scorecard ([README](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_10_closing_and_principles/README.md)) |

## Prerequisites

- Python 3.13.
- The MCP Python SDK: `python -m pip install mcp`.
- [aisuite](https://github.com/andrewyng/aisuite) (`python -m pip install aisuite`). The course client talks to every provider through aisuite.
- A **local** OpenAI-compatible model by default (`http://127.0.0.1:8000/v1`, vLLM `nvidia/Qwen3.6-35B-A3B-NVFP4`). Switch to Claude or others with a gitignored `.env` (`LLM_PROVIDER=anthropic`, `LLM_MODEL=claude-sonnet-4-5`, `ANTHROPIC_API_KEY=...`). Never commit keys. `run_all_modules.py` fails if the configured backend is down. Simulated fallback is opt-in only (`HARNESS_ALLOW_SIMULATED_LLM=1`).

Example configuration:

```env
LLM_PROVIDER=openai
LLM_MODEL=nvidia/Qwen3.6-35B-A3B-NVFP4
LLM_BASE_URL=http://127.0.0.1:8000/v1
LLM_API_KEY=EMPTY
```

## Quickstart

```bash
git clone https://github.com/kenhuangus/packt-harness.git
cd packt-harness
python -m pip install mcp
python run_all_modules.py
```

Each module folder under [course_implementation/](https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/)
has its own `README.md` with what that module teaches, the absolute-path
run command, and captured stdout in `RUN_RESULTS.md`.

Open [`course_implementation/dashboard/index.html`](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/dashboard/index.html) for the dashboard, or view the [interactive HTML slide deck](https://kenhuangus.github.io/packt-harness/slides.html).

## What is actually verified here

[`VERIFIED_FACTS.md`](https://github.com/kenhuangus/packt-harness/blob/main/VERIFIED_FACTS.md) records the Claude Code and MCP claims checked against official Anthropic and MCP documentation, including exact hook events, skill and subagent frontmatter, plugin structure, protocol versioning, and current transports. It also links the official sources so readers can verify those claims directly.

## Online resources

- [Live course website](https://kenhuangus.github.io/packt-harness/)
- [Live HTML presentation](https://kenhuangus.github.io/packt-harness/slides.html)
