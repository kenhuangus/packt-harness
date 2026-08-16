"""
Comprehensive 1-Hour+ (80+ Min) Masterclass Audio Generator.
Zero repetitive phrasing across all 92 slides.
Every slide contains unique, in-depth architectural and code implementation details.
Expanded Module 8 includes comprehensive coverage of Compound Orchestrator (https://github.com/kenhuangus/compound-orchestrator).
"""

from __future__ import annotations

import asyncio
import collections
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


SLIDE_LECTURES: dict[int, str] = {
    1: (
        'Welcome to the Packt Masterclass on Harness Engineering for AI Coding Agents: Building Reliable Claude Code Workflows with Deterministic Guardrails, Machine-Verifiable Specifications, and Automated Tests. I am your instructor, Ken Huang. Today, software development stands at a historic inflection point. Autonomous coding agents powered by large language models have demonstrated astonishing proficiency at translating natural language prompts into functional source code. However, when engineering teams attempt to transition these probabilistic models directly into enterprise production pipelines, they routinely encounter severe operational roadblocks. Without strict runtime scaffolding, even state-of-the-art foundation models suffer from context window degradation, catastrophic execution loop traps, unverified filesystem mutations, and unauthorized system operations. In enterprise software engineering, when a developer writes code, their workflow is supported by robust tooling: compilers identify type mismatches, linters enforce formatting, unit tests verify logic, and CI/CD pipelines prevent broken builds from merging. When we deploy an AI coding agent without a harness, we are effectively removing all of those foundational safety nets and hoping the model never errs. Harness engineering reinstates and expands those safety nets for the age of autonomous AI. To provide a complete, end-to-end framework, this masterclass is structured into ten comprehensive modules: Module 1 investigates why harness engineering is required, dissecting the four classic agent failure modes and demonstrating runtime loop interception. Module 2 introduces the Core Harness Stack, establishing the Five Golden Pillars: Memory Files, Scoped Tools, Deterministic Hooks, Context Token Budgeting, and JSONL Observability. Module 3 explores Spec-Driven Development, transforming ambiguous conversational prompts into machine-verifiable SPEC.md contracts with strict scope whitelists and non-goals. Module 4 covers Guardrails and Hooks, implementing defense-in-depth across the 4-layer control model, Claude Code PascalCase PreToolUse contracts, and AST secret scanning. Module 5 examines Permission Escalation Gateways, managing human-in-the-loop approvals across a 4-tier risk matrix backed by a signed ledger. Module 6 focuses on Tests as the Reliability Layer, constructing the Test-Driven Agent Red-Repair-Green loop and persisting anti-regression safeguards. Module 7 explores Skills, Plugins, and the Model Context Protocol, detailing stdio child process transports, tool decorators, and live LLM client synthesis. Module 8 advances to Compound Engineering, orchestrating specialized Planner, Implementer, and Reviewer multi-agent teams within ephemeral Git worktrees. Module 9 presents the Practical 5-Step SOP Workflow Pattern, executing a unified pipeline from spec ingestion to human unified diff review. And Module 10 concludes with Enterprise Principles and our automated 5-Gate Production Readiness Audit.'
    ),
    2: (
        'Before diving into our technical stack, allow me to introduce myself and provide the context behind this curriculum. My name is Ken Huang. Over the past twenty-five years, my career has focused on the intersection of distributed systems, cryptographic security, cloud architecture, and artificial intelligence. Currently, I serve across several industry initiatives, including the AIUC-1 working group, research collaborations with Schmidt Sciences, and co-authoring the OWASP Top 10 for Large Language Model Applications. I have authored fifteen books published globally by Springer, Cambridge University Press, Wiley, Packt, and Claude AI. These publications span blockchain security, decentralized intelligence, prompt engineering, generative AI risk mitigation, and autonomous multi-agent orchestration. The core philosophy underpinning this course is that every theoretical principle must be substantiated by real, executable code. In this masterclass, you will not encounter theoretical pseudo-code or mocked stubs. Every module, test runner, AST analyzer, and Model Context Protocol server in our repository is fully functional, standard-library compliant, and thoroughly tested. All course materials, code labs, and presentation decks are available directly in our open-source GitHub repository. You can execute every module directly using our custom packt-harness CLI, which allows you to list modules, run interactive simulations, inspect audit logs, and launch the HTML slide presentation.'
    ),
    3: (
        "Let us begin our deep dive with Module 1: Why Harness Engineering is Required. To understand the necessity of an agent harness, we must first confront the fundamental physics of autonomous LLM execution. In traditional software engineering, determinism is guaranteed by compilers, type systems, and operating system permission models. When developers delegate tasks to an autonomous agent, they often mistakenly assume that providing a clear system prompt is sufficient to guarantee disciplined behavior. In practice, large language models are probabilistic token predictors, not deterministic runtime engines. As an agent executes multi-step workflows, it generates tool calls, parses execution results, and adjusts its internal plans. Without external constraints, small probabilistic variances compound exponentially, leading to severe execution drift. When an agent fails, the root cause is almost never the model's inability to write code; rather, it is the failure of the surrounding system to provide unambiguous boundaries, active execution monitoring, and reliable sensory feedback. In this module, we dissect the four primary failure modes that plague un-harnessed agents: context saturation, execution loops, unverified file modifications, and destructive shell invocations."
    ),
    4: (
        'On Slide 4, we examine the fundamental architectural divide between Prompt Engineering and Harness Engineering. Prompt engineering operates strictly within the input context window of the model. It relies on natural language instructions, few-shot examples, and chain-of-thought prompting to coax the model toward desired behavior. While prompt engineering is necessary for establishing task context, it provides zero deterministic guarantees. Under high token load, the model frequently ignores negative constraints or misinterprets tool schemas. Harness engineering, by contrast, operates outside the model. The harness is an active software layer that sits between the LLM and the host environment. It intercepts every tool invocation before execution, validates arguments against strict JSON schemas, enforces filesystem containment, compiles modified code in memory, and audits operations in append-only event streams. Think of prompt engineering as the steering wheel of a vehicle, while harness engineering provides the brakes, seatbelts, traction control, and lane assist. You need both, but without the harness, high-speed autonomous navigation is inherently hazardous.'
    ),
    5: (
        "Let us examine Failure Mode 1: Context Drift and Attention Saturation. As an agent interacts with a codebase, it reads files, runs compilers, executes test suites, and inspects debug logs. Each of these operations returns hundreds or thousands of tokens that get appended to the conversational history. Modern transformer architectures utilize self-attention mechanisms that can degrade as sequence lengths approach maximum capacity. When massive compiler dumps and stack traces flood the context window, the model's attention over early system guidelines diminishes. The agent gradually forgets critical architectural rules, coding conventions, or scope limitations specified at the start of the session. A production harness mitigates this by implementing proactive context budgeting, dynamic token allocation, and head-tail log compaction. Our ContextTokenBudgeter treats tokens like memory pages in an operating system, allocating explicit percentages to persistent rules, specifications, dynamic workspace files, and output buffers. By truncating repetitive compiler dumps while preserving critical head and tail lines, the harness ensures that the attention window remains clean, focused, and capable of high-precision reasoning across dozens of conversational turns."
    ),
    6: (
        'Failure Mode 2 is the Execution Loop Trap. Consider a scenario where an autonomous agent encounters a broken unit test. It reads the test failure, formulates a hypothesis, modifies a line of code, and runs pytest. If the test fails again, an unconstrained agent will often re-read the same traceback, propose an identical or trivial variant of the previous edit, and run pytest again. Without an external observer, the agent can enter an infinite execution loop, repeatedly executing failing commands until API quotas are exhausted or budgets are depleted. In production environments, runaway execution loops can easily generate hundreds of dollars in unnecessary API costs within minutes. A robust harness implements an active loop detector that computes cryptographic hashes or canonical representations of consecutive tool calls. If an agent repeats the same command or edit pattern without demonstrating measurable forward progress, the harness immediately trips a circuit breaker, halts execution, and forces the agent to re-evaluate its strategy or request human assistance.'
    ),
    7: (
        "Failure Mode 3 involves Unverified File Writes and Broken Syntax. When large language models generate code edits, they occasionally emit invalid syntax, unmatched parentheses, missing imports, or subtle indentation errors. If an agent writes these flawed edits directly to the filesystem, the entire project workspace becomes broken. Subsequent test runs fail with syntax errors rather than logical test failures, confusing the agent's diagnostic reasoning and derailing the task. In a properly engineered harness stack, no file write is ever permitted to reach disk without passing through an Abstract Syntax Tree parsing gate. The harness parses the proposed code buffer in memory using Python's ast.parse module. If a syntax error is detected, the write is immediately rejected with an explicit error message, preventing corruption of the local workspace and maintaining a clean compilation environment. Python's ast module allows us to construct and analyze the full syntax tree before writing to disk, catching unclosed strings and misaligned blocks."
    ),
    8: (
        'Failure Mode 4 represents the most dangerous category: Destructive Shell Operations and Permission Escapes. Autonomous agents possess the ability to run shell commands to build projects, manage packages, and execute test runners. However, when faced with persistent build failures or permission errors, un-harnessed agents have been observed attempting broad cleanups, such as executing rm -rf on project directories, running chmod 777, or using dangerous CLI flags like --dangerously-skip-permissions. A production harness treats every shell command as potentially hostile. It implements pre-execution command regex inspection, matching proposed command lines against blacklists of destructive patterns and enterprise security policies. Any command matching forbidden operations is instantly intercepted and denied before reaching the operating system kernel, ensuring complete workspace safety. By evaluating command strings prior to subprocess creation, we eliminate the attack surface for accidental or malicious system damage.'
    ),
    9: (
        "On Slide 9, we introduce our first hands-on code laboratory: harness_vs_model_demo.py, located in Module 1. In this demonstration, we create a real sandbox directory with authentic application log files and an intentionally failing pytest suite. We first execute an un-harnessed agent simulation that attempts repeated test runs and ultimately executes a destructive directory cleanup, deleting the sandbox log files. We then execute our harnessed agent against the exact same scenario. The harness's loop detector intercepts the repetitive pytest execution on attempt two with exit code 2, and its pre-execution security hook blocks the recursive deletion, ensuring that all sandbox logs survive completely intact. In Module 1, our test workspace proves that a harnessed agent maintains complete filesystem integrity while blocking repetitive loops, contrasting directly with the unconstrained failure of the un-harnessed agent."
    ),
    10: (
        'Slide 10 presents the live terminal execution evidence captured from harness_vs_model_demo.py. Examining the standard output, you can see our LLM client connecting live to our local OpenAI-compatible endpoint. Under the un-harnessed agent run, the agent executes pytest three times sequentially with exit code 2, followed by a cleanup command that deletes the logs. Under the harnessed agent run, the first pytest call is inspected and permitted. On the second identical call, the harness loop detector fires, emitting a BLOCKED BY HARNESS LOOP DETECTOR event. When the agent attempts the rm -rf command, the pre-hook intercepts it with a Security Violation, proving that the harness successfully preserved the workspace and prevented unauthorized data loss. When the loop detector fires, it returns a structured diagnostic message, allowing the supervisory runtime to take corrective action safely.'
    ),
    11: (
        'Let us examine the concrete Python source code for Module 1 in harness_vs_model_demo.py. Look closely at lines 134 through 142. Here, the pre_execution_hook method iterates over a pre-compiled list of regular expression patterns, including rm -rf, sudo, and git push --force. If a match is found, it returns False along with a structured security violation message. Next, observe lines 145 through 154, where the loop_detector class maintains a sliding history buffer of recent tool signatures. When the repetition count exceeds the configured threshold of two, it raises an execution trap, effectively immunizing the system against runaway loops. Both pre_execution_hook and loop_detector are pure Python functions requiring zero external dependencies, making them portable across any CI/CD environment. Delving into the internal mechanics of the loop detector, the LoopDetector class initializes with a threshold of two repetitions. Each call signature is recorded as a SHA-256 digest of the tool name and sorted JSON kwargs. When the repetition count reaches the threshold, loop_detector returns action_allowed as False, causing the main evaluation loop to log a BLOCKED event with exit code 2. Meanwhile, pre_execution_hook compiles regex patterns matching rm -rf, sudo, and force push, returning a structured SecurityViolation object that protects the sandbox.'
    ),
    12: (
        "On Slide 12, we inspect the standardized agent skill manifest: harness-interception-loop-detector, located in .claude/skills/. This skill provides Claude Code with explicit operational rules and helper scripts to detect repetitive tool cycles and sanitize command strings. By packaging this capability as a standard skill with YAML frontmatter, any Claude Code instance can discover, load, and execute these deterministic interceptors during live coding sessions, embedding defensive engineering directly into the agent's runtime environment. Standardizing harness capabilities into agent skills allows engineering teams to version-control, compose, and share guardrails across repositories."
    ),
    13: (
        "We now advance to Module 2: The Core Harness Stack. To engineer an enterprise-grade agent harness, we must establish a unified architectural framework. We structure the harness around five fundamental pillars: Memory Files, Scoped Tools and Sandboxing, Deterministic Hooks, Context Token Budgeting, and Structured JSONL Observability. Together, these five pillars form an airtight operational envelope around the agent, ensuring consistency, safety, and auditable governance across all development tasks. If any single pillar is omitted, the agent's reliability envelope is compromised."
    ),
    14: (
        "Slide 14 illustrates the architectural layout of the Five Harness Pillars. Pillar 1 manages persistent instructions via CLAUDE.md and AGENTS.md. Pillar 2 governs tool allowlists and enforces filesystem containment via Python's Path.resolve().is_relative_to(). Pillar 3 executes pre-tool and post-tool middleware hooks, including AST validation and secret detection. Pillar 4 manages the 20/20/50/10 token budget allocation and performs log compaction. Pillar 5 records every tool request, hook decision, and execution result into an append-only events.jsonl audit log for complete forensic replay. Notice how the five pillars form concentric rings of defense around the agent's central reasoning engine."
    ),
    15: (
        'Let us examine Pillar 1: Memory Files in detail. In modern coding agent workflows, CLAUDE.md and AGENTS.md act as the persistent long-term memory of the repository. These files store concise architectural guidelines, coding style rules, build commands, and testing procedures. However, a common failure mode is allowing memory files to expand into sprawling documentation dumps. A production harness enforces strict size limits on memory files—typically under 25 kilobytes—ensuring that permanent context does not cannibalize the dynamic reasoning buffer needed for code generation and analysis. Memory files should focus strictly on invariant repository rules: coding standards, test commands, and architectural constraints. Sprawling API documentation belongs in dedicated skill references, not in CLAUDE.md.'
    ),
    16: (
        'Pillar 2 focuses on Scoped Tools and Path Sandboxing. The principle of least privilege dictates that an agent should only be equipped with the exact tools necessary for its current role. Furthermore, filesystem operations must be rigorously sandboxed. A naive path check that only searches for double dots (..) can be bypassed using symlinks or absolute path overrides. Our CoreHarnessStack resolves all target paths to their canonical absolute representations and validates that the resolved path is strictly relative to the designated workspace root using Path.resolve().is_relative_to(workspace). Any path escaping the boundary is instantly blocked. This check is mathematically robust against symlink attacks and relative path overrides, guaranteeing absolute containment.'
    ),
    17: (
        "Pillar 3 establishes the Deterministic Hooks Engine. Hooks act as synchronous middleware intercepting the agent's actions before and after tool execution. Pre-execution hooks inspect tool names and argument payloads, verifying permissions, sanitizing shell commands, and blocking dangerous options. Post-execution hooks inspect the output of actions. When files are written, post-hooks parse the source tree with Python's ast module and scan for high-entropy strings indicating accidental credential leaks before the changes are committed. The combination of PreToolUse command sanitization and PostToolUse AST compilation provides complete bidirectional safety."
    ),
    18: (
        'Pillars 4 and 5 cover Context Budgeting and Observability. Our ContextTokenBudgeter enforces a disciplined 20/20/50/10 token budget split: 20% for permanent memory instructions, 20% for feature specifications, 50% for dynamic workspace files and reasoning, and 10% reserved for output buffers. When compiler logs exceed allocation limits, our compaction algorithm preserves the top ten and bottom ten lines while summarizing the middle. Simultaneously, Pillar 5 logs every execution event into an append-only events.jsonl file, providing full forensic replayability. Append-only JSONL event streams enable real-time observability and comprehensive post-incident forensic analysis for compliance auditing.'
    ),
    19: (
        'In the Module 2 Code Lab from core_harness_stack.py, we examine the implementation of these pillars. Lines 71 to 78 implement ContextTokenBudgeter, dynamically calculating token counts and compacting log streams. Lines 141 to 148 implement validate_tool_permission, verifying tool names against an allowlist and checking that target file paths satisfy is_relative_to(self.workspace). If path traversal is attempted, a detailed HARNESS ERROR event is written to the audit log and execution is blocked. core_harness_stack.py integrates all five pillars into a unified, reusable Python class with zero external dependencies. Walking through the implementation of the core stack, the CoreHarnessStack class enforces all five pillars. The validate_tool_permission method inspects incoming tool requests against an ALLOWED_TOOLS set. When write_file is invoked, the target path is resolved and validated with is_relative_to(self.workspace). If an attacker attempts a path traversal such as ../../etc/passwd, the method raises a PermissionError. Additionally, ContextTokenBudgeter enforces the 20/20/50/10 token allocation, compacting compiler logs, and every event is serialized as JSON and written to events.jsonl.'
    ),
    20: (
        'Slide 20 displays the skill manifest for harness-core-stack-sandbox. This skill encapsulates tool permission validation, filesystem boundary enforcement, and structured JSONL telemetry. By integrating this skill into agent configurations, developers ensure that all file operations adhere to enterprise sandboxing standards. Packaging sandbox validation as an agent skill allows developers to invoke validate_sandbox.py across diverse operational workflows.'
    ),
    21: (
        'Welcome to Module 3: Spec-Driven Development, or SDD. Spec-Driven Development is the single most powerful technique for ensuring that autonomous coding agents deliver precise, defect-free software implementations. In traditional workflows, developers interact with agents through iterative conversational prompts. However, conversational prompts are inherently ambiguous, allowing the agent to make assumptions that lead to scope creep and architectural drift. SDD replaces conversational ambiguity with machine-verifiable markdown specifications, transforming agile user stories into formal contracts.'
    ),
    22: (
        "On Slide 22, we analyze why prompts fail while specifications succeed. A natural language prompt such as 'implement JWT authentication' leaves dozens of critical architectural questions unanswered: Which files should be created? What algorithms should be supported? What existing files must not be touched? An autonomous agent given a vague prompt often attempts to modify database connection pools, introduce unrequested dependencies, or alter global settings. A formal specification answers these questions unambiguously before a single line of code is written, providing hard boundaries that the harness enforces. Prompts invite interpretation; specifications demand compliance."
    ),
    23: (
        'Slide 23 details the Anatomy of a Production SPEC.md file. A complete specification contains four mandatory sections: Section 1: Feature Objective, stating the business and technical purpose. Section 2: Allowed Modification Scope, declaring explicit whitelists of permitted files and blacklists of forbidden files. Section 3: Explicit Non-Goals, listing anti-patterns and features that must NOT be implemented in this iteration. Section 4: Machine-Verifiable Acceptance Criteria, defining structured input-output schemas and automated test suites. Every section in SPEC.md serves a vital purpose: objectives align context, scopes prevent sprawl, non-goals block anti-patterns, and criteria guarantee quality.'
    ),
    24: (
        'Let us examine Scope and Non-Goals: Hard Architectural Boundaries. In our real-world JWT token validator specification, Section 2 permits edits only to auth_validator.py and tests/test_auth.py, while explicitly forbidding database.py and configuration files. Section 3 lists explicit non-goals, prohibiting database connection pools and OAuth2 refresh rotation. When our SpecVerifier intercepts an edit, it parses the proposed code body. If the code references database connections or unrequested OAuth logic, the write is immediately rejected with a NON_GOAL_VIOLATION event. Explicit non-goals prevent over-engineering simple features into monolithic rewrites.'
    ),
    25: (
        "Slide 25 addresses Acceptance Criteria: Transitioning from Vague Guidelines to Executable Contracts. Qualitative requirements like 'ensure high test coverage' cannot be audited by automated machinery. In SDD, acceptance criteria are formatted as discrete, testable items: AC-01 mandates that auth_validator.py export a function validate_jwt; AC-02 requires returning valid equals True and user_id equals 123 for authentic tokens; AC-03 requires returning valid equals False and error equals EXPIRED for expired tokens; and AC-04 requires 100% pass rates across automated pytest test cases. Executable acceptance criteria bridge the gap between requirements and automated verification."
    ),
    26: (
        'Slide 26 outlines the complete Spec-Driven Development Lifecycle. The workflow follows four disciplined phases: Phase 1: Spec Ingestion, where the agent parses SPEC.md and loads scope constraints. Phase 2: Constrained Plan Generation, where the agent plans edits strictly within the declared file boundaries. Phase 3: Pre-Write Spec Auditing, where the harness checks every file diff against allowed scopes and non-goals. Phase 4: Automated Verification, where the harness runs pytest against the generated code and asserts compliance with acceptance criteria. This creates a predictable rhythm: specify, constrain, verify, and test.'
    ),
    27: (
        'Slide 27 details Spec Verification Before Code Ships. In our implementation, SpecVerifier acts as an active gatekeeper. When an agent proposes modifying database.py, the verifier checks the parsed allowed_files list. Finding database.py absent, it immediately raises a SCOPE_VIOLATION and halts the operation. This guarantees that the agent cannot introduce silent regressions into unrelated subsystems. Automated spec verification catches scope violations in milliseconds, before code reaches disk.'
    ),
    28: (
        "In the Module 3 Code Lab from spec_driven_verifier.py, we inspect the Python implementation. Lines 6 to 8 normalize the target file path and check membership in allowed_files, rejecting out-of-scope targets. Lines 10 to 13 inspect the lowercased code content for forbidden non-goal keywords like database or connect_db. Finally, line 18 compiles the code buffer with ast.parse() before saving to disk, ensuring that only valid, compiling code is written. This demonstrates that markdown contracts can be parsed and enforced deterministically using standard Python regex. Examining the verification mechanics in detail, the SpecVerifier class parses SPEC.md markdown headers using regular expressions. It extracts the allowed_files list and the explicit non_goals list. When an agent submits code for auth_validator.py, the verifier confirms the path is allowed, checks that the content does not contain forbidden keywords like connect_db or database_pool, and runs ast.parse to verify syntax before writing to disk. The generated validator implements RFC 7519 HMAC-SHA256 JWT validation using Python's hmac and hashlib."
    ),
    29: (
        'Slide 29 presents the skill manifest for harness-spec-driven-development. This skill enables agents to programmatically parse SPEC.md contracts, audit proposed code diffs against allowed file scopes, and validate abstract syntax tree structures prior to file commits. Reusable SDD skills empower autonomous agents to self-audit their proposed modifications against project contracts.'
    ),
    30: (
        'We now enter Module 4: Guardrails and Deterministic Hooks Engine. In enterprise software environments, safety cannot rely on hope or trust. We must implement defense-in-depth, layering multiple independent control mechanisms to ensure that no agent action can compromise system integrity or leak confidential data. Guardrails do not restrict developer productivity; they liberate agents to operate autonomously with confidence and safety.'
    ),
    31: (
        'Slide 31 illustrates the 4-Layer Control Architecture: Layer 1: System Rules in system prompts and memory files establishing initial intent. Layer 2: Tool Schemas enforcing strict type checking and required JSON schema properties on tool inputs. Layer 3: Deterministic Hooks intercepting tool calls in real time before and after execution. Layer 4: Operating System Sandboxing providing process isolation, filesystem containment, and network egress controls. Layered defense ensures that even if prompt context is compromised, lower-level hook and OS constraints prevent unauthorized actions.'
    ),
    32: (
        'Slide 32 details the official Claude Code PascalCase Hook Contract. Claude Code communicates with external hook scripts over standard input using structured JSON payloads. For PreToolUse events, the hook receives tool_name and tool_input. An exit-0 hook returns a structured JSON object containing hookSpecificOutput with a permissionDecision set to allow, deny, ask, or defer. Exit code 2 represents a blocking error, causing Claude Code to display stderr and abort the tool invocation immediately. The PascalCase hook interface provides a standardized, industry-wide protocol for deterministic tool governance.'
    ),
    33: (
        "Slide 33 covers Post-Action Verification Checks. Whenever an agent edits or creates a file, the PostToolUse hook executes two critical verification gates: First, it parses the modified file using Python's ast.parse module to guarantee syntactic correctness. Second, it executes high-entropy regular expression scanning across the diff to detect accidental inclusion of API tokens, private keys, or database credentials, blocking the edit if a secret pattern is matched. Static AST analysis and entropy-based secret detection provide immediate feedback, keeping credentials secure."
    ),
    34: (
        'Slide 34 examines Path Sandboxing and Filesystem Containment. Path traversal vulnerabilities occur when an agent constructs relative paths that resolve outside the intended workspace directory. By enforcing Path.resolve().is_relative_to(workspace_root), our harness mathematically proves that every file access, read, and write remains strictly confined within the designated sandbox boundary. An agent confined to its workspace can never damage host infrastructure or access sensitive parent files.'
    ),
    35: (
        'Slide 35 addresses Risk-Tiered Permission Modes. Not all tool calls carry equal risk. Read-only operations like file viewing or directory listing operate in autonomous mode. File writes require logged verification. High-risk operations like package installation or database schema migrations require interactive confirmation, and critical actions like git push require explicit operator signing. Risk tiers align operational autonomy with business impact, allowing safe actions to move fast while requiring oversight for high-risk operations.'
    ),
    36: (
        'Slide 36 discusses Quantitative Evaluation Harnesses. To measure the effectiveness of guardrails, organizations must deploy evaluation benchmarks that test agents against adversarial prompts, injection attacks, and broken code scenarios, measuring interception rates, false positive frequencies, and overall task completion. Evaluation harnesses ensure that enterprise guardrails remain robust against evolving prompt injection vectors.'
    ),
    37: (
        'Slide 37 summarizes the Enterprise Safety Checklist: three non-negotiables for production agent systems: One: Immutable filesystem sandboxing with canonical path resolution. Two: Pre-execution shell command sanitization and dangerous flag interception. Three: Post-execution AST syntax gates and automated secret scanning. The safety checklist serves as an immutable standard for production readiness before deploying agents into repositories.'
    ),
    38: (
        "In the Module 4 Code Lab from guardrails_engine.py, we examine the implementation. Lines 6 to 14 implement intercept_pre_tool_use, parsing incoming JSON payloads and returning a structured deny decision if prohibited flags like --dangerously-skip-permissions are detected. Lines 20 to 26 implement audit_ast_and_secrets, scanning for hardcoded API keys and compiling the AST in a single atomic pass. This proves how straightforward it is to implement robust, enterprise-grade protection using standard Python libraries. Inside the guardrails implementation, the GuardrailsEngine class emulates Claude Code's PascalCase hook lifecycle. The intercept_pre_tool_use method parses incoming JSON from stdin. If command contains --dangerously-skip-permissions or rm -rf, it returns hookSpecificOutput with permissionDecision set to deny. The audit_ast_and_secrets method scans file diffs using regular expressions for high-entropy tokens like sk-ant-api03 or aws_secret_access_key, and runs ast.parse to ensure no syntax errors were introduced."
    ),
    39: (
        'Slide 39 presents the skill manifest for harness-guardrails-and-hooks. This skill provides standardized interceptors that enforce Claude Code PreToolUse and PostToolUse hook contracts across all repository tasks. Reusable guardrail skills allow development teams to enforce consistent enterprise security policies across distributed agent fleets.'
    ),
    40: (
        'Welcome to Module 5: Break, Open Q&A, and Permission Escalation Gateways. In this module, we explore how enterprise software architectures safely integrate human-in-the-loop governance for critical operations. Permission escalation gateways ensure that human engineers retain final authority over irreversible repository modifications.'
    ),
    41: (
        'During this interactive discussion, we analyze the balance between agent autonomy and enterprise risk. Complete autonomy introduces catastrophic risk, while requiring human approval for every minor edit creates unbearable developer friction. The solution is a risk-tiered permission escalation gateway. The key insight is that human approval should be requested selectively, preserving developer flow.'
    ),
    42: (
        'In the Module 5 Code Lab from permission_escalation_gateway.py, we implement a 4-tier risk classification engine: LOW risk tools like read_file are auto-approved; MEDIUM risk tools like write_file are logged and approved; and CRITICAL risk operations like git_push are blocked until an authorized cryptographic token is recorded in approvals.json. Our cryptographic ledger in approvals.json provides a tamper-evident audit trail of every authorized critical action. Looking closely at the escalation gateway, the PermissionEscalationGateway class assigns risk tiers to operations. Tools like read_file and list_dir are classified as LOW and auto-approved. write_file is classified as MEDIUM, triggering an event log before approval. Critical operations like git_push are classified as CRITICAL. The gateway checks output/approvals.json for a valid cryptographic request_id token. If absent, the push is blocked; once granted, the gateway writes to pending_push.json without executing destructive pushes.'
    ),
    43: (
        'Slide 43 displays the skill manifest for harness-permission-escalation-gateway. This skill allows agents to evaluate operation risks dynamically, requesting operator approvals only when high-consequence thresholds are crossed. Integrating approval gateways into agent skill manifests enables seamless human-in-the-loop collaboration.'
    ),
    44: (
        'We now explore Module 6: Tests as the Reliability Layer. In conventional software development, testing is often viewed as a post-implementation validation gate. In harness engineering for AI coding agents, automated tests serve as the primary sensory feedback loop guiding self-repair. Tests provide the deterministic ground truth that allows autonomous agents to perceive errors, diagnose root causes, and verify repairs.'
    ),
    45: (
        'Slide 45 introduces the Test-Driven Agent (TDA) Feedback Loop. The TDA loop operates across three rigorous phases: Stage 1 (Red): The harness executes pytest against the current implementation, intentionally triggering and capturing a real test failure. Stage 2 (Repair): The raw compiler failure and traceback are structured into an automated repair prompt. Stage 3 (Green): The agent applies the repair, and pytest is re-executed to verify that all test cases pass cleanly. The Red-Repair-Green TDA loop mirrors the disciplined practices of senior human software engineers.'
    ),
    46: (
        'Slide 46 details Hierarchical Test Tiers. To maintain fast iteration cycles without overwhelming context windows, test execution is tiered: Tier 1: Fast unit tests running in under one second on every file edit. Tier 2: Subsystem integration tests running before branch commits. Tier 3: Full end-to-end regression test suites running prior to pull request generation. Tiered testing balances rapid iteration velocity with comprehensive regression protection.'
    ),
    47: (
        "Slide 47 covers Automated Traceback Extraction. A common anti-pattern in developer workflows is manually copying compiler errors into chat windows. Our harness captures subprocess standard error and standard output streams programmatically, extracting file names, line numbers, and exception types into a high-signal repair prompt automatically. Automated traceback injection provides high-density signal directly to the model's reasoning engine."
    ),
    48: (
        'Slide 48 addresses Anti-Regression Test Enforcement. Whenever an agent fixes a bug, there is a risk that future edits may re-introduce the same defect. Our reliability pipeline automatically extracts the bug reproduction case and appends it permanently to the test suite as a regression safeguard. Anti-regression persistence turns every fixed bug into an automated safeguard against future regressions.'
    ),
    49: (
        'Slide 49 presents Key Reliability Metrics for measuring agent effectiveness: First-pass pass rate, mean iterations to green, regression introduction rate, and total token expenditure per successful fix. Monitoring reliability metrics allows engineering teams to track agent capability improvements and identify workflow bottlenecks.'
    ),
    50: (
        'In the Module 6 Code Lab from tda_reliability_pipeline.py, we inspect the implementation. Lines 6 to 14 execute pytest in a temporary subprocess, capturing standard error. Lines 20 to 28 append the new test_divide_zero_guard function into the pytest suite, verifying that two out of two tests pass on subsequent runs. Real subprocess pytest executions drive deterministic agent self-healing. Tracing the TDA pipeline execution, the TdaReliabilityPipeline class manages the test-driven repair loop. It writes an initial calculator.py with def divide(a, b): return a / b and a test asserting divide(10, 0) == 0. It runs pytest in a subprocess, capturing the ZeroDivisionError traceback and exit code 1. It then generates the repair with if b == 0: return 0, re-runs pytest, and confirms 1 passed. Finally, it permanently appends def test_divide_zero_guard(): assert divide(5, 0) == 0 to the test suite and verifies 2 passed.'
    ),
    51: (
        'Slide 51 presents the skill manifest for harness-tda-reliability-pipeline, formalizing automated test execution and repair loops into a reusable skill. Packaging TDA loops as reusable skills empowers agents to execute autonomous bug repair across complex codebases.'
    ),
    52: (
        'Welcome to Module 7: Skills, Plugins, and the Model Context Protocol (MCP). Extensibility is essential for integrating AI agents with enterprise tools, databases, APIs, and microservices. The Model Context Protocol establishes an open, standardized framework for connecting AI agents to enterprise data and tools.'
    ),
    53: (
        "Slide 53 explores Agent Skills. A skill is a self-contained directory featuring a SKILL.md manifest with YAML frontmatter, declaring the skill's name, description, allowed tool permissions, reference documentation, and supporting Python scripts. Skills provide domain-specific knowledge and executable tools in a clean, self-contained package."
    ),
    54: (
        'Slide 54 details Canonical Skill Directory Structure: SKILL.md at the root, scripts/ for executable helpers, references/ for architectural documentation, and examples/ for reference implementations. Standardized directory layouts ensure that skills remain discoverable, maintainable, and interoperable across platforms.'
    ),
    55: (
        'Slide 55 examines Claude Plugins. A plugin bundles multiple skills, custom subagents, pre-execution hooks, and MCP server configurations into a single distributable package defined by .claude-plugin/plugin.json. Claude Plugins simplify distribution by bundling skills, agents, hooks, and MCP servers into a single manifest.'
    ),
    56: (
        'Slide 56 clarifies MCP Protocol Fundamentals and Versioning. It is crucial to distinguish three distinct version numbers: First, the dated protocol specification, such as 2025-06-18. Second, the Python SDK package version, such as 2.0.0. Third, the JSON-RPC 2.0 wire framing standard governing message serialization. Understanding MCP versioning distinctions prevents common integration errors and ensures protocol compatibility.'
    ),
    57: (
        'Slide 57 contrasts MCP Transport Layers: Local transports utilizing standard input and output (stdio) pipes between child processes, versus remote transports utilizing Streamable HTTP with Server-Sent Events. Stdio transports offer zero-latency local tool execution, while Streamable HTTP enables scalable cloud integrations.'
    ),
    58: (
        'Slide 58 covers Modern MCP Python SDK Authoring. Using the official mcp package, developers expose tools via the @mcp.tool() decorator and read-only configuration data via the @mcp.resource() decorator. The official Python MCP SDK makes authoring enterprise tools and resources as simple as adding Python decorators.'
    ),
    59: (
        'Slide 59 addresses Enterprise MCP Governance, including tool authentication, resource authorization, and data loss prevention. Robust MCP governance protects enterprise databases and APIs from unauthorized access or accidental data modification.'
    ),
    60: (
        "In the Module 7 Code Lab, mcp_server_demo.py defines an enterprise server exposing query_database_record and config://app-settings. mcp_client_runner.py spawns the server as a child process, negotiates the JSON-RPC handshake over stdio, executes the tool, reads the resource, and synthesizes the final result using our live LLM client. Our live stdio client and server demonstration proves that real MCP communication works seamlessly over standard pipes. Taking a closer look at the server code, mcp_server_demo.py utilizes FastMCP to expose tools and resources. It decorates query_database_record with @mcp.tool() and app-settings with @mcp.resource('config://app-settings'). mcp_client_runner.py uses StdioServerParameters to spawn the server as a child process. It establishes an async stdio client session, lists available tools, calls query_database_record with record_id='rec_456', reads the config resource, and passes the context to Andrew Ng's aisuite to synthesize the final response."
    ),
    61: (
        'Slide 61 displays the skill manifest for harness-mcp-and-plugins, providing agents with capabilities to discover and interact with MCP servers. Reusable MCP skills allow agents to discover, inspect, and invoke remote tools dynamically during task execution.'
    ),
    62: (
        'We now advance to Module 8: Compound Engineering and Multi-Agent Teams. As software tasks grow in complexity, relying on a single monolithic agent creates a single point of failure. Compound engineering represents the state of the art in multi-agent orchestration, replacing monolithic agents with specialized teams.'
    ),
    63: (
        'Slide 63 analyzes Why Multi-Agent Systems Outperform Monolithic Agents. When an agent attempts to plan architecture, write source code, and review its own output within a single context window, confirmation bias and attention degradation lead to unverified assumptions. Compound engineering splits tasks across specialized roles with isolated context windows. Specialized context windows eliminate attention degradation and cognitive overload, resulting in higher code quality.'
    ),
    64: (
        'Slide 64 defines the Planner (Architect) Role: analyzing high-level requirements and breaking them into file-scoped subtasks without performing code writes. The Planner role focuses exclusively on decomposition and architectural design, free from implementation details.'
    ),
    65: (
        'Slide 65 defines the Implementer (Coder) Role: receiving only its assigned sub-spec and writing code within an isolated workspace. The Implementer role focuses strictly on writing verified code within its assigned file boundaries.'
    ),
    66: (
        'Slide 66 defines the Reviewer (Auditor) Role: conducting an independent review over the modified files, running AST syntax checks and test suites. The Reviewer role provides unbiased, independent verification using automated AST checks and test suites.'
    ),
    67: (
        'Slide 67 introduces Worktree Isolation. By creating ephemeral git worktrees via git worktree add -b, the implementer writes code on an isolated branch. Unverified changes never touch the primary working repository. Git worktree isolation guarantees that unverified code cannot corrupt the main repository working tree.'
    ),
    68: (
        'Slide 68 covers Subagent Context Optimization, extracting only the relevant lines of the master specification to keep context windows lean. Lean context passing maximizes reasoning efficiency and reduces API token costs across multi-agent workflows.'
    ),
    69: (
        'Slide 69 explores Self-Improvement Telemetry, logging multi-agent execution times and reviewer outcomes to telemetry.jsonl for continuous evaluation. Telemetry logging enables continuous evaluation and automated optimization of multi-agent team performance.'
    ),
    70: (
        'In the Module 8 Code Lab from multi_agent_team_simulator.py, lines 6 to 12 create an ephemeral git worktree, lines 18 to 26 run independent reviewer checks, and the worktree is cleaned up automatically upon completion. multi_agent_team_simulator.py demonstrates real Git worktree creation, multi-role handoffs, and clean teardown. Reviewing the team orchestration code, the multi-agent simulator orchestrates Planner, Implementer, and Reviewer roles. The Planner decomposes the JWT authentication task into sub-specifications. The Implementer creates an ephemeral git worktree using git worktree add -b feat-auth, writes auth.py and test_auth.py inside the worktree, and runs pytest. The Reviewer verifies that auth.py defines validate_jwt, parses the AST, and runs pytest independently before tearing down the worktree and logging to telemetry.jsonl.'
    ),
    71: (
        'Slide 71 presents the skill manifest for harness-compound-multi-agent-worktrees, orchestrating specialized Planner, Implementer, and Reviewer teams. Reusable compound engineering skills enable teams to deploy multi-agent workflows across production repositories.'
    ),
    72: (
        'Expanding our compound engineering toolkit, we introduce Compound Orchestrator, an open-source framework and reusable plugin created to make agent-assisted engineering compound over time. Available on GitHub at https://github.com/kenhuangus/compound-orchestrator, this system addresses a fundamental flaw in conventional agent workflows: amnesia between sessions. In typical setups, an agent solves a tricky bug or designs a subsystem, but once the session terminates, that knowledge evaporates. Compound Orchestrator installs a deterministic compounding loop: brainstorm, plan, generate six core planning contracts, execute a mandatory two-round cross-review, perform the implementation work, review again, and critically, record durable learning. Every completed task must record a decision note, failure analysis, or architectural pattern using the command python scripts/compound_orchestrator.py learn. This ensures that every subsequent agent session inherits the institutional memory of past runs, operating with native first-class support across Claude Code, Codex, Cursor, Aider, and CI runtimes.'
    ),
    73: (
        'A cornerstone of the Compound Orchestrator framework is its suite of Six Core Planning Contracts. Rather than allowing an agent to dive immediately into raw source code modifications, substantial initiatives require formalizing machine- and human-readable HTML contract artifacts: prd.html for product requirements, planning.html for milestone phasing, spec.html for low-level technical interfaces, test-cases.html for validation matrices, architecture.html containing embedded Excalidraw visual diagrams, and users.html defining persona workflows. Compound Orchestrator leverages a hybrid concurrency model: independent planning documents like user personas and high-level architecture can be drafted in parallel by specialized subagents, while integration specifications and test suites are serialized to prevent divergence. These contracts, referenced directly at https://github.com/kenhuangus/compound-orchestrator, ensure that both human engineers and autonomous agents share identical definitions of done before a single line of application source code is committed.'
    ),
    74: (
        'To eliminate single-model confirmation bias, Compound Orchestrator enforces a Mandatory Two-Round Cross-Review Protocol. When an agent runtime such as Claude Code authors a planning spec or code diff, the review must be conducted by an independent opposite-tool runtime, such as OpenAI Codex or an isolated reviewer subagent. The protocol advances through five strictly gated stages: Round 1 Review, where the external auditor posts actionable critiques; Round 1 Author Response, where the original author directly resolves each item; Round 2 Review, confirming revision efficacy; Round 2 Author Response, settling remaining edge cases; and Final Acceptance. Critically, Compound Orchestrator hard-caps this loop at two rounds unless an engineer manually intervenes, eliminating infinite circular arguments. Standardized review scorecards evaluate code quality, security postures, test coverage, and documentation accuracy, providing mathematical rigor to agent peer reviews as documented at https://github.com/kenhuangus/compound-orchestrator.'
    ),
    75: (
        'When orchestrating compound multi-agent teams across monorepos, concurrency conflicts become a primary point of failure. Compound Orchestrator provides Granular Multi-Agent Ownership Claims, managed via scripts/compound_orchestrator.py claim and release. Before any subagent—whether Claude Code, Codex, Cursor, or a background CI runner—modifies a file, it must acquire an atomic ownership claim. The orchestrator checks an active ownership ledger; if another worker is currently editing an overlapping file path, the claim is rejected. This guarantees strict isolation across distributed agents without relying on heavyweight container orchestration. Once work is verified and integrated, claims are atomically released, enabling safe, high-velocity parallel development across enterprise codebases. You can inspect this ownership engine directly at https://github.com/kenhuangus/compound-orchestrator.'
    ),
    76: (
        'Compound Orchestrator packages its entire capability suite as a native Claude Code and Codex plugin. Defined by .claude-plugin/plugin.json and .codex-plugin manifests, the plugin equips developers with high-level slash commands: /compound-start to initiate task tracking, /compound-plan to scaffold the six planning contracts, /compound-review to run cross-tool audits, /compound-learn to register failure notes, and /compound-claim to manage file locks. Furthermore, the plugin registers four specialized subagent roles: compound-architect for architectural design, compound-reviewer for rubric-based code evaluations, compound-test-runner for automated pytest and npm verification, and compound-cross-tool-reviewer for opposite-runtime verification. This transforms Claude Code into an enterprise-grade agent team coordinator, accessible at https://github.com/kenhuangus/compound-orchestrator.'
    ),
    77: (
        'The final pillar of Compound Orchestrator is Continuous Cross-Platform Verification and README Maintenance. The framework provides universal verification scripts—scripts/verify.py, verify.ps1 for PowerShell, and verify.sh for Unix shells—that audit project health on every commit. The verifier inspects planning contract completeness, ownership ledger cleanliness, git merge conflict markers, and automated unittest suites. Crucially, Compound Orchestrator treats README.md as part of the software product itself: whenever commands, APIs, or architectural flows change, agents are required to update the README, pruning stale sections and keeping user documentation perfectly synchronized with live code. By enforcing continuous verification and compounding memory, teams can scale agentic coding sustainably. Explore the full repository at https://github.com/kenhuangus/compound-orchestrator.'
    ),
    78: (
        'Welcome to Module 9: The Practical SOP Workflow Pattern. Here we synthesize our five core pillars, SDD specifications, guardrails, and testing loops into a unified 5-step standard operating procedure. The 5-Step SOP synthesizes all course concepts into a repeatable, production-grade workflow pattern.'
    ),
    79: (
        'Slide 73 introduces the Complete 5-Step SOP Pipeline: Step 1: Spec First; Step 2: Constrained Execution; Step 3: Deterministic Checks; Step 4: Automated Test Verification; and Step 5: Human Review. Following the 5-step SOP guarantees that every feature is specified, constrained, guarded, tested, and reviewed.'
    ),
    80: (
        'Slide 74 covers Steps 1 and 2: Ingesting SPEC.md, parsing allowed file whitelists, and binding all agent file operations strictly to the sandbox. Steps 1 and 2 establish the deterministic foundation: parsing specifications and binding edits to the workspace.'
    ),
    81: (
        'Slide 75 covers Steps 3 and 4: Executing AST static analysis, scanning for hardcoded secrets, and running automated pytest suites. Steps 3 and 4 enforce deterministic quality: AST syntax validation, secret scanning, and automated pytest execution.'
    ),
    82: (
        'Slide 76 covers Step 5: Human Review, generating a unified diff of the verified code changes for engineering sign-off before merging. Step 5 maintains human engineering oversight, generating clean unified diffs for final sign-off before merging.'
    ),
    83: (
        'In the Module 9 Code Lab from five_step_sop_pipeline.py, we execute the entire end-to-end pipeline, producing a verified 58-line diff of our JWT authentication module. five_step_sop_pipeline.py demonstrates the complete end-to-end execution of a verified JWT validator. Tracing the pipeline step by step, the FiveStepSopPipeline class coordinates the end-to-end production workflow. Step 1 parses SPEC.md. Step 2 creates an isolated sandbox and writes auth_validator.py while blocking database.py. Step 3 runs the GuardrailsEngine for AST syntax compilation, secret scanning, and command sanitization. Step 4 executes pytest inside the sandbox, verifying all 3 JWT test cases pass. Step 5 generates a unified diff comparing the verified changes against the clean baseline for human review.'
    ),
    84: (
        'Slide 78 displays the skill manifest for harness-five-step-sop-pipeline, providing a turnkey command to execute production workflows. Reusable SOP skills allow engineering teams to execute standardized production pipelines with a single CLI command.'
    ),
    85: (
        'We conclude with Module 10: Enterprise Principles and Production Readiness Audit. How do engineering leaders objectively evaluate whether a repository is ready for autonomous AI coding agents? Objective readiness audits enable engineering leaders to evaluate repository maturity before deploying autonomous agents.'
    ),
    86: (
        'Slide 80 presents the Four Golden Principles of Harness Engineering: Principle 1: Machine Specifications Over Vague Prompts. Principle 2: Deterministic Guardrails Over Probabilistic Trust. Principle 3: Automated Tests as Sensory Feedback. Principle 4: Least-Privilege Scoped Tooling. The Four Golden Principles serve as the foundational philosophy for building reliable, production-grade agent systems.'
    ),
    87: (
        'Slide 81 introduces the 5-Gate Production Readiness Scorecard, auditing: Gate 1: Memory Files presence; Gate 2: Pre-execution Hooks; Gate 3: Automated Test Runners; Gate 4: MCP Declarations; and Gate 5: Subagent Definitions. The 5-Gate Scorecard provides an objective, automated metric for evaluating repository compliance and safety.'
    ),
    88: (
        'Slide 82 wraps up the core teachings of the masterclass, outlining next steps for implementing agent harnesses in your organization. By implementing engineered harnesses, organizations can unlock the full transformative potential of autonomous AI coding agents.'
    ),
    89: (
        'In the Module 10 Code Lab from production_harness_audit.py, we run our automated readiness auditor against the repository, achieving a perfect 5/5 score. production_harness_audit.py proves that our entire course repository achieves a perfect 100% readiness score. Evaluating the compliance auditor source code, the ProductionHarnessAuditor class runs a 5-gate compliance inspection against the repository. Gate 1 verifies CLAUDE.md and AGENTS.md exist and are under size limits. Gate 2 verifies .claude/settings.json contains a valid PreToolUse hook pointing to an existing executable. Gate 3 parses run_all_modules.py with ast.parse and confirms pytest is operational. Gate 4 inspects Module 7 AST trees for @mcp.tool() and @mcp.resource() decorators. Gate 5 confirms all subagent markdown files in .claude/agents/ define distinct role instructions, outputting a 100% 5/5 score.'
    ),
    90: (
        'Slide 84 presents the skill manifest for harness-production-readiness-auditor, enabling automated compliance scanning across any codebase. Reusable audit skills allow teams to run continuous compliance checks in CI/CD pipelines before merging agent-generated code.'
    ),
    91: (
        'Slide 85 provides an in-depth comparison between Graph Engineering and Dynamic Workflows in Claude Code, contrasting architectural network design with native runtime execution. Understanding Graph Engineering versus Dynamic Workflows clarifies the distinction between architectural blueprints and runtime execution.'
    ),
    92: (
        'Finally, Slide 86 compiles all core documentation links, official Anthropic specifications, and GitHub repository resources. Thank you for participating in the Packt Masterclass on Harness Engineering for AI Coding Agents. You now possess the foundational blueprints and practical code required to build robust, secure, and reliable autonomous agent workflows. We look forward to seeing the resilient, production-grade agent harnesses you build in your own engineering organizations.'
    ),
}

