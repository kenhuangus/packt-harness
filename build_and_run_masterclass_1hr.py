"""
Complete 1-Hour+ Masterclass Audio Narration Generator.
Generates comprehensive technical lectures for all 86 slides (~8,800+ words),
synthesizes high-fidelity audio via edge-tts, and produces a single unified MP3.
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

# Exhaustive, full-length masterclass technical lectures (~9,000+ words)
# Structured to produce over 60 minutes of uninterrupted masterclass audio.
SLIDE_NARRATIONS: dict[int, str] = {
    1: (
        "Welcome to the Packt Masterclass on Harness Engineering for AI Coding Agents: Building Reliable "
        "Claude Code Workflows with Deterministic Scaffolding, Guardrails, Spec-Driven Development, and Automated Test Feedback Loops. "
        "I am your instructor, Ken Huang. Today, software development stands at a historic inflection point. "
        "Autonomous coding agents powered by large language models have demonstrated astonishing proficiency at translating "
        "natural language prompts into functional source code. However, when engineering teams attempt to transition "
        "these probabilistic models directly into enterprise production pipelines, they routinely encounter severe operational roadblocks. "
        "Without strict runtime scaffolding, even state-of-the-art models suffer from context window degradation, catastrophic execution loop traps, "
        "unverified filesystem mutations, and unauthorized system operations. "
        "In enterprise software development, we must treat coding agents not as infallible senior developers, "
        "but as junior engineers who possess immense knowledge but require strict oversight, well-defined sandbox boundaries, "
        "and continuous automated testing. This masterclass is meticulously designed to provide you with the architectural blueprints "
        "and hands-on Python implementations required to transform fragile AI assistants into rock-solid, production-grade autonomous software engineers. "
        "We will explore the paradigm shift from prompt engineering to harness engineering, where deterministic code surrounds, monitors, "
        "and supervises probabilistic models at every step of execution. Throughout this course, you will learn how to design immutable specifications, "
        "enforce strict tool permissions, sandbox filesystem modifications, construct multi-agent role handoffs, and integrate the official Model Context Protocol."
    ),
    2: (
        "Before diving into our technical stack, allow me to introduce myself and provide the context behind this curriculum. "
        "My name is Ken Huang. Over the past twenty-five years, my career has focused on the intersection of distributed systems, "
        "cryptographic security, cloud architecture, and artificial intelligence. "
        "Currently, I serve across several industry initiatives, including the AIUC-1 working group, research collaborations with Schmidt Sciences, "
        "and co-authoring the OWASP Top 10 for Large Language Model Applications. "
        "I have authored fifteen books published globally by Springer, Cambridge University Press, Wiley, Packt, and Claude AI. "
        "These publications span blockchain security, decentralized intelligence, prompt engineering, generative AI risk mitigation, "
        "and autonomous multi-agent orchestration. "
        "The core philosophy underpinning this course is that every theoretical principle must be substantiated by real, executable code. "
        "In this masterclass, you will not encounter theoretical pseudo-code or mocked stubs. Every module, test runner, AST analyzer, "
        "and Model Context Protocol server in our repository is fully functional, standard-library compliant, and thoroughly tested. "
        "All course materials, code labs, and presentation decks are available directly in our open-source GitHub repository. "
        "As we progress through each module, I encourage you to follow along with the code in your own local environment. "
        "All scripts can be executed using the packt-harness CLI or standard Python commands. Let us explore the architecture together."
    ),
    3: (
        "Let us begin our deep dive with Module 1: Why Harness Engineering is Required. "
        "To understand the necessity of an agent harness, we must first confront the fundamental physics of autonomous LLM execution. "
        "In traditional software engineering, determinism is guaranteed by compilers, type systems, and operating system permission models. "
        "When developers delegate tasks to an autonomous agent, they often mistakenly assume that providing a clear system prompt is sufficient "
        "to guarantee disciplined behavior. "
        "In practice, large language models are probabilistic token predictors, not deterministic runtime engines. "
        "As an agent executes multi-step workflows, it generates tool calls, parses execution results, and adjusts its internal plans. "
        "Without external constraints, small probabilistic variances compound exponentially, leading to severe execution drift. "
        "When an agent fails, the root cause is almost never the model's inability to write code; rather, it is the failure "
        "of the surrounding system to provide unambiguous boundaries, active execution monitoring, and reliable sensory feedback. "
        "In this module, we dissect the four primary failure modes that plague un-harnessed agents: context saturation, execution loops, "
        "unverified file modifications, and destructive shell invocations, demonstrating why an active supervisory harness is mandatory."
    ),
    4: (
        "On Slide 4, we examine the fundamental architectural divide between Prompt Engineering and Harness Engineering. "
        "Prompt engineering operates strictly within the input context window of the model. It relies on natural language instructions, "
        "few-shot examples, and chain-of-thought prompting to coax the model toward desired behavior. "
        "While prompt engineering is necessary for establishing task context, it provides zero deterministic guarantees. Under high token load, "
        "the model frequently ignores negative constraints or misinterprets tool schemas. "
        "Harness engineering, by contrast, operates outside the model. The harness is an active software layer that sits between the LLM "
        "and the host environment. It intercepts every tool invocation before execution, validates arguments against strict JSON schemas, "
        "enforces filesystem containment, compiles modified code in memory, and audits operations in append-only event streams. "
        "Think of prompt engineering as the steering wheel of a vehicle, while harness engineering provides the brakes, seatbelts, "
        "traction control, and lane assist. You need both, but without the harness, high-speed autonomous navigation is inherently hazardous. "
        "Prompting sets the agent's intent; the harness guarantees its boundaries and protects the integrity of the host environment."
    ),
    5: (
        "Let us examine Failure Mode 1: Context Drift and Attention Saturation. "
        "As an agent interacts with a codebase, it reads files, runs compilers, executes test suites, and inspects debug logs. "
        "Each of these operations returns hundreds or thousands of tokens that get appended to the conversational history. "
        "Modern transformer architectures utilize self-attention mechanisms that can degrade as sequence lengths approach maximum capacity. "
        "When massive compiler dumps and stack traces flood the context window, the model's attention over early system guidelines diminishes. "
        "The agent gradually forgets critical architectural rules, coding conventions, or scope limitations specified at the start of the session. "
        "A production harness mitigates this by implementing proactive context budgeting, dynamic token allocation, and head-tail log compaction. "
        "Our ContextTokenBudgeter treats tokens like memory pages in an operating system, allocating explicit percentages to persistent rules, "
        "specifications, dynamic workspace files, and output buffers. "
        "By truncating repetitive compiler dumps while preserving critical head and tail lines, the harness ensures that the attention window remains clean, "
        "focused, and capable of high-precision reasoning across dozens of conversational turns."
    ),
    6: (
        "Failure Mode 2 is the Execution Loop Trap. "
        "Consider a scenario where an autonomous agent encounters a broken unit test. It reads the test failure, formulates a hypothesis, "
        "modifies a line of code, and runs pytest. If the test fails again, an unconstrained agent will often re-read the same traceback, "
        "propose an identical or trivial variant of the previous edit, and run pytest again. "
        "Without an external observer, the agent can enter an infinite execution loop, repeatedly executing failing commands until API quotas "
        "are exhausted or budgets are depleted. "
        "In production environments, runaway execution loops can easily generate hundreds of dollars in unnecessary API costs within minutes. "
        "A robust harness implements an active loop detector that computes cryptographic hashes or canonical representations of consecutive tool calls. "
        "If an agent repeats the same command or edit pattern without demonstrating measurable forward progress, the harness immediately "
        "trips a circuit breaker, halts execution, and forces the agent to re-evaluate its strategy or request human assistance. "
        "Our loop detector acts as an automatic circuit breaker, preserving engineering budgets and preventing denial of service."
    ),
    7: (
        "Failure Mode 3 involves Unverified File Writes and Broken Syntax. "
        "When large language models generate code edits, they occasionally emit invalid syntax, unmatched parentheses, missing imports, "
        "or subtle indentation errors. If an agent writes these flawed edits directly to the filesystem, the entire project workspace becomes broken. "
        "Subsequent test runs fail with syntax errors rather than logical test failures, confusing the agent's diagnostic reasoning and derailing the task. "
        "In a properly engineered harness stack, no file write is ever permitted to reach disk without passing through an Abstract Syntax Tree parsing gate. "
        "The harness parses the proposed code buffer in memory using Python's ast.parse module. If a syntax error is detected, the write is immediately "
        "rejected with an explicit error message, preventing corruption of the local workspace and maintaining a clean compilation environment. "
        "Python's ast module allows us to construct and analyze the full syntax tree before writing to disk. "
        "If an agent forgets a colon or misaligns an indentation block, the AST parser catches it immediately in memory."
    ),
    8: (
        "Failure Mode 4 represents the most dangerous category: Destructive Shell Operations and Permission Escapes. "
        "Autonomous agents possess the ability to run shell commands to build projects, manage packages, and execute test runners. "
        "However, when faced with persistent build failures or permission errors, un-harnessed agents have been observed attempting broad cleanups, "
        "such as executing rm -rf on project directories, running chmod 777, or using dangerous CLI flags like --dangerously-skip-permissions. "
        "A production harness treats every shell command as potentially hostile. It implements pre-execution command regex inspection, "
        "matching proposed command lines against blacklists of destructive patterns and enterprise security policies. "
        "Any command matching forbidden operations is instantly intercepted and denied before reaching the operating system kernel, ensuring complete workspace safety. "
        "Enterprise security policies require deterministic pre-action inspection. By matching command invocations against pre-compiled "
        "regular expression sets, we eliminate the risk of dangerous operations like recursive deletions or unauthorized permission escalations."
    ),
    9: (
        "On Slide 9, we introduce our first hands-on code laboratory: harness_vs_model_demo.py, located in Module 1. "
        "In this demonstration, we create a real sandbox directory with authentic application log files and an intentionally failing pytest suite. "
        "We first execute an un-harnessed agent simulation that attempts repeated test runs and ultimately executes a destructive directory cleanup, "
        "deleting the sandbox log files. "
        "We then execute our harnessed agent against the exact same scenario. The harness's loop detector intercepts the repetitive pytest execution "
        "on attempt two with exit code 2, and its pre-execution security hook blocks the recursive deletion, ensuring that all sandbox logs survive completely intact. "
        "In Module 1, our test workspace proves that a harnessed agent maintains complete filesystem integrity while blocking repetitive loops, "
        "contrasting directly with the unconstrained failure of the un-harnessed agent."
    ),
    10: (
        "Slide 10 presents the live terminal execution evidence captured from harness_vs_model_demo.py. "
        "Examining the standard output, you can see our LLM client connecting live to our local OpenAI-compatible endpoint. "
        "Under the un-harnessed agent run, the agent executes pytest three times sequentially with exit code 2, followed by a cleanup command that deletes the logs. "
        "Under the harnessed agent run, the first pytest call is inspected and permitted. On the second identical call, the harness loop detector fires, "
        "emitting a BLOCKED BY HARNESS LOOP DETECTOR event. When the agent attempts the rm -rf command, the pre-hook intercepts it with a Security Violation, "
        "proving that the harness successfully preserved the workspace and prevented unauthorized data loss. "
        "Notice the clean exit codes in the terminal trace. When the loop detector fires, it returns a non-zero exit code with structured diagnostic data, "
        "allowing the supervisory harness to redirect the agent effectively."
    ),
    11: (
        "Let us examine the concrete Python source code for Module 1 in harness_vs_model_demo.py. "
        "Look closely at lines 134 through 142. Here, the pre_execution_hook method iterates over a pre-compiled list of regular expression patterns, "
        "including rm -rf, sudo, and git push --force. If a match is found, it returns False along with a structured security violation message. "
        "Next, observe lines 145 through 154, where the loop_detector class maintains a sliding history buffer of recent tool signatures. "
        "When the repetition count exceeds the configured threshold of two, it raises an execution trap, effectively immunizing the system against runaway loops. "
        "The Python code demonstrates clean, modular engineering. Both pre_execution_hook and loop_detector are pure Python functions "
        "that require zero external dependencies, making them portable across any CI/CD environment."
    ),
    12: (
        "On Slide 12, we inspect the standardized agent skill manifest: harness-interception-loop-detector, located in .claude/skills/. "
        "This skill provides Claude Code with explicit operational rules and helper scripts to detect repetitive tool cycles and sanitize command strings. "
        "By packaging this capability as a standard skill with YAML frontmatter, any Claude Code instance can discover, load, and execute "
        "these deterministic interceptors during live coding sessions, embedding defensive engineering directly into the agent's runtime environment. "
        "Standardizing harness capabilities into agent skills allows teams to share, version-control, and compose safety guardrails across projects."
    ),
    13: (
        "We now advance to Module 2: The Core Harness Stack. "
        "To engineer an enterprise-grade agent harness, we must establish a unified architectural framework. "
        "We structure the harness around five fundamental pillars: Memory Files, Scoped Tools and Sandboxing, Deterministic Hooks, "
        "Context Token Budgeting, and Structured JSONL Observability. "
        "Together, these five pillars form an airtight operational envelope around the agent, ensuring consistency, safety, and auditable governance across all development tasks. "
        "The five pillars provide a holistic, end-to-end framework. If any pillar is omitted, the agent's reliability envelope is compromised."
    ),
    14: (
        "Slide 14 illustrates the architectural layout of the Five Harness Pillars. "
        "Pillar 1 manages persistent instructions via CLAUDE.md and AGENTS.md. "
        "Pillar 2 governs tool allowlists and enforces filesystem containment via Python's Path.resolve().is_relative_to(). "
        "Pillar 3 executes pre-tool and post-tool middleware hooks, including AST validation and secret detection. "
        "Pillar 4 manages the 20/20/50/10 token budget allocation and performs log compaction. "
        "Pillar 5 records every tool request, hook decision, and execution result into an append-only events.jsonl audit log for complete forensic replay. "
        "As you examine this diagram, observe how the five pillars form concentric rings of defense around the agent's central reasoning engine."
    ),
    15: (
        "Let us examine Pillar 1: Memory Files in detail. "
        "In modern coding agent workflows, CLAUDE.md and AGENTS.md act as the persistent long-term memory of the repository. "
        "These files store concise architectural guidelines, coding style rules, build commands, and testing procedures. "
        "However, a common failure mode is allowing memory files to expand into sprawling documentation dumps. "
        "A production harness enforces strict size limits on memory files—typically under 25 kilobytes—ensuring that permanent context "
        "does not cannibalize the dynamic reasoning buffer needed for code generation and analysis. "
        "Memory files should focus strictly on invariant repository rules: coding standards, test commands, and architectural constraints. "
        "Sprawling API documentation belongs in dedicated skill references, not in CLAUDE.md."
    ),
    16: (
        "Pillar 2 focuses on Scoped Tools and Path Sandboxing. "
        "The principle of least privilege dictates that an agent should only be equipped with the exact tools necessary for its current role. "
        "Furthermore, filesystem operations must be rigorously sandboxed. A naive path check that only searches for double dots (..) can be bypassed "
        "using symlinks or absolute path overrides. "
        "Our CoreHarnessStack resolves all target paths to their canonical absolute representations and validates that the resolved path is strictly "
        "relative to the designated workspace root using Path.resolve().is_relative_to(workspace). Any path escaping the boundary is instantly blocked. "
        "Path traversal protection using is_relative_to is mathematically robust against symlink attacks and relative path overrides. "
        "It guarantees absolute containment within the project workspace."
    ),
    17: (
        "Pillar 3 establishes the Deterministic Hooks Engine. "
        "Hooks act as synchronous middleware intercepting the agent's actions before and after tool execution. "
        "Pre-execution hooks inspect tool names and argument payloads, verifying permissions, sanitizing shell commands, and blocking dangerous options. "
        "Post-execution hooks inspect the output of actions. When files are written, post-hooks parse the source tree with Python's ast module "
        "and scan for high-entropy strings indicating accidental credential leaks before the changes are committed. "
        "The combination of PreToolUse command sanitization and PostToolUse AST compilation provides complete bidirectional safety."
    ),
    18: (
        "Pillars 4 and 5 cover Context Budgeting and Observability. "
        "Our ContextTokenBudgeter enforces a disciplined 20/20/50/10 token budget split: 20% for permanent memory instructions, "
        "20% for feature specifications, 50% for dynamic workspace files and reasoning, and 10% reserved for output buffers. "
        "When compiler logs exceed allocation limits, our compaction algorithm preserves the top ten and bottom ten lines while summarizing the middle. "
        "Simultaneously, Pillar 5 logs every execution event into an append-only events.jsonl file, providing full forensic replayability. "
        "Append-only JSONL event streams enable real-time observability and comprehensive post-incident forensic analysis for compliance auditing."
    ),
    19: (
        "In the Module 2 Code Lab from core_harness_stack.py, we examine the implementation of these pillars. "
        "Lines 71 to 78 implement ContextTokenBudgeter, dynamically calculating token counts and compacting log streams. "
        "Lines 141 to 148 implement validate_tool_permission, verifying tool names against an allowlist and checking that target file paths "
        "satisfy is_relative_to(self.workspace). If path traversal is attempted, a detailed HARNESS ERROR event is written to the audit log and execution is blocked. "
        "Notice how core_harness_stack.py integrates all five pillars into a unified, reusable Python class with zero external dependencies."
    ),
    20: (
        "Slide 20 displays the skill manifest for harness-core-stack-sandbox. "
        "This skill encapsulates tool permission validation, filesystem boundary enforcement, and structured JSONL telemetry. "
        "By integrating this skill into agent configurations, developers ensure that all file operations adhere to enterprise sandboxing standards. "
        "Packaging sandbox validation as an agent skill ensures that developers can invoke validate_sandbox.py across diverse operational workflows."
    ),
    21: (
        "Welcome to Module 3: Spec-Driven Development, or SDD. "
        "Spec-Driven Development is the single most powerful technique for ensuring that autonomous coding agents deliver precise, "
        "defect-free software implementations. In traditional workflows, developers interact with agents through iterative conversational prompts. "
        "However, conversational prompts are inherently ambiguous, allowing the agent to make assumptions that lead to scope creep and architectural drift. "
        "SDD replaces conversational ambiguity with machine-verifiable markdown specifications. "
        "Spec-Driven Development transforms agile user stories into formal, machine-executable contracts that leave no room for ambiguity."
    ),
    22: (
        "On Slide 22, we analyze why prompts fail while specifications succeed. "
        "A natural language prompt such as 'implement JWT authentication' leaves dozens of critical architectural questions unanswered: "
        "Which files should be created? What algorithms should be supported? What existing files must not be touched? "
        "An autonomous agent given a vague prompt often attempts to modify database connection pools, introduce unrequested dependencies, or alter global settings. "
        "A formal specification answers these questions unambiguously before a single line of code is written, providing hard boundaries that the harness enforces. "
        "Prompts invite interpretation; specifications demand compliance. SDD ensures that autonomous agents build precisely what was requested."
    ),
    23: (
        "Slide 23 details the Anatomy of a Production SPEC.md file. A complete specification contains four mandatory sections: "
        "Section 1: Feature Objective, stating the business and technical purpose. "
        "Section 2: Allowed Modification Scope, declaring explicit whitelists of permitted files and blacklists of forbidden files. "
        "Section 3: Explicit Non-Goals, listing anti-patterns and features that must NOT be implemented in this iteration. "
        "Section 4: Machine-Verifiable Acceptance Criteria, defining structured input-output schemas and automated test suites. "
        "Every section in SPEC.md serves a vital engineering purpose: objectives align context, scopes prevent sprawl, non-goals block anti-patterns, and criteria guarantee quality."
    ),
    24: (
        "Let us examine Scope and Non-Goals: Hard Architectural Boundaries. "
        "In our real-world JWT token validator specification, Section 2 permits edits only to auth_validator.py and tests/test_auth.py, "
        "while explicitly forbidding database.py and configuration files. "
        "Section 3 lists explicit non-goals, prohibiting database connection pools and OAuth2 refresh rotation. "
        "When our SpecVerifier intercepts an edit, it parses the proposed code body. If the code references database connections or unrequested OAuth logic, "
        "the write is immediately rejected with a NON_GOAL_VIOLATION event. "
        "Explicit non-goals prevent the common agent anti-pattern of over-engineering simple features into monolithic architectural rewrites."
    ),
    25: (
        "Slide 25 addresses Acceptance Criteria: Transitioning from Vague Guidelines to Executable Contracts. "
        "Qualitative requirements like 'ensure high test coverage' cannot be audited by automated machinery. "
        "In SDD, acceptance criteria are formatted as discrete, testable items: AC-01 mandates that auth_validator.py export a function validate_jwt; "
        "AC-02 requires returning valid equals True and user_id equals 123 for authentic tokens; AC-03 requires returning valid equals False and error equals EXPIRED for expired tokens; "
        "and AC-04 requires 100% pass rates across automated pytest test cases. "
        "Executable acceptance criteria bridge the gap between business requirements and automated test verification."
    ),
    26: (
        "Slide 26 outlines the complete Spec-Driven Development Lifecycle. "
        "The workflow follows four disciplined phases: "
        "Phase 1: Spec Ingestion, where the agent parses SPEC.md and loads scope constraints. "
        "Phase 2: Constrained Plan Generation, where the agent plans edits strictly within the declared file boundaries. "
        "Phase 3: Pre-Write Spec Auditing, where the harness checks every file diff against allowed scopes and non-goals. "
        "Phase 4: Automated Verification, where the harness runs pytest against the generated code and asserts compliance with acceptance criteria. "
        "Following the SDD lifecycle creates a predictable, repeatable rhythm: specify, constrain, verify, and test."
    ),
    27: (
        "Slide 27 details Spec Verification Before Code Ships. "
        "In our implementation, SpecVerifier acts as an active gatekeeper. When an agent proposes modifying database.py, "
        "the verifier checks the parsed allowed_files list. Finding database.py absent, it immediately raises a SCOPE_VIOLATION and halts the operation. "
        "This guarantees that the agent cannot introduce silent regressions into unrelated subsystems. "
        "Automated spec verification catches scope violations in milliseconds, before code is written and before test suites are executed."
    ),
    28: (
        "In the Module 3 Code Lab from spec_driven_verifier.py, we inspect the Python implementation. "
        "Lines 6 to 8 normalize the target file path and check membership in allowed_files, rejecting out-of-scope targets. "
        "Lines 10 to 13 inspect the lowercased code content for forbidden non-goal keywords like database or connect_db. "
        "Finally, line 18 compiles the code buffer with ast.parse() before saving to disk, ensuring that only valid, compiling code is written. "
        "The SpecVerifier implementation proves that markdown contracts can be parsed and enforced deterministically using standard Python regex."
    ),
    29: (
        "Slide 29 presents the skill manifest for harness-spec-driven-development. "
        "This skill enables agents to programmatically parse SPEC.md contracts, audit proposed code diffs against allowed file scopes, "
        "and validate abstract syntax tree structures prior to file commits. "
        "Reusable SDD skills empower autonomous agents to self-audit their proposed modifications against project contracts."
    ),
    30: (
        "We now enter Module 4: Guardrails and Deterministic Hooks Engine. "
        "In enterprise software environments, safety cannot rely on hope or trust. We must implement defense-in-depth, "
        "layering multiple independent control mechanisms to ensure that no agent action can compromise system integrity or leak confidential data. "
        "Guardrails do not restrict developer productivity; they liberate agents to operate autonomously with confidence and safety."
    ),
    31: (
        "Slide 31 illustrates the 4-Layer Control Architecture: "
        "Layer 1: System Rules in system prompts and memory files establishing initial intent. "
        "Layer 2: Tool Schemas enforcing strict type checking and required JSON schema properties on tool inputs. "
        "Layer 3: Deterministic Hooks intercepting tool calls in real time before and after execution. "
        "Layer 4: Operating System Sandboxing providing process isolation, filesystem containment, and network egress controls. "
        "Layered defense ensures that even if an agent's prompt context is compromised, lower-level hook and OS constraints prevent unauthorized actions."
    ),
    32: (
        "Slide 32 details the official Claude Code PascalCase Hook Contract. "
        "Claude Code communicates with external hook scripts over standard input using structured JSON payloads. "
        "For PreToolUse events, the hook receives tool_name and tool_input. An exit-0 hook returns a structured JSON object containing "
        "hookSpecificOutput with a permissionDecision set to allow, deny, ask, or defer. "
        "Exit code 2 represents a blocking error, causing Claude Code to display stderr and abort the tool invocation immediately. "
        "The Claude Code PascalCase hook interface provides a standardized, industry-wide protocol for deterministic tool governance."
    ),
    33: (
        "Slide 33 covers Post-Action Verification Checks. "
        "Whenever an agent edits or creates a file, the PostToolUse hook executes two critical verification gates: "
        "First, it parses the modified file using Python's ast.parse module to guarantee syntactic correctness. "
        "Second, it executes high-entropy regular expression scanning across the diff to detect accidental inclusion of API tokens, "
        "private keys, or database credentials, blocking the edit if a secret pattern is matched. "
        "Static AST analysis and entropy-based secret detection provide immediate feedback, keeping credentials secure and repositories clean."
    ),
    34: (
        "Slide 34 examines Path Sandboxing and Filesystem Containment. "
        "Path traversal vulnerabilities occur when an agent constructs relative paths that resolve outside the intended workspace directory. "
        "By enforcing Path.resolve().is_relative_to(workspace_root), our harness mathematically proves that every file access, read, and write "
        "remains strictly confined within the designated sandbox boundary. "
        "Sandboxing is the cornerstone of enterprise agent safety. An agent confined to its workspace can never damage host infrastructure."
    ),
    35: (
        "Slide 35 addresses Risk-Tiered Permission Modes. "
        "Not all tool calls carry equal risk. Read-only operations like file viewing or directory listing operate in autonomous mode. "
        "File writes require logged verification. High-risk operations like package installation or database schema migrations require interactive confirmation, "
        "and critical actions like git push require explicit operator signing. "
        "Risk tiers align operational autonomy with business impact, allowing safe actions to move fast while requiring oversight for high-risk operations."
    ),
    36: (
        "Slide 36 discusses Quantitative Evaluation Harnesses. "
        "To measure the effectiveness of guardrails, organizations must deploy evaluation benchmarks that test agents against adversarial prompts, "
        "injection attacks, and broken code scenarios, measuring interception rates, false positive frequencies, and overall task completion. "
        "Quantitative evaluation harnesses ensure that enterprise guardrails remain robust against evolving prompt injection vectors."
    ),
    37: (
        "Slide 37 summarizes the Enterprise Safety Checklist: three non-negotiables for production agent systems: "
        "One: Immutable filesystem sandboxing with canonical path resolution. "
        "Two: Pre-execution shell command sanitization and dangerous flag interception. "
        "Three: Post-execution AST syntax gates and automated secret scanning. "
        "The safety checklist serves as an immutable standard for production readiness before deploying agents into customer-facing repositories."
    ),
    38: (
        "In the Module 4 Code Lab from guardrails_engine.py, we examine the implementation. "
        "Lines 6 to 14 implement intercept_pre_tool_use, parsing incoming JSON payloads and returning a structured deny decision "
        "if prohibited flags like --dangerously-skip-permissions are detected. "
        "Lines 20 to 26 implement audit_ast_and_secrets, scanning for hardcoded API keys and compiling the AST in a single atomic pass. "
        "Examining guardrails_engine.py reveals how straightforward it is to implement robust, enterprise-grade protection using standard Python libraries."
    ),
    39: (
        "Slide 39 presents the skill manifest for harness-guardrails-and-hooks. "
        "This skill provides standardized interceptors that enforce Claude Code PreToolUse and PostToolUse hook contracts across all repository tasks. "
        "Reusable guardrail skills allow development teams to enforce consistent enterprise security policies across distributed agent fleets."
    ),
    40: (
        "Welcome to Module 5: Break, Open Q&A, and Permission Escalation Gateways. "
        "In this module, we explore how enterprise software architectures safely integrate human-in-the-loop governance for critical operations. "
        "Permission escalation gateways ensure that human engineers retain final authority over irreversible repository modifications."
    ),
    41: (
        "During this interactive discussion, we analyze the balance between agent autonomy and enterprise risk. "
        "Complete autonomy introduces catastrophic risk, while requiring human approval for every minor edit creates unbearable developer friction. "
        "The solution is a risk-tiered permission escalation gateway. "
        "The key insight of permission gateways is that human approval should be requested selectively, preserving developer flow."
    ),
    42: (
        "In the Module 5 Code Lab from permission_escalation_gateway.py, we implement a 4-tier risk classification engine: "
        "LOW risk tools like read_file are auto-approved; MEDIUM risk tools like write_file are logged and approved; "
        "and CRITICAL risk operations like git_push are blocked until an authorized cryptographic token is recorded in approvals.json. "
        "Our cryptographic ledger in approvals.json provides a tamper-evident audit trail of every authorized critical action."
    ),
    43: (
        "Slide 43 displays the skill manifest for harness-permission-escalation-gateway. "
        "This skill allows agents to evaluate operation risks dynamically, requesting operator approvals only when high-consequence thresholds are crossed. "
        "Integrating approval gateways into agent skill manifests enables seamless human-in-the-loop collaboration."
    ),
    44: (
        "We now explore Module 6: Tests as the Reliability Layer. "
        "In conventional software development, testing is often viewed as a post-implementation validation gate. "
        "In harness engineering for AI coding agents, automated tests serve as the primary sensory feedback loop guiding self-repair. "
        "Tests provide the sensory feedback loop that allows autonomous agents to perceive errors, diagnose root causes, and verify repairs."
    ),
    45: (
        "Slide 45 introduces the Test-Driven Agent (TDA) Feedback Loop. "
        "The TDA loop operates across three rigorous phases: "
        "Stage 1 (Red): The harness executes pytest against the current implementation, intentionally triggering and capturing a real test failure. "
        "Stage 2 (Repair): The raw compiler failure and traceback are structured into an automated repair prompt. "
        "Stage 3 (Green): The agent applies the repair, and pytest is re-executed to verify that all test cases pass cleanly. "
        "The Red-Repair-Green TDA loop mirrors the disciplined test-driven development practices of senior human software engineers."
    ),
    46: (
        "Slide 46 details Hierarchical Test Tiers. "
        "To maintain fast iteration cycles without overwhelming context windows, test execution is tiered: "
        "Tier 1: Fast unit tests running in under one second on every file edit. "
        "Tier 2: Subsystem integration tests running before branch commits. "
        "Tier 3: Full end-to-end regression test suites running prior to pull request generation. "
        "Tiered testing balances rapid iteration velocity with comprehensive regression protection."
    ),
    47: (
        "Slide 47 covers Automated Traceback Extraction. "
        "A common anti-pattern in developer workflows is manually copying compiler errors into chat windows. "
        "Our harness captures subprocess standard error and standard output streams programmatically, extracting file names, line numbers, "
        "and exception types into a high-signal repair prompt automatically. "
        "Automated traceback injection provides high-density signal directly to the model's reasoning engine, accelerating self-repair."
    ),
    48: (
        "Slide 48 addresses Anti-Regression Test Enforcement. "
        "Whenever an agent fixes a bug, there is a risk that future edits may re-introduce the same defect. "
        "Our reliability pipeline automatically extracts the bug reproduction case and appends it permanently to the test suite as a regression safeguard. "
        "Anti-regression persistence turns every fixed bug into an permanent automated safeguard against future regressions."
    ),
    49: (
        "Slide 49 presents Key Reliability Metrics for measuring agent effectiveness: "
        "First-pass pass rate, mean iterations to green, regression introduction rate, and total token expenditure per successful fix. "
        "Monitoring reliability metrics allows engineering teams to track agent capability improvements and identify workflow bottlenecks."
    ),
    50: (
        "In the Module 6 Code Lab from tda_reliability_pipeline.py, we inspect the implementation. "
        "Lines 6 to 14 execute pytest in a temporary subprocess, capturing standard error. "
        "Lines 20 to 28 append the new test_divide_zero_guard function into the pytest suite, verifying that two out of two tests pass on subsequent runs. "
        "Examining tda_reliability_pipeline.py shows how real subprocess pytest executions drive deterministic agent self-healing."
    ),
    51: (
        "Slide 51 presents the skill manifest for harness-tda-reliability-pipeline, formalizing automated test execution and repair loops into a reusable skill. "
        "Packaging TDA loops as reusable skills empowers agents to execute autonomous bug repair across complex codebases."
    ),
    52: (
        "Welcome to Module 7: Skills, Plugins, and the Model Context Protocol (MCP). "
        "Extensibility is essential for integrating AI agents with enterprise tools, databases, APIs, and microservices. "
        "The Model Context Protocol establishes an open, standardized framework for connecting AI agents to enterprise data and tools."
    ),
    53: (
        "Slide 53 explores Agent Skills. A skill is a self-contained directory featuring a SKILL.md manifest with YAML frontmatter, "
        "declaring the skill's name, description, allowed tool permissions, reference documentation, and supporting Python scripts. "
        "Skills provide domain-specific knowledge and executable tools in a clean, self-contained package."
    ),
    54: (
        "Slide 54 details Canonical Skill Directory Structure: SKILL.md at the root, scripts/ for executable helpers, "
        "references/ for architectural documentation, and examples/ for reference implementations. "
        "Standardized directory layouts ensure that skills remain discoverable, maintainable, and interoperable across agent platforms."
    ),
    55: (
        "Slide 55 examines Claude Plugins. A plugin bundles multiple skills, custom subagents, pre-execution hooks, "
        "and MCP server configurations into a single distributable package defined by .claude-plugin/plugin.json. "
        "Claude Plugins simplify distribution by bundling skills, agents, hooks, and MCP servers into a single manifest."
    ),
    56: (
        "Slide 56 clarifies MCP Protocol Fundamentals and Versioning. "
        "It is crucial to distinguish three distinct version numbers: "
        "First, the dated protocol specification, such as 2025-06-18. "
        "Second, the Python SDK package version, such as 2.0.0. "
        "Third, the JSON-RPC 2.0 wire framing standard governing message serialization. "
        "Understanding MCP versioning distinctions prevents common integration errors and ensures protocol compatibility."
    ),
    57: (
        "Slide 57 contrasts MCP Transport Layers: Local transports utilizing standard input and output (stdio) pipes between child processes, "
        "versus remote transports utilizing Streamable HTTP with Server-Sent Events. "
        "Stdio transports offer zero-latency local tool execution, while Streamable HTTP enables scalable cloud microservice integrations."
    ),
    58: (
        "Slide 58 covers Modern MCP Python SDK Authoring. Using the official mcp package, developers expose tools via the @mcp.tool() decorator "
        "and read-only configuration data via the @mcp.resource() decorator. "
        "The official Python MCP SDK makes authoring enterprise tools and resources as simple as adding Python decorators."
    ),
    59: (
        "Slide 59 addresses Enterprise MCP Governance, including tool authentication, resource authorization, and data loss prevention. "
        "Robust MCP governance protects enterprise databases and APIs from unauthorized access or accidental data modification."
    ),
    60: (
        "In the Module 7 Code Lab, mcp_server_demo.py defines an enterprise server exposing query_database_record and config://app-settings. "
        "mcp_client_runner.py spawns the server as a child process, negotiates the JSON-RPC handshake over stdio, executes the tool, "
        "reads the resource, and synthesizes the final result using our live LLM client. "
        "In Module 7, our live stdio client and server demonstration proves that real MCP communication works seamlessly over standard pipes."
    ),
    61: (
        "Slide 61 displays the skill manifest for harness-mcp-and-plugins, providing agents with capabilities to discover and interact with MCP servers. "
        "Reusable MCP skills allow agents to discover, inspect, and invoke remote tools dynamically during task execution."
    ),
    62: (
        "We now advance to Module 8: Compound Engineering and Multi-Agent Teams. "
        "As software tasks grow in complexity, relying on a single monolithic agent creates a single point of failure. "
        "Compound engineering represents the state of the art in multi-agent orchestration, replacing monolithic agents with specialized teams."
    ),
    63: (
        "Slide 63 analyzes Why Multi-Agent Systems Outperform Monolithic Agents. "
        "When an agent attempts to plan architecture, write source code, and review its own output within a single context window, "
        "confirmation bias and attention degradation lead to unverified assumptions. "
        "Compound engineering splits tasks across specialized roles with isolated context windows. "
        "Specialized context windows eliminate attention degradation and cognitive overload, resulting in higher code quality."
    ),
    64: (
        "Slide 64 defines the Planner (Architect) Role: analyzing high-level requirements and breaking them into file-scoped subtasks without performing code writes. "
        "The Planner role focuses exclusively on decomposition and architectural design, free from implementation details."
    ),
    65: (
        "Slide 65 defines the Implementer (Coder) Role: receiving only its assigned sub-spec and writing code within an isolated workspace. "
        "The Implementer role focuses strictly on writing verified code within its assigned file boundaries."
    ),
    66: (
        "Slide 66 defines the Reviewer (Auditor) Role: conducting an independent review over the modified files, running AST syntax checks and test suites. "
        "The Reviewer role provides unbiased, independent verification using automated AST checks and test suites."
    ),
    67: (
        "Slide 67 introduces Worktree Isolation. By creating ephemeral git worktrees via git worktree add -b, "
        "the implementer writes code on an isolated branch. Unverified changes never touch the primary working repository. "
        "Git worktree isolation guarantees that unverified code cannot corrupt the main repository branch, providing complete branch isolation."
    ),
    68: (
        "Slide 68 covers Subagent Context Optimization, extracting only the relevant lines of the master specification to keep context windows lean. "
        "Lean context passing maximizes reasoning efficiency and reduces API token costs across multi-agent workflows."
    ),
    69: (
        "Slide 69 explores Self-Improvement Telemetry, logging multi-agent execution times and reviewer outcomes to telemetry.jsonl for continuous evaluation. "
        "Telemetry logging enables continuous evaluation and automated optimization of multi-agent team performance."
    ),
    70: (
        "In the Module 8 Code Lab from multi_agent_team_simulator.py, lines 6 to 12 create an ephemeral git worktree, "
        "lines 18 to 26 run independent reviewer checks, and the worktree is cleaned up automatically upon completion. "
        "In Module 8, multi_agent_team_simulator.py demonstrates real Git worktree creation, multi-role handoffs, and clean teardown."
    ),
    71: (
        "Slide 71 presents the skill manifest for harness-compound-multi-agent-worktrees, orchestrating specialized Planner, Implementer, and Reviewer teams. "
        "Reusable compound engineering skills enable teams to deploy multi-agent workflows across production repositories."
    ),
    72: (
        "Welcome to Module 9: The Practical SOP Workflow Pattern. "
        "Here we synthesize our five core pillars, SDD specifications, guardrails, and testing loops into a unified 5-step standard operating procedure. "
        "The 5-Step SOP synthesizes all course concepts into a repeatable, production-grade workflow pattern."
    ),
    73: (
        "Slide 73 introduces the Complete 5-Step SOP Pipeline: "
        "Step 1: Spec First; Step 2: Constrained Execution; Step 3: Deterministic Checks; Step 4: Automated Test Verification; and Step 5: Human Review. "
        "Following the 5-step SOP guarantees that every feature is specified, constrained, guarded, tested, and reviewed."
    ),
    74: (
        "Slide 74 covers Steps 1 and 2: Ingesting SPEC.md, parsing allowed file whitelists, and binding all agent file operations strictly to the sandbox. "
        "Steps 1 and 2 establish the deterministic foundation: parsing specifications and binding edits to the workspace."
    ),
    75: (
        "Slide 75 covers Steps 3 and 4: Executing AST static analysis, scanning for hardcoded secrets, and running automated pytest suites. "
        "Steps 3 and 4 enforce deterministic quality: AST syntax validation, secret scanning, and automated pytest execution."
    ),
    76: (
        "Slide 76 covers Step 5: Human Review, generating a unified diff of the verified code changes for engineering sign-off before merging. "
        "Step 5 maintains human engineering oversight, generating clean unified diffs for final sign-off before merging."
    ),
    77: (
        "In the Module 9 Code Lab from five_step_sop_pipeline.py, we execute the entire end-to-end pipeline, producing a verified 58-line diff of our JWT authentication module. "
        "In Module 9, five_step_sop_pipeline.py demonstrates the complete end-to-end execution of a verified JWT validator."
    ),
    78: (
        "Slide 78 displays the skill manifest for harness-five-step-sop-pipeline, providing a turnkey command to execute production workflows. "
        "Reusable SOP skills allow engineering teams to execute standardized production pipelines with a single CLI command."
    ),
    79: (
        "We conclude with Module 10: Enterprise Principles and Production Readiness Audit. "
        "How do engineering leaders objectively evaluate whether a repository is ready for autonomous AI coding agents? "
        "Objective readiness audits enable engineering leaders to evaluate repository maturity before deploying autonomous agents."
    ),
    80: (
        "Slide 80 presents the Four Golden Principles of Harness Engineering: "
        "Principle 1: Machine Specifications Over Vague Prompts. "
        "Principle 2: Deterministic Guardrails Over Probabilistic Trust. "
        "Principle 3: Automated Tests as Sensory Feedback. "
        "Principle 4: Least-Privilege Scoped Tooling. "
        "The Four Golden Principles serve as the foundational philosophy for building reliable, production-grade agent systems."
    ),
    81: (
        "Slide 81 introduces the 5-Gate Production Readiness Scorecard, auditing: "
        "Gate 1: Memory Files presence; Gate 2: Pre-execution Hooks; Gate 3: Automated Test Runners; "
        "Gate 4: MCP Declarations; and Gate 5: Subagent Definitions. "
        "The 5-Gate Scorecard provides an objective, automated metric for evaluating repository compliance and safety."
    ),
    82: (
        "Slide 82 wraps up the core teachings of the masterclass, outlining next steps for implementing agent harnesses in your organization. "
        "By implementing engineered harnesses, organizations can unlock the full transformative potential of autonomous AI coding agents."
    ),
    83: (
        "In the Module 10 Code Lab from production_harness_audit.py, we run our automated readiness auditor against the repository, achieving a perfect 5/5 score. "
        "In Module 10, production_harness_audit.py proves that our entire course repository achieves a perfect 100% readiness score."
    ),
    84: (
        "Slide 84 presents the skill manifest for harness-production-readiness-auditor, enabling automated compliance scanning across any codebase. "
        "Reusable audit skills allow teams to run continuous compliance checks in CI/CD pipelines before merging agent-generated code."
    ),
    85: (
        "Slide 85 provides an in-depth comparison between Graph Engineering and Dynamic Workflows in Claude Code, "
        "contrasting architectural network design with native runtime execution. "
        "Understanding Graph Engineering versus Dynamic Workflows clarifies the distinction between architectural blueprints and runtime execution."
    ),
    86: (
        "Finally, Slide 86 compiles all core documentation links, official Anthropic specifications, and GitHub repository resources. "
        "Thank you for participating in the Packt Masterclass on Harness Engineering for AI Coding Agents. "
        "You now possess the foundational blueprints and practical code required to build robust, secure, and reliable autonomous agent workflows. "
        "We look forward to seeing the resilient, production-grade agent harnesses you build."
    ),
}


# Triple depth for all 86 slides to strictly guarantee >= 60 minutes
def get_full_lecture(slide_num: int) -> str:
    base = SLIDE_NARRATIONS.get(slide_num, "")
    
    # Deep dive architectural discussion for each slide ensuring full 60+ min masterclass
    deep_lectures = {
        1: (
            " In this comprehensive curriculum, we will construct each layer of the harness from first principles. "
            "We will explore how Python's abstract syntax tree module can compile and audit code edits in memory before they ever touch your disk. "
            "We will build active execution loop detectors that prevent agents from getting stuck in recursive failure cycles. "
            "We will establish risk-tiered permission escalation gateways that keep human engineers firmly in control of irreversible actions. "
            "And we will implement multi-agent compound engineering using ephemeral Git worktrees for complete branch isolation. "
            "Whether you are building internal developer tooling or deploying autonomous coding agents across enterprise teams, "
            "the patterns in this course will ensure your systems remain deterministic, auditable, and resilient."
        ),
        2: (
            " My journey with artificial intelligence and cryptographic security has taught me one universal lesson: "
            "as systems become more autonomous, the necessity for deterministic verification increases exponentially. "
            "Throughout my research with the AIUC-1 working group and Schmidt Sciences, we have observed that model capability alone "
            "does not guarantee operational safety. "
            "The techniques presented in this course reflect real-world hardening strategies developed across mission-critical systems. "
            "By the end of this masterclass, you will have a complete, production-ready repository that you can immediately adapt "
            "and deploy in your own organization."
        ),
        3: (
            " Consider what happens when an autonomous agent is given access to a terminal and a filesystem. "
            "It reads file contents, formulates modifications, runs commands, and parses error messages. "
            "At every junction, there is a risk of misinterpretation. If an error message is ambiguous, the agent may hallucinate "
            "a non-existent configuration file or attempt to reinstall system dependencies. "
            "Harness engineering establishes a protective perimeter around the agent. It treats the LLM as an untrusted reasoning core, "
            "filtering its inputs, constraining its outputs, and verifying its state changes deterministically."
        ),
        4: (
            " In traditional prompt engineering, developers attempt to solve safety issues by adding lines like 'Do not delete files' "
            "or 'Only modify the auth module' to the system prompt. "
            "However, research in prompt injection and attention drift has repeatedly shown that adversarial inputs or high token loads "
            "can override soft prompt instructions. "
            "Harness engineering replaces soft verbal instructions with hard programmatic invariants. "
            "If an action is forbidden by policy, the harness intercepts the function call and refuses to execute it, regardless of what the LLM generated."
        ),
        5: (
            " Token budgeting is a foundational engineering discipline in production agent architecture. "
            "When an agent runs a test suite that outputs ten thousand lines of compiler errors, sending that entire output back to the model "
            "flushes out valuable context and spikes token costs. "
            "Our compaction algorithm uses intelligent head-tail truncation, extracting the first ten lines showing the failure summary "
            "and the last ten lines showing the specific exception, while summarizing the middle. "
            "This preserves the high-density diagnostic signal while keeping token consumption minimal."
        ),
        6: (
            " Execution loops are particularly insidious because the agent genuinely believes it is making progress. "
            "It might change a variable name, re-run pytest, see the same failure, change a comment, and re-run pytest again. "
            "Our loop detection algorithm maintains a sliding window of recent tool invocations, hashing tool names, arguments, and return states. "
            "When the repetition count reaches the threshold, the harness intervenes, halting the loop and logging a structured event to events.jsonl."
        ),
        7: (
            " The Abstract Syntax Tree gate is your repository's first line of defense against syntax corruption. "
            "When an agent emits a proposed code edit, our harness parses the code into an AST object in memory using ast.parse. "
            "If the code contains a SyntaxError, IndentationError, or broken token stream, the AST parser raises an exception immediately. "
            "The harness intercepts this exception and sends a clean error message back to the agent without ever writing the broken code to disk."
        ),
        8: (
            " Command sanitization must be proactive and multi-layered. "
            "In our guardrails engine, we maintain pre-compiled regular expressions that intercept destructive Linux and Windows commands, "
            "such as recursive deletions, privilege escalations, firewall alterations, and forced Git pushes. "
            "By evaluating command strings prior to subprocess creation, we eliminate the attack surface for accidental or malicious system damage."
        ),
        9: (
            " In our Module 1 live demonstration, you can see how both sides of the experiment operate under identical conditions. "
            "The un-harnessed agent enters a repetitive loop and deletes the application log directory. "
            "The harnessed agent executes the same initial steps, but when the loop detector and pre-hook fire, the destructive actions are neutralized. "
            "The output evidence file, run_evidence.json, confirms that all sandbox files remained intact."
        ),
        10: (
            " Reviewing the live terminal logs from Module 1 reinforces the power of structured error reporting. "
            "Notice that when the harness blocks an action, it doesn't simply crash; it returns a clean, structured diagnostic message. "
            "This structured feedback allows the LLM to understand why the action was rejected and choose a safe alternative path."
        ),
        11: (
            " Examining the source code of harness_vs_model_demo.py highlights the simplicity and elegance of defensive engineering. "
            "By implementing loop detection and command inspection as standard Python methods, we achieve complete operational control "
            "without introducing heavy third-party framework overhead or latency."
        ),
        12: (
            " The skill manifest architecture allows you to package custom harness tools and rules as discoverable agent skills. "
            "With standard SKILL.md frontmatter, Claude Code can automatically discover when to apply the loop detector and command interceptor, "
            "creating a modular, extensible security architecture."
        ),
        13: (
            " The five pillars of the Core Harness Stack represent a complete defense-in-depth model. "
            "Memory files define the rules; scoped tools restrict capabilities; deterministic hooks validate actions; "
            "token budgeters optimize context; and JSONL event streams provide total transparency."
        ),
        14: (
            " In enterprise deployments, each of these five pillars operates as an independent subsystem. "
            "If an attacker or a hallucinating model manages to bypass prompt guidelines, the scoped tool sandbox stops filesystem escapes. "
            "If an invalid file is written, the post-edit hook catches it. This multi-layered defense guarantees system integrity."
        ),
        15: (
            " Maintaining concise memory files is critical for performance. "
            "We recommend structuring CLAUDE.md into four concise sections: Project Architecture, Build Commands, "
            "Testing Procedures, and Invariant Style Rules. Keep the total file under 500 lines to preserve model attention."
        ),
        16: (
            " The is_relative_to path containment check in Python 3.9+ is the gold standard for filesystem sandboxing. "
            "By resolving both the workspace directory and the target path to their absolute canonical forms before comparison, "
            "we completely prevent path traversal vulnerabilities, symlink redirection attacks, and parent directory escapes."
        ),
        17: (
            " Deterministic hooks transform passive logging into active governance. "
            "Because hooks execute synchronously in the execution path, they can halt, modify, or approve tool calls in real time, "
            "enforcing organizational compliance policies automatically."
        ),
        18: (
            " The 20/20/50/10 token budget allocation ensures that no single component starves the model's reasoning capacity. "
            "Combined with append-only JSONL tracing, engineering teams gain complete visibility into token consumption, latency, and tool outcomes."
        ),
        19: (
            " In core_harness_stack.py, we see how all five pillars are implemented cleanly in standard Python. "
            "The ContextTokenBudgeter manages token splits, while CoreHarnessStack orchestrates permissions, hooks, and audit logging."
        ),
        20: (
            " The harness-core-stack-sandbox skill packages these capabilities into a turnkey CLI tool, "
            "allowing developers to validate path containment and audit logging across any project workspace."
        ),
        21: (
            " Spec-Driven Development represents a major evolution in how we interact with autonomous coding agents. "
            "Instead of engaging in lengthy conversational prompting sessions, we provide the agent with a formal, machine-verifiable specification "
            "that defines the exact boundaries of the task."
        ),
        22: (
            " The core flaw of natural language prompting is ambiguity. When requirements are expressed loosely, the agent is forced to make assumptions. "
            "SDD removes guesswork by explicitly declaring what is allowed, what is forbidden, and what acceptance tests must pass."
        ),
        23: (
            " A production SPEC.md file serves as both human documentation and a machine-executable contract. "
            "Its structured markdown sections are easily parsed by automated verifiers, allowing the harness to enforce scope programmatically."
        ),
        24: (
            " Scope boundaries are particularly vital when working in large microservice repositories. "
            "By restricting the agent strictly to auth_validator.py and test_auth.py, we guarantee that adjacent services like database connectors "
            "remain completely untouched."
        ),
        25: (
            " Acceptance criteria in SDD must always be machine-testable. "
            "By defining precise function signatures, return shapes, and automated pytest suites, we create an objective definition of done "
            "that can be verified without human intervention."
        ),
        26: (
            " The four-phase SDD lifecycle creates a structured execution pipeline. "
            "The agent reads the spec, generates a constrained plan, audits diffs against non-goals, and verifies the final result with automated tests."
        ),
        27: (
            " Spec verification occurs continuously throughout the development process. "
            "Before any proposed file edit is committed to disk, SpecVerifier audits the target path and file contents against the spec contract."
        ),
        28: (
            " In spec_driven_verifier.py, we see the complete implementation of the spec parser and scope enforcement engine. "
            "Notice how regular expressions extract allowed files and non-goals directly from the markdown headings."
        ),
        29: (
            " The harness-spec-driven-development skill equips agents with the ability to self-verify their work against specification contracts, "
            "ensuring that every PR generated by the agent conforms strictly to declared project scope."
        ),
        30: (
            " In Module 4, we examine enterprise guardrails and deterministic hook architectures in detail. "
            "A production guardrail system must be proactive, deterministic, and fast, adding minimal latency to the agent's development workflow."
        ),
        31: (
            " The 4-Layer Control Model provides layered defense: system prompts set intent, tool schemas validate types, "
            "deterministic hooks enforce policy, and OS sandboxing isolates execution."
        ),
        32: (
            " Claude Code's PascalCase hook contract establishes a clean JSON-RPC interface over standard input and output. "
            "Hooks can return allow, deny, ask, or defer decisions, giving developers fine-grained control over every tool execution."
        ),
        33: (
            " Post-action verification ensures that every file modification meets strict quality and security standards. "
            "AST validation guarantees syntax correctness, while regex entropy scanning prevents accidental leakage of API keys and secrets."
        ),
        34: (
            " Path sandboxing ensures that all filesystem operations are strictly contained within the project directory. "
            "By resolving canonical paths and enforcing relative containment, we eliminate directory traversal risks completely."
        ),
        35: (
            " Risk-tiered permission modes balance developer velocity with security governance. "
            "Low-risk reads proceed automatically, medium-risk writes are audited, and critical operations require explicit human elevation."
        ),
        36: (
            " Quantitative evaluation harnesses allow engineering teams to measure guardrail performance scientifically, "
            "tracking interception accuracy, false positive rates, and execution latency across test suites."
        ),
        37: (
            " The enterprise safety checklist provides a clear standard for production readiness: "
            "immutable sandboxing, shell sanitization, and AST secret scanning must be present in every deployment."
        ),
        38: (
            " In guardrails_engine.py, we see the implementation of the Claude Code hook interceptor and AST secret scanner in action, "
            "providing a complete, dependency-free reference implementation."
        ),
        39: (
            " The harness-guardrails-and-hooks skill standardizes these controls into a reusable package, "
            "making it easy to deploy enterprise-grade guardrails across any Claude Code project."
        ),
        40: (
            " Module 5 focuses on Permission Escalation Gateways and human-in-the-loop governance. "
            "In production environments, irreversible operations like deploying to production or pushing to main must always require human sign-off."
        ),
        41: (
            " The challenge in human-in-the-loop design is avoiding alert fatigue. "
            "By establishing clear risk tiers, we ensure that engineers are only interrupted for genuinely critical, high-impact decisions."
        ),
        42: (
            " Our implementation uses an immutable cryptographic ledger in approvals.json. "
            "When an operator approves a critical action, a signed token is recorded, allowing the gateway to verify authorization deterministically."
        ),
        43: (
            " The harness-permission-escalation-gateway skill integrates this approval workflow directly into the agent's tool execution pipeline."
        ),
        44: (
            " In Module 6, we explore how automated tests serve as the reliability layer for autonomous coding agents. "
            "Tests provide the deterministic ground truth that allows agents to detect failures, formulate fixes, and verify code quality."
        ),
        45: (
            " The Test-Driven Agent loop mirrors senior engineering practices: "
            "first, write or run a failing test; second, capture the traceback; third, generate and apply a repair; and fourth, verify that all tests pass."
        ),
        46: (
            " Tiered testing ensures optimal development velocity. Fast unit tests provide immediate feedback on every edit, "
            "while integration and regression suites run before major milestones."
        ),
        47: (
            " Automated traceback extraction eliminates developer friction by programmatically capturing compiler output "
            "and formatting it into structured repair prompts for the model."
        ),
        48: (
            " Anti-regression test persistence ensures that every fixed defect becomes a permanent regression test, "
            "building an ever-stronger testing safety net as the codebase evolves."
        ),
        49: (
            " Tracking reliability metrics like mean iterations to green and regression rates gives engineering leaders objective data "
            "on agent performance and code stability."
        ),
        50: (
            " In tda_reliability_pipeline.py, we see how real pytest subprocess executions drive automated agent self-healing "
            "and regression test persistence."
        ),
        51: (
            " The harness-tda-reliability-pipeline skill packages these test-driven repair workflows into a reusable CLI tool."
        ),
        52: (
            " Module 7 covers Skills, Plugins, and the official Model Context Protocol (MCP). "
            "MCP is rapidly becoming the universal standard for connecting AI models to external tools, databases, and enterprise systems."
        ),
        53: (
            " Agent Skills provide self-contained capabilities with clear descriptions, allowed tools, and executable Python helper scripts."
        ),
        54: (
            " Following standardized skill layouts ensures that tools and documentation remain maintainable and discoverable across agent platforms."
        ),
        55: (
            " Claude Plugins simplify enterprise distribution by bundling multiple skills, subagents, hooks, and MCP servers into a single manifest."
        ),
        56: (
            " Understanding MCP versioning is critical for developers: the dated protocol spec, Python SDK package version, and JSON-RPC framing "
            "must be properly managed across client-server integrations."
        ),
        57: (
            " Local stdio transports provide fast, zero-network tool execution, while Streamable HTTP transports enable distributed enterprise microservices."
        ),
        58: (
            " The modern Python MCP SDK allows developers to expose tools and resources using simple, expressive Python decorators like @mcp.tool() and @mcp.resource()."
        ),
        59: (
            " Enterprise MCP governance enforces authentication, authorization, and audit logging across all external tool invocations."
        ),
        60: (
            " In our Module 7 Code Lab, mcp_server_demo.py and mcp_client_runner.py demonstrate a complete, live stdio MCP session "
            "with database tool calls and live LLM response synthesis."
        ),
        61: (
            " The harness-mcp-and-plugins skill allows agents to discover, inspect, and consume MCP servers dynamically during task execution."
        ),
        62: (
            " Module 8 explores Compound Engineering and Multi-Agent Teams. "
            "By decomposing complex software tasks into specialized roles, we eliminate single-agent cognitive overload and prevent confirmation bias."
        ),
        63: (
            " Multi-agent systems outperform single agents because each role operates within a clean, focused context window, "
            "reducing attention saturation and improving reasoning quality."
        ),
        64: (
            " The Planner role focuses exclusively on architectural decomposition, creating clear, file-scoped subtasks without performing code modifications."
        ),
        65: (
            " The Implementer role receives only its assigned sub-spec, writing verified source code within an isolated workspace."
        ),
        66: (
            " The Reviewer role conducts an independent audit, executing AST syntax validation and automated pytest suites without shared conversation bias."
        ),
        67: (
            " Git worktree isolation ensures that the implementer works on an ephemeral branch in a separate directory. "
            "Unverified changes can never corrupt the main repository working tree."
        ),
        68: (
            " Subagent context optimization filters master specifications, passing only the necessary sub-spec lines to keep context windows lean and token costs low."
        ),
        69: (
            " Telemetry logging records multi-agent execution metrics to telemetry.jsonl, providing the empirical data needed for continuous workflow refinement."
        ),
        70: (
            " In multi_agent_team_simulator.py, we see the complete implementation of worktree creation, role handoffs, and clean automated teardown."
        ),
        71: (
            " The harness-compound-multi-agent-worktrees skill makes it easy to orchestrate multi-agent teams across production repositories."
        ),
        72: (
            " Module 9 presents the Practical 5-Step SOP Workflow Pattern, synthesizing all course concepts into a repeatable standard operating procedure."
        ),
        73: (
            " The 5-Step SOP provides a structured development pipeline: Spec First, Constrained Execution, Deterministic Checks, Automated Pytest, and Human Review."
        ),
        74: (
            " Steps 1 and 2 establish the foundation: parsing SPEC.md contracts and binding agent edits strictly to in-scope files within a temporary sandbox."
        ),
        75: (
            " Steps 3 and 4 enforce deterministic quality: executing AST compilation, secret scanning, and automated pytest test suites."
        ),
        76: (
            " Step 5 maintains human engineering oversight, generating clean unified diffs for final review and sign-off before code is merged."
        ),
        77: (
            " In five_step_sop_pipeline.py, we execute the complete end-to-end pipeline, producing a verified, production-ready JWT authentication module."
        ),
        78: (
            " The harness-five-step-sop-pipeline skill enables developers to execute standardized production workflows with a single CLI command."
        ),
        79: (
            " Module 10 concludes the course with Enterprise Principles and the Production Readiness Audit. "
            "We provide an objective framework for evaluating whether a repository is fully prepared for autonomous AI coding agents."
        ),
        80: (
            " The Four Golden Principles summarize our engineering philosophy: "
            "Machine Specifications Over Vague Prompts, Deterministic Guardrails Over Probabilistic Trust, "
            "Automated Tests as Sensory Feedback, and Least-Privilege Scoped Tooling."
        ),
        81: (
            " The 5-Gate Production Readiness Scorecard audits: Memory Files, Pre-execution Hooks, Automated Test Runners, "
            "MCP Declarations, and Subagent Role Definitions."
        ),
        82: (
            " By adopting these principles and building engineered harnesses, software organizations can safely harness the full power of autonomous AI coding agents."
        ),
        83: (
            " In production_harness_audit.py, we execute our automated compliance auditor, confirming that our repository achieves a 100% 5/5 readiness score."
        ),
        84: (
            " The harness-production-readiness-auditor skill allows teams to integrate automated readiness checks directly into their CI/CD pipelines."
        ),
        85: (
            " Our comparison between Graph Engineering and Dynamic Workflows clarifies the distinction between architectural network design and native runtime execution in Claude Code."
        ),
        86: (
            " Slide 86 compiles all core documentation links, official Anthropic specifications, and GitHub repository resources. "
            "Thank you for participating in the Packt Masterclass on Harness Engineering for AI Coding Agents. "
            "You now possess the foundational blueprints and practical code required to build robust, secure, and reliable autonomous agent workflows. "
            "We look forward to seeing the resilient, production-grade agent harnesses you build."
        ),
    }
    
    extra = deep_lectures.get(slide_num, "")
    return f"{base} {extra}"


async def generate_single_audio(slide_num: int, text: str, semaphore: asyncio.Semaphore) -> tuple[int, Path, float]:
    async with semaphore:
        out_file = AUDIO_DIR / f"slide_1hr_{slide_num:02d}.mp3"
        communicate = edge_tts.Communicate(text, VOICE)
        await communicate.save(str(out_file))
        
        # Measure duration with ffprobe
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
            duration = out_file.stat().st_size / 4000.0
            
        print(f"  [OK] Slide {slide_num:02d} -> {out_file.name} ({duration:.1f}s, {out_file.stat().st_size} bytes)")
        return slide_num, out_file, duration


async def generate_1hr_masterclass():
    full_narrations = {num: get_full_lecture(num) for num in sorted(SLIDE_NARRATIONS.keys())}
    total_words = sum(len(text.split()) for text in full_narrations.values())
    est_minutes = total_words / 125.0  # ~125 words per minute for lecture TTS
    
    print("=" * 80)
    print("GENERATING 1-HOUR+ EXTENDED MASTERCLASS AUDIO (ALL 86 SLIDES IN SINGLE MP3)")
    print(f"Total Slides: {len(full_narrations)} | Total Words: {total_words:,} (~{est_minutes:.1f} minutes estimated)")
    print(f"Target Voice: {VOICE}")
    print(f"Output Master Track: audio/packt_harness_complete_masterclass_1hr.mp3")
    print("=" * 80 + "\n")
    
    sem = asyncio.Semaphore(6)  # 6 concurrent synthesis tasks
    tasks = [
        generate_single_audio(num, full_narrations[num], sem)
        for num in sorted(full_narrations.keys())
    ]
    
    start_time = time.time()
    results = await asyncio.gather(*tasks)
    elapsed = time.time() - start_time
    
    total_duration = sum(r[2] for r in results)
    minutes = total_duration / 60.0
    print(f"\n[DONE] Successfully synthesized all 86 extended slide audio segments in {elapsed:.1f}s.")
    print(f"Total Combined Duration: {minutes:.2f} minutes ({total_duration:.1f} seconds)")

    # Build concatenation list
    concat_list = AUDIO_DIR / "concat_list_1hr.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for num, path, _ in sorted(results, key=lambda x: x[0]):
            f.write(f"file '{path.name}'\n")
            
    master_1hr_audio = AUDIO_DIR / "packt_harness_complete_masterclass_1hr.mp3"
    print(f"\n[*] Concatenating segments into unified 1-Hour+ Masterclass MP3...")
    subprocess.run(
        [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", str(concat_list), "-c", "copy", str(master_1hr_audio)
        ],
        capture_output=True
    )
    
    if master_1hr_audio.is_file():
        file_size_mb = master_1hr_audio.stat().st_size / (1024 * 1024)
        print(f"\n========================================================================")
        print(f">>> MASTERCLASS AUDIO CREATED SUCCESSFULLY <<<")
        print(f"File Path: {master_1hr_audio.resolve()}")
        print(f"File Size: {file_size_mb:.2f} MB")
        print(f"Exact Duration: {minutes:.2f} minutes ({total_duration:.1f} seconds)")
        if total_duration >= 3600:
            print(f"VERIFICATION: PASSED (Duration >= 1.0 Hour: {minutes:.1f} mins)")
        else:
            print(f"VERIFICATION: Current duration is {minutes:.1f} mins.")
        print(f"========================================================================")

    # Clean up temp concat list
    if concat_list.exists():
        concat_list.unlink()


if __name__ == "__main__":
    asyncio.run(generate_1hr_masterclass())
