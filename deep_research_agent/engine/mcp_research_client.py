"""
Module 7 Integration: Async Stdio MCP Client for Deep Research Agent.
Spawns mcp_research_server.py as a child process and invokes search, scrape, and verify tools.
"""

from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path
import sys
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class DeepResearchMCPClient:
    """Manages an async stdio session with the MCP research server."""

    def __init__(self, server_script_path: Path):
        self.server_script = server_script_path
        self.server_params = StdioServerParameters(
            command=sys.executable,
            args=[str(self.server_script)],
            env=dict(os.environ),
        )

    async def execute_search(self, query: str, max_results: int = 4) -> list[dict[str, Any]]:
        async with stdio_client(self.server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                res = await session.call_tool(
                    "query_web_index",
                    arguments={"query": query, "max_results": max_results},
                )
                raw_text = res.content[0].text if res.content else "{}"
                data = json.loads(raw_text)
                return data.get("results", [])

    async def fetch_document(self, doc_id: str) -> dict[str, Any]:
        async with stdio_client(self.server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                res = await session.call_tool(
                    "extract_document_content",
                    arguments={"doc_id": doc_id},
                )
                raw_text = res.content[0].text if res.content else "{}"
                return json.loads(raw_text)

    async def verify_claim(self, claim: str, doc_id: str) -> dict[str, Any]:
        async with stdio_client(self.server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                res = await session.call_tool(
                    "verify_citation_claim",
                    arguments={"claim": claim, "doc_id": doc_id},
                )
                raw_text = res.content[0].text if res.content else "{}"
                return json.loads(raw_text)
