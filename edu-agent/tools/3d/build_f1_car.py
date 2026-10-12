"""Build a stylised Formula 1 car from primitives in Blender and render turntable frames.

Proportions follow a real F1 car (length ~5.6 m, width ~2 m, height ~1 m); nose points +X,
the car is side-on to the camera at angle 0. Everything is joined into one object so the
turntable rotates the whole car.

Run headless:
    blender -b -P build_f1_car.py -- <out_dir> <angles_deg,comma> [width height samples]
"""
import math
import os
import sys

import bpy

argv = sys.argv[sys.argv.index("--") + 1:]
out_dir = argv[0]
angles = [float(a) for a in argv[1].split(",")] if argv[1] != "none" else [-999.0]
W = int(argv[2]) if len(argv) > 2 else 1080
H = int(argv[3]) if len(argv) > 3 else 1920
SAMPLES = int(argv[4]) if len(argv) > 4 else 96
os.makedirs(out_dir, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)


def mat(name, rgba, metallic=0.0, rough=0.35, emit=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = rgba
    b.inputs["Metallic"].default_value = metallic
    b.inputs["Roughness"].default_value = rough
    if emit:
        b.inputs["Emission Color"].default_value = rgba
        b.inputs["Emission Strength"].default_value = emit
    return m


RED = mat("ferrari_red", (0.80, 0.02, 0.01, 1), metallic=0.25, rough=0.18)
WHITE = mat("white", (0.92, 0.92, 0.90, 1), metallic=0.0, rough=0.3)
BLACK = mat("carbon", (0.015, 0.015, 0.016, 1), metallic=0.1, rough=0.55)
RUBBER = mat("rubber", (0.02, 0.02, 0.02, 1), metallic=0.0, rough=0.8)
CHROME = mat("chrome", (0.8, 0.8, 0.82, 1), metallic=1.0, rough=0.12)
YELLOW = mat("accent", (1.0, 0.82, 0.05, 1), metallic=0.0, rough=0.3)

parts = []


def smooth(o):
    for p in o.data.polygons:
        p.use_smooth = True


def add(kind, loc, scale=(1, 1, 1), rot=(0, 0, 0), m=None, **kw):
    if kind == "sphere":
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=loc, segments=48, ring_count=24)
    elif kind == "cube":
        bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    elif kind == "cyl":
        bpy.ops.mesh.primitive_cylinder_add(radius=kw.get("r", 0.5), depth=kw.get("d", 1),
                                            location=loc, vertices=56)
    elif kind == "torus":
        bpy.ops.mesh.primitive_torus_add(major_radius=kw["R"], minor_radius=kw["r"],
                                         location=loc, major_segments=64, minor_segments=12)
    o = bpy.context.active_object
    o.scale = scale
    o.rotation_euler = rot
    if m is not None:
        o.data.materials.append(m)
    if kind in ("sphere", "torus", "cyl"):
        smooth(o)
    parts.append(o)
    return o


# --- monocoque and bodywork -------------------------------------------------
add("sphere", (0, 0, 0.42), (1.9, 0.42, 0.22), m=RED)                 # tub
add("sphere", (2.25, 0, 0.30), (1.05, 0.2, 0.13), m=RED)               # tapered nose
add("sphere", (2.85, 0, 0.23), (0.28, 0.1, 0.06), m=WHITE)             # nose tip
add("sphere", (-0.55, 0, 0.80), (0.95, 0.26, 0.26), m=RED)             # engine cover
add("sphere", (0.1, 0.62, 0.40), (1.15, 0.28, 0.2), m=RED)             # sidepod L
add("sphere", (0.1, -0.62, 0.40), (1.15, 0.28, 0.2), m=RED)            # sidepod R
add("sphere", (0.2, 0, 0.66), (0.5, 0.24, 0.12), m=BLACK)              # cockpit
add("sphere", (0.2, 0, 0.73), (0.14, 0.14, 0.14), m=WHITE)             # helmet
add("sphere", (0.2, 0, 0.75), (0.1, 0.1, 0.08), m=RED)                 # visor
add("cyl", (-1.95, 0, 0.62), r=0.07, d=0.5, rot=(0, math.radians(90), 0), m=CHROME)  # exhaust
add("cube", (-1.1, 0, 0.42), (0.18, 0.8, 0.12), m=YELLOW)              # accent strip (sponsor band)

