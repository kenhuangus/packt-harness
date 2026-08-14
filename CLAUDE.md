# Repository guidance

This repository is a Packt masterclass on harness engineering for AI coding agents. Its examples should model the same truthful, evidence-backed practices that the course teaches.

## Repository layout

- `course_implementation/module_01` through `module_10` contain the runnable course modules.
- `build_all_63_svg_slides.py` is the canonical deck builder. It reads `harness_course_presentation/slides_data.json` and generates both `slides.html` and `docs/slides.html`.
- `run_all_modules.py` is the repository-wide test runner.
- `VERIFIED_FACTS.md` is the source of truth for Claude Code and Model Context Protocol claims.

## Non-negotiable integrity rule

`RUN_RESULTS.md` files must be regenerated from real executions. Never invent, embellish, or preserve stale command output as though it came from a current run.

No module may print a `[PASS]` line for a check it did not actually perform. A passing result must be backed by evidence gathered during that run; an unmet condition must fail honestly. This is the repository's core principle.

Before editing teaching content about Claude Code, subagents, hooks, skills, plugins, or MCP, consult `VERIFIED_FACTS.md`. If other content conflicts with it, correct the other content rather than weakening the verified facts.

## Common commands

Run all modules (preflight requires the local vLLM model at `http://127.0.0.1:8000/v1`):

```powershell
python run_all_modules.py
```

Do not test against paid cloud APIs. Use the local model. Simulated LLM output is allowed only when `HARNESS_ALLOW_SIMULATED_LLM=1`.

Rebuild the slide deck:

```powershell
python build_all_63_svg_slides.py
```

Review generated artifacts after rebuilding and commit them only when they reflect the actual source and execution results.

## Cross-tool instructions

The `AGENTS.md` open standard is the cross-tool equivalent of this Claude Code memory file. Module 11 discusses the `ln -s AGENTS.md CLAUDE.md` pattern, but committed symlinks are fragile on Windows. This repository therefore uses regular files, with `AGENTS.md` pointing tools to this canonical guidance.
