"""Generator for additional_scaffolded:H1 -- copy 3-cells by marker vector.

Rule: markers 1 and 2 define a vector; color-3 cells copied by that vector
become 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, vector_choice,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_marker_pair, no_3_cells, copy_out_of_bounds.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "7b0c20fe6f33"
VERSION = "1.1.0"
TASK_ID = "7b0c20fe6f33"
SUMMARY = "Markers 1 and 2 define a vector; color-3 cells copied by that vector become 8."

INVARIANTS = [
    "there is one color-1 source marker and one color-2 destination marker",
    "the color-3 motif has in-bounds translated positions",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_marker_pair", "no_3_cells", "copy_out_of_bounds")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "vector_choice":  {"type": "int", "default": "rng 0..3", "valid": "0..3"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "marker_pair_with_3cells",
                       "valid": "marker_pair_with_3cells"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 8, 12)
    rng = ctx.draw_rng("layout")
    dr, dc = rng.choice([(1, 2), (2, 1), (-1, 2), (2, -1)])
    g = full_grid(h, w, 0)
    mr = 1 if dr >= 0 else 3
    mc = 1 if dc >= 0 else w - 3
    g[mr][mc] = 1
    g[mr + dr][mc + dc] = 2
    occupied = {(mr, mc), (mr + dr, mc + dc)}
    candidates = [
        (r, c)
        for r in range(1, h - 1)
        for c in range(1, w - 1)
        if (r, c) not in occupied
        and (r + dr, c + dc) not in occupied
        and 0 <= r + dr < h
        and 0 <= c + dc < w
    ]
    rng.shuffle(candidates)
    for r, c in candidates[:4]:
        g[r][c] = 3
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "no_marker_pair":
        # only one of the two markers → vector underdetermined
        g[2][2] = 1   # source only, no dest
        g[5][3] = 3; g[6][6] = 3
        return g
    if name == "no_3_cells":
        # vector defined but no 3-cells → rule has nothing to copy
        g[1][1] = 1; g[2][3] = 2
        return g
    if name == "copy_out_of_bounds":
        # 3-cells near edge such that translation goes out of bounds
        g[1][1] = 1; g[2][3] = 2   # vector (+1, +2)
        g[h - 1][w - 1] = 3        # +1,+2 out of bounds
        g[h - 1][w - 2] = 3
        g[h - 2][w - 1] = 3
        return g
    return g
