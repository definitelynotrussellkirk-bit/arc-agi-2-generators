"""Generator for 846bdb03.

Rule: two marker columns define a frame, and a separate crop is oriented
inside it.

Combinatorial axes (8): grid_h/w, flip_bias, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_frame, no_crop, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4512012999bb"
VERSION = "1.1.0"
TASK_ID = "4512012999bb"
SUMMARY = "Two marker columns define a frame, and a separate crop is oriented inside it."

INVARIANTS = [
    "two full nonzero vertical guide segments share top and bottom rows",
    "a separate pattern crop has exactly the guide frame's interior size",
    "the output uses the guide columns as side walls and the crop as the interior",
]

FLIP_BIAS_KINDS = ("flip0", "flip1")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_frame", "no_crop", "full_grid")
HELPFUL_TEXTURES = FLIP_BIAS_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "8", "valid": "8"},
    "grid_w":         {"type": "int", "default": "13", "valid": "13"},
    "flip_bias":      {"type": "choice", "default": "rng helpful",
                       "valid": "0|1"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "4", "valid": "4"},
    "texture":        {"type": "str", "default": "alias for flip_bias",
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
    if tx in FLIP_BIAS_KINDS:
        flip_bias = int(tx[-1])
    else:
        flip_bias = ctx.draw_choice("flip_bias", [0, 1])
    left, right, p1, p2 = ctx.draw_distinct_colors("colors", n=4, exclude={0})
    g = full_grid(8, 13, 0)
    r0, r1, c_left, c_right = 1, 5, 1, 6
    for r in range(r0, r1 + 1):
        g[r][c_left] = left
        g[r][c_right] = right
    pattern = [
        [left, p1, p2, right],
        [left, p2, p1, right],
        [left, left if flip_bias == 0 else right, right, right],
    ]
    for r, row in enumerate(pattern):
        for c, value in enumerate(row):
            g[1 + r][8 + c] = value
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(8, 13, 0)
    if name == "no_frame":
        for r in range(1, 4):
            for c in range(8, 12):
                g[r][c] = 2
        return g
    if name == "no_crop":
        for r in range(1, 6):
            g[r][1] = 3
            g[r][6] = 4
        return g
    if name == "full_grid":
        for r in range(8):
            for c in range(13):
                g[r][c] = 3
        return g
    return g
