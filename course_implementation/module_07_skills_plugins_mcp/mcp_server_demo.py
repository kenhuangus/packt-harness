"""
Module 7: Model Context Protocol (MCP) Server

Exposes an enterprise-record tool and a read-only application-settings
resource through the MCP Python SDK 2.x authoring API.
"""

import json

from mcp.server.mcpserver import MCPServer


mcp = MCPServer("Harness-Enterprise-Tools")


@mcp.tool()
def query_database_record(record_id: int) -> str:
    """Query one enterprise database record by its numeric identifier."""
    return (
        f"DB_RECORD #{record_id}: "
        "status=ACTIVE, owner=admin, env=production"
    )


@mcp.resource("config://app-settings")
def app_settings() -> str:
    """Return the demo application's read-only settings as JSON."""
    return json.dumps(
        {
            "application": "harness-enterprise",
            "environment": "production",
            "record_access": "read-only",
        },
        indent=2,
    )


if __name__ == "__main__":
    # MCPServer uses stdio by default. Do not print to stdout here because stdout
    # carries the JSON-RPC protocol messages.
    mcp.run()
