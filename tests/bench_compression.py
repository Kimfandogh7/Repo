#!/usr/bin/env python3
"""
STRICT BENCHMARK: do the token-compression tools actually deliver?
Measures REAL token counts (tiktoken cl100k_base) before/after, and checks
whether CRITICAL information (failures, errors, paths) survives.

This is deliberately adversarial: we do not trust vendor numbers.
"""
import json, os, random, subprocess, sys, textwrap
import tiktoken  # noqa: F401  (kept for parity; real counting via node/js-tiktoken)
import subprocess as _sp
NODE = "/home/user/agent-test/tok/count.js"
def tok(s):
    """Real cl100k_base token count, computed OFFLINE via js-tiktoken (bundled ranks)."""
    p = _sp.run(["node", NODE], input=s, capture_output=True, text=True, timeout=120)
    if p.returncode != 0:
        raise RuntimeError(p.stderr[:200])
    return int(p.stdout.strip())

# ---------------------------------------------------------------- fixtures
random.seed(7)

def fixture_git_status():
    lines = ["On branch feature/agent-toolkit",
             "Your branch is ahead of 'origin/main' by 14 commits.",
             "  (use \"git push\" to publish your local commits)", ""]
    states = ["M ", "?? ", "A ", " D ", "R "]
    dirs = ["src/", "src/core/", "src/handlers/", "tests/", "docs/", "scripts/", ".github/workflows/"]
    exts = [".py", ".ts", ".md", ".json", ".yml", ".toml"]
    names = ["engine","parser","router","codec","index","client","server","util","schema","loader","worker","cache"]
    files = []
    for i in range(120):
        d = random.choice(dirs); n = random.choice(names)+str(random.randint(1,40))
        files.append(f"{d}{n}{random.choice(exts)}")
    for f in files[:60]:
        lines.append(f"\tmodified:   {f}")
    lines.append("")
    lines.append("Untracked files:")
    lines.append("  (use \"git add <file>...\" to include in what will be committed)")
    for f in files[60:]:
        lines.append(f"\t{f}")
    lines += ["", "no changes added to commit (use \"git add\" and/or \"git commit -a\")"]
    return "\n".join(lines)

def fixture_pytest():
    out = ["platform linux -- Python 3.11.2, pytest-8.3.2, pluggy-1.5.0",
           "rootdir: /home/user/project", "collected 214 items", ""]
    classes = ["TestParser","TestRouter","TestCodec","TestEngine","TestCache","TestLoader"]
    methods = ["test_basic","test_edge_case","test_unicode","test_empty_input","test_large_payload",
               "test_error_path","test_retry","test_timeout","test_concurrent","test_serialization"]
    for c in classes:
        out.append(f"tests/test_{c.lower()[4:]}.py ")
        row = ""
        for i, m in enumerate(methods):
            row += "."
            if (i+1) % 40 == 0:
                out.append(row + f"  [ {i+1}% ]"); row = ""
        out.append(row + "".join("F" if j==7 else "." for j in range(4)) + "   [100%]")
        out.append("")
        out.append("=" * 30 + f" FAILURES {c} " + "=" * 30)
        out.append(f"______ {c}.{methods[7]} ______")
        out.append("")
        out.append(textwrap.dedent(f"""\
            def {methods[7]}(self):
                result = {c.lower()[4:]}.run(payload=SAMPLE)
            >       assert result.status == "ok"
            E       AssertionError: assert 'error' == 'ok'
            E        +  where 'error' = Result(status='error', retries=3).status
            E       tests/test_{c.lower()[4:]}.py:{random.randint(20,300)}: AssertionError"""))
        out.append("")
    out.append("=========== short test summary info ============")
    for c in classes:
        out.append(f"FAILED tests/test_{c.lower()[4:]}.py::{c}::{methods[7]} - AssertionError")
    out.append("=" * 20 + " 6 failed, 208 passed in 43.21s " + "=" * 20)
    return "\n".join(out)

def fixture_npm_install():
    out = []
    for i in range(60):
        out.append(f"npm http fetch GET 200 https://registry.npmjs.org/@scope%2fpkg-{i} 183ms (cache miss)")
    for i in range(40):
        out.append(f"npm http fetch GET 200 https://registry.npmjs.org/pkg-{i}/-/pkg-{i}-1.{i}.0.tgz 92ms")
    out += ["", "added 431 packages, and audited 432 packages in 21s", "",
            "102 packages are looking for funding", "  run `npm fund` for details", "",
            "1 high severity vulnerability", "",
            "To address all issues, run:", "  npm audit fix", "",
            "npm notice", "npm notice New major version of npm available! 10.9.8 -> 11.2.0",
            "npm notice Changelog: https://github.com/npm/cli/releases/tag/v11.2.0",
            "npm notice Run npm install -g npm@11.2.0 to update!"]
    return "\n".join(out)

def fixture_big_json():
    recs = []
    for i in range(300):
        recs.append({
            "id": f"evt_{i:05d}", "timestamp": "2026-10-11T09:%02d:%02dZ" % (i%60, (i*7)%60),
            "level": random.choice(["INFO","INFO","INFO","DEBUG","WARN"]),
            "service": random.choice(["api-gateway","auth","billing","search","notifier"]),
            "message": f"request completed in {random.randint(3,900)}ms",
            "trace_id": f"{i:032x}", "user_id": f"u_{random.randint(1000,9999)}",
            "metadata": {"region":"eu-central-1","version":"2.14.3","cached": i%3==0, "bytes": random.randint(200,9000)},
        })
    return json.dumps({"page":1,"per_page":300,"total":12483,"events":recs}, indent=2)

