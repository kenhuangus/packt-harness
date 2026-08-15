# Model Context Protocol (MCP) 2.x Reference

- `@mcp.tool()`: Decorates callable actions with arguments that perform operations.
- `@mcp.resource("uri://...")`: Decorates read-only application state over standard URIs.
- **Stdio Transport**: Standard JSON-RPC over `sys.stdin`/`sys.stdout`.
