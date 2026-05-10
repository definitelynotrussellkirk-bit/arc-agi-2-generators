"""Generator for arc_additional_puzzle_bank_volume10:M68 — Mark interior intersection of 1-cols and 2-rows.

Rule: marker bbox = bbox of {1,2,4} cells. Inside that bbox: cells where
row has a 2 in left col AND col has a 1 in top row → 3.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_ones,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_frame, no_top_ones, no_left_twos.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "6218f3968071"
VERSION = "1.1.0"
TASK_ID = "6218f3968071"
SUMMARY = "4-frame around interior with 1s on top edge, 2 on left edge."

INVARIANTS = [
    "4-frame surrounds interior",
    "top edge (row r0) has 4s and 1s alternating",
    "left edge (col c0) has 4s and 2s",
    "interior cells where col has 1 above and row has 2 left → 3",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frame", "no_top_ones", "no_left_twos")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "11", "valid": "11..11"},
    "grid_w":         {"type": "int", "default": "11", "valid": "11..11"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_ones":         {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "n_twos":         {"type": "int", "default": "rng 1..2", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "frame_with_top_ones_left_twos",
                       "valid": "frame_with_top_ones_left_twos"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "5..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    h, w = 11, 11
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    r0, c0, r1, c1 = 3, 2, 8, 7
    for c in range(c0, c1 + 1):
        g[r0][c] = 4; g[r1][c] = 4
    for r in range(r0, r1 + 1):
        g[r][c0] = 4; g[r][c1] = 4
    cols_avail = list(range(c0 + 1, c1))
    rng.shuffle(cols_avail)
    if difficulty == "easy":
        n_ones = rng.randint(2, 2)
        n_twos = rng.randint(1, 1)
    elif difficulty == "hard":
        n_ones = rng.randint(3, 3)
        n_twos = rng.randint(2, 2)
    else:
        n_ones = rng.randint(2, 3)
        n_twos = rng.randint(1, 2)
    for c in cols_avail[:n_ones]:
        g[r0][c] = 1
    rows_avail = list(range(r0 + 1, r1))
    rng.shuffle(rows_avail)
    for r in rows_avail[:n_twos]:
        g[r][c0] = 2
    g[r1 + 1][c1 + 2] = 8
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 11
    g = full_grid(h, w, 0)
    if name == "no_frame":
        # 1s and 2s exist but no 4-frame → bbox undefined
        g[3][4] = 1
        g[5][2] = 2
        return g
    if name == "no_top_ones":
        # frame and left-2s but no top-1s → no col-anchor for intersection
        r0, c0, r1, c1 = 3, 2, 8, 7
        for c in range(c0, c1 + 1):
            g[r0][c] = 4; g[r1][c] = 4
        for r in range(r0, r1 + 1):
            g[r][c0] = 4; g[r][c1] = 4
        g[5][c0] = 2
        return g
    if name == "no_left_twos":
        # frame and top-1s but no left-2s → no row-anchor for intersection
        r0, c0, r1, c1 = 3, 2, 8, 7
        for c in range(c0, c1 + 1):
            g[r0][c] = 4; g[r1][c] = 4
        for r in range(r0, r1 + 1):
            g[r][c0] = 4; g[r][c1] = 4
        g[r0][4] = 1
        return g
    return g
