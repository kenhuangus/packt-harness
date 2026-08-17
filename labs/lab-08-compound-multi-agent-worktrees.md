# Lab 08 — Compound Multi-Agent Worktrees

**Skill:** `harness-compound-multi-agent-worktrees`  
**Module:** [module_08_compound_engineering](https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_08_compound_engineering)  
**Time:** 55 minutes

## What you will end up with
You will run one isolated worktree implementation cycle and a side-by-side reviewer comparison showing what a fresh context catches that the implementer context misses.

## Before you start
Use your own repository for the comparison exercise and this repo for the reference simulator run.  
This lab can involve generation when you run real agents. If your local model is unavailable, set `HARNESS_ALLOW_SIMULATED_LLM=1`.

## Steps
1. Run the reference simulator once to see planner -> implementer -> reviewer flow with worktree cleanup.

```bash
cd /path/to/packt-harness
python course_implementation/module_08_compound_engineering/multi_agent_team_simulator.py
```

2. In your own repo, create a feature branch and one temporary worktree.

```bash
cd /path/to/your-repo
git worktree add -b lab08-temp .worktrees/lab08-temp HEAD
```

3. Run your implementer agent in the worktree and save its self-review findings to `same-context-findings.txt`.

```bash
cd .worktrees/lab08-temp
printf "Paste same-context reviewer findings here.\n" > same-context-findings.txt
```

4. Run the same review prompt in a fresh reviewer context and save findings to `fresh-context-findings.txt`.

```bash
printf "Paste fresh-context reviewer findings here.\n" > fresh-context-findings.txt
```

5. Compare the two outputs and note what only the fresh context caught.

```bash
diff -u same-context-findings.txt fresh-context-findings.txt
```

6. Remove the temporary worktree and branch.

```bash
cd /path/to/your-repo
git worktree remove .worktrees/lab08-temp --force
git branch -D lab08-temp
```

## Expected output
Real captured output:

```text
[Isolation] git worktree created at ...\module08-agent-...
[Reviewer Subagent (Auditor)] AST + pytest in the worktree...
[PASS] pytest passed inside the isolated worktree.
[Isolation] git worktree removed.
```

The same-context vs fresh-context review diff is shape-only because it depends on your repo and your prompts.

## Break it on purpose
Skip the fresh reviewer context and only keep the implementer self-review.

```bash
printf "fresh context skipped\n" >> harness-lab-notes.txt
```

You should observe that the review list is thinner and misses at least one issue the fresh context usually catches.

## You are done when
- You created and removed one temporary worktree.
- You captured same-context and fresh-context reviewer outputs separately.
- You compared both outputs and listed at least one difference in findings.

## If it goes wrong
- If `git worktree add` fails, confirm your repo has no conflicting `lab08-temp` branch.
- If diff is empty, rerun the reviewer prompt with stricter checks (tests, security, edge cases).
- If model-backed agents fail to respond, enable `HARNESS_ALLOW_SIMULATED_LLM=1` for that run.
