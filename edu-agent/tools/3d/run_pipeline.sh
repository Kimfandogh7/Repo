#!/usr/bin/env bash
# image -> TripoSR mesh -> Blender turntable. Never exits non-zero so logs always get committed.
set +e
ROOT="${GITHUB_WORKSPACE:-$PWD}"
OUT="$ROOT/out3d"; mkdir -p "$OUT"
LOG="$OUT/pipeline.log"
say() { echo "[$(date -u +%H:%M:%S)] $*" | tee -a "$LOG"; }
say "memory:"; free -m | tee -a "$LOG"; nproc | tee -a "$LOG"

export PYTHONPATH="$ROOT/edu-agent/tools/3d/shim"
export TRIPOSR_DIR=/tmp/triposr
python3 "$ROOT/edu-agent/tools/3d/mesh_from_image.py" \
  "$ROOT/edu-agent/artifacts/finale/car_studio.png" "$OUT/mesh" 256 > "$OUT/mesh.log" 2>&1
MESH_RC=$?
say "mesh exit=$MESH_RC"; tail -4 "$OUT/mesh.log" | tee -a "$LOG"
free -m | tee -a "$LOG"

if [ "$MESH_RC" = "0" ] && [ -f "$OUT/mesh/object.ply" ]; then
  ANGLES="0,40,80,120,160,200,240,280,320"
  blender -b -P "$ROOT/edu-agent/tools/3d/render_turntable.py" -- \
    "$OUT/mesh/object.ply" "$OUT/frames" "$ANGLES" 1080 1920 48 > "$OUT/render.log" 2>&1
  say "render exit=$?"; grep -cE '^rendered' "$OUT/render.log" | tee -a "$LOG"
else
  say "skipping render: no mesh"
fi
exit 0
