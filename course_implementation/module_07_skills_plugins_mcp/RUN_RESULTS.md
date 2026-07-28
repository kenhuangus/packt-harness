# Module 7 Run Results

Real end-to-end MCP session over subprocess stdio, captured from an actual run.

```text
> python mcp_client_runner.py
============================================================
MODULE 7 DEMO: MODEL CONTEXT PROTOCOL (MCP) TEST RUNNER
============================================================
  [PASS] MCP session initialized over subprocess stdio.

[MCP Client] Sending 'tools/list' request...
  [PASS] Tool Available: 'query_database_record' - Query one enterprise database record by its numeric identifier.

[MCP Client] Sending 'tools/call' request...
  [PASS] Tool Execution Result: 'DB_RECORD #4092: status=ACTIVE, owner=admin, env=production'

[LLM Client] Synthesizing the MCP tool result...
[LLM Client] Configured LLM client with model 'openai:nvidia/Qwen3.6-35B-A3B-NVFP4' | Endpoint: 'http://127.0.0.1:8000/v1'
  [SKIPPED] LLM synthesis unavailable: the configured endpoint did not return a live response.

[MCP Client] Sending 'resources/list' request...
  [PASS] Resource Available: 'config://app-settings' (app_settings)

[MCP Client] Sending 'resources/read' request...
  [PASS] Resource Read Result: '{
  "application": "harness-enterprise",
  "environment": "production",
  "record_access": "read-only"
}'

============================================================
MODULE 7 DEMO COMPLETE: REAL MCP STDIO SESSION VERIFIED!
============================================================
EXIT=0
```

Environment: Python 3.13, MCP Python SDK 2.0.0 (`mcp.server.mcpserver.MCPServer`).

The LLM synthesis step reports `[SKIPPED]` by design when no OpenAI-compatible
endpoint is reachable at the configured `LLM_BASE_URL`; the MCP protocol steps are
independent of it and still pass.
