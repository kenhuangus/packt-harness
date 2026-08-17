# Harness Skills — Live Demo Guide

## Before you start
- Open this folder in Claude Code.
- Keep your terminal at this folder root for every command below.
- One-line skills check to type in Claude Code:
  `List every loaded skill in .claude/skills that starts with harness-.`
- If that list is empty, stop and fix the workspace before demoing.

## How a skill demo works
- Beat 1: You type one natural sentence.
- Beat 2: You show `/skill-name` as the safe fallback.
- Beat 3: You run one command from this folder root.
- Beat 4: You read the terminal result, then break it on purpose.
- Keep saying the base-directory line out loud: "We run from repo root."
- That line is the key concept: reproducible paths, no hidden local setup.
- Students should see allow behavior and block behavior back to back.
- End each demo by naming the control they just watched.

## Demo 01 — Interception and Loop Detector
**Skill** `harness-interception-loop-detector`

**Say this** Audit shell commands and block retry loops while I run an automated test-fix cycle.

**Or invoke directly** `/harness-interception-loop-detector`

**The command it runs**
```bash
python .claude/skills/harness-interception-loop-detector/scripts/intercept_command.py --command "pytest -q" --json
```

**What appears**
```text
{
  "verdict": "ALLOW",
  "risk_level": "LOW",
  "reason": "ALLOWED: Command passed pattern and loop checks.",
  "loop_detected": false
}
```

**Break it**
```bash
python .claude/skills/harness-interception-loop-detector/scripts/intercept_command.py --command "pytest -q" --history "pytest -q" --history "pytest -q" --max-retries 2 --json
```
```text
{
  "verdict": "BLOCK",
  "risk_level": "HIGH",
  "reason": "BLOCKED: Detected 2 identical recent retries of 'pytest -q'. Change strategy instead of retrying the same command.",
  "loop_detected": true
}
```

**Say this out loud** This blocker is expected. A block exits non-zero on purpose so the loop cannot silently spin forever.

## Demo 02 — Core Stack Sandbox
**Skill** `harness-core-stack-sandbox`

**Say this** Enforce workspace boundaries and reject any write path that escapes the sandbox.

**Or invoke directly** `/harness-core-stack-sandbox`

**The command it runs**
```bash
python .claude/skills/harness-core-stack-sandbox/scripts/validate_sandbox.py --workspace "." --path "./.claude"
```

**What appears**
```text
Path containment: VALID
```

**Break it**
```bash
python .claude/skills/harness-core-stack-sandbox/scripts/validate_sandbox.py --workspace "." --path "../outside.py"
```
```text
Path containment: VIOLATION
```

**Say this out loud** A violation here is success for the guardrail. Non-zero exit is the correct outcome when path safety fails.

## Demo 03 — Spec Scope Gate
**Skill** `harness-spec-driven-development`

**Say this** Scope this task to allowed files only and reject edits that drift outside the spec contract.

**Or invoke directly** `/harness-spec-driven-development`

**The command it runs**
```bash
python .claude/skills/harness-spec-driven-development/scripts/verify_spec_scope.py
```

**What appears**
```text
[PASS] OK
```

**Break it**
```bash
python .claude/skills/harness-spec-driven-development/scripts/verify_spec_scope.py --allowed auth_validator.py tests/test_auth.py --file database.py --content "x"
```
```text
[FAIL] SCOPE VIOLATION: 'database.py' is not in allowed files ['auth_validator.py', 'tests/test_auth.py'].
```

**Say this out loud** This is how you stop architecture drift before it starts. If you run the full module with generation, local endpoint is `http://127.0.0.1:8000/v1`; fallback is PowerShell `$env:HARNESS_ALLOW_SIMULATED_LLM=1` or bash `export HARNESS_ALLOW_SIMULATED_LLM=1`.

## Demo 04 — Guardrails Hook PreToolUse
**Skill** `harness-guardrails-and-hooks`

**Say this** Configure a PreToolUse hook that inspects shell commands and denies dangerous flags before execution.

**Or invoke directly** `/harness-guardrails-and-hooks`

**The command it runs**
```bash
python -c "import json,subprocess,sys; payload=json.dumps({'tool_name':'Bash','tool_input':{'command':'pytest -q'}}); r=subprocess.run([sys.executable,'.claude/skills/harness-guardrails-and-hooks/scripts/hook_pre_tool_use.py'],input=payload,text=True,capture_output=True); print(r.stdout.strip())"
```

**What appears**
```text
{"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "allow"}}
```

