"""Generator for arc_additional_puzzles_21_set21_bundle:E141 — 4-ray from 9-seed using row-0 palette.

Rule: row 0 has 2 palette cells (non-zero). 9 is the seed elsewhere.
Draw 4 rays (up/down/left/right) from seed using palette repeating.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_palette,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_palette, no_seed, seed_at_corner.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "edb55a59dc46"
VERSION = "1.1.0"
TASK_ID = "edb55a59dc46"
SUMMARY = "Row 0 with 2 distinct non-zero palette cells, 1 seed cell of color 9 below."

INVARIANTS = [
    "exactly 2 non-zero cells in row 0 (the palette)",
    "row 0's 2 cells use distinct non-9 colors",
    "exactly one 9-cell at (r, c) with r≥2",
    "nothing else non-zero",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_palette", "no_seed", "seed_at_corner")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_palette":      {"type": "int", "default": "2", "valid": "2..2"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "row0_palette_with_seed",
                       "valid": "row0_palette_with_seed"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
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
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 7, 10)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8], 2)
    c0 = rng.randint(0, w - 3)
    g[0][c0] = palette[0]
    g[0][c0 + 1] = palette[1]
    for _ in range(40):
        r = rng.randint(2, h - 2); c = rng.randint(1, w - 2)
        if g[r][c] == 0:
            g[r][c] = 9
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 9
    g = full_grid(h, w, 0)
    if name == "no_palette":
        # 9-seed but no row-0 palette → ray colors undefined
        g[3][4] = 9
        return g
    if name == "no_seed":
        # palette in row 0 but no 9-seed → no anchor for rays
        g[0][2] = 4; g[0][3] = 6
        return g
    if name == "seed_at_corner":
        # 9-seed at corner → 2 of 4 rays would shoot off-grid (length 0)
        g[0][2] = 4; g[0][3] = 6
        g[h - 1][w - 1] = 9
        return g
    return g
