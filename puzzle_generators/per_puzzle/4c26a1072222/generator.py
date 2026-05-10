"""Generator for b0722778.

Rule: infer 2x2 transform and color map from A/B bands, then apply
to C.

Combinatorial axes (8): grid_h/w, transform, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_bands, single_band, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4c26a1072222"
VERSION = "1.1.0"
TASK_ID = "4c26a1072222"
SUMMARY = "Infer 2x2 transform and color map from A/B bands; apply to C."

INVARIANTS = [
    "each nonzero band is two rows high",
    "A, B, and C are 2x2 blocks at fixed column offsets",
    "B provides a color mapping from a transformed A",
    "all eight colors are distinct and non-zero",
]

TRANSFORMS = ("identity", "flip_lr")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_bands", "single_band", "full_grid")
HELPFUL_TEXTURES = TRANSFORMS

AXES = {
    "grid_h":         {"type": "int", "default": "5", "valid": "5"},
    "grid_w":         {"type": "int", "default": "9", "valid": "9"},
    "transform":      {"type": "str", "default": "rng helpful",
                       "valid": "|".join(TRANSFORMS)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "8", "valid": "8"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "8", "valid": "8"},
    "texture":        {"type": "str", "default": "alias for transform",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    tx = overrides.get("texture")
    if tx in TRANSFORMS:
        transform = tx
    else:
        transform = ctx.draw_choice("transform", list(TRANSFORMS))
        if "transform" not in overrides:
            transform = "identity" if sample_index % 2 == 0 else "flip_lr"
    a, b, c, d, ma, mb, mc, md = ctx.draw_distinct_colors("colors", n=8, exclude={0})
    g = full_grid(5, 9, 0)
    rows = [0, 3]
    for band, r0 in enumerate(rows):
        avals = [[a, b], [c, d]] if band == 0 else [[b, c], [d, a]]
        cmap = {a: ma, b: mb, c: mc, d: md}
        if transform == "identity":
            bvals = [[cmap[v] for v in row] for row in avals]
            cvals = [[d, c], [b, a]]
        else:
            bvals = [[cmap[row[1]], cmap[row[0]]] for row in avals]
            cvals = [[a, d], [c, b]]
        for rr in range(2):
            for cc in range(2):
                g[r0 + rr][cc] = avals[rr][cc]
                g[r0 + rr][3 + cc] = bvals[rr][cc]
                g[r0 + rr][7 + cc] = cvals[rr][cc]
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(5, 9, 0)
    if name == "no_bands":
        return g
    if name == "single_band":
        for r in range(2):
            for c in range(2):
                g[r][c] = 2
        return g
    if name == "full_grid":
        for r in range(5):
            for c in range(9):
                g[r][c] = 2
        return g
    return g
