---
name: harness-mcp-and-plugins
description: Authors and consumes Model Context Protocol (MCP) 2.x SDK servers, exposing @mcp.tool() actions and @mcp.resource() URIs over stdio JSON-RPC, and bundles agent skills into .claude-plugin/plugin.json manifests. Use when extending agent capabilities with custom tools, reading application resources, or building plugins.
allowed-tools: Read, Write, Glob, Grep, Bash
---

# MCP 2.x SDK & Plugin Ecosystem (Module 7 Skill)

This skill provides patterns for authoring MCP 2.x SDK servers (`mcp.server.mcpserver.MCPServer`), handling async client handshakes, and bundling skills, hooks, and tools into `.claude-plugin/plugin.json` manifests.

## When to Use
- When extending agent capabilities with custom callable tools via `@mcp.tool()`.
- When exposing application state and configuration schemas as read-only URIs via `@mcp.resource("uri://...")`.
- When running async stdio client sessions to list tools, call tools, and read resources.
- When configuring plugin manifests in `.claude-plugin/plugin.json`.

## How to Use
1. **Server Authoring with MCP 2.x SDK**:
   ```python
   from mcp.server.mcpserver import MCPServer
   mcp = MCPServer("Harness-Enterprise-Tools")

   @mcp.tool()
   def query_database_record(record_id: int) -> str:
       return f"DB_RECORD #{record_id}: status=ACTIVE, owner=admin"

   @mcp.resource("config://app-settings")
   def app_settings() -> str:
       return json.dumps({"application": "harness-enterprise", "record_access": "read-only"})

   if __name__ == "__main__":
       mcp.run()  # stdio JSON-RPC
   ```

2. **Async Client Connection**:
   ```python
   server_params = StdioServerParameters(command=sys.executable, args=["mcp_server_demo.py"])
   async with stdio_client(server_params) as (read_stream, write_stream):
       async with ClientSession(read_stream, write_stream) as session:
           await session.initialize()
           tools = await session.list_tools()
           res = await session.call_tool("query_database_record", arguments={"record_id": 4092})
           data = await session.read_resource("config://app-settings")
   ```

3. **Verification**:
   ```bash
   python course_implementation/module_07_skills_plugins_mcp/mcp_client_runner.py
   ```

## Key Files & Implementation
- `course_implementation/module_07_skills_plugins_mcp/mcp_server_demo.py`
- `course_implementation/module_07_skills_plugins_mcp/mcp_client_runner.py`
- `course_implementation/module_07_skills_plugins_mcp/.claude-plugin/plugin.json`
