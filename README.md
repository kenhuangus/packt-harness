# Harness Engineering for AI Coding Agents (Packt Training Masterclass)

This repository supports the Packt masterclass **Build Reliable Claude Code Workflows with Guardrails and Tests**.

> **Course focus:** deterministic scaffolding, guardrails, Spec-Driven Development (SDD), the Model Context Protocol (MCP), and multi-agent workflows.

## Course architecture

| Module | Title | Schedule | Key concepts and implementation |
| :--- | :--- | :--- | :--- |
| **Module 1** | Why Harness Engineering | 09:00–09:15 | Failure modes, context drift, loops, and unverified edits ([`module_01_why_harness_engineering/`](./course_implementation/module_01_why_harness_engineering/)) |
| **Module 2** | Core Harness Stack | 09:15–09:30 | Five pillars, repository instructions, token budgeting, and `events.jsonl` ([`module_02_core_harness_stack/`](./course_implementation/module_02_core_harness_stack/)) |
| **Module 3** | Spec-Driven Development | 09:30–09:50 | `SPEC.md` contracts, allowed file scopes, and machine-verifiable acceptance criteria ([`module_03_spec_driven_development/`](./course_implementation/module_03_spec_driven_development/)) |
| **Module 4** | Guardrails and Hooks | 09:50–10:10 | Layered controls, `PreToolUse` command guards, `PostToolUse` checks, and secret scanning ([`module_04_guardrails_and_hooks/`](./course_implementation/module_04_guardrails_and_hooks/)) |
| **Module 5** | Break, Q&A, and Permission Gateways | 10:10–10:20 | Risk-tiered approval policy and explicit confirmation for critical actions ([`module_05_break_and_qna/`](./course_implementation/module_05_break_and_qna/)) |
| **Module 6** | Tests as the Reliability Layer | 10:20–10:35 | Test-driven agent loops, traceback capture, and anti-regression tests ([`module_06_tests_as_reliability_layer/`](./course_implementation/module_06_tests_as_reliability_layer/)) |
| **Module 7** | Skills, Plugins, and MCP | 10:35–10:50 | Description-driven skills; `.claude-plugin/plugin.json` bundles for skills, agents, hooks, MCP/LSP servers, and monitors; MCP over stdio or Streamable HTTP ([`module_07_skills_plugins_mcp/`](./course_implementation/module_07_skills_plugins_mcp/)) |
| **Module 8** | Compound Engineering | 10:50–11:05 | Planner/implementer/reviewer roles and `isolation: worktree` ([`module_08_compound_engineering/`](./course_implementation/module_08_compound_engineering/)) |
| **Module 9** | Practical Workflow SOP | 11:05–11:15 | A five-step pipeline combining specs, sandboxing, hooks, tests, and review ([`module_09_practical_workflow_pattern/`](./course_implementation/module_09_practical_workflow_pattern/)) |
| **Module 10** | Closing Principles and Audit | 11:15–11:30 | Core principles and a production-readiness scorecard ([`module_10_closing_and_principles/`](./course_implementation/module_10_closing_and_principles/)) |

## Prerequisites

- Python 3.13.
- The MCP Python SDK: `python -m pip install mcp`.
- For live LLM demos, an OpenAI-compatible endpoint configured with `LLM_PROVIDER`, `LLM_MODEL`, `LLM_BASE_URL`, and `LLM_API_KEY` in a root `.env` file or the environment. Without a reachable endpoint, the demos fall back to simulated output so the harness exercises can still run.

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

Each module folder under `C:\Users\kenhu\packt-harness\course_implementation\`
has its own `README.md` with what that module teaches, the absolute-path
run command, and captured stdout in `RUN_RESULTS.md`.

Open [`course_implementation/dashboard/index.html`](./course_implementation/dashboard/index.html) for the dashboard, or view the [interactive HTML slide deck](https://kenhuangus.github.io/packt-harness/slides.html).

## What is actually verified here

[`VERIFIED_FACTS.md`](./VERIFIED_FACTS.md) records the Claude Code and MCP claims checked against official Anthropic and MCP documentation, including exact hook events, skill and subagent frontmatter, plugin structure, protocol versioning, and current transports. It also links the official sources so readers can verify those claims directly.

## Online resources

- [Live course website](https://kenhuangus.github.io/packt-harness/)
- [Live HTML presentation](https://kenhuangus.github.io/packt-harness/slides.html)
