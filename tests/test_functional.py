#!/usr/bin/env python3
"""
STRICT FUNCTIONAL TESTS — does each tool DO something, offline, without an API key?
We deliberately avoid anything that needs a paid API or a blocked host.
"""
import subprocess, sys, os, json, tempfile, shutil, time

PY = "/home/user/agent-test/venv/bin/python"
VENV = "/home/user/agent-test/venv"
NPMBIN = "/home/user/agent-test/npmtest/node_modules/.bin"
rows = []

def run(cmd, timeout=180, env=None, cwd=None, stdin=None):
    t0 = time.time()
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout,
                           env=env or os.environ, cwd=cwd, input=stdin)
        return p.returncode, (p.stdout or "") + (p.stderr or ""), time.time() - t0
    except subprocess.TimeoutExpired:
        return -9, f"TIMEOUT after {timeout}s", time.time() - t0
    except Exception as e:
        return -1, f"{type(e).__name__}: {e}", time.time() - t0

def add(name, verdict, detail, secs=0.0):
    rows.append((name, verdict, detail.strip()[:300], secs))
    print(f"\n▶ {name}\n   VERDICT: {verdict}\n   {detail.strip()[:300]}")

# ---------------------------------------------------------------- 1. uv
rc, out, s = run([f"{VENV}/bin/uv", "venv", "/tmp/uvtest"], 120)
rc2, out2, s2 = run([f"{VENV}/bin/uv", "pip", "install", "--python", "/tmp/uvtest/bin/python", "tiktoken"], 300)
add("uv 0.13 (env/package manager)",
    "PASS" if rc == 0 and rc2 == 0 else "FAIL",
    f"venv: rc={rc} | install tiktoken into venv: rc={rc2}\n   {out2.strip()[:200]}", s + s2)

# ---------------------------------------------------------------- 2. ast-grep
demo = tempfile.mkdtemp()
open(f"{demo}/sample.py", "w").write(
    "def foo(a, b):\n    return a + b\n\nclass Old:\n    def legacy(self, x):\n        print(x)\n        return x\n")
rule = "id: find-defs\nlanguage: python\nrule:\n  pattern: def $N($$$)\n"
open(f"{demo}/rule.yml", "w").write(rule)
rc, out, s = run([f"{NPMBIN}/ast-grep", "scan", "-r", f"{demo}/rule.yml", demo], 120)
hits = out.count("sample.py")
add("ast-grep 0.50 (structural code search)",
    "PASS" if rc == 0 and hits >= 2 else ("PARTIAL" if rc == 0 else "FAIL"),
    f"rc={rc}, matches found referencing sample.py: {hits}\n   {out.strip()[:220]}", s)

# ---------------------------------------------------------------- 3. dotenvx
d2 = tempfile.mkdtemp()
env_plain = "SECRET_TOKEN=supersecret123\nAPI_KEY=abc\n"
open(f"{d2}/.env", "w").write(env_plain)
rc1, o1, _ = run([f"{NPMBIN}/dotenvx", "encrypt"], 120, cwd=d2)
enc = open(f"{d2}/.env").read()
rc2, o2, _ = run([f"{NPMBIN}/dotenvx", "get", "SECRET_TOKEN"], 120, cwd=d2)
ok = rc1 == 0 and rc2 == 0 and "supersecret123" in o2 and "supersecret123" not in enc
add("dotenvx 2.34 (secret management for agents)",
    "PASS" if ok else "FAIL",
    f"encrypt rc={rc1}; get rc={rc2}; plaintext hidden in file: {'supersecret123' not in enc}\n"
    f"   decrypted value returned: {o2.strip()[:80]!r}\n   encrypted file head: {enc.strip()[:80]!r}")

