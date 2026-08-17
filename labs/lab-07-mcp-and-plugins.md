# Lab 07 — MCP and Plugins

**Skill:** `harness-mcp-and-plugins`  
**Module:** [module_07_skills_plugins_mcp](https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_07_skills_plugins_mcp)  
**Time:** 50 minutes

## What you will end up with
You will verify a working MCP stdio handshake in this repo, then port the same pattern into your own repository with one tool and one resource.

## Before you start
Start this lab in this repository first, then move to your own repo in the second half.  
This lab uses generation in the module client demo. If your local model is down, set `HARNESS_ALLOW_SIMULATED_LLM=1`.  
Use the MCP Python SDK 2.x import form: `from mcp.server.mcpserver import MCPServer`.

## Steps
1. Move to the module directory before running the inspector script.

```bash
cd /path/to/packt-harness/course_implementation/module_07_skills_plugins_mcp
pwd
```

2. Confirm the SDK import form works in your environment.

```bash
python -c 'from mcp.server.mcpserver import MCPServer; print(MCPServer.__name__)'
```

3. Run the inspector script from this module directory.

```bash
python skills/harness-mcp-and-plugins/scripts/inspect_mcp_server.py
```

4. Run the end-to-end module client demo with fallback enabled if needed.

```bash
export HARNESS_ALLOW_SIMULATED_LLM=1
python mcp_client_runner.py
```

5. Move to your own repo and create a minimal MCP server with one `@mcp.tool()` and one `@mcp.resource()`.

```bash
cd /path/to/your-repo
```

## Expected output
Real captured output:

```text
[PASS] Connected to MCP server. Tools: ['query_database_record'], Resources: ['config://app-settings']
```

The output from your own repo server is shape-only and should list your own tool names and resource URIs.

## Break it on purpose
Run the inspector from the wrong directory context.

```bash
cd /path/to/packt-harness
python course_implementation/module_07_skills_plugins_mcp/skills/harness-mcp-and-plugins/scripts/inspect_mcp_server.py
```

On student machines, this commonly fails with a JSON-RPC parse-style error that looks like a server bug but is usually a directory-context mistake. Return to the module directory and rerun.

## You are done when
- You can import `MCPServer` from `mcp.server.mcpserver`.
- The inspector lists at least one tool and one resource.
- You moved the same pattern into your own repo with your own names.

## If it goes wrong
- If import fails, verify the `mcp` package is installed in the active environment.
- If inspector errors, confirm you are in `module_07_skills_plugins_mcp` before running it.
- If the module client demo cannot reach the local model, keep `HARNESS_ALLOW_SIMULATED_LLM=1`.
