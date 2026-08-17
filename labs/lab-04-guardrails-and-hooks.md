# Lab 04 — Guardrails and Hooks

**Skill:** `harness-guardrails-and-hooks`  
**Module:** [module_04_guardrails_and_hooks](https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_04_guardrails_and_hooks)  
**Time:** 35 minutes

## What you will end up with
You will have a working PreToolUse hook check that allows safe commands and denies dangerous flags with structured JSON.

## Before you start
Use your own repository for hook registration, and keep this repo available to run the reference hook script.  
This lab does not require live generation.

## Steps
1. Add a PreToolUse hook entry in your own `.claude/settings.json` that points to your copied hook script.

```bash
cd /path/to/your-repo
```

2. Send a safe payload to the hook script and capture the JSON decision.

```bash
python -c 'import json,subprocess,sys; payload=json.dumps({"tool_name":"Bash","tool_input":{"command":"pytest -q"}}); r=subprocess.run([sys.executable,"/path/to/packt-harness/.claude/skills/harness-guardrails-and-hooks/scripts/hook_pre_tool_use.py"],input=payload,text=True,capture_output=True); print(r.stdout.strip())'
```

3. Send a dangerous payload to the same script and capture the deny decision.

```bash
python -c 'import json,subprocess,sys; payload=json.dumps({"tool_name":"Bash","tool_input":{"command":"npm install --dangerously-skip-permissions"}}); r=subprocess.run([sys.executable,"/path/to/packt-harness/.claude/skills/harness-guardrails-and-hooks/scripts/hook_pre_tool_use.py"],input=payload,text=True,capture_output=True); print(r.stdout.strip())'
```

4. Run the full module guardrails demo once.

```bash
cd /path/to/packt-harness
python course_implementation/module_04_guardrails_and_hooks/guardrails_engine.py
```

## Expected output
Real captured output:

```text
{"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "allow"}}
{"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": "Prohibited CLI flag '--dangerously-skip-permissions'."}}
```

## Break it on purpose
Set the command to include `-y` and run the hook again.

```bash
python -c 'import json,subprocess,sys; payload=json.dumps({"tool_name":"Bash","tool_input":{"command":"rm -rf build -y"}}); r=subprocess.run([sys.executable,"/path/to/packt-harness/.claude/skills/harness-guardrails-and-hooks/scripts/hook_pre_tool_use.py"],input=payload,text=True,capture_output=True); print(r.stdout.strip())'
```

The hook should return `permissionDecision: "deny"` with a reason referencing the prohibited flag.

## You are done when
- Safe payload returns `permissionDecision: "allow"`.
- Dangerous payload returns `permissionDecision: "deny"`.
- The deny response includes `hookEventName: "PreToolUse"`.
- Your own `.claude/settings.json` points to a real hook script path.

## If it goes wrong
- If you get JSON parse errors, verify the payload is valid JSON with double quotes.
- If every command is allowed, check the hook script path and whether your editor reloaded settings.
- If the module demo fails, run it from `/path/to/packt-harness` exactly.
