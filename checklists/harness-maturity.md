# Harness maturity checklist — one page

Score your project: one point per line. Under 4 = you're trusting the model, not the harness.

## Feedforward (guides)
- [ ] `CLAUDE.md` exists, is committed, and contains "never do X" rules — not just style notes
- [ ] Non-trivial changes start from a **spec** with scope, constraints, and testable
      acceptance criteria (EARS: "WHEN ⟨trigger⟩, the system SHALL ⟨behavior⟩")
- [ ] The spec is reviewed by a human *before* implementation (cheapest gate you have)

## Deterministic controls
- [ ] `.claude/settings.json` has **deny rules** for secrets, destructive commands, publishing
- [ ] A **PreToolUse hook** blocks dangerous tool calls (exit 2 + reason)
- [ ] A **PostToolUse hook** runs lint/tests after edits and feeds failures back

## Feedback (sensors)
- [ ] Acceptance criteria exist as **executable tests before** the agent implements
- [ ] A hook re-runs the suite after every edit and feeds failures back, so "done" tracks
      green — not just the agent's word (a `Stop` hook makes it a hard gate)
- [ ] Every observed agent failure becomes a regression test, a CLAUDE.md rule, or a
      hook pattern — *the same failure never ships twice*

## Observability & review
- [ ] Every tool call is **audit-logged** (JSONL) and reviewable after the fact
- [ ] A human reviews diffs at defined gates (spec approval, pre-merge) — not every keystroke

## Reuse & scale
- [ ] The harness is **committed to the repo** (settings, hooks, skills) — new teammates
      and CI get it automatically
- [ ] Shared workflows are packaged (skill → subagent → plugin) instead of pasted prompts
- [ ] Subagents have **restricted tool allowlists**; handoffs happen through specs/contracts

**Team adoption path:** commit `CLAUDE.md` + `settings.json` (day 1) → add the three
hooks (week 1) → tests-as-gates in CI (week 2) → package as a plugin (when a second
team wants it).
