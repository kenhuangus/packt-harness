# Lab 10 — Production Readiness Auditor

**Skill:** `harness-production-readiness-auditor`  
**Module:** [module_10_closing_and_principles](https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_10_closing_and_principles)  
**Time:** 35 minutes

## What you will end up with
You will produce a before/after readiness comparison for your own repository using the Lab 01 baseline and a final current audit score.

## Before you start
You must have your Lab 01 baseline score recorded from session 1. This lab is the post measurement and compares against that baseline.  
This audit script does not require live generation.

## Steps
1. Move into your own repository and find your saved Lab 01 baseline note.

```bash
cd /path/to/your-repo
grep "session_1_baseline" harness-lab-notes.txt
```

2. Run the auditor against your current repository state.

```bash
python /path/to/packt-harness/.claude/skills/harness-production-readiness-auditor/scripts/run_audit.py "$(pwd)"
```

3. Record your post score and compute the change from Lab 01.

```bash
printf "lab10_post_score: <replace>\nlab10_delta_from_baseline: <replace>\n" >> harness-lab-notes.txt
```

4. Run the auditor once in this repo as a reference implementation.

```bash
cd /path/to/packt-harness
python .claude/skills/harness-production-readiness-auditor/scripts/run_audit.py
```

## Expected output
Real captured output (reference run in this repo):

```text
AUDIT SUMMARY: 5/5 Checks Passed (100% Production Readiness Score)
STATUS: ALL AUDITED READINESS CHECKS PASSED.
```

Your own-repo audit details are shape-only and should show five gate lines plus one final summary score for comparison with Lab 01.

## Break it on purpose
Temporarily hide one required memory file in your own repo and rerun the audit.

```bash
mv AGENTS.md AGENTS.md.bak
python /path/to/packt-harness/.claude/skills/harness-production-readiness-auditor/scripts/run_audit.py "$(pwd)"
mv AGENTS.md.bak AGENTS.md
```

The audit should fail the memory-files gate and lower the total score.

## You are done when
- You can show both Lab 01 baseline and Lab 10 post scores.
- You calculated the score delta.
- You triggered at least one deliberate gate failure and restored the file.

## If it goes wrong
- If your baseline note is missing, rerun Lab 01 first and record the score before continuing.
- If the audit script path fails, verify `/path/to/packt-harness`.
- If all gates still pass after breaking a prerequisite, confirm you changed the audited repo, not another directory.
