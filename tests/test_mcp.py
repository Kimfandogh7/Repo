#!/usr/bin/env python3
"""
STRICT TEST: do the MCP servers actually speak MCP and expose working tools?
We do a real stdio handshake (initialize -> tools/list -> tools/call) using the
official `mcp` client library. No vendor claims trusted.
"""
import asyncio, json, os, sys, shutil, textwrap

NM = "/home/user/agent-test/npmtest/node_modules/.bin"

SERVERS = {
    "sequential-thinking": ["node", f"/home/user/agent-test/npmtest/node_modules/@modelcontextprotocol/server-sequential-thinking/dist/index.js"],
    "firecrawl-mcp":       ["node", f"/home/user/agent-test/npmtest/node_modules/firecrawl-mcp/dist/index.js"] if shutil.which("node") else None,
    "exa-mcp-server":      ["node", f"/home/user/agent-test/npmtest/node_modules/exa-mcp-server/build/index.js"],
    "tavily-mcp":          ["node", f"/home/user/agent-test/npmtest/node_modules/tavily-mcp/build/index.js"],
}

ENV = {**os.environ, "PATH": f"{NM}:{os.environ['PATH']}"}

async def probe(name, cmd):
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    out = {"tool": name, "install": True, "handshake": False, "tools": [], "call": None, "error": ""}
    try:
        params = StdioServerParameters(command=cmd[0], args=cmd[1:], env=ENV)
        async with stdio_client(params) as (r, w):
            async with ClientSession(r, w) as s:
                init = await s.initialize()
                out["handshake"] = True
                out["server_info"] = str(init.serverInfo)
                tl = await s.list_tools()
                out["tools"] = [t.name for t in tl.tools]
                # --- functional call where possible ---
                if name == "sequential-thinking" and "sequentialthinking" in out["tools"]:
                    res = await s.call_tool("sequentialthinking", {
                        "thought": "Step 1: the build failed with E0308 mismatched types.",
                        "nextThoughtNeeded": True, "thoughtNumber": 1, "totalThoughts": 3})
                    res2 = await s.call_tool("sequentialthinking", {
                        "thought": "Step 2: revision - the real cause is u64 vs u32 in compute().",
                        "nextThoughtNeeded": True, "thoughtNumber": 2, "totalThoughts": 3,
                        "isRevision": True, "revisesThought": 1})
                    txt = "\n".join(getattr(c, "text", "") for c in res2.content)
                    out["call"] = {"ok": True, "excerpt": txt[:220].replace("\n", " ⏎ ")}
    except Exception as e:
        out["error"] = f"{type(e).__name__}: {str(e)[:220]}"
    return out

async def main():
    results = []
    for name, cmd in SERVERS.items():
        if cmd is None:
            results.append({"tool": name, "install": False, "error": "not installed"}); continue
        if not os.path.exists(cmd[1]):
            results.append({"tool": name, "install": False, "error": f"entrypoint missing: {cmd[1]}"}); continue
        try:
            results.append(await asyncio.wait_for(probe(name, cmd), timeout=90))
        except asyncio.TimeoutError:
            results.append({"tool": name, "install": True, "handshake": False, "error": "TIMEOUT 90s"})
    print("=" * 100)
    print("STRICT TEST — MCP servers: real stdio handshake + tool discovery + tool call")
    print("=" * 100)
    for r in results:
        print(f"\n▶ {r['tool']}")
        print(f"   installed : {r.get('install')}")
        print(f"   handshake : {r.get('handshake')}")
        print(f"   tools     : {r.get('tools')}")
        if r.get("server_info"): print(f"   server    : {r['server_info']}")
        if r.get("call"): print(f"   tool call : {r['call']['ok']}  ->  {r['call']['excerpt']}")
        if r.get("error"): print(f"   ERROR     : {r['error']}")
    print()

asyncio.run(main())
