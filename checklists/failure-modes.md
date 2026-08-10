# Coding-agent failure modes — and the harness layer that catches each

| # | Failure mode | What it looks like | Harness counter |
|---|---|---|---|
| 1 | **Scope creep** | "Fixed the bug" — plus refactored 6 unrelated files | Spec's Scope section + CLAUDE.md minimal-diff rule + reviewer scope check |
| 2 | **Plausible-but-wrong code** | Compiles, looks right, fails on real input | Acceptance criteria written as tests *before* implementation |
| 3 | **Destructive actions** | `rm -rf`, force-push, `DROP TABLE` | Permission deny rules + PreToolUse guard (deterministic, unpersuadable) |
| 4 | **Secret leakage** | Reads `.env`, commits a key | Read deny rules + secret-path patterns in the guard |
| 5 | **Prompt injection** | Fetched page / tool result contains instructions the agent obeys | Treat tool output as data; restrict tools per subagent; human gate on side effects |
| 6 | **Silent skipped verification** | "All tests pass" — never ran them | PostToolUse hook runs the suite itself; audit log proves what actually ran |
| 7 | **Context rot** | Forgets constraints deep into a long session | Standing rules in CLAUDE.md (reloaded every session), specs as files not chat |
| 8 | **Non-reproducibility** | Worked in the demo, never again | Harness as versioned code: settings + hooks + skills committed to the repo |

**The pattern:** every failure mode gets a *deterministic* counter where possible
(hooks, permissions, tests) and a *semantic* one where needed (specs, reviewer agent).
Prompting alone counters none of them reliably.