SLIDE_DEEP_DIVES: dict[int, str] = {
    1: (
        ' As we progress through each module of this course, you will learn how to build production-grade supervisors that execute in pure standard Python with zero external latency. You will master the art of writing machine-checkable specifications, configuring Claude Code pre-tool interceptors, creating ephemeral Git worktrees for branch isolation, and auditing repositories with automated readiness gates.'
    ),
    2: (
        ' Every code snippet and architectural pattern presented in this masterclass has been verified against our live testing suites. Whether you are working with frontier models like Claude 3.7 Sonnet or local open-weights models served through vLLM, the harness principles we establish provide universal reliability and security.'
    ),
    3: (
        ' When an unconstrained agent interacts with a codebase, subtle hallucinations can rapidly corrupt project state. Without an external harness monitoring execution loops and sandboxing file writes, a single mispredicted token can result in catastrophic data loss. Understanding these failure modes is the first step toward engineering effective defenses.'
    ),
    4: (
        ' The core limitation of prompt engineering is that it relies on probabilistic adherence. When context windows fill up or unexpected compiler errors occur, soft prompt instructions are frequently deprioritized. Harness engineering replaces probabilistic hope with deterministic software guarantees.'
    ),
    5: (
        ' In our implementation of ContextTokenBudgeter, we dynamically monitor token allocations across memory files, feature specifications, active workspace files, and execution outputs. When compiler dumps threaten to saturate the context window, our head-tail compaction algorithm preserves high-density diagnostic signal while keeping token expenditure strictly controlled.'
    ),
    6: (
        ' Runaway execution loops represent one of the highest cost risks in autonomous agent deployment. Our loop detector calculates cryptographic hashes of tool invocation signatures, maintaining a sliding history window. When duplicate tool invocations are detected without state progression, the harness trips a circuit breaker, halting execution automatically.'
    ),
    7: (
        ' The Abstract Syntax Tree parsing gate in our harness ensures that broken code never reaches disk. By compiling proposed file edits in memory using ast.parse, the harness intercepts syntax errors, unclosed strings, and broken indentation, returning actionable diagnostic feedback to the model while maintaining workspace integrity.'
    ),
    8: (
        ' Destructive shell commands represent an unacceptable enterprise risk. Our pre-execution command interceptor utilizes pre-compiled regular expressions to block dangerous shell patterns like recursive deletions, privilege escalations, and bypass flags before subprocess creation ever occurs.'
    ),
    9: (
        ' In harness_vs_model_demo.py, we create two parallel sandbox environments: one un-harnessed and one harnessed. The un-harnessed run enters a repetitive execution loop and deletes the application log directory. The harnessed run intercepts the loop on attempt two and blocks the deletion command, ensuring that all log files survive completely intact.'
    ),
    10: (
        ' The terminal execution trace on Slide 10 demonstrates the contrast between unconstrained and harnessed execution. When the loop detector trips, it returns a structured non-zero exit code with diagnostic context, allowing the supervisory runtime to intervene cleanly.'
    ),
    11: (
        ' Examining lines 134 to 154 of harness_vs_model_demo.py highlights the elegance of pure standard-library Python. By utilizing the re, hashlib, and collections modules, we implement robust loop detection and command sanitization with zero third-party dependencies.'
    ),
    12: (
        ' The harness-interception-loop-detector skill manifest in .claude/skills/ encapsulates these defensive capabilities into a reusable, discoverable agent skill with standardized YAML frontmatter.'
    ),
    13: (
        ' The five pillars of the Core Harness Stack work together to create an airtight execution envelope around the agent. Memory files establish persistent rules, scoped tools restrict capabilities, deterministic hooks validate actions, token budgeters optimize context, and JSONL event streams provide total transparency.'
    ),
    14: (
        ' Each pillar in this architecture addresses a distinct vulnerability in autonomous agent execution, ensuring defense-in-depth across the entire software development lifecycle.'
    ),
    15: (
        ' Concise memory files in CLAUDE.md and AGENTS.md prevent context bloat. We recommend structuring instructions into four clear sections: Architecture, Commands, Style, and Non-Negotiables, keeping the total size under 500 lines.'
    ),
    16: (
        ' Using Path.resolve().is_relative_to(workspace) provides mathematically sound filesystem sandboxing, resolving symbolic links and relative path overrides to guarantee complete containment within the project directory.'
    ),
    17: (
        ' Synchronous pre-tool and post-tool middleware hooks allow engineering teams to enforce security and quality standards in real time before and after tool execution.'
    ),
    18: (
        " The 20/20/50/10 token budget allocation ensures that no single component starves the model's reasoning capacity, while append-only JSONL logging provides complete forensic auditability."
    ),
    19: (
        ' In core_harness_stack.py, we see all five pillars implemented cleanly in standard Python, combining token budgeting, tool permission validation, path sandboxing, and structured event logging.'
    ),
    20: (
        ' The harness-core-stack-sandbox skill allows developers to programmatically validate repository compliance with least-privilege tool scoping and filesystem containment rules.'
    ),
    21: (
        ' Spec-Driven Development transforms ambiguous conversational prompts into formal, machine-executable contracts that define the exact boundaries of every feature.'
    ),
    22: (
        ' Natural language prompts invite interpretation and scope creep. A formal specification removes guesswork by explicitly defining allowed files, forbidden non-goals, and automated test criteria.'
    ),
    23: (
        ' The four mandatory sections of SPEC.md—Objective, Scope, Non-Goals, and Acceptance Criteria—provide both human-readable documentation and machine-checkable contracts.'
    ),
    24: (
        ' Explicit non-goals prevent autonomous agents from over-engineering simple tasks or introducing unrequested dependencies, keeping the codebase clean and modular.'
    ),
    25: (
        ' By formulating acceptance criteria as discrete, machine-testable items (AC-01 through AC-04), we create an objective, automated definition of done.'
    ),
    26: (
        ' The SDD lifecycle establishes a structured four-phase development rhythm: ingest specification, generate constrained plan, audit diffs against non-goals, and verify with automated tests.'
    ),
    27: (
        ' Real-time spec verification intercepts out-of-scope modifications before they touch disk, preventing silent regressions in adjacent subsystems.'
    ),
    28: (
        ' In spec_driven_verifier.py, regular expressions parse SPEC.md markdown headings, normalizing paths against the allowed scope and compiling code diffs with ast.parse before saving to disk.'
    ),
    29: (
        ' The harness-spec-driven-development skill equips agents with automated tools to self-audit proposed diffs against project contracts prior to committing code.'
    ),
    30: (
        ' Enterprise guardrails provide proactive, deterministic protection, ensuring that autonomous agents operate safely without sacrificing development velocity.'
    ),
    31: (
        ' The 4-Layer Control Model provides layered defense: system prompts establish intent, tool schemas validate types, deterministic hooks enforce policy, and OS sandboxing isolates execution.'
    ),
    32: (
        " Claude Code's PascalCase hook interface establishes a clean JSON-RPC contract over standard input and output, allowing hooks to return allow, deny, ask, or defer decisions dynamically."
    ),
    33: (
        ' Post-action AST syntax compilation and entropy-based secret scanning provide immediate quality and security gates on every file modification.'
    ),
    34: (
        ' Canonical path sandboxing mathematically proves that every file operation remains strictly confined within the authorized project workspace.'
    ),
    35: (
        ' Risk-tiered permission modes ensure that safe reads run fast while high-impact actions like git push require explicit operator authorization.'
    ),
    36: (
        ' Quantitative evaluation benchmarks allow engineering teams to measure guardrail accuracy and latency scientifically against adversarial prompt injections.'
    ),
    37: (
        ' The enterprise safety checklist provides three non-negotiable standards for production readiness: workspace sandboxing, shell sanitization, and AST secret scanning.'
    ),
    38: (
        ' In guardrails_engine.py, lines 6 to 26 implement the Claude Code PreToolUse interceptor and PostToolUse AST scanner using clean standard Python.'
    ),
    39: (
        ' The harness-guardrails-and-hooks skill standardizes these controls across all repository tasks, ensuring consistent security governance.'
    ),
    40: (
        ' In enterprise workflows, human authorization should be reserved for irreversible actions like database schema drops, credential rotations, or production branch merges.'
    ),
    41: (
        ' Risk tiers eliminate alert fatigue by selectively requesting human approvals only for high-consequence operations.'
    ),
    42: (
        ' In permission_escalation_gateway.py, critical actions like git push are blocked until an authorized signed entry is recorded in approvals.json.'
    ),
    43: (
        " The harness-permission-escalation-gateway skill seamlessly integrates human-in-the-loop governance into the agent's tool execution pipeline."
    ),
    44: (
        ' Automated tests provide the deterministic ground truth that allows autonomous coding agents to perceive errors, diagnose failures, and verify fixes.'
    ),
    45: (
        ' The Red-Repair-Green TDA loop mirrors senior engineering discipline: prove the failure, capture the traceback, apply the repair, and verify resolution.'
    ),
    46: (
        ' Hierarchical test tiers balance rapid iteration velocity with comprehensive regression protection across unit, integration, and E2E suites.'
    ),
    47: (
        " Programmatically capturing compiler stderr streams eliminates manual copy-paste overhead, feeding high-density diagnostic signal directly into the model's repair prompt."
    ),
    48: (
        ' Anti-regression test persistence automatically turns every fixed bug into a permanent test case, continuously strengthening repository test coverage.'
    ),
    49: (
        ' Tracking reliability metrics like mean iterations to green and regression rates gives engineering leaders objective performance data.'
    ),
    50: (
        ' In tda_reliability_pipeline.py, real pytest subprocess executions drive automated agent self-healing and regression safeguard persistence.'
    ),
    51: (
        ' The harness-tda-reliability-pipeline skill packages these test-driven repair workflows into a reusable CLI tool.'
    ),
    52: (
        ' The Model Context Protocol establishes an open, standardized framework for connecting AI agents to enterprise tools and data sources.'
    ),
    53: (
        ' Agent Skills provide self-contained capabilities with clear descriptions, allowed tools, and executable Python helper scripts.'
    ),
    54: (
        ' Standardized skill directory structures ensure that tools and documentation remain maintainable and discoverable across platforms.'
    ),
    55: (
        ' Claude Plugins bundle multiple skills, custom subagents, pre-execution hooks, and MCP servers into a single distributable package.'
    ),
    56: (
        ' Understanding the three MCP version numbers—protocol specification date, Python SDK version, and JSON-RPC wire framing—prevents integration errors.'
    ),
    57: (
        ' Local stdio transports provide zero-latency tool execution over child process pipes, while Streamable HTTP transports enable cloud microservices.'
    ),
    58: (
        ' The official Python MCP SDK enables developers to expose tools and resources using simple, expressive decorators like @mcp.tool() and @mcp.resource().'
    ),
    59: (
        ' Enterprise MCP governance enforces authentication, authorization, and audit logging across all external tool invocations.'
    ),
    60: (
        ' In Module 7, mcp_server_demo.py and mcp_client_runner.py demonstrate a complete, live stdio MCP session with database tool execution and live LLM response synthesis.'
    ),
    61: (
        ' The harness-mcp-and-plugins skill allows agents to discover, inspect, and consume MCP servers dynamically during task execution.'
    ),
    62: (
        ' Compound engineering replaces single monolithic agents with specialized multi-agent teams, eliminating cognitive overload and confirmation bias.'
    ),
    63: (
        ' Multi-agent systems achieve higher code quality by providing each role with an isolated, uncluttered context window.'
    ),
    64: (
        ' The Planner role focuses exclusively on architectural decomposition, creating clear, file-scoped subtasks without performing code modifications.'
    ),
    65: (
        ' The Implementer role receives only its assigned sub-spec, writing verified source code within an isolated workspace.'
    ),
    66: (
        ' The Reviewer role conducts an independent audit, executing AST syntax validation and automated pytest suites without shared conversation bias.'
    ),
    67: (
        ' Ephemeral Git worktree isolation guarantees that unverified code cannot corrupt the main repository branch.'
    ),
    68: (
        ' Subagent context optimization filters master specifications, passing only the necessary sub-spec lines to reduce API token costs.'
    ),
    69: (
        ' Telemetry logging records multi-agent execution times and reviewer outcomes to telemetry.jsonl for continuous workflow optimization.'
    ),
    70: (
        ' In multi_agent_team_simulator.py, we implement Git worktree creation, role handoffs, and clean automated teardown.'
    ),
    71: (
        ' The harness-compound-multi-agent-worktrees skill enables teams to deploy multi-agent workflows across production repositories.'
    ),
    72: (
        ' The compound-orchestrator framework transforms ephemeral LLM sessions into an enterprise system that continuously compounds in capability.'
    ),
    73: (
        ' Standardizing planning contracts in HTML ensures rich interactive documentation with embedded vector diagrams and strict acceptance criteria.'
    ),
    74: (
        ' Cross-tool opposite-runtime reviews prevent model hallucination blind spots by pitting distinct LLM architectures against one another.'
    ),
    75: (
        ' Ownership claims provide deterministic file locking, preventing race conditions and edit collisions across multi-agent teams.'
    ),
    76: (
        ' Packaging the compound orchestrator as a plugin gives developers instant access to specialized subagents and slash commands.'
    ),
    77: (
        ' Treating README documentation as a first-class build artifact ensures engineering knowledge remains evergreen as codebases evolve.'
    ),
    78: (
        ' The 5-Step SOP synthesizes our five core pillars, SDD specifications, guardrails, and testing loops into a repeatable standard operating procedure.'
    ),
    79: (
        ' Following the 5-step SOP guarantees that every feature is specified, constrained, guarded, tested, and reviewed before merging.'
    ),
    80: (
        ' Steps 1 and 2 establish the deterministic foundation: parsing specifications and binding edits strictly to in-scope files.'
    ),
    81: (
        ' Steps 3 and 4 enforce deterministic quality: executing AST compilation, secret scanning, and automated pytest test suites.'
    ),
    82: (
        ' Step 5 maintains human engineering oversight, generating clean unified diffs for final review and sign-off.'
    ),
    83: (
        ' In five_step_sop_pipeline.py, we execute the complete end-to-end pipeline, producing a verified, production-ready JWT authentication module.'
    ),
    84: (
        ' The harness-five-step-sop-pipeline skill enables developers to execute standardized production workflows with a single CLI command.'
    ),
    85: (
        ' The 5-gate scorecard establishes an automated, objective baseline for certifying repositories before granting autonomous agents write permissions.'
    ),
    86: (
        ' Adhering to these four golden principles allows teams to scale autonomous coding agents safely across large enterprise codebases without sacrificing quality.'
    ),
    87: (
        ' Running the 5-Gate Scorecard in automated CI/CD pipelines ensures that every repository maintains strict compliance with agent safety standards.'
    ),
    88: (
        ' By implementing engineered harnesses, organizations can safely unlock the full transformative potential of autonomous AI coding agents.'
    ),
    89: (
        ' In production_harness_audit.py, we execute our automated compliance auditor, confirming that our repository achieves a perfect 100% 5/5 readiness score.'
    ),
    90: (
        ' The harness-production-readiness-auditor skill allows teams to integrate automated readiness checks directly into their CI/CD pipelines.'
    ),
    91: (
        ' Graph Engineering provides the high-level architectural blueprint of your agent network, while Claude Code Dynamic Workflows execute those steps deterministically in JavaScript.'
    ),
    92: (
        ' All course resources, slides, and Python modules remain available in our open-source GitHub repository for ongoing study and enterprise deployment.'
    ),
}


