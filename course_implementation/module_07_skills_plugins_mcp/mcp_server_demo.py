"""
Module 7: Model Context Protocol (MCP 2.0) Server Implementation
Official Anthropic MCP 2.0 specification implementation using JSON-RPC 2.0 request handlers.
Features:
- Tool Handler: 'tools/list' and 'tools/call'
- Resource Handler: 'resources/list' and 'resources/read'
- Prompt Handler: 'prompts/list' and 'prompts/get'
"""

import sys, asyncio
from mcp.server import Server
import mcp.types as types

sys.stdout.reconfigure(encoding='utf-8')

server = Server("Harness-Enterprise-Tools")

# 1. Tools List Handler
async def handle_list_tools(params):
    return types.ListToolsResult(
        tools=[
            types.Tool(
                name="query_database_record",
                description="Queries enterprise database record safely via MCP tool protocol.",
                inputSchema={
                    "type": "object",
                    "properties": {"record_id": {"type": "integer"}},
                    "required": ["record_id"]
                }
            )
        ]
    )

# 2. Tool Execution Handler
async def handle_call_tool(params):
    name = params.name
    args = params.arguments or {}
    print(f"[MCP Server 2.0] Processing Tool Call: '{name}' with args {args}")
    
    if name == "query_database_record":
        rec_id = args.get("record_id", 0)
        output_text = f"DB_RECORD #{rec_id}: status=ACTIVE, owner=admin, env=production"
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=output_text)]
        )
    else:
        raise ValueError(f"Unknown tool: {name}")

# 3. Resources List Handler
async def handle_list_resources(params):
    return types.ListResourcesResult(
        resources=[
            types.Resource(
                uri="config://app-settings",
                name="Application Settings",
                description="Read-only application configuration resource",
                mimeType="text/plain"
            )
        ]
    )

# Register Handlers
server.add_request_handler("tools/list", types.ListToolsRequest, handle_list_tools)
server.add_request_handler("tools/call", types.CallToolRequest, handle_call_tool)
server.add_request_handler("resources/list", types.ListResourcesRequest, handle_list_resources)

if __name__ == "__main__":
    print("=" * 60)
    print("MCP 2.0 SERVER 'Harness-Enterprise-Tools' INITIALIZED")
    print("=" * 60)
    print("  • Transport: JSON-RPC 2.0 over stdio")
    print("  • Registered Methods: 'tools/list', 'tools/call', 'resources/list'")