# ---------------------------------------------------------------- 4. pydantic-ai (offline agent run)
code = '''
import asyncio
from pydantic_ai import Agent
from pydantic_ai.models.test import TestModel
agent = Agent(TestModel())
@agent.tool_plain
def get_weather(city: str) -> str:
    """Get weather for a city."""
    return f"sunny in {city}"
r = asyncio.run(agent.run("What is the weather in Berlin?"))
print("OUTPUT:", r.output)
'''
rc, out, s = run([PY, "-c", code], 240)
add("pydantic-ai 2.55 (agent framework — offline TestModel run)",
    "PASS" if rc == 0 and "OUTPUT" in out else "FAIL",
    f"rc={rc}\n   {out.strip()[:260]}", s)

# ---------------------------------------------------------------- 5. DSPy (offline)
code = '''
import dspy
print("dspy", dspy.__version__)
class QA(dspy.Signature):
    """Answer with a single word."""
    question: str = dspy.InputField()
    answer: str = dspy.OutputField()
pred = dspy.Predict(QA)
print("signature built OK:", pred)
from dspy.utils.dummies import DummyLM
lm = DummyLM([{"answer": "4"}])
dspy.configure(lm=lm)
r = pred(question="2+2?")
print("RESULT:", r.answer)
'''
rc, out, s = run([PY, "-c", code], 300)
add("dspy 3.4 (prompt/program optimisation — offline DummyLM)",
    "PASS" if rc == 0 and "RESULT" in out else "FAIL",
    f"rc={rc}\n   {out.strip()[-260:]}", s)

# ---------------------------------------------------------------- 6. DeepEval (no-LLM metric)
code = '''
import deepeval
from deepeval.metrics import ExactMatchMetric
from deepeval.test_case import LLMTestCase
m = ExactMatchMetric()
tc = LLMTestCase(input="2+2", actual_output="4", expected_output="4")
m.measure(tc)
print("score:", m.score, "success:", m.success, "reason:", str(m.reason)[:80])
tc2 = LLMTestCase(input="2+2", actual_output="5", expected_output="4")
m2 = ExactMatchMetric(); m2.measure(tc2)
print("negative-case success:", m2.success)
'''
rc, out, s = run([PY, "-c", code], 300)
add("deepeval 4.2 (eval harness — offline deterministic metric)",
    "PASS" if rc == 0 and "success: True" in out and "negative-case success: False" in out else "FAIL",
    f"rc={rc}\n   {out.strip()[-260:]}", s)

# ---------------------------------------------------------------- 7. litellm proxy boot
rc, out, s = run([PY, "-c",
    "import litellm,litellm.proxy.proxy_server as p;"
    "print('litellm',litellm.__version__);"
    "print('proxy app:',type(p.app).__name__);"
    "print('routes:',len(p.app.routes))"], 300)
add("litellm 1.104 (model gateway — import + proxy app)",
    "PASS" if rc == 0 and "routes:" in out else "FAIL",
    f"rc={rc}\n   {out.strip()[-260:]}", s)

# ---------------------------------------------------------------- 8-12. imports only
for mod, label in [("mem0", "mem0ai 2.2 (memory)"),
                   ("graphiti_core", "graphiti-core 0.30 (temporal KG memory)"),
                   ("verifiers", "verifiers 0.3 (RL environments)"),
                   ("smolagents", "smolagents 1.26 (code agents)"),
                   ("opik", "opik 2.2 (tracing/evals)"),
                   ("mcpm", "mcpm 2.15 (MCP manager)")]:
    rc, out, s = run([PY, "-c", f"import {mod}; print('OK', getattr({mod},'__version__','?'))"], 300)
    add(label, "PASS" if rc == 0 else "FAIL", f"rc={rc} {out.strip()[-200:]}", s)

# ---------------------------------------------------------------- summary
print("\n" + "=" * 100)
print("SUMMARY")
print("=" * 100)
for n, v, d, s in rows:
    print(f"  {v:<8} {n}")
npass = sum(1 for r in rows if r[1] == "PASS")
print(f"\n  {npass}/{len(rows)} passed")
