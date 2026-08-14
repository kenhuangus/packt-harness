"""
Module 7: Model Context Protocol (MCP) Client Test Runner

Starts the MCPServer process and communicates with it over stdio.
"""

import asyncio
import os
from pathlib import Path
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


sys.stdout.reconfigure(encoding="utf-8")

MODULE_DIR = Path(__file__).resolve().parent
sys.path.append(os.path.abspath(MODULE_DIR.parent))

from common.llm_client import CourseLLMClient  # noqa: E402


def synthesize_with_llm(tool_output: str) -> None:
    """
    Optional live-model step. Not required for the MCP PASS lines.

    If aisuite is missing, the endpoint is down, or the client returns
    its simulated fallback string, this prints [SKIPPED]. The MCP
    session is independent and has already succeeded by this point.
    """
    try:
        llm_client = CourseLLMClient()
        response = llm_client.generate(
            f"Synthesize MCP tool output: {tool_output}"
        )
    except Exception as exc:
        print(f"  [SKIPPED] LLM synthesis unavailable: {exc}")
        return

    if not response or response.startswith("[Harness Simulated Output"):
        print(
            "  [SKIPPED] LLM synthesis unavailable: "
            "the configured endpoint did not return a live response."
        )
        return

    print(f"  [PASS] Live LLM synthesis received ({len(response)} chars).")


async def main_async() -> None:
    print("=" * 60)
    print("MODULE 7 DEMO: MODEL CONTEXT PROTOCOL (MCP) TEST RUNNER")
    print("=" * 60)

    # Spawn mcp_server_demo.py as a child process. The SDK wires the
    # child's stdin/stdout to JSON-RPC; we never parse the bytes ourselves.
    server_parameters = StdioServerParameters(
        command=sys.executable,
        args=[str(MODULE_DIR / "mcp_server_demo.py")],
    )

    async with stdio_client(server_parameters) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            # initialize is the MCP handshake (protocol version + capabilities).
            await session.initialize()
            print("  [PASS] MCP session initialized over subprocess stdio.")

            print("\n[MCP Client] Sending 'tools/list' request...")
            tools_result = await session.list_tools()
            for tool in tools_result.tools:
                print(
                    f"  [PASS] Tool Available: '{tool.name}' - "
                    f"{tool.description}"
                )

            print("\n[MCP Client] Sending 'tools/call' request...")
            call_result = await session.call_tool(
                "query_database_record",
                arguments={"record_id": 4092},
            )
            text_items = [
                content.text
                for content in call_result.content
                if getattr(content, "type", None) == "text"
            ]
            if not text_items:
                raise RuntimeError("MCP tool call returned no text content.")
            tool_output = text_items[0]
            print(f"  [PASS] Tool Execution Result: '{tool_output}'")

            print("\n[LLM Client] Synthesizing the MCP tool result...")
            synthesize_with_llm(tool_output)

            print("\n[MCP Client] Sending 'resources/list' request...")
            resources_result = await session.list_resources()
            for resource in resources_result.resources:
                print(
                    f"  [PASS] Resource Available: "
                    f"'{resource.uri}' ({resource.name})"
                )

            print("\n[MCP Client] Sending 'resources/read' request...")
            resource_result = await session.read_resource(
                "config://app-settings"
            )
            resource_text_items = [
                content.text
                for content in resource_result.contents
                if getattr(content, "text", None) is not None
            ]
            if not resource_text_items:
                raise RuntimeError("MCP resource read returned no text content.")
            print(
                "  [PASS] Resource Read Result: "
                f"'{resource_text_items[0]}'"
            )

    print("\n" + "=" * 60)
    print("MODULE 7 DEMO COMPLETE: REAL MCP STDIO SESSION VERIFIED!")
    print("=" * 60)


def main() -> None:
    try:
        asyncio.run(main_async())
    except Exception as exc:
        print(f"\n  [FAIL] MCP client/server demo failed: {exc}")
        raise


if __name__ == "__main__":
    main()