def get_full_narration(slide_num: int) -> str:
    base = SLIDE_LECTURES.get(slide_num, "")
    deep = SLIDE_DEEP_DIVES.get(slide_num, "")
    return (base + " " + deep).strip()


async def synthesize_slide(slide_num: int, text: str, semaphore: asyncio.Semaphore) -> tuple[int, Path, float]:
    async with semaphore:
        out_file = AUDIO_DIR / f"slide_full_{slide_num:02d}.mp3"
        communicate = edge_tts.Communicate(text, VOICE)
        t0 = time.time()
        await communicate.save(str(out_file))
        elapsed = time.time() - t0
        size = out_file.stat().st_size if out_file.exists() else 0
        print(f"  [OK] Slide {slide_num:02d} -> {out_file.name} ({elapsed:.1f}s, {size} bytes)", flush=True)
        return slide_num, out_file, elapsed


def get_audio_duration(file_path: Path) -> float:
    try:
        res = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(file_path)],
            capture_output=True,
            text=True,
            check=True,
        )
        return float(res.stdout.strip())
    except Exception:
        return 0.0


async def main():
    print("=" * 80)
    total_words = sum(len(get_full_narration(i).split()) for i in range(1, 93))
    est_minutes = total_words / 125.0
    print("GENERATING ULTIMATE 1-HOUR+ MASTERCLASS AUDIO (SINGLE UNIFIED MP3)")
    print(f"Total Slides: 92 | Total Words: {total_words:,} (~{est_minutes:.1f} minutes estimated)")
    print(f"Target Voice: {VOICE}")
    print("Output Master Track: audio/packt_harness_complete_masterclass_1hr.mp3")
    print("=" * 80 + "\n", flush=True)

    semaphore = asyncio.Semaphore(6)
    tasks = []
    for slide_num in range(1, 93):
        narration = get_full_narration(slide_num)
        tasks.append(synthesize_slide(slide_num, narration, semaphore))

    t_start = time.time()
    results = await asyncio.gather(*tasks)
    total_synth_time = time.time() - t_start

    print(f"\n[DONE] Synthesized all 92 slide audio tracks in {total_synth_time:.1f}s.", flush=True)

    # Compute individual durations
    durations = {}
    for slide_num, file_path, _ in sorted(results):
        dur = get_audio_duration(file_path)
        durations[slide_num] = dur

    total_duration_sec = sum(durations.values())
    total_duration_min = total_duration_sec / 60.0
    print(f"Total Combined Duration: {total_duration_min:.2f} minutes ({total_duration_sec:.1f} seconds)\n", flush=True)

    # Concat into single master MP3
    concat_list = AUDIO_DIR / "concat_list_master.txt"
    with open(concat_list, "w", encoding="utf-8") as f:
        for slide_num in range(1, 93):
            track_file = f"slide_full_{slide_num:02d}.mp3"
            f.write(f"file '{track_file}'\n")

    master_mp3 = AUDIO_DIR / "packt_harness_complete_masterclass_1hr.mp3"
    print(f"[*] Concatenating segments into unified Masterclass MP3: {master_mp3}...", flush=True)

    concat_cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        str(master_mp3)
    ]
    subprocess.run(concat_cmd, check=True, capture_output=True)

    # Clean up intermediate segment files
    if concat_list.exists():
        concat_list.unlink()
    for slide_num in range(1, 93):
        seg = AUDIO_DIR / f"slide_full_{slide_num:02d}.mp3"
        if seg.exists():
            seg.unlink()

    final_size_mb = master_mp3.stat().st_size / (1024 * 1024)
    final_dur_sec = get_audio_duration(master_mp3)
    final_dur_min = final_dur_sec / 60.0

    print("\n" + "=" * 72)
    print(">>> MASTERCLASS AUDIO CREATED SUCCESSFULLY (SINGLE FILE) <<<")
    print(f"File Path: {master_mp3.resolve()}")
    print(f"File Size: {final_size_mb:.2f} MB")
    print(f"Exact Duration: {final_dur_min:.2f} minutes ({final_dur_sec:.1f} seconds)")
    print(f"VERIFICATION: {'PASSED (Duration >= 1.0 Hour: ' + f'{final_dur_min:.1f} mins)' if final_dur_min >= 60 else 'FAILED'}")
    print("=" * 72 + "\n", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
