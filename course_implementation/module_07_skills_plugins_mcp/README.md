# Module 7: Skills, Plugins & Model Context Protocol (MCP)

## Overview
This module demonstrates extending AI agent capabilities via reusable Skills (`SKILL.md`), modular Plugins, and Anthropic's **Model Context Protocol (MCP 2.0)**.

## Core Concepts
1. **Agent Skills**: Folder-based instructions loaded dynamically via YAML frontmatter triggers.
2. **Modular Plugins**: Packaging skills, subagents, and sidecars into a single deployable bundle (`plugin.json`).
3. **Model Context Protocol (MCP)**: JSON-RPC 2.0 specification over `stdio` or `SSE` exposing:
   - **Tools**: Executable functions (`@mcp.tool()`)
   - **Resources**: Read-only data streams (`@mcp.resource()`)
   - **Prompts**: Reusable prompt templates (`@mcp.prompt()`)
