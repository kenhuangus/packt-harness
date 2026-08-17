# Lab 01 — Interception and Loop Detector Baseline

**Skill:** `harness-interception-loop-detector`  
**Module:** [module_01_why_harness_engineering](https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_01_why_harness_engineering)  
**Time:** 35 minutes

## What you will end up with
You will have a recorded session-1 baseline audit score for your own repository and a working command interceptor that blocks dangerous and repeated shell commands.

## Before you start
You need two local folders: your own project repo and this course repo. This lab runs against your own repo path for the audit, then uses this repo's script for interception checks.  
This lab does not require live generation. You do not need the local vLLM endpoint for these steps.

## Steps
1. Move into your own project repository and confirm the path.

```bash
cd /path/to/your-repo
pwd
```

2. Run the production-readiness auditor against your repo and record the score as your session-1 baseline.

```bash
python /path/to/packt-harness/.claude/skills/harness-production-readiness-auditor/scripts/run_audit.py "$(pwd)"
```

3. Save that baseline score in your own notes file so you can compare in Lab 10.

```bash
printf "session_1_baseline: <replace-with-your-score>\n" >> harness-lab-notes.txt
```

4. Run the interception script on a destructive command.

```bash
cd /path/to/packt-harness
python .claude/skills/harness-interception-loop-detector/scripts/intercept_command.py --command "rm -rf /tmp/data" --json
```

5. Run the interception script on a safe command.

```bash
python .claude/skills/harness-interception-loop-detector/scripts/intercept_command.py --command "pytest -q" --json
```

## Expected output
Your baseline audit output depends on your own repository, so that part is shape-only and should show a 5-check report with a final score line.

Real captured output from the interception command:

```text
{
  "verdict": "BLOCK",
  "risk_level": "CRITICAL",
  "reason": "BLOCKED: Destructive pattern '\\brm\\s+-[rR][fF]\\b' detected.",
  "loop_detected": false
}
```

## Break it on purpose
Run the same safe command with repeated history to trigger the loop detector.

```bash
python .claude/skills/harness-interception-loop-detector/scripts/intercept_command.py --command "pytest -q" --history "pytest -q" --history "pytest -q" --max-retries 2 --json
```

The skill should block it with `loop_detected: true` and a reason that says to change strategy instead of retrying.

## You are done when
- You saved a baseline audit score from your own repo before building other harness controls.
- A destructive command returns `verdict: BLOCK`.
- A repeated safe command is blocked by loop detection.
- A normal one-off safe command returns `verdict: ALLOW`.

## If it goes wrong
- If `python ...run_audit.py` fails, verify `pip install -e .` was run in this repo.
- If command paths fail, replace `/path/to/packt-harness` with the real absolute path.
- If a command that should block is allowed, verify you passed the exact command text shown above.
