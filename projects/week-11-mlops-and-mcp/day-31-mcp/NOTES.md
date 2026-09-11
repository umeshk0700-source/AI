# Day 31 — MCP cheat sheet

## Why
- Direct agent↔tool wiring is M×N integrations. MCP makes it M + N: tools live in **servers**,
  agents are **clients**, discovery happens at runtime.

## The protocol
- JSON-RPC 2.0. Request: `{jsonrpc, id, method, params}`. Response: `{jsonrpc, id, result|error}`.
  Notification: no `id`.
- Lifecycle:
  - `initialize` → capability handshake (`serverInfo`, `capabilities`); client then sends the
    `notifications/initialized` notification.
  - `tools/list` → `{tools: [{name, description, inputSchema}]}`
  - `tools/call` `{name, arguments}` → `{content: [{type:"text", text}], isError}`
- Tool error vs protocol error: a failing tool returns `result` with `isError: true`; an
  unknown method / bad params returns a JSON-RPC `error` object.

## Primitives
| Primitive | Discover / use | Model's view |
| --- | --- | --- |
| Tool | `tools/list`, `tools/call` | a tool in the tool-use schema |
| Resource | `resources/list`, `resources/read` (by URI) | context you attach |
| Prompt | `prompts/list`, `prompts/get` | a user-invoked template |
| `sampling` | server → client LLM completion | inverted call; gate it |

## Transports
- **stdio** — client spawns server subprocess, newline-delimited JSON on stdin/stdout. Local.
- **Streamable HTTP / SSE** — remote servers, needs auth (OAuth / bearer).

## SDK (`mcp<2`)
```python
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("name")
@mcp.tool()
def f(x: str) -> str: ...
mcp.run()                              # stdio by default
```
```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
async with stdio_client(params) as (r, w):
    async with ClientSession(r, w) as s:
        await s.initialize()
        tools = (await s.list_tools()).tools
        out = await s.call_tool("f", {"x": "..."})
```
- Jupyter owns the event loop → run SDK client code as a subprocess script, not inline.

## MCP → Anthropic tools
```python
[{"name": t.name, "description": t.description or "", "input_schema": t.inputSchema}
 for t in mcp_tools]
```
`tools/list` feeds function-calling; `tools/call` runs the model's pick. MCP does not replace
tool use — it supplies the schemas.

## Trust
- Tool `description` is untrusted text the model obeys → prompt-injection surface.
- Tool shadowing (a rogue server redefines `kb_search`) → namespace tools by server.
- Least-privilege server credentials; gate `sampling`; pass user identity for authz.