**Break it**
```bash
python -c "import json,subprocess,sys; payload=json.dumps({'tool_name':'Bash','tool_input':{'command':'npm install --dangerously-skip-permissions'}}); r=subprocess.run([sys.executable,'.claude/skills/harness-guardrails-and-hooks/scripts/hook_pre_tool_use.py'],input=payload,text=True,capture_output=True); print(r.stdout.strip())"
```
```text
{"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": "Prohibited CLI flag '--dangerously-skip-permissions'."}}
```

**Say this out loud** The hook is a gate before command execution, not after damage. You get a deterministic allow or deny every time.

## Demo 05 — Permission Escalation Gateway
**Skill** `harness-permission-escalation-gateway`

**Say this** Gate sensitive operations by risk tier and require human approval tokens for critical actions.

**Or invoke directly** `/harness-permission-escalation-gateway`

**The command it runs**
```bash
python .claude/skills/harness-permission-escalation-gateway/scripts/evaluate_gateway.py
```

**What appears**
```text
Permission Escalation Gateway Evaluator active.
```

**Break it**
```bash
python -c "from pathlib import Path; import importlib.util; p=Path('.claude/skills/harness-permission-escalation-gateway/scripts/evaluate_gateway.py'); spec=importlib.util.spec_from_file_location('gw', p); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); print(m.evaluate('git_push','req_push_001','approvals.json'))"
```
```text
{'status': 'BLOCKED', 'reason': 'Requires human approval token in approvals.json'}
```

**Say this out loud** Critical actions do not proceed on intent alone. For full module generation runs, local endpoint is `http://127.0.0.1:8000/v1`; fallback is PowerShell `$env:HARNESS_ALLOW_SIMULATED_LLM=1` or bash `export HARNESS_ALLOW_SIMULATED_LLM=1`.

## Demo 06 — TDA Reliability Runner
**Skill** `harness-tda-reliability-pipeline`

**Say this** Run test-driven agent loops in isolated subprocesses and feed exact failures back into the repair step.

**Or invoke directly** `/harness-tda-reliability-pipeline`

**The command it runs**
```bash
python .claude/skills/harness-tda-reliability-pipeline/scripts/run_tda_loop.py
```

**What appears**
```text
TDA Subprocess runner ready.
```

**Break it**
```bash
python -c "import sys; from importlib.util import spec_from_file_location,module_from_spec; from pathlib import Path; p=Path('.claude/skills/harness-tda-reliability-pipeline/scripts/run_tda_loop.py'); s=spec_from_file_location('tda',p); m=module_from_spec(s); s.loader.exec_module(m); ok,out=m.run_pytest('tests/does_not_exist.py'); print(out.strip()); sys.exit(0 if ok else 1)"
```
```text
no tests ran in 0.47s
ERROR: file or directory not found: tests/does_not_exist.py
```

**Say this out loud** The failure text is the payload for repair. This is why test output must stay concise and real.

## Demo 07 — MCP Inspector
**Skill** `harness-mcp-and-plugins`

**Say this** Inspect MCP tools and resources over stdio to verify the server registration surface.

**Or invoke directly** `/harness-mcp-and-plugins`

**The command it runs**
```bash
python .claude/skills/harness-mcp-and-plugins/scripts/inspect_mcp_server.py
```

**What appears**
```text
[PASS] Connected to MCP server. Tools: ['query_database_record'], Resources: ['config://app-settings']
```

**Break it**
```bash
python .claude/skills/harness-mcp-and-plugins/scripts/inspect_mcp_server.py .claude/skills/harness-mcp-and-plugins/scripts/does_not_exist.py
```
```text
mcp.shared.exceptions.MCPError: Connection closed
```

**Say this out loud** Notice we did not `cd` anywhere first; this inspector works from the folder root. For module client runs that use generation, local endpoint is `http://127.0.0.1:8000/v1`; fallback is PowerShell `$env:HARNESS_ALLOW_SIMULATED_LLM=1` or bash `export HARNESS_ALLOW_SIMULATED_LLM=1`.

## Demo 08 — Compound Multi-Agent Worktrees
**Skill** `harness-compound-multi-agent-worktrees`

**Say this** Coordinate planner, implementer, and reviewer roles with isolated worktrees and explicit review handoffs.

**Or invoke directly** `/harness-compound-multi-agent-worktrees`

**The command it runs**
```bash
python .claude/skills/harness-compound-multi-agent-worktrees/scripts/worktree_manager.py
```

**What appears**
```text
Worktree manager ready.
```

