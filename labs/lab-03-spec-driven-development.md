# Lab 03 — Spec-Driven Development

**Skill:** `harness-spec-driven-development`  
**Module:** [module_03_spec_driven_development](https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_03_spec_driven_development)  
**Time:** 40 minutes

## What you will end up with
You will have one spec-bounded edit that passes and one out-of-scope edit that is rejected, using the same verifier command.

## Before you start
Create a short `SPEC.md` in your own repo listing allowed files and non-goals for one small feature.  
If you run the full module demo and your local model is down, use `HARNESS_ALLOW_SIMULATED_LLM=1`. The verifier script steps below do not require live generation.

## Steps
1. Move into your own repository and decide one file that is allowed for this lab.

```bash
cd /path/to/your-repo
```

2. Run a scope check that targets an allowed file.

```bash
python /path/to/packt-harness/.claude/skills/harness-spec-driven-development/scripts/verify_spec_scope.py --allowed auth_validator.py tests/test_auth.py --file auth_validator.py --content $'def validate_jwt(t):\n    return {"valid": True}\n'
```

3. Run a scope check that targets a forbidden file.

```bash
python /path/to/packt-harness/.claude/skills/harness-spec-driven-development/scripts/verify_spec_scope.py --allowed auth_validator.py tests/test_auth.py --file database.py --content $'def x():\n    return 1\n'
```

4. Run the full module demo once to see spec checks plus tests together.

```bash
cd /path/to/packt-harness
export HARNESS_ALLOW_SIMULATED_LLM=1
python course_implementation/module_03_spec_driven_development/spec_driven_verifier.py
```

## Expected output
Real captured output:

```text
[PASS] OK
[FAIL] SCOPE VIOLATION: 'database.py' is not in allowed files ['auth_validator.py', 'tests/test_auth.py'].
```

## Break it on purpose
Send syntactically invalid code content to prove AST enforcement.

```bash
python /path/to/packt-harness/.claude/skills/harness-spec-driven-development/scripts/verify_spec_scope.py --allowed auth_validator.py tests/test_auth.py --file auth_validator.py --content "def bad(:"
```

The skill should return an `AST SYNTAX ERROR` failure.

## You are done when
- One allowed target returns `[PASS] OK`.
- One forbidden target returns `SCOPE VIOLATION`.
- An invalid code string returns `AST SYNTAX ERROR`.
- Your `SPEC.md` includes at least one explicit non-goal.

## If it goes wrong
- If shell quoting breaks the `--content` value, run the command in Bash exactly as shown.
- If every file passes, verify your `--allowed` list does not include the forbidden target.
- If the full demo fails on model access, keep `HARNESS_ALLOW_SIMULATED_LLM=1` set for that step.
