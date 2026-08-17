# Lab 02 — Core Stack Sandbox

**Skill:** `harness-core-stack-sandbox`  
**Module:** [module_02_core_harness_stack](https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_02_core_harness_stack)  
**Time:** 30 minutes

## What you will end up with
You will have a repeatable path-containment check you can run before writes, plus an explicit fail case proving out-of-workspace paths are blocked.

## Before you start
Use your own repository as the workspace root for all containment checks.  
This lab does not require live generation, so you are not blocked by the local model endpoint.

## Steps
1. Move into your own repository.

```bash
cd /path/to/your-repo
pwd
```

2. Run a containment check on an in-repo target path.

```bash
python /path/to/packt-harness/.claude/skills/harness-core-stack-sandbox/scripts/validate_sandbox.py --workspace "." --path "./src"
```

3. Run a containment check on a parent-directory escape path.

```bash
python /path/to/packt-harness/.claude/skills/harness-core-stack-sandbox/scripts/validate_sandbox.py --workspace "." --path "../outside.py"
```

4. Write down the allow/violation result in your repo notes for later hook policy tuning.

```bash
printf "lab02_sandbox_checked: yes\n" >> harness-lab-notes.txt
```

## Expected output
Real captured output:

```text
Path containment: VALID
Path containment: VIOLATION
```

Your exact in-repo path will differ, but the status words should match.

## Break it on purpose
Point `--path` at a sibling or parent path that is outside your repository root.

```bash
python /path/to/packt-harness/.claude/skills/harness-core-stack-sandbox/scripts/validate_sandbox.py --workspace "." --path "../../secrets.txt"
```

The skill should return `Path containment: VIOLATION` and exit non-zero.

## You are done when
- A path inside your repo is reported as `VALID`.
- A path outside your repo is reported as `VIOLATION`.
- You can explain which exact root path is being enforced.

## If it goes wrong
- If everything reports `VALID`, check that `--workspace` is set to `.` in your repo directory.
- If `python` cannot find the script, verify your `/path/to/packt-harness`.
- If output is unexpected on Windows symlinks, test again with fully resolved absolute paths.
