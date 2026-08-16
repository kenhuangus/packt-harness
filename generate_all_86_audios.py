"""
Generate High-Quality In-Depth Audio Narration for all 86 Course Slides using Local Neural TTS (edge-tts).
All audio is stored in the local audio/ directory (gitignored).
"""

from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path
import subprocess
import sys
import time

import edge_tts

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

AUDIO_DIR = Path("audio")
AUDIO_DIR.mkdir(exist_ok=True)

VOICE = "en-US-ChristopherNeural"

# Deep, comprehensive technical narration for each slide
SLIDE_NARRATIONS: dict[int, str] = {
    1: (
        "Welcome to the Packt Masterclass on Harness Engineering for AI Coding Agents. "
        "I am Ken Huang. In modern software engineering, raw large language models often struggle when operating "
        "autonomously inside production codebases. Without deterministic scaffolding, even the most capable frontier models "
        "suffer from hallucinated tool parameters, path traversal escapes, and runaway retry loops. "
        "This masterclass is designed to teach you how to build a production-grade harness—a deterministic runtime supervisor "
        "that enforces immutable specifications, intercepts unsafe actions before execution, budgets context windows, "
        "and coordinates multi-agent workflows."
    ),
    2: (
        "Before we dive into the architecture, a brief introduction. I am Ken Huang, working across generative AI security, "
        "agent reliability, and cloud architectures. My research spans the AIUC-1 working group, Schmidt Sciences, and co-authoring "
        "the OWASP Top 10 for Large Language Models. Over the past decade, I have authored fifteen books across Springer, "
        "Cambridge University Press, Wiley, Packt, and Claude AI, covering blockchain security, decentralized AI, prompt engineering, "
        "and autonomous agents. Throughout this course, every concept we cover is backed by real, executable Python code and automated test suites."
    ),
    3: (
        "Let us begin with Module 1: Why Harness Engineering is Required. "
        "A common industry misconception is that simply upgrading to a larger foundation model resolves agent hallucinations. "
        "In reality, without a deterministic harness, scaling model intelligence often increases the velocity of failures. "
        "In this module, we examine the four catastrophic failure modes of un-harnessed agents: context drift, execution traps, "
        "unverified file edits, and destructive command execution."
    ),
    4: (
        "Here we contrast prompt engineering with harness engineering. Prompt engineering relies entirely on probabilistic "
        "natural language instructions inside the context window. However, under high context pressure or unexpected compiler outputs, "
        "agents frequently violate soft prompt guidelines. Harness engineering replaces soft suggestions with deterministic, "
        "machine-enforced boundaries: validating tool arguments against schemas, trapping repetitive commands, and sandboxing workspace paths."
    ),
    5: (
        "Failure Mode 1 is Context Drift. As multi-turn conversations expand, compiler dumps, stack traces, and intermediate tool responses "
        "flood the context window. Crucial architectural constraints placed in the initial prompt get pushed out of the model's active attention span. "
        "The harness solves this through strict token budgeting and automated log compaction, preserving core architectural guidelines across long sessions."
    ),
    6: (
        "Failure Mode 2 is the Execution Loop Trap. When a test fails, an unconstrained agent often repeats the exact same failing command "
        "or minor variations in a circular loop, burning thousands of API tokens without making forward progress. "
        "A production harness implements active loop detection, counting identical tool invocations and forcibly intercepting execution when a threshold is breached."
    ),
    7: (
        "Failure Mode 3 is Unverified File Writes. Autonomous agents often generate plausible-looking code that contains subtle syntax errors, "
        "missing imports, or broken dependencies. If written directly to disk without verification, these edits break the build. "
        "A harness enforces an abstract syntax tree parsing gate, compiling every code diff in memory before committing changes to the workspace."
    ),
    8: (
        "Failure Mode 4 is Destructive Actions. When attempting to clean up build artifacts or reset test state, agents may execute broad "
        "shell commands such as rm -rf or permission overrides that destroy critical repositories. "
        "The harness implements pre-execution command regex inspection, blocking dangerous shell patterns before they reach the operating system."
    ),
    9: (
        "In our first laboratory demonstration in Module 1, we execute harness_vs_model_demo.py. "
        "We simulate an un-harnessed agent attempting repetitive pytest runs and a reckless directory wipe, contrasted against our harnessed agent "
        "which intercepts the loop and blocks the deletion, allowing the sandbox log files to survive intact."
    ),
    10: (
        "This terminal trace demonstrates the live execution of Module 1. Notice how the un-harnessed run deletes the log file after repeated failures, "
        "whereas the harnessed evaluator intercepts the loop on attempt two with code 2 and blocks the rm -rf command with a security violation."
    ),
    11: (
        "Let us examine the Python code lab for Module 1 in harness_vs_model_demo.py. "
        "Lines 134 to 142 implement pre_execution_hook, checking proposed commands against forbidden regex patterns. "
        "Lines 145 to 154 implement the loop_detector class, tracking call signatures in a sliding history buffer and halting execution when repetitions occur."
    ),
    12: (
        "Here is the skill manifest for harness-interception-loop-detector located in .claude/skills/. "
        "This skill equips Claude Code with the ability to detect runaway execution traps and sanitize shell invocations before token waste or data loss occurs."
    ),
    13: (
        "We now move to Module 2: The Core Harness Stack. "
        "A robust agent harness is built upon five foundational pillars: Memory Files, Scoped Tools and Sandboxing, "
        "Deterministic Hooks, Context Token Budgeting, and Structured JSONL Observability."
    ),
    14: (
        "This diagram illustrates the five pillars in detail. Memory files like CLAUDE.md and AGENTS.md provide persistent rules. "
        "Scoped tools restrict agent actions to least privilege. Deterministic hooks run static analysis before and after tool calls. "
        "Context budgeting manages token allocations, and JSONL tracing provides immutable auditability."
    ),
    15: (
        "Pillar 1 focuses on Memory Files: CLAUDE.md and AGENTS.md. "
        "These files store concise, permanent project instructions, coding standards, and build commands. "
        "Crucially, memory files must be strictly budget-capped so they do not exhaust the agent's context window."
    ),
    16: (
        "Pillar 2 is Scoped Tools and Path Sandboxing. "
        "An agent should only possess the minimum set of tools required for its role. Furthermore, all filesystem modifications "
        "must be strictly bound using Python's Path.resolve().is_relative_to() to prevent directory traversal attacks outside the workspace."
    ),
    17: (
        "Pillar 3 is the Deterministic Hooks Engine. "
        "Hooks act as active middleware. PreToolUse hooks inspect tool names and arguments prior to execution, while PostToolUse hooks "
        "perform automated abstract syntax tree parsing and regex-based secret scanning on modified files."
    ),
    18: (
        "Pillars 4 and 5 cover Context Budgeting and Tracing. "
        "Our ContextTokenBudgeter enforces a 20/20/50/10 split across memory, spec, workspace, and output buffers, compacting long compiler dumps. "
        "Meanwhile, all operations are appended to events.jsonl for complete post-incident forensic replay."
    ),
    19: (
        "In this Module 2 Code Lab, we inspect core_harness_stack.py. "
        "Lines 71 to 78 enforce the 20/20/50/10 token budget allocation. "
        "Lines 141 to 148 validate tool permissions and resolve paths against the workspace boundary, raising a harness error on traversal attempts."
    ),
    20: (
        "Slide 20 displays the skill manifest for harness-core-stack-sandbox. "
        "It formalizes path containment, post-edit secret scanning, and append-only event logging into a reusable agent skill."
    ),
    21: (
        "Welcome to Module 3: Spec-Driven Development, or SDD. "
        "SDD is the single most effective methodology for constraining autonomous coding agents. Instead of vague conversational prompts, "
        "we provide machine-checkable markdown contracts."
    ),
    22: (
        "Why do prompts fail while specs succeed? Prompts are ambiguous and subject to probabilistic interpretation drift. "
        "A formal specification defines explicit allowed files, non-goals, and automated acceptance criteria, rejecting out-of-scope diffs before they are merged."
    ),
    23: (
        "Here is the anatomy of a production SPEC.md file. It contains four mandatory sections: "
        "Section 1: Feature Objective; Section 2: Allowed Modification Scope; Section 3: Explicit Non-Goals; "
        "and Section 4: Machine-Verifiable Acceptance Criteria."
    ),
    24: (
        "Defining Scope and Non-Goals creates hard architectural boundaries. "
        "For example, in our JWT authentication feature, we allow edits to auth_validator.py and test_auth.py, while strictly forbidding database.py and configuration files. "
        "If an agent attempts to write database connection logic, the harness immediately blocks the write."
    ),
    25: (
        "Acceptance criteria must be executable rather than qualitative. "
        "Instead of saying 'make the authentication secure', AC-01 specifies that auth_validator.py must export validate_jwt returning a dictionary, "
        "and AC-04 requires passing the full pytest suite in tests/test_auth.py."
    ),
    26: (
        "The SDD Lifecycle operates in four continuous stages: first, the agent reads and parses SPEC.md; second, it generates code strictly inside declared scope; "
        "third, the harness audits diffs against non-goals; and fourth, automated pytest suites verify the criteria."
    ),
    27: (
        "Spec verification before code ships guarantees that no unauthorized files are touched. "
        "In our demonstration, SpecVerifier parses SPEC.md markdown headings and enforces boundary checks on every file write attempt."
    ),
    28: (
        "In the Module 3 Code Lab from spec_driven_verifier.py, lines 6 to 8 enforce the allowed_files scope whitelist, "
        "lines 10 to 13 filter proposed diffs against non-goal keywords, and line 18 runs ast.parse() before saving to disk."
    ),
    29: (
        "This is the skill manifest for harness-spec-driven-development, providing automated validation of SPEC.md contracts and AST syntax gates."
    ),
    30: (
        "We now advance to Module 4: Guardrails and Deterministic Hooks. "
        "In enterprise deployments, defense-in-depth is non-negotiable. We implement a multi-layered guardrail architecture to ensure total execution safety."
    ),
    31: (
        "The 4-Layer Control Model consists of: Layer 1, System Prompt Rules; Layer 2, Tool Argument JSON Schemas; "
        "Layer 3, Deterministic PreToolUse and PostToolUse Hooks; and Layer 4, Operating System Sandboxing and Path Isolation."
    ),
    32: (
        "Here we examine the Claude Code PascalCase hook contract. "
        "Claude Code writes a JSON payload to the hook's standard input. For PreToolUse events, the hook returns a structured JSON object "
        "with permissionDecision set to allow, deny, ask, or defer."
    ),
    33: (
        "Post-Action verification checks include static syntax validation via ast.parse() and high-entropy regex scans for hardcoded API secret keys. "
        "If an agent accidentally embeds an API key in generated source code, the PostToolUse hook rejects the change immediately."
    ),
    34: (
        "Path Sandboxing prevents agents from accessing sensitive files across the parent filesystem. "
        "By enforcing Path.resolve().is_relative_to(workspace), any attempt to escape into ../../etc or parent user directories is intercepted."
    ),
    35: (
        "Permission modes define the autonomy level of the agent. "
        "Safe read actions run automatically, while high-risk commands require interactive operator elevation."
    ),
    36: (
        "Evaluation harnesses measure agent safety quantitatively across test suites, ensuring that guardrails do not degrade coding efficiency."
    ),
    37: (
        "Our safety checklist mandates three non-negotiables: immutable workspace sandboxes, pre-action shell sanitization, and post-write syntax compilation."
    ),
    38: (
        "In this Module 4 Code Lab from guardrails_engine.py, lines 6 to 14 evaluate PreToolUse payloads, specifically blocking dangerous CLI flags "
        "such as --dangerously-skip-permissions, while lines 20 to 26 run secret scanning and AST parsing."
    ),
    39: (
        "Slide 39 outlines the harness-guardrails-and-hooks skill manifest, standardizing PascalCase PreToolUse and PostToolUse hook evaluation."
    ),
    40: (
        "Welcome to Module 5: Break, Q&A, and Permission Escalation Gateways. "
        "Here we explore how to safely manage high-risk enterprise actions using an approval ledger."
    ),
    41: (
        "During this interactive module, we analyze common failure scenarios and how human-in-the-loop controls protect production environments."
    ),
    42: (
        "In the Module 5 Code Lab from permission_escalation_gateway.py, we implement a 4-tier risk matrix: LOW for reads, MEDIUM for writes, "
        "HIGH for deletions, and CRITICAL for operations like git push. Critical actions are blocked until a signed record is recorded in approvals.json."
    ),
    43: (
        "The harness-permission-escalation-gateway skill manifest allows agents to request explicit human confirmation before executing irreversible changes."
    ),
    44: (
        "We now explore Module 6: Tests as the Reliability Layer. "
        "Automated testing is not merely a post-build verification step; it is the fundamental sensory feedback loop for agentic self-repair."
    ),
    45: (
        "The Test-Driven Agent, or TDA, loop follows three rigorous stages: Red, where we prove the bug exists with a failing test; "
        "Repair, where captured traceback output is formatted into a targeted repair prompt; and Green, where pytest confirms resolution."
    ),
    46: (
        "Test Tiers define execution velocity. Fast unit tests run on every file write, integration tests execute before branch commits, "
        "and full end-to-end regression suites run prior to pull request submission."
    ),
    47: (
        "Traceback feedback must be automated. The harness captures raw pytest compiler errors and injects them directly into the agent's prompt, "
        "eliminating manual copy-paste overhead."
    ),
    48: (
        "Anti-regression guarantees that solved bugs stay fixed. Whenever an agent repairs a defect, the harness persists the reproduction test "
        "into the permanent test suite to prevent future regressions."
    ),
    49: (
        "Key reliability metrics include first-pass pass rate, repair iterations to green, and regression test coverage."
    ),
    50: (
        "In the Module 6 Code Lab from tda_reliability_pipeline.py, lines 6 to 14 execute pytest in a temporary subprocess, "
        "while lines 20 to 28 append the new regression safeguard test_divide_zero_guard directly into test_calculator.py."
    ),
    51: (
        "Slide 51 details the harness-tda-reliability-pipeline skill manifest, enabling agents to execute deterministic test repair cycles."
    ),
    52: (
        "Welcome to Module 7: Skills, Plugins, and the Model Context Protocol, or MCP. "
        "Here we explore modern extensibility frameworks for AI coding agents."
    ),
    53: (
        "Agent Skills are encapsulated directories containing a SKILL.md manifest with YAML frontmatter, providing domain-specific knowledge and scripts."
    ),
    54: (
        "The canonical skill layout includes a name, description, allowed tools, reference documentation, and executable Python helper scripts."
    ),
    55: (
        "Claude Plugins bundle skills, agents, hooks, and MCP servers into a single discoverable plugin.json manifest."
    ),
    56: (
        "Understanding MCP requires distinguishing three different version numbers: the dated protocol specification like 2025-06-18, "
        "the Python SDK package version such as 2.0.0, and the JSON-RPC 2.0 wire framing standard."
    ),
    57: (
        "MCP transports operate locally over child-process standard input and output streams, or remotely using Streamable HTTP."
    ),
    58: (
        "Authoring modern MCP servers uses the official Python SDK's @mcp.tool() and @mcp.resource() decorators, communicating cleanly over stdio."
    ),
    59: (
        "MCP Governance ensures least-privilege tool exposure and prevents unauthorized data exfiltration."
    ),
    60: (
        "In the Module 7 Code Lab, mcp_server_demo.py exposes query_database_record and config://app-settings, "
        "while mcp_client_runner.py connects over stdio, queries the database, and synthesizes the live result using aisuite."
    ),
    61: (
        "Slide 61 outlines the harness-mcp-and-plugins skill manifest for discovering and interacting with MCP servers."
    ),
    62: (
        "We now enter Module 8: Compound Engineering and Multi-Agent Workflows. "
        "Single agents attempting to plan, implement, and review their own code represent a single point of failure."
    ),
    63: (
        "Why multi-agent teams? Separating roles into specialized agents with dedicated, uncluttered context windows prevents hallucination and cognitive overload."
    ),
    64: (
        "The Planner agent acts as the architect, breaking broad specifications into discrete, file-scoped subtasks without performing writes."
    ),
    65: (
        "The Implementer agent receives only its assigned sub-spec and writes code strictly inside an isolated workspace."
    ),
    66: (
        "The Reviewer agent conducts an independent audit, running AST syntax checks and pytest suites without shared conversation bias."
    ),
    67: (
        "Worktree Isolation creates ephemeral git worktrees for the implementer, ensuring that unverified code cannot corrupt the main repository branch."
    ),
    68: (
        "Subagent context isolation passes only the necessary sub-spec lines, drastically reducing token consumption."
    ),
    69: (
        "Self-improvement telemetry logs multi-agent execution metrics into telemetry.jsonl for continuous workflow optimization."
    ),
    70: (
        "In the Module 8 Code Lab from multi_agent_team_simulator.py, lines 6 to 12 create an ephemeral git worktree, "
        "and lines 18 to 26 run independent reviewer checks before cleaning up the worktree."
    ),
    71: (
        "Slide 71 displays the harness-compound-multi-agent-worktrees skill manifest for orchestrating multi-agent teams."
    ),
    72: (
        "Welcome to Module 9: The Practical SOP Workflow Pattern. "
        "Here we synthesize everything learned into a repeatable five-step production standard operating procedure."
    ),
    73: (
        "The Five-Step SOP comprises: Step 1, Spec First; Step 2, Constrained Execution; Step 3, Deterministic Checks; "
        "Step 4, Automated Test Verification; and Step 5, Human Review and Diff Approval."
    ),
    74: (
        "Steps 1 and 2 parse SPEC.md and bind agent edits strictly to in-scope files within a temporary sandbox."
    ),
    75: (
        "Steps 3 and 4 execute AST compilation, secret scanning, and real pytest test suites."
    ),
    76: (
        "Step 5 generates a unified diff of the verified changes for human engineering sign-off before merging."
    ),
    77: (
        "In the Module 9 Code Lab from five_step_sop_pipeline.py, we execute the complete end-to-end pipeline, producing a clean 58-line diff of our JWT validator."
    ),
    78: (
        "Slide 78 details the harness-five-step-sop-pipeline skill manifest for running production SOP workflows."
    ),
    79: (
        "We conclude with Module 10: Enterprise Principles and Readiness Audit. "
        "How do you know if your codebase is truly ready for autonomous AI coding agents?"
    ),
    80: (
        "The Four Golden Principles: Specs over Prompts, Deterministic Gates over Probabilistic Hopes, "
        "Tests as the Sensory Feedback Layer, and Least-Privilege Scoped Tooling."
    ),
    81: (
        "The 5-Gate Production Readiness Scorecard evaluates: Memory Files, Pre-execution Hooks, Test Runners, "
        "MCP Declarations, and Subagent Role Definitions."
    ),
    82: (
        "In summary, building reliable AI coding workflows requires moving beyond basic chat interfaces into engineered harnesses."
    ),
    83: (
        "In the Module 10 Code Lab from production_harness_audit.py, we run our automated auditor against the repository, achieving a 100% 5/5 readiness score."
    ),
    84: (
        "Slide 84 presents the harness-production-readiness-auditor skill manifest for auditing repositories."
    ),
    85: (
        "This comparison slide contrasts Graph Engineering with Dynamic Workflows in Claude Code, distinguishing architectural blueprint design from native runtime execution."
    ),
    86: (
        "Finally, Slide 86 compiles all core references, documentation links, and GitHub repositories. "
        "Thank you for attending this masterclass on Harness Engineering for AI Coding Agents."
    ),
}


