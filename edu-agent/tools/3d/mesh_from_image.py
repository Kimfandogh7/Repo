"""Image -> coloured triangle mesh with TripoSR (MIT, stabilityai/TripoSR).

Usage (on a machine with TripoSR cloned at $TRIPOSR_DIR and HF access):
    python mesh_from_image.py <input.png> <out_dir> [resolution]

Writes <out_dir>/object.ply (vertex colours) and <out_dir>/input_rgb.png
(the background-removed, composited input the model actually saw).
"""
import os
import sys

import numpy as np
import torch
from PIL import Image

TRIPOSR_DIR = os.environ.get("TRIPOSR_DIR", "/tmp/triposr")
sys.path.insert(0, TRIPOSR_DIR)

from tsr.system import TSR  # noqa: E402
from tsr.utils import remove_background, resize_foreground  # noqa: E402
import rembg  # noqa: E402


def main():
    src, out_dir = sys.argv[1], sys.argv[2]
    res = int(sys.argv[3]) if len(sys.argv) > 3 else 256
    os.makedirs(out_dir, exist_ok=True)
    device = "cuda" if torch.cuda.is_available() else "cpu"

    model = TSR.from_pretrained(
        "stabilityai/TripoSR",
        config_name="config.yaml",
        weight_name="model.ckpt",
    )
    model.renderer.set_chunk_size(8192)
    model.to(device)

    # Background removal exactly as TripoSR's own run.py does it.
    session = rembg.new_session("u2net")  # default is bria-rmbg (1 GB) and OOMs the runner
    img = Image.open(src).convert("RGB")
    img = remove_background(img, session)
    img = resize_foreground(img, 0.85)
    arr = np.array(img).astype(np.float32) / 255.0
    rgb = arr[:, :, :3] * arr[:, :, 3:4] + 0.5 * (1 - arr[:, :, 3:4])
    img = Image.fromarray((rgb * 255.0).astype(np.uint8))
    img.save(os.path.join(out_dir, "input_rgb.png"))

    with torch.no_grad():
        codes = model([img], device=device)
        meshes = model.extract_mesh(codes, has_vertex_color=True, resolution=res)
    meshes[0].export(os.path.join(out_dir, "object.ply"))
    m = meshes[0]
    print("vertices", len(m.vertices), "faces", len(m.faces))
    print("extents", m.extents)


if __name__ == "__main__":
    main()
