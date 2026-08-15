# Claude Code PascalCase Hooks Specification

Hook events supported in `.claude/settings.json`:
- `PreToolUse`: Evaluated before any tool call executes.
- `PostToolUse`: Evaluated after tool execution completes.

### Permission Decisions
- `allow`: Proceed with execution.
- `deny`: Block execution with reason feedback.
- `ask`: Prompt human user for interactive decision.
- `defer`: Yield decision to fallback handler.