def fixture_build_log():
    out = []
    for i in range(80):
        out.append(f"[{i//10:02d}:{(i*13)%60:02d}:{(i*7)%60:02d}] [INFO] Compiling module_{i}.rs (elapsed {random.randint(20,900)}ms)")
    out += ["warning: unused variable `ctx`", "  --> src/handlers/router.rs:142:9",
            "    |", "142 |     let ctx = build_context(&cfg);", "    |         ^^^ help: if this is intentional, prefix it with an underscore: `_ctx`",
            "    |", "    = note: `#[warn(unused_variables)]` on by default", "",
            "error[E0308]: mismatched types", "  --> src/core/engine.rs:88:21",
            "   |", "88  |     let n: u32 = compute(&input);", "   |             ---   ^^^^^^^^^^^^^^ expected `u32`, found `u64`",
            "   |             |", "   |             expected due to this", "",
            "error: could not compile `engine` (lib) due to 1 previous error"]
    return "\n".join(out)

FIXTURES = {
    "git status (120 files)":   (fixture_git_status(),  ["modified:", "Untracked files:"]),
    "pytest (214 tests, 6 fail)": (fixture_pytest(),     ["FAILED", "AssertionError", "6 failed"]),
    "npm install (431 pkgs)":   (fixture_npm_install(), ["1 high severity vulnerability", "added 431 packages"]),
    "JSON API (300 records)":   (fixture_big_json(),    ["evt_00299", "total", "trace_id"]),
    "Rust build log (error)":   (fixture_build_log(),   ["error[E0308]", "mismatched types", "could not compile"]),
}

# ---------------------------------------------------------------- results
results = []
def record(tool, name, before, after, crit_total, crit_kept, note=""):
    red = 0.0 if before == 0 else 100.0*(before-after)/before
    results.append(dict(tool=tool, fixture=name, before=before, after=after,
                        reduction=red, crit=f"{crit_kept}/{crit_total}",
                        lossless=(crit_kept==crit_total), note=note))

def check_critical(text, markers):
    kept = sum(1 for m in markers if m in text)
    return kept, len(markers)

# ---------------------------------------------------------------- headroom
try:
    from headroom.compression import UniversalCompressor, UniversalCompressorConfig
    uc = UniversalCompressor(config=UniversalCompressorConfig(use_magika=False, use_kompress=False))
    for name, (text, markers) in FIXTURES.items():
        before = tok(text)
        r = uc.compress(text)
        after_text = r.content if hasattr(r, "content") else str(r)
        after = tok(after_text)
        kept, tot = check_critical(after_text, markers)
        record("headroom-ai 0.40", name, before, after, tot, kept,
               f"ratio_field={getattr(r,'ratio',None)}")
except Exception as e:
    results.append(dict(tool="headroom-ai 0.40", fixture="ALL", before=0, after=0,
                        reduction=0.0, crit="0/0", lossless=False, note=f"ERROR: {type(e).__name__}: {e}"))

# ---------------------------------------------------------------- entroly
import tempfile, shutil
ENT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "venv/bin/entroly")
try:
    tmpd = tempfile.mkdtemp(prefix="entroly_")
    for name, (text, markers) in FIXTURES.items():
        src = os.path.join(tmpd, "in.txt"); dst = os.path.join(tmpd, "out.txt")
        open(src, "w").write(text)
        before = tok(text)
        p = subprocess.run([ENT, "compress", src, "--out", dst, "--json"],
                           capture_output=True, text=True, timeout=300,
                           env={**os.environ, "ENTROLY_DIR": os.path.join(tmpd, "state")})
        if p.returncode != 0:
            record("entroly 1.0.86", name, before, before, 0, 1, f"CLI failed rc={p.returncode}: {p.stderr.strip()[:160]}")
            continue
        out_text = open(dst).read() if os.path.exists(dst) else ""
        after = tok(out_text) if out_text else before
        kept, tot = check_critical(out_text, markers)
        try:
            rec = json.loads(p.stdout or "{}")
        except Exception:
            rec = {}
        record("entroly 1.0.86", name, before, after, tot, kept,
               f"receipt_keys={list(rec)[:6]}")
    shutil.rmtree(tmpd, ignore_errors=True)
except Exception as e:
    results.append(dict(tool="entroly 1.0.86", fixture="ALL", before=0, after=0,
                        reduction=0.0, crit="0/0", lossless=False, note=f"ERROR: {type(e).__name__}: {e}"))
print()

# ---------------------------------------------------------------- report
print("=" * 104)
print("STRICT BENCHMARK — tool-output token compression (real tiktoken cl100k_base counts)")
print("=" * 104)
print(f"{'tool':<20} {'fixture':<30} {'before':>8} {'after':>8} {'saved %':>9} {'critical':>10} {'lossless':>9}")
print("-" * 104)
for r in results:
    print(f"{r['tool']:<20} {r['fixture']:<30} {r['before']:>8} {r['after']:>8} "
          f"{r['reduction']:>8.1f}% {r['crit']:>10} {'YES' if r['lossless'] else 'NO':>9}")
print("-" * 104)
ok = [r for r in results if r['before'] and r['lossless']]
if ok:
    avg = sum(r['reduction'] for r in ok)/len(ok)
    print(f"Average reduction over fixtures where ALL critical markers survived: {avg:.1f}%  ({len(ok)}/{len(results)})")
print()
print("NOTES:")
for r in results:
    if r['note']: print(f"  - {r['tool']} / {r['fixture']}: {r['note']}")