**Break it**
```bash
python -c "import sys; sys.path.insert(0,'.claude/skills/harness-compound-multi-agent-worktrees/scripts'); import worktree_manager as wm; wm.create_worktree('.', 'demo-conflict', '.worktrees/demo-08')"
python -c "from pathlib import Path; main=Path('.git'); wt=Path('.worktrees/demo-08/.git'); print(f'main .git -> exists={main.exists()} is_file={main.is_file()} is_dir={main.is_dir()}'); print(f'worktree .git -> exists={wt.exists()} is_file={wt.is_file()} is_dir={wt.is_dir()}')"
python -c "import sys; sys.path.insert(0,'.claude/skills/harness-compound-multi-agent-worktrees/scripts'); import worktree_manager as wm; wm.remove_worktree('.', 'demo-conflict', '.worktrees/demo-08')"
```
```text
Preparing worktree (new branch 'demo-conflict')
HEAD is now at ffde42b Make skill invocations work from a plain clone on any platform
main .git -> exists=True is_file=False is_dir=True
worktree .git -> exists=True is_file=True is_dir=False
Deleted branch demo-conflict (was ffde42b).
```

**Say this out loud** The big lesson is reviewer isolation: run the reviewer in a fresh context, not the implementer context, or blind spots survive. The subtle gotcha is that worktrees store `.git` as a file pointer, so repo-root checks must use `.exists()` rather than `.is_dir()`. If you run real model-backed subagents, local endpoint is `http://127.0.0.1:8000/v1`; fallback is PowerShell `$env:HARNESS_ALLOW_SIMULATED_LLM=1` or bash `export HARNESS_ALLOW_SIMULATED_LLM=1`.

## Demo 09 — Five-Step SOP Pipeline
**Skill** `harness-five-step-sop-pipeline`

**Say this** Run the full five-gate SOP sequence from spec parsing through test verification and human diff review.

**Or invoke directly** `/harness-five-step-sop-pipeline`

**The command it runs**
```bash
python .claude/skills/harness-five-step-sop-pipeline/scripts/run_sop_pipeline.py
```

**What appears**
```text
[STEP 1: SPEC FIRST] Parsing SPEC.md requirements...
[STEP 2: CONSTRAINED EXECUTION] Enforcing the parsed allowed-file scope...
[STEP 3: DETERMINISTIC CHECKS] Running module 4 guardrails...
[STEP 4: TEST VERIFICATION] Running a real temporary pytest suite...
[PASS] Pytest suite: return code 0; 3 passed, 0 failed.
[STEP 5: HUMAN REVIEW] Showing the implementation actually produced...
PIPELINE COMPLETE: ALL REPORTED CHECKS EXECUTED AND PASSED
```

**Break it**
```bash
python -c "import sys,tempfile; from pathlib import Path; from course_implementation.module_09_practical_workflow_pattern.five_step_sop_pipeline import ScopeEnforcer; d=Path(tempfile.mkdtemp()); e=ScopeEnforcer(d,['auth_validator.py']); ok,reason=e.attempt_write('database.py','def x():\n    return 1\n'); print(reason); sys.exit(0 if ok else 1)"
```
```text
'database.py' is not in the allowed file scope.
```

**Say this out loud** The gate order matters. If scope fails early, you avoid wasted test and review cycles later.

## Demo 10 — Production Readiness Auditor
**Skill** `harness-production-readiness-auditor`

**Say this** Audit this repository against the five production gates, then compare with a bare folder to show readiness gap.

**Or invoke directly** `/harness-production-readiness-auditor`

**The command it runs**
```bash
python .claude/skills/harness-production-readiness-auditor/scripts/run_audit.py
```

**What appears**
```text
AUDIT SUMMARY: 5/5 Checks Passed (100% Production Readiness Score)
STATUS: ALL AUDITED READINESS CHECKS PASSED.
```

**Break it**
```bash
python -c "import tempfile,subprocess,sys; from pathlib import Path; d=Path(tempfile.gettempdir())/'harness-empty-audit'; d.mkdir(exist_ok=True); r=subprocess.run([sys.executable,'.claude/skills/harness-production-readiness-auditor/scripts/run_audit.py',str(d)]); sys.exit(r.returncode)"
```
```text
AUDIT SUMMARY: 0/5 Checks Passed (0% Production Readiness Score)
STATUS: READINESS GAPS FOUND; THE TARGET IS NOT FULLY READY.
```

**Say this out loud** This is the grading instrument for the course. On a bare folder it fails hard, and on this repo it passes all five gates.

## If a demo fails live
- **Failure:** wrong working directory.  
  **Recovery line:** "We reset to repo root, then rerun the same command."
- **Failure:** local model endpoint is down during model-backed module demos.  
  **Recovery line:** "I will use simulation fallback now: PowerShell `$env:HARNESS_ALLOW_SIMULATED_LLM=1`, bash `export HARNESS_ALLOW_SIMULATED_LLM=1`."
- **Failure:** command blocked and audience thinks it crashed.  
  **Recovery line:** "That non-zero exit is the control doing its job; block is the expected result."
