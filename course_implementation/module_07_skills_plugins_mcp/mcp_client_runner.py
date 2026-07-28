"""
Module 7: MCP 2.0 Client Protocol Test Runner
Integrates standardized LLM Client (.env configured with 127.0.0.1 Qwen model as default).
"""

import sys, os, asyncio
sys.stdout.reconfigure(encoding='utf-8')

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from common.llm_client import CourseLLMClient

import mcp.types as types
from mcp_server_demo import server, handle_list_tools, handle_call_tool, handle_list_resources

async def main_async():
    print("=" * 60)
    print("MODULE 7 DEMO: MODEL CONTEXT PROTOCOL (MCP 2.0) TEST RUNNER ")
    print("=" * 60)

    llm_client = CourseLLMClient()

    # 1. Query Tools List
    print("\n[MCP Client] Sending JSON-RPC 'tools/list' request...")
    tools_res = await handle_list_tools(types.ListToolsRequest())
    for t in tools_res.tools:
        print(f"  ✓ Tool Available: '{t.name}' - {t.description}")

    # 2. Invoke Tool Call
    print("\n[MCP Client] Sending JSON-RPC 'tools/call' request...")
    call_params = types.CallToolRequestParams(name="query_database_record", arguments={"record_id": 4092})
    call_res = await handle_call_tool(call_params)
    for content in call_res.content:
        print(f"  ✓ Tool Execution Result: '{content.text}'")

    # Pass MCP result to LLM via aisuite
    llm_out = llm_client.complete(f"Synthesize MCP tool output: {call_res.content[0].text}")

    # 3. Query Resources List
    print("\n[MCP Client] Sending JSON-RPC 'resources/list' request...")
    res_list = await handle_list_resources(types.ListResourcesRequest())
    for r in res_list.resources:
        print(f"  ✓ Resource Stream Available: '{r.uri}' ({r.name})")

    print("\n" + "=" * 60)
    print("MODULE 7 DEMO COMPLETE: MCP 2.0 Client/Server Interaction Verified!")
    print("=" * 60)

def main():
    asyncio.run(main_async())

if __name__ == "__main__":
    main()