async def generate_single_audio(slide_num: int, text: str, semaphore: asyncio.Semaphore) -> tuple[int, Path, float]:
    async with semaphore:
        out_file = AUDIO_DIR / f"slide_{slide_num:02d}.mp3"
        communicate = edge_tts.Communicate(text, VOICE)
        await communicate.save(str(out_file))
        
        # Measure duration with ffprobe if available
        duration = 0.0
        try:
            res = subprocess.run(
                [
                    "ffprobe", "-v", "error", "-show_entries", "format=duration",
                    "-of", "default=noprint_wrappers=1:nokey=1", str(out_file)
                ],
                capture_output=True, text=True
            )
            duration = float(res.stdout.strip())
        except Exception:
            duration = out_file.stat().st_size / 4000.0  # Approx fallback
            
        print(f"  [OK] Slide {slide_num:02d} -> {out_file.name} ({duration:.1f}s, {out_file.stat().st_size} bytes)")
        return slide_num, out_file, duration


async def generate_all_audios():
    print("=" * 70)
    print(f"GENERATING IN-DEPTH COURSE AUDIO NARRATIONS ({len(SLIDE_NARRATIONS)} SLIDES)")
    print(f"Target Directory: {AUDIO_DIR.resolve()}")
    print(f"Voice: {VOICE}")
    print("=" * 70 + "\n")
    
    sem = asyncio.Semaphore(5)  # 5 concurrent synthesis tasks
    tasks = [
        generate_single_audio(num, text, sem)
        for num, text in sorted(SLIDE_NARRATIONS.items())
    ]
    
    start_time = time.time()
    results = await asyncio.gather(*tasks)
    elapsed = time.time() - start_time
    
    total_duration = sum(r[2] for r in results)
    print(f"\n[DONE] Successfully generated {len(results)} slide audio files in {elapsed:.1f}s!")
    print(f"Total Course Audio Duration: {total_duration / 60:.1f} minutes ({total_duration:.1f} seconds)\n")

    # Combine into full course masterclass audio using ffmpeg
    print("[*] Concatenating all slide audios into complete masterclass audio...")
    concat_list = AUDIO_DIR / "concat_list.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for num, path, _ in sorted(results, key=lambda x: x[0]):
            f.write(f"file '{path.name}'\n")
            
    master_audio = AUDIO_DIR / "packt_harness_masterclass_complete.mp3"
    subprocess.run(
        [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", str(concat_list), "-c", "copy", str(master_audio)
        ],
        capture_output=True
    )
    if master_audio.is_file():
        print(f"[SUCCESS] Complete masterclass audio created: {master_audio} ({master_audio.stat().st_size} bytes)")
        
    # Generate audio README index
    readme_path = AUDIO_DIR / "README.md"
    readme_lines = [
        "# Packt Harness Engineering Masterclass - Audio Narrations\n",
        f"Generated using local neural TTS ({VOICE}).\n",
        f"- **Total Slides**: {len(results)}",
        f"- **Total Duration**: {total_duration / 60:.1f} minutes ({total_duration:.1f} seconds)",
        f"- **Complete Audio Track**: [`packt_harness_masterclass_complete.mp3`](packt_harness_masterclass_complete.mp3)\n",
        "## Individual Slide Audio Tracks\n",
        "| Slide # | File | Duration | Topic |",
        "| :--- | :--- | :--- | :--- |",
    ]
    for num, path, dur in sorted(results, key=lambda x: x[0]):
        snippet = SLIDE_NARRATIONS[num][:60].replace("\n", " ") + "..."
        readme_lines.append(f"| Slide {num:02d} | `{path.name}` | {dur:.1f}s | {snippet} |")
        
    readme_path.write_text("\n".join(readme_lines), encoding="utf-8")
    print(f"[*] Audio catalog written to: {readme_path}")


if __name__ == "__main__":
    asyncio.run(generate_all_audios())
