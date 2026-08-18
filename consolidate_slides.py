"""
Consolidates redundant slides across the masterclass presentation deck:
- Merges duplicate intro/title slides with their subsequent concept slides.
- Removes repetitive filler and combines related points into substantive, high-impact slides.
- Renumbers all slides cleanly.
"""

import json
from pathlib import Path

DATA_FILE = Path("harness_course_presentation/slides_data.json")
slides = json.loads(DATA_FILE.read_text(encoding="utf-8"))
print(f"Original total slides: {len(slides)}")

# Build the consolidated list of slides
consolidated = []

for s in slides:
    raw = s.get("raw_lines", [])
    title = raw[0] if raw else ""
    stype = s.get("slide_type", "standard")

    # 1. Slide 4: Already combined Module 1
    if title.startswith("MODULE 1: Why Harness Engineering"):
        s["raw_lines"] = [
            "MODULE 1: Why Harness Engineering",
            "Probabilistic Model vs. Deterministic Control System",
            "• Model Capability ≠ production reliability: Fast generation, weak follow-through without harness controls.",
            "• Probabilistic Model Layer: Proposes code; prone to amnesia, hallucination, drift, and retry traps.",
            "• Deterministic Harness Layer: Enforces sandboxing, AST parsing, loop detection, and secret scanning.",
            "• Key Failure Modes: Context decay, repetitive execution loops, destructive shell commands, unverified edits.",
            "• Core Mandate: The harness, not the model, is the control system — optimize for trust over raw speed."
        ]
        consolidated.append(s)
        continue

    # Skip old redundant "Model vs Harness" if present
    if title == "Model vs Harness":
        print("  -> Dropping redundant 'Model vs Harness' (consolidated into Slide 4)")
        continue

    # 2. Module 2: Combine "MODULE 2" and "The 5 Harness Pillars"
    if title == "MODULE 2":
        print("  -> Dropping redundant 'MODULE 2' intro slide (consolidated into 5 Pillars slide)")
        continue
    if title == "The 5 Harness Pillars":
        s["raw_lines"] = [
            "MODULE 2: The 5 Core Harness Pillars",
            "Architectural Scaffolding for Coding Agents",
            "• Pillar 1: Memory (CLAUDE.md & AGENTS.md persistent project instructions)",
            "• Pillar 2: Scoped Tools (least privilege allowlists & Path.is_relative_to() sandboxing)",
            "• Pillar 3: Deterministic Hooks (PascalCase PreToolUse & PostToolUse AST / secret guards)",
            "• Pillar 4: Token Budgeting (20/20/50/10 budget allocation & head/tail log compaction)",
            "• Pillar 5: Structured Tracing (events.jsonl append-only immutable audit trail)"
        ]
        consolidated.append(s)
        continue

    # 3. Module 3: Combine "MODULE 3" and "Why Prompts Fail"
    if title == "MODULE 3":
        print("  -> Dropping redundant 'MODULE 3' intro slide (consolidated into Specs Succeed slide)")
        continue
    if title == "Why Prompts Fail":
        s["raw_lines"] = [
            "MODULE 3: Spec-Driven Development",
            "Why Prompts Fail & Machine-Readable Specs Succeed",
            "• Prompts are ambiguous, under-specified, and prone to context drift over long chats.",
            "• Machine-Verifiable Contracts: SPEC.md defines allowed file scopes, schemas, and non-goals.",
            "• Hard Scope Boundaries: SpecVerifier rejects out-of-scope diffs and blocks unapproved writes.",
            "• Non-Goal Filtering: Blocks architectural sprawl and unrequested dependencies before code is saved.",
            "• Automated Verification: Verifies syntax via ast.parse() and runs pytest before shipping."
        ]
        consolidated.append(s)
        continue

    # 4. Module 4: Combine "MODULE 4" and "4-Layer Control"
    if title == "MODULE 4":
        print("  -> Dropping redundant 'MODULE 4' intro slide (consolidated into 4-Layer Control slide)")
        continue
    if title == "4-Layer Control":
        s["raw_lines"] = [
            "MODULE 4: Guardrails, Hooks & 4-Layer Control",
            "Defense-in-Depth for Safe Tool Execution",
            "• Layer 1 (System Prompt): Standing project rules and memory in CLAUDE.md and AGENTS.md.",
            "• Layer 2 (Tool Schemas): Strongly typed JSON schema argument validation.",
            "• Layer 3 (Hooks): PascalCase PreToolUse flag denial & PostToolUse AST / secret scanners.",
            "• Layer 4 (OS Sandbox): Resolved-path isolation and process-level least privilege.",
            "• Deterministic Enforcement: Security policies written in code, never left to model discretion."
        ]
        consolidated.append(s)
        continue

    # 5. Module 5: Combine "MODULE 5" and "Open Q&A"
    if title == "MODULE 5":
        print("  -> Dropping redundant 'MODULE 5' intro slide (consolidated into Q&A slide)")
        continue
    if title == "Open Q&A":
        s["raw_lines"] = [
            "MODULE 5: Break & Permission Gateways",
            "Risk-Tiered Approval Gateways & Mid-Course Q&A",
            "• 4-Tier Risk Matrix: LOW (auto-approve reads), MEDIUM (sandboxed writes), HIGH (scanned commands), CRITICAL (approvals.json).",
            "• Cryptographic Escalation: Critical operations (e.g. git_push) require explicit authorization tokens.",
            "• Checkpoint Discussion: How does your organization gate agent permissions in CI/CD?",
            "• Failure Analysis: Where have un-gated agent loops caused accidental outages or data loss?",
            "• Lab Demo: https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_05_break_and_qna/README.md"
        ]
        consolidated.append(s)
        continue

    # 6. Module 6: Combine "MODULE 6" and "TDA Loop"
    if title == "MODULE 6":
        print("  -> Dropping redundant 'MODULE 6' intro slide (consolidated into TDA Loop slide)")
        continue
    if title == "TDA Loop":
        s["raw_lines"] = [
            "MODULE 6: Tests as Reliability Layer",
            "The Test-Driven Coding Agent (TDCA) Red-Repair-Green Loop",
            "• Grounded Execution: Replace unverified agent claims with deterministic pytest subprocess return codes.",
            "• Real Traceback Capture: Feed raw stdout/stderr error tracebacks directly into repair prompts without copy-paste.",
            "• Anti-Regression Safeguards: Automatically register discovered bugs as permanent test suite fixtures.",
            "• Quantitative Reliability: Track first-pass pass rate, mean repair iterations, and regression count."
        ]
        consolidated.append(s)
        continue

    # 7. Module 7: Combine "Agent Skills" and "Skill Layout"
    if title == "Agent Skills":
        s["raw_lines"] = [
            "Agent Skills & Directory Layout",
            "Standard Architecture: SKILL.md, Scripts & References",
            "• Self-Contained Modularity: Encapsulates domain expertise, execution scripts, and API schemas in one directory.",
            "• SKILL.md Entry Point: YAML frontmatter with description defining what the skill does and when to use it.",
            "• Progressive Disclosure: Heavy scripts/ and references/ are only loaded into context when triggered.",
            "• Precedence Hierarchy (Highest to Lowest): 1. Enterprise Managed > 2. Personal User-Level (~/.claude/skills/) > 3. Project Root (.claude/skills/) > 4. Installed Plugins."
        ]
        consolidated.append(s)
        continue
    if title == "Skill Layout":
        print("  -> Dropping redundant 'Skill Layout' (consolidated into Agent Skills slide)")
        continue

    # 8. Module 8: Combine "MODULE 8" and "Why Multi-Agent"
    if title == "MODULE 8":
        print("  -> Dropping redundant 'MODULE 8' intro slide (consolidated into Why Multi-Agent slide)")
        continue
    if title == "Why Multi-Agent":
        s["raw_lines"] = [
            "MODULE 8: Compound Engineering",
            "Why Multi-Agent Roles & Context Isolation",
            "• Cognitive Overload: A single un-scoped agent drowns in fat context and degraded reasoning.",
            "• Specialization: Divide execution into Planner (architect), Implementer (coder), and Reviewer (auditor).",
            "• Git Worktree Isolation: Ephemeral isolation: worktree branches prevent implementer edits from dirtying main.",
            "• Sub-Spec Extraction: Deliver lean, slice-specific prompt contexts to subagents for maximum efficiency.",
            "• Compounding Loop: telemetry.jsonl feeds lessons and failure patterns into AGENTS.md for continuous improvement."
        ]
        consolidated.append(s)
        continue

    # 9. Module 9: Combine "MODULE 9" and "Five-Step SOP"
    if title == "MODULE 9":
        print("  -> Dropping redundant 'MODULE 9' intro slide (consolidated into Five-Step SOP slide)")
        continue
    if title == "Five-Step SOP":
        s["raw_lines"] = [
            "MODULE 9: The Five-Step Practical SOP Pipeline",
            "Deterministic End-to-End Delivery Lifecycle",
            "• Step 1 (Spec First): Formulate machine-verifiable SPEC.md with strict scope whitelists.",
            "• Step 2 (Sandbox Execution): Execute implementation tasks in isolated ephemeral git worktrees.",
            "• Step 3 (Guardrails & Scanning): Intercept dangerous flags and scan AST/regex for secret leaks.",
            "• Step 4 (Pytest TDA Loop): Run automated test suites and self-heal from captured tracebacks.",
            "• Step 5 (Human Review & Audit): Generate unified diffs and verify 5-gate production readiness scorecard."
        ]
        consolidated.append(s)
        continue

    # 10. Module 10: Combine "MODULE 10" and "Four Principles"
    if title == "MODULE 10":
        print("  -> Dropping redundant 'MODULE 10' intro slide (consolidated into Four Principles slide)")
        continue
    if title == "Four Principles":
        s["raw_lines"] = [
            "MODULE 10: Four Principles of Harness Engineering",
            "Core Tenets & Production Readiness Benchmarking",
            "• Principle 1: Predictability over randomness (deterministic scaffolding over prompt tuning).",
            "• Principle 2: Specs over prompts (machine-readable contracts over conversational requests).",
            "• Principle 3: Automated checks over vigilance (compiler AST, pytest, and hook interceptors).",
            "• Principle 4: Trust over raw speed (verified correctness before merging to main).",
            "• 5-Gate Scorecard: Memory files, PreToolUse hooks, test runner, MCP tools, and subagent schemas."
        ]
        consolidated.append(s)
        continue

    # Default: keep slide
    consolidated.append(s)

# Renumber all slides sequentially
for idx, s in enumerate(consolidated, start=1):
    s["number"] = idx

DATA_FILE.write_text(json.dumps(consolidated, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"[OK] Consolidated slide count: {len(consolidated)} (Renumbered 1 to {len(consolidated)})")
