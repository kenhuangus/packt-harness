"""
Module 7: Model Context Protocol (MCP) Server

Exposes an enterprise-record tool and a read-only application-settings
resource through the MCP Python SDK 2.x authoring API.
"""

import json

from mcp.server.mcpserver import MCPServer

# MCP Python SDK 2.x authoring API. The server speaks JSON-RPC on stdio
# when mcp.run() is called. Do not print to stdout: that stream is the
# protocol, not a log.
mcp = MCPServer("Harness-Enterprise-Tools")


@mcp.tool()
def query_database_record(record_id: int) -> str:
    """
    Teaching MCP tool: return one fake enterprise record.

    The client calls this with record_id=4092. A real server would
    talk to a database; this one returns a fixed ACTIVE row so the
    protocol exchange can be verified without credentials.
    """
    return (
        f"DB_RECORD #{record_id}: "
        "status=ACTIVE, owner=admin, env=production"
    )


@mcp.resource("config://app-settings")
def app_settings() -> str:
    """
    Teaching MCP resource: a read-only JSON document.

    Resources are not tools. The client lists them, then reads the URI
    `config://app-settings`. The payload is static so the read can be
    asserted in RUN_RESULTS.md.
    """
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
