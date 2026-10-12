"""Drop-in replacement for torchmcubes.marching_cubes (CPU, via scikit-image).

torchmcubes needs a CUDA toolchain to build; TripoSR only calls
marching_cubes(grid, level) -> (verts, faces), so skimage is enough.
"""
import numpy as np
import torch
from skimage.measure import marching_cubes as _mc


def marching_cubes(grid, level):
    g = grid.detach().cpu().numpy().astype(np.float32)
    verts, faces, _, _ = _mc(g, level=float(level))
    return (torch.from_numpy(verts.copy()).to(grid.device),
            torch.from_numpy(faces.astype(np.int64).copy()).to(grid.device))
