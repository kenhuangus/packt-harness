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

- Python 3.10 or newer (3.13 on the authoring machine).
- A **local** OpenAI-compatible model by default (`http://127.0.0.1:8000/v1`, vLLM `nvidia/Qwen3.6-35B-A3B-NVFP4`). Switch to Claude or others with a gitignored `.env` (`LLM_PROVIDER=anthropic`, `LLM_MODEL=claude-sonnet-4-5`, `ANTHROPIC_API_KEY=...`). Never commit keys. `run_all_modules.py` fails if the configured backend is down. Simulated fallback is opt-in only (`HARNESS_ALLOW_SIMULATED_LLM=1`).

Example configuration:

```env
LLM_PROVIDER=openai
LLM_MODEL=nvidia/Qwen3.6-35B-A3B-NVFP4
LLM_BASE_URL=http://127.0.0.1:8000/v1
LLM_API_KEY=EMPTY
```

## Setup

Every module launches its subprocesses with `sys.executable`, so whichever
interpreter starts a module is the one that runs its pytest. A virtual
environment is what makes that interpreter predictable — and it is why a
module cannot pass by finding a different Python on `PATH`.

```powershell
git clone https://github.com/kenhuangus/packt-harness.git
cd packt-harness
python -m venv .venv
.venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt # or: pip install -e ".[capstone]"
python -m playwright install chromium
```

That installs `pytest`, `mcp`, `python-dotenv`, `aisuite[openai]`, `aisuite[anthropic]`, and `playwright`, and puts the `packt-harness` CLI on the venv's path.

Activating is optional. These are equivalent:

```powershell
.venv\Scripts\Activate.ps1     # then plain `python ...` means the venv
.venv\Scripts\python.exe ...   # no activation needed
```

Prefer the second form if PowerShell blocks activation with an execution
policy error. Everything below assumes the venv interpreter is what `python`
resolves to.

Clone rather than downloading a ZIP. Module 8 drives `git worktree` and fails
with `not a git repository` when there is no `.git` directory.

On Windows, clone into a short directory. The longest path in the repository is
140 characters, so a clone directory over about 119 characters trips the 260
character `MAX_PATH` limit and checkout fails with `Filename too long`. If that
happens, or to avoid it up front:

```powershell
git config --global core.longpaths true
```

### AI Model Provider Configuration (aisuite)

The default is the local OpenAI-compatible endpoint and needs no key. To switch,
set `LLM_PROVIDER` and the matching key in a gitignored `.env` (see
`course_implementation/.env.example`):

| Provider | `LLM_PROVIDER` | Key / Configuration | Endpoint / Extra |
| --- | --- | --- | --- |
| Local vLLM (Default) | `openai` | none (`LLM_API_KEY=EMPTY`) | `http://127.0.0.1:8000/v1` |
| OpenAI Cloud | `openai` | `OPENAI_API_KEY` | standard OpenAI API |
| OpenRouter | `openrouter` | `OPENROUTER_API_KEY` | `https://openrouter.ai/api/v1` |
| Ollama | `ollama` | none (local endpoint) | `http://127.0.0.1:11434` |
| Claude (Anthropic) | `anthropic` | `ANTHROPIC_API_KEY` | Anthropic SDK via aisuite |
| Gemini (Google) | `google` | `GEMINI_API_KEY` / `GOOGLE_API_KEY` | `generativelanguage.googleapis.com/v1beta/openai/` |

Gemini routes through Google's OpenAI-compatible endpoint (not Vertex AI), so no GCP credentials are required.

### Verify the install

```powershell
python run_all_modules.py
```

Expect `Summary: 14 passed, 0 failed`. The run starts with a preflight
against the configured model and stops immediately if that backend is down.

### Using the `packt-harness` CLI

```bash
# List all 10 modules and architectural summaries
packt-harness list

# Run any module demo (1-10 or 'all')
packt-harness run 3
packt-harness run all

# Run the 5-Gate production readiness audit
packt-harness audit

# Run the complete test suite
packt-harness test

# Launch and view the interactive HTML presentation slide deck
packt-harness slides --port 8080
```

## 🚀 Capstone Project: Autonomous Deep Research Agent

A production-grade, end-to-end autonomous research platform synthesizing all 10 harness engineering modules:

* 📐 **[System Architecture Specification](https://github.com/kenhuangus/packt-harness/blob/main/deep_research_agent/docs/architecture_diagram.svg)** (with interactive SVG and 4K diagrams).
* 🔄 **[End-to-End Execution Flow](https://github.com/kenhuangus/packt-harness/blob/main/deep_research_agent/docs/flow_diagram.svg)** (8-stage deterministic execution pipeline).
* 🌐 **Live Web UI 2.0**: High-contrast white theme, real-time SVG multi-hop research graph visualizer, citation confidence matrix, and unified diff reviewer.
* 🐙 **Zero-API Public Search Streams**: Playwright browser agent for public GitHub code/repositories, Playwright YouTube technical video search, HackerNews Algolia open index, OpenAlex scholarly DOIs, arXiv preprints, and Wikipedia.
* 🎥 **[1080p Full HD Demo Video Walkthrough](https://github.com/kenhuangus/packt-harness/blob/main/deep_research_agent/demo/deep_research_agent_demo.mp4)** (3.87 mins, 19 stages).
* 🛡️ **Verification**: 100% 5-Gate Scorecard certification and 14/14 passing automated Pytest TDA tests.
* 📖 **[Deep Research Agent Documentation](https://github.com/kenhuangus/packt-harness/tree/main/deep_research_agent/)**.

```bash
# Launch the Deep Research Web UI & Server on port 8090
python deep_research_agent/server.py 8090

# Run all 14 unit and TDA test suites
pytest -v
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
