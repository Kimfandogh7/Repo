"""Finale deck: put the built 3D car on every slide of the 5-slide morph deck.

Input : edu-agent/artifacts/ferrariv5/ferrariv5.pptx   (morph chain on !!stage groups)
        edu-agent/artifacts/finale/f1/car_*.png          (Blender turntable, RGBA)
Output: edu-agent/artifacts/finale/finale.pptx

Each slide gets one picture named "!!car". Same name on every slide = PowerPoint Morph
moves, scales and cross-fades it between slides, so the car visibly continues and turns.
All car crops share one aspect ratio so Morph never stretches them.
"""
import copy
import os
import sys

from PIL import Image, ImageDraw, ImageFilter
from pptx import Presentation

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
SRC = os.path.join(ROOT, "edu-agent/artifacts/ferrariv5/ferrariv5.pptx")
RENDERS = os.path.join(ROOT, "edu-agent/artifacts/finale/f1")
OUT_DIR = os.path.join(ROOT, "edu-agent/artifacts/finale")
OUT = os.path.join(OUT_DIR, "finale.pptx")
CROPS = os.path.join(OUT_DIR, "crops")
PX = 9525  # EMU per pixel on the 1080x1920 story canvas

# Shared crop box, union of all turntable silhouettes (with padding) -> one aspect ratio.
CROP = (60, 800, 1020, 1150)  # 960 x 350
ASPECT = (CROP[2] - CROP[0]) / (CROP[3] - CROP[1])

# slide -> (angle, x, y, width_px)
PLAN = {
    1: (0, 60, 250, 960),     # hero, big, top
    2: (120, 180, 1625, 720),  # under the bars (was 520px: too small to read)
    3: (200, 140, 180, 800),   # big, top
    4: (280, 180, 1625, 720),  # under the stats
    5: (40, 160, 781, 760),    # centred over the rings
}


def dark_glow(size):
    """Soft studio spotlight: dark radial ellipse that fades to transparent at the edges."""
    w, h = size
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for k in range(40):
        t = k / 40
        rx = int(w * 0.48 * (1 - t * 0.85))
        ry = int(h * 0.46 * (1 - t * 0.85))
        a = int(190 * (t ** 0.8)) if t < 1 else 0
        d.ellipse([w / 2 - rx, h / 2 - ry, w / 2 + rx, h / 2 + ry], fill=(14, 3, 3, 255 - a))
    return layer.filter(ImageFilter.GaussianBlur(10))


def make_crop(angle):
    src = os.path.join(RENDERS, f"car_{angle:03d}.png")
    car = Image.open(src).convert("RGBA").crop(CROP)
    glow = dark_glow(car.size)
    # glow stays dark; car sits on top of it
    base = Image.new("RGBA", car.size, (0, 0, 0, 0))
    base.alpha_composite(glow)
    base.alpha_composite(car)
    os.makedirs(CROPS, exist_ok=True)
    out = os.path.join(CROPS, f"car_{angle:03d}.png")
    base.save(out)
    return out


def main():
    prs = Presentation(SRC)
    for idx, slide in enumerate(prs.slides, 1):
        angle, x, y, w_px = PLAN[idx]
        # 1) drop the old photo layers from the stage groups on slides 1 and 3
        for sh in list(slide.shapes):
            if sh.name == "!!stage" and sh.shape_type == 6:
                for child in list(sh.shapes):
                    if child.shape_type == 13:  # PICTURE
                        child._element.getparent().remove(child._element)
        # 2) add the car as a top-level picture with the shared morph name
        path = make_crop(angle)
        w = w_px * PX
        h = int(w / ASPECT)
        pic = slide.shapes.add_picture(path, x * PX, y * PX, width=w, height=h)
        pic._element.nvPicPr.cNvPr.set("name", "!!car")
        pic._element.nvPicPr.cNvPr.set("descr", f"F1 car, turntable angle {angle} deg")
        # keep it above the stage groups: move right after the first !!stage group
        tree = slide.shapes._spTree
        stage = next(sh for sh in slide.shapes if sh.name == "!!stage")
        tree.remove(pic._element)
        stage._element.addnext(pic._element)
        print(f"slide {idx}: car angle={angle} box=({x},{y}) {w_px}x{round(w_px / ASPECT)} px")
    os.makedirs(OUT_DIR, exist_ok=True)
    prs.save(OUT)
    print("saved", OUT)


if __name__ == "__main__":
    sys.exit(main())
