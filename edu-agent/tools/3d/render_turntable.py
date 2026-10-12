"""Render a coloured PLY mesh to transparent PNG frames with Blender (Cycles, CPU).

Run headless:
    blender -b -P render_turntable.py -- <object.ply> <out_dir> <angles_deg,comma> [width height samples]

Each angle rotates the object around the vertical axis. Output: <out_dir>/car_<angle>.png (RGBA).
"""
import math
import os
import sys

import bpy

argv = sys.argv[sys.argv.index("--") + 1:]
ply, out_dir = argv[0], argv[1]
angles = [float(a) for a in argv[2].split(",")]
W = int(argv[3]) if len(argv) > 3 else 1080
H = int(argv[4]) if len(argv) > 4 else 1920
SAMPLES = int(argv[5]) if len(argv) > 5 else 48
os.makedirs(out_dir, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.wm.ply_import(filepath=ply)
obj = next(o for o in bpy.context.scene.objects if o.type == "MESH")
bpy.context.view_layer.objects.active = obj
obj.select_set(True)

# Normalise: centre on bounds, scale longest side to 2 units.
bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center="BOUNDS")
obj.location = (0, 0, 0)
dims = max(obj.dimensions)
s = 2.0 / dims
obj.scale = (s, s, s)  # rotate about the bounds centre; no transform_apply (multi-user data)

# TripoSR meshes are longest along Y; the camera looks along Y, so the car would be
# seen nose-on. Base rotation 90 deg puts the length across the frame.
BASE_ROT = 90.0

# Smooth shading + a Smooth modifier to remove the faceted "crystal" look of raw marching cubes.
bpy.ops.object.shade_smooth()
mod = obj.modifiers.new("smooth", "SMOOTH")
mod.factor = 0.6
mod.iterations = 12

# Material: use vertex colours if the mesh has them, else a clean red.
mat = bpy.data.materials.new("car")
mat.use_nodes = True
nt = mat.node_tree
bsdf = nt.nodes["Principled BSDF"]
bsdf.inputs["Roughness"].default_value = 0.22
bsdf.inputs["Specular IOR Level"].default_value = 0.6
if obj.data.color_attributes:
    va = nt.nodes.new("ShaderNodeVertexColor")
    va.layer_name = obj.data.color_attributes[0].name
    nt.links.new(va.outputs["Color"], bsdf.inputs["Base Color"])
else:
    bsdf.inputs["Base Color"].default_value = (0.8, 0.02, 0.01, 1)
obj.data.materials.clear()
obj.data.materials.append(mat)

# Camera looking at the origin from slightly above.
cam_data = bpy.data.cameras.new("cam")
cam_data.lens = 58
cam = bpy.data.objects.new("cam", cam_data)
bpy.context.collection.objects.link(cam)
cam.location = (0, -7.0, 0.9)
track = cam.constraints.new("TRACK_TO")
empty = bpy.data.objects.new("target", None)
bpy.context.collection.objects.link(empty)
empty.location = (0, 0, 0)
track.target = empty
track.track_axis = "TRACK_NEGATIVE_Z"
track.up_axis = "UP_Y"
bpy.context.scene.camera = cam


def area(name, loc, energy, size):
    ld = bpy.data.lights.new(name, "AREA")
    ld.energy = energy
    ld.size = size
    lo = bpy.data.objects.new(name, ld)
    bpy.context.collection.objects.link(lo)
    lo.location = loc
    tr = lo.constraints.new("TRACK_TO")
    tr.target = empty
    tr.track_axis = "TRACK_NEGATIVE_Z"
    tr.up_axis = "UP_Y"


area("key", (4, -6, 5), 2600, 6)
area("fill", (-5, -4, 2), 700, 8)
area("rim", (0, 6, 4), 2400, 4)

scene = bpy.context.scene
scene.render.engine = "CYCLES"
scene.cycles.device = "CPU"
scene.cycles.samples = SAMPLES
scene.cycles.use_denoising = False  # apt Blender has no OpenImageDenoise
scene.render.resolution_x = W
scene.render.resolution_y = H
scene.render.resolution_percentage = 100
scene.render.film_transparent = True
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_mode = "RGBA"

for a in angles:
    obj.rotation_euler = (0, 0, math.radians(BASE_ROT + a))
    scene.render.filepath = os.path.join(out_dir, f"car_{int(round(a)):03d}.png")
    bpy.ops.render.render(write_still=True)
    print("rendered", scene.render.filepath, flush=True)
