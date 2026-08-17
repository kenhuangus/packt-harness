# Verified Claude Code / MCP facts (source of truth for this repo)

Verified 2026-07-28 against official docs. **Do not contradict this file.** If a slide,
README, or code comment disagrees with something here, the slide/README/code is wrong.

Sources:
- https://code.claude.com/docs/en/hooks
- https://code.claude.com/docs/en/skills
- https://code.claude.com/docs/en/sub-agents
- https://code.claude.com/docs/en/plugins-reference
- https://modelcontextprotocol.io/specification/versioning

## 1. There is no "MCP 2.0" *protocol*

MCP **protocol** versions are dated spec revisions, `YYYY-MM-DD`, incremented only on
breaking changes. Known revisions: `2024-11-05`, `2025-03-26`, `2025-06-18`, `2025-11-25`,
and the current dated revision line continuing into 2026. There is no protocol version
"2.0".

Three separate version numbers get conflated into the phrase "MCP 2.0":

1. the **protocol** revision — dated, e.g. `2025-11-25`;
2. **JSON-RPC 2.0** — the RPC framing MCP rides on, unrelated to MCP's own version;
3. the **Python SDK package** version — which genuinely *is* `2.0.0` right now
   (`pip show mcp` → `Version: 2.0.0`).

So "the MCP 2.0 Python SDK" is defensible; **"the MCP 2.0 specification" and "MCP 2.0
protocol" are not.** In this repo, replace protocol/spec uses with "Model Context Protocol
(MCP)" or a dated revision; where the SDK is meant, say "MCP Python SDK 2.x".

## 2. MCP transports

- `stdio` — local subprocess servers. Current.
- **Streamable HTTP** — the remote transport since revision `2025-03-26`.
- **HTTP+SSE is the legacy transport** it replaced. Do not present "stdio vs SSE" as the
  live choice; present "stdio vs Streamable HTTP (SSE = deprecated predecessor)".

## 3. MCP Python SDK idiom — VERSION-SENSITIVE

**This machine has `mcp` 2.0.0 installed. Verify with `pip show mcp` before writing code.**

`FastMCP` was **renamed in SDK 2.x**. `from mcp.server.fastmcp import FastMCP` raises
`ModuleNotFoundError: No module named 'mcp.server.fastmcp'` here — `mcp.server` exposes
`mcpserver`, not `fastmcp`. Verified by introspection, not memory:

| SDK | Server class |
|---|---|
| 1.x | `from mcp.server.fastmcp import FastMCP` |
| **2.x (installed here)** | `from mcp.server.mcpserver import MCPServer` |

Correct idiom for the installed 2.x SDK:

```python
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("harness-tools")

@mcp.tool()
def query_record(record_id: int) -> str: ...

@mcp.resource("config://app-settings")
def settings() -> str: ...

mcp.run()                              # transport defaults to "stdio"
mcp.run(transport="streamable-http")   # also accepts "sse" (legacy)
```

`MCPServer.run(transport=...)` accepts exactly `'stdio' | 'sse' | 'streamable-http'`.
Async variants: `run_stdio_async()`, `run_streamable_http_async()`, `run_sse_async()`.

`Server.add_request_handler(...)` exists but is not the documented authoring API and
produces code no real client can talk to.

A client demo that imports the server's handler functions and calls them in-process is
**not** an MCP client and must not claim "Client/Server Interaction Verified". A real
client uses `mcp.client.stdio.stdio_client` + `ClientSession`, does `await
session.initialize()`, then `list_tools()` / `call_tool()`.

## 4. Claude Code hook events — exact names (PascalCase)

`SessionStart`, `Setup`, `UserPromptSubmit`, `UserPromptExpansion`, `PreToolUse`,
`PermissionRequest`, `PermissionDenied`, `PostToolUse`, `PostToolUseFailure`,
`PostToolBatch`, `Notification`, `MessageDisplay`, `SubagentStart`, `SubagentStop`,
`TaskCreated`, `TaskCompleted`, `Stop`, `StopFailure`, `TeammateIdle`,
`InstructionsLoaded`, `ConfigChange`, `CwdChanged`, `FileChanged`, `WorktreeCreate`,
`WorktreeRemove`, `PreCompact`, `PostCompact`, `Elicitation`, `ElicitationResult`,
`SessionEnd`.

**There is no `pre-commit` hook event, and the names are not kebab-case.** The repo's
`pre-tool-use` / `post-tool-use` / `pre-commit` are all wrong.

