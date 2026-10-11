#!/usr/bin/env python3
"""STRICT TEST: does Serena actually deliver semantic (symbol-level) code intelligence?"""
import asyncio, os, sys, json

PROJ = "/home/user/agent-test/target-proj"
BIN = "/home/user/agent-test/bin/serena"

async def main():
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    env = {**os.environ, "PATH": f"/home/user/agent-test/bin:/home/user/agent-test/venv/bin:{os.environ[chr(80)+chr(65)+chr(84)+chr(72)]}"}
    params = StdioServerParameters(
        command=BIN,
        args=["start-mcp-server", "--project", PROJ, "--context", "codex"],
        env=env)

    async with stdio_client(params) as (r, w):
        async with ClientSession(r, w) as s:
            init = await s.initialize()
            print("server:", init.server_info)
            tl = await s.list_tools()
            names = [t.name for t in tl.tools]
            print(f"\ntools ({len(names)}):")
            for n in names:
                print("   -", n)

            async def call(name, args, label):
                try:
                    res = await asyncio.wait_for(s.call_tool(name, args), timeout=240)
                    txt = "\n".join(getattr(c, "text", "") for c in res.content)
                    print(f"\n### {label}  ({name})")
                    print(txt[:900])
                    return txt
                except asyncio.TimeoutError:
                    print(f"\n### {label}  ({name}) -> TIMEOUT")
                    return ""
                except Exception as e:
                    print(f"\n### {label}  ({name}) -> ERROR {type(e).__name__}: {str(e)[:200]}")
                    return ""

            # 1) activate project / onboarding
            await call("activate_project", {"project": PROJ}, "activate project")
            # 2) symbol overview (semantic!)
            await call("get_symbols_overview", {"relative_path": "src/engine.py"}, "symbols overview engine.py")
            # 3) find symbol by name across project
            await call("find_symbol", {"name_path": "Engine/compute", "substring_matching": False}, "find symbol Engine/compute")
            # 4) find referencing symbols (the killer feature)
            await call("find_referencing_symbols",
                       {"name_path": "Engine", "relative_path": "src/engine.py"}, "find references to Engine")
            # 5) the self-check tools
            await call("think_about_task_adherence", {}, "self-check: task adherence")
            await call("think_about_whether_you_are_done", {}, "self-check: am I done?")

asyncio.run(main())
