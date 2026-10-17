# 5 Core Harness Pillars

1. **Persistent Memory**: `CLAUDE.md` and `AGENTS.md` provide continuous system guidance.
2. **Sandboxing**: Path isolation (`is_relative_to()`) and explicit tool allowlists.
3. **Deterministic Hooks**: Pre/post execution guards for secret filtering and AST checks.
4. **Token Budgeting**: Head/tail compaction to preserve critical prompt space.
5. **Observability Tracing**: Harness-owned `EventLogger` appends ISO UTC spans to `events.jsonl` (tool, permission, hook, latency, token fields). The same spans can be mirrored to **LangSmith** or **Langfuse** for dashboards and evals — the harness remains the system of record.
