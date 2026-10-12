#!/usr/bin/env bash
# usage: run_pipeline.sh mesh|render   (always exits 0; state is in out3d/*.log)
set +e
MODE="$1"
ROOT="${GITHUB_WORKSPACE:-$PWD}"
OUT="$ROOT/out3d"; mkdir -p "$OUT"
LOG="$OUT/pipeline.log"
say() { echo "[$(date -u +%H:%M:%S)] $*" | tee -a "$LOG"; }

if [ "$MODE" = "mesh" ]; then
  say "memory before mesh:"; free -m | tee -a "$LOG"
  export PYTHONPATH="$ROOT/edu-agent/tools/3d/shim"
  export TRIPOSR_DIR=/tmp/triposr
  /usr/bin/time -v python3 "$ROOT/edu-agent/tools/3d/mesh_from_image.py" \
    "$ROOT/edu-agent/artifacts/finale/car_studio.png" "$OUT/mesh" "${RES:-192}" > "$OUT/mesh.log" 2>&1
  say "mesh exit=$?"; grep -E 'Maximum resident|Elapsed' "$OUT/mesh.log" | tee -a "$LOG"
  tail -6 "$OUT/mesh.log" | tee -a "$LOG"
fi

if [ "$MODE" = "render" ]; then
  if [ ! -f "$OUT/mesh/object.ply" ]; then say "no mesh, skipping render"; exit 0; fi
  ANGLES="0,40,80,120,160,200,240,280,320"
  blender -b -P "$ROOT/edu-agent/tools/3d/render_turntable.py" -- \
    "$OUT/mesh/object.ply" "$OUT/frames" "$ANGLES" 1080 1920 48 > "$OUT/render.log" 2>&1
  say "render exit=$?"; grep -c '^rendered' "$OUT/render.log" | tee -a "$LOG"
fi
exit 0
