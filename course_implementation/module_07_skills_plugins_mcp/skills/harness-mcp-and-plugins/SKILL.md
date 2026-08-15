---
name: harness-mcp-and-plugins
description: Authors and consumes Model Context Protocol (MCP) 2.x SDK servers, exposing
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Harness Mcp And Plugins

Authors and consumes Model Context Protocol (MCP) 2.x SDK servers, exposing @mcp.tool() actions and @mcp.resource() URIs over stdio JSON-RPC, and bundles agent skills into .claude-plugin/plugin.json manifests. Use when extending agent capabilities with custom tools, reading application resources, or building plugins.

## Structure & Available Components
- `scripts/`: Executable helper tools for this skill.
- `references/`: Architectural rules, patterns, and guides.
- `assets/`: Config templates and validation schemas.

## When to Use
Trigger this skill when:
- Operating within `module_07_skills_plugins_mcp` or applying its design patterns.
- Auditing, executing, or enforcing harness guarantees for this domain.

## How to Use
1. Consult references in `references/` for specifications and policies.
2. Execute scripts in `scripts/` to validate inputs and enforce constraints.
3. Apply configurations in `assets/` for standardized settings.

## Key Files & Implementation (GitHub Links)
- [https://github.com/kenhuangus/packt-harness/tree/main/.claude/skills/harness-mcp-and-plugins/](https://github.com/kenhuangus/packt-harness/tree/main/.claude/skills/harness-mcp-and-plugins/)
- [https://github.com/kenhuangus/packt-harness/blob/main/.claude/skills/harness-mcp-and-plugins/SKILL.md](https://github.com/kenhuangus/packt-harness/blob/main/.claude/skills/harness-mcp-and-plugins/SKILL.md)
- [https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_07_skills_plugins_mcp/](https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_07_skills_plugins_mcp/)
