# Harness Engineering for AI Coding Agents (Packt Training Masterclass)

Welcome to the official repository for the **Packt Training Masterclass: Build Reliable Claude Code Workflows with Guardrails and Tests**.

> **Course Focus**: Deterministic Scaffolding, Guardrails, Spec-Driven Development (SDD), MCP 2.0, & Multi-Agent Swarms

---

## 📌 Master Course Architecture

| Module | Title | Schedule | Key Concepts & Code Implementation |
| :--- | :--- | :--- | :--- |
| **Mod 1** | Why Harness Engineering | 09:00 - 09:15 | Failure modes, context amnesia, infinite loops, & unverified edits ([`module_01_why_harness_engineering/`](./course_implementation/module_01_why_harness_engineering/)) |
| **Mod 2** | Core Harness Stack | 09:15 - 09:30 | 5 Pillars, `CLAUDE.md` / `AGENTS.md` symlinks, token budgeting, & `events.jsonl` ([`module_02_core_harness_stack/`](./course_implementation/module_02_core_harness_stack/)) |
| **Mod 3** | Spec-Driven Development | 09:30 - 09:50 | `SPEC.md` contracts, allowed file scopes, & machine-verifiable acceptance criteria ([`module_03_spec_driven_development/`](./course_implementation/module_03_spec_driven_development/)) |
| **Mod 4** | Guardrails & Hooks | 09:50 - 10:10 | 4-layer control matrix, regex shell pre-hooks, Python AST linters, & secret scanners ([`module_04_guardrails_and_hooks/`](./course_implementation/module_04_guardrails_and_hooks/)) |
| **Mod 5** | Break & Permission Gateways | 10:10 - 10:20 | Risk-tiered approval matrix (auto-approve, log, interactive confirmation) ([`module_05_break_and_qna/`](./course_implementation/module_05_break_and_qna/)) |
| **Mod 6** | Tests as Reliability Layer | 10:20 - 10:35 | Test-Driven Agent (TDA) loops, zero-touch traceback capture, & anti-regression suite ([`module_06_tests_as_reliability_layer/`](./course_implementation/module_06_tests_as_reliability_layer/)) |
| **Mod 7** | Skills, Plugins & MCP 2.0 | 10:35 - 10:50 | `SKILL.md` open standard, `plugin.json` bundles, & MCP 2.0 FastMCP stdio/SSE tools ([`module_07_skills_plugins_mcp/`](./course_implementation/module_07_skills_plugins_mcp/)) |
| **Mod 8** | Compound Engineering | 10:50 - 11:05 | Planner/Implementer/Reviewer role division & `git worktree add` sandboxing ([`module_08_compound_engineering/`](./course_implementation/module_08_compound_engineering/)) |
| **Mod 9** | Practical Workflow SOP | 11:05 - 11:15 | 5-step SOP pipeline combining Spec First, Sandboxing, Hooks, Tests, & Review ([`module_09_practical_workflow_pattern/`](./course_implementation/module_09_practical_workflow_pattern/)) |
| **Mod 10**| Closing Principles & Audit | 11:15 - 11:30 | 4 Core Principles & 100% production readiness scorecard audit ([`module_10_closing_and_principles/`](./course_implementation/module_10_closing_and_principles/)) |

---

## 🛠️ Multi-Provider LLM Integration

All module implementations interact with LLMs through a standardized client layer located at [`course_implementation/common/llm_client.py`](./course_implementation/common/llm_client.py).

### Configuration (`.env`)

Create a `.env` file in the root directory or load environment variables:

```env
LLM_PROVIDER=openai
LLM_MODEL=nvidia/Qwen3.6-35B-A3B-NVFP4
LLM_BASE_URL=http://127.0.0.1:8000/v1
LLM_API_KEY=EMPTY
```

---

## 🚀 Quickstart

1. **Clone the repository**:
   ```bash
   git clone https://github.com/kenhuangus/packt-harness.git
   cd packt-harness
   ```

2. **Run all 10 module test suites**:
   ```bash
   python run_all_modules.py
   ```

3. **Launch the Web Dashboard**:
   Open [`course_implementation/dashboard/index.html`](./course_implementation/dashboard/index.html) in your browser.

4. **View Interactive HTML Slides**:
   Open [`slides.html`](https://kenhuangus.github.io/packt-harness/slides.html) in your browser or local file.

---

## 🌐 Online Resources

- **Live Course Website**: [https://kenhuangus.github.io/packt-harness/](https://kenhuangus.github.io/packt-harness/)
- **Live HTML Presentation App**: [https://kenhuangus.github.io/packt-harness/slides.html](https://kenhuangus.github.io/packt-harness/slides.html)
