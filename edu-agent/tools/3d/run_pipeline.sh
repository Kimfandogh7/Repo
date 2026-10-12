#!/usr/bin/env bash
# usage: run_pipeline.sh mesh|render   (always exits 0; state is in out3d/*.log)
set +e
MODE="$1"
ROOT="${GITHUB_WORKSPACE:-$PWD}"
OUT="$ROOT/out3d"; mkdir -p "$OUT"
LOG="$OUT/pipeline.log"
say() { echo "[$(date -u +%H:%M:%S)] $*" | tee -a "$LOG"; }

if [ "$MODE" = "mesh" ] && [ -f "$ROOT/edu-agent/artifacts/finale/3d/object.ply" ] && [ -z "$REMESH" ]; then
  mkdir -p "$OUT/mesh" && cp "$ROOT/edu-agent/artifacts/finale/3d/object.ply" "$OUT/mesh/"
  say "reusing committed mesh (set REMESH=1 to rebuild)"; exit 0
fi

if [ "$MODE" = "mesh" ]; then
  mkdir -p "$ROOT/edu-agent/artifacts/finale/3d"
  git -C "$ROOT" config user.name "arena-agent"; git -C "$ROOT" config user.email "agent@arena.ai"
  ( while true; do
      { date -u; free -m; ps -o rss=,etime=,cmd= -C python3 | head -2; tail -2 "$OUT/mesh.log" 2>/dev/null; } >> "$OUT/monitor.log"
      cp "$OUT/monitor.log" "$OUT/mesh.log" "$OUT/pipeline.log" "$ROOT/edu-agent/artifacts/finale/3d/" 2>/dev/null
      git -C "$ROOT" add -f edu-agent/artifacts/finale/3d >/dev/null 2>&1
      git -C "$ROOT" commit -qm "3d: پایش حافظه" >/dev/null 2>&1
      git -C "$ROOT" push -q origin HEAD:arena/758efc2d-repo >/dev/null 2>&1
      sleep 40
    done ) &
  MON=$!
  say "memory before mesh:"; free -m | tee -a "$LOG"
  export PYTHONPATH="$ROOT/edu-agent/tools/3d/shim"
  export TRIPOSR_DIR=/tmp/triposr
  /usr/bin/time -v python3 "$ROOT/edu-agent/tools/3d/mesh_from_image.py" \
    "$ROOT/edu-agent/artifacts/finale/car_studio.png" "$OUT/mesh" "${RES:-192}" > "$OUT/mesh.log" 2>&1
  say "mesh exit=$?"; grep -E 'Maximum resident|Elapsed' "$OUT/mesh.log" | tee -a "$LOG"
  tail -6 "$OUT/mesh.log" | tee -a "$LOG"
  kill $MON 2>/dev/null
fi

if [ "$MODE" = "render" ]; then
  if [ ! -f "$OUT/mesh/object.ply" ]; then say "no mesh, skipping render"; exit 0; fi
  ANGLES="0,40,80,120,160,200,240,280,320"
  blender -b -P "$ROOT/edu-agent/tools/3d/render_turntable.py" -- \
    "$OUT/mesh/object.ply" "$OUT/frames" "$ANGLES" 1080 1920 48 > "$OUT/render.log" 2>&1
  say "render exit=$?"; grep -c '^rendered' "$OUT/render.log" | tee -a "$LOG"
fi
exit 0