### Config shape (`.claude/settings.json`)

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{ "type": "command", "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/guard.py", "timeout": 10 }]
      }
    ]
  }
}
```

Matcher matches the **tool name** for tool events; `"*"`/`""`/omitted matches all;
`"Edit|Write"` for alternation; anything with other characters is a regex.
Hook types: `command`, `http`, `mcp_tool`, `prompt`, `agent`.
Placeholders: `${CLAUDE_PROJECT_DIR}`, `${CLAUDE_PLUGIN_ROOT}`, `${CLAUDE_PLUGIN_DATA}`.

### Hook I/O contract

Input arrives as **JSON on stdin**, with `session_id`, `transcript_path`, `cwd`,
`permission_mode`, `hook_event_name`, plus `tool_name` / `tool_input` on tool events.

Output — exit codes:
| Exit | Meaning |
|---|---|
| `0` | success; stdout parsed as JSON if valid |
| `2` | **blocking error**; stderr is fed to Claude, stdout ignored |
| other | non-blocking error; execution continues |

Structured `PreToolUse` decision (exit 0 + JSON on stdout):

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow|deny|ask|defer",
    "permissionDecisionReason": "...",
    "updatedInput": { "command": "..." }
  }
}
```

Universal output fields: `continue`, `stopReason`, `suppressOutput`, `systemMessage`.
`decision: "block"` + `reason` is the top-level form used by `UserPromptSubmit`, `Stop`,
`SubagentStop`, etc.

Permission modes: `default`, `plan`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions`.

## 5. Skills

Locations: personal `~/.claude/skills/<name>/SKILL.md`, project
`.claude/skills/<name>/SKILL.md`, plugin `skills/` dir. Nested `.claude/skills/` below cwd
also load. Custom commands (`.claude/commands/*.md`) have been merged into skills — both
create `/<name>`.

Frontmatter fields that actually exist: `name`, `description`, `allowed-tools`,
`disable-model-invocation`, `context` (e.g. `fork`), `agent`, `model`.
**There is no `triggers` field** — discovery is driven by `description`, so the
description must state *what it does and when to use it*.

Skills follow the Agent Skills open standard (agentskills.io); Claude Code extends it with
invocation control, subagent execution, and dynamic context injection.

## 6. Subagents

File: `.claude/agents/<name>.md` (project) or `~/.claude/agents/<name>.md` (personal).

```yaml
---
name: code-reviewer
description: Reviews code for quality and best practices
tools: Read, Grep        # or disallowedTools: Write, Edit
model: sonnet
isolation: worktree            # gives the subagent its own git worktree
---
```

Each subagent gets **its own context window** and only the frontmatter body as system
prompt. `disallowedTools` is applied first, then `tools` resolves against the remainder.
`tools`/`disallowedTools` accept MCP patterns `mcp__<server>` / `mcp__<server>__*`.
The Task tool was renamed **Agent** in v2.1.63 (`Task(...)` still aliases).

Worktree isolation is a real first-class frontmatter field — do **not** invent
"Inherit Mode / Branch Mode / Worktree Mode" terminology.

## 7. Plugins

Manifest: **`.claude-plugin/plugin.json`** (not a bare `plugin.json` at the root).
Fields include `name` (required), `description`, `version`, `author`, `dependencies`
(`[{ "name": "...", "version": "~2.1.0" }]`).

A plugin bundles: **skills, agents, hooks, MCP servers, LSP servers, monitors**. There is
no such component as a "sidecar" — delete that word.

Distribution is via a marketplace `marketplace.json`; a folder under a skills dir
containing `.claude-plugin/plugin.json` loads in place as `<name>@skills-dir`.

## 8. Terminology corrections summary

| Wrong (current repo) | Right |
|---|---|
| MCP 2.0 | Model Context Protocol (MCP), revision `YYYY-MM-DD` |
| `pre-tool-use`, `post-tool-use` | `PreToolUse`, `PostToolUse` |
| `pre-commit` hook event | does not exist |
| SSE as the remote transport | Streamable HTTP (SSE is legacy) |
| `server.add_request_handler(...)` | `FastMCP` + `@mcp.tool()` |
| SKILL.md `triggers:` frontmatter | `description:` drives discovery |
| plugin.json at plugin root | `.claude-plugin/plugin.json` |
| Plugins bundle "sidecars" | skills, agents, hooks, MCP/LSP servers, monitors |
| Subagent "Inherit/Branch/Worktree mode" | `isolation: worktree` frontmatter |
| Task tool | Agent tool (renamed v2.1.63) |