# --- wings --------------------------------------------------------------------
add("cube", (2.45, 0, 0.12), (0.45, 2.15, 0.05), m=BLACK)              # front wing plane
add("cube", (2.45, 0, 0.2), (0.25, 2.15, 0.03), m=BLACK)               # front flap
for y in (1.07, -1.07):
    add("cube", (2.35, y, 0.2), (0.35, 0.05, 0.42), m=BLACK)           # front endplates
add("cube", (-2.2, 0, 1.0), (0.52, 1.5, 0.05), m=BLACK)                # rear wing plane
add("cube", (-2.05, 0, 1.2), (0.36, 1.5, 0.04), m=RED)                 # rear upper flap
for y in (0.76, -0.76):
    add("cube", (-2.2, y, 0.78), (0.6, 0.05, 0.62), m=BLACK)           # rear endplates
add("cube", (-1.95, 0, 0.68), (0.14, 0.08, 0.6), m=BLACK)              # rear pylon

# --- wheels -------------------------------------------------------------------
WHEELS = [(1.75, 1.0, 0.36, 0.36), (1.75, -1.0, 0.36, 0.36),
          (-1.6, 1.0, 0.38, 0.42), (-1.6, -1.0, 0.38, 0.42)]
for x, y, r, wdt in WHEELS:
    rot = (math.radians(90), 0, 0)
    add("cyl", (x, y, r), rot=rot, r=r, d=wdt, m=RUBBER)                # tyre
    add("cyl", (x, y + (0.01 if y > 0 else -0.01), r), rot=rot, r=r * 0.58, d=wdt + 0.02, m=CHROME)  # rim

# --- join, normalise, light, render ------------------------------------------
bpy.ops.object.select_all(action="DESELECT")
for o in parts:
    o.select_set(True)
bpy.context.view_layer.objects.active = parts[0]
bpy.ops.object.join()
car = bpy.context.active_object
car.name = "f1car"
bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center="BOUNDS")
car.location = (0, 0, 0)
def _world_bbox(o):
    import mathutils
    ws = [o.matrix_world @ v.co for v in o.data.vertices]
    return [(min(w[i] for w in ws), max(w[i] for w in ws)) for i in range(3)]

print("RAW dims", tuple(round(d, 3) for d in car.dimensions), "parts", len(parts), flush=True)
for ax, (lo, hi) in zip("XYZ", _world_bbox(car)):
    print(f"RAW WORLD {ax}: {lo:.3f} .. {hi:.3f}", flush=True)
if angles == [-999.0]:
    print("GEOM_ONLY exit", flush=True)
    sys.exit(0)
s = 2.0 / max(car.dimensions)
car.scale = (s, s, s)
for ax, (lo, hi) in zip("XYZ", _world_bbox(car)):
    print(f"NORM WORLD {ax}: {lo:.3f} .. {hi:.3f}", flush=True)

cam_data = bpy.data.cameras.new("cam")
cam_data.lens = 58
cam = bpy.data.objects.new("cam", cam_data)
bpy.context.collection.objects.link(cam)
cam.location = (0, -7.0, 0.9)
target = bpy.data.objects.new("target", None)
bpy.context.collection.objects.link(target)
target.location = (0, 0, 0)
tr = cam.constraints.new("TRACK_TO")
tr.target = target
tr.track_axis = "TRACK_NEGATIVE_Z"
tr.up_axis = "UP_Y"
bpy.context.scene.camera = cam


def area(name, loc, energy, size):
    ld = bpy.data.lights.new(name, "AREA")
    ld.energy = energy
    ld.size = size
    lo = bpy.data.objects.new(name, ld)
    bpy.context.collection.objects.link(lo)
    lo.location = loc
    t = lo.constraints.new("TRACK_TO")
    t.target = target
    t.track_axis = "TRACK_NEGATIVE_Z"
    t.up_axis = "UP_Y"


area("key", (4, -6, 5), 2600, 6)
area("fill", (-5, -4, 2), 800, 8)
area("rim", (0, 6, 4), 2600, 4)

scene = bpy.context.scene
scene.render.engine = "CYCLES"
scene.cycles.device = "CPU"
scene.cycles.samples = SAMPLES
scene.cycles.use_denoising = False
scene.render.resolution_x = W
scene.render.resolution_y = H
scene.render.resolution_percentage = 100
scene.render.film_transparent = True
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_mode = "RGBA"

for a in angles:
    car.rotation_euler = (0, 0, math.radians(a))
    scene.render.filepath = os.path.join(out_dir, f"car_{int(round(a)):03d}.png")
    bpy.ops.render.render(write_still=True)
    print("rendered", scene.render.filepath, flush=True)
