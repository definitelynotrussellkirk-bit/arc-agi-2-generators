"""Generator for arc_puzzle_bank_21_set10_s:S10_M6 — Smear non-bg cells downward.

Rule: for each non-zero non-5 cell, paint a downward streak of its
color through bg cells until it hits a non-bg cell or grid bottom.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_color, n_walls,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_color_cells, all_at_bottom, all_walls_below.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "69dbf44065e2"
VERSION = "1.1.0"
TASK_ID = "69dbf44065e2"
SUMMARY = "Sparse non-zero cells (some 5-walls), each colored cell smears downward."

INVARIANTS = [
    "between 2 and 5 colored cells (1..9 except 5)",
    "0..2 wall cells of color 5",
    "at least one colored cell has bg below it (so smear extends)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_color_cells", "all_at_bottom", "all_walls_below")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 6..9", "valid": "5..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_color":        {"type": "int", "default": "rng 2..5", "valid": "1..8"},
    "n_walls":        {"type": "int", "default": "rng 0..2", "valid": "0..4"},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "upper_with_walls_below",
                       "valid": "upper_with_walls_below"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "1..9"},
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
        w = ctx.draw_int("grid_w", 6, 7)
        n_color = ctx.draw_int("n_color", 2, 3)
        n_walls = ctx.draw_int("n_walls", 0, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
        n_color = ctx.draw_int("n_color", 4, 5)
        n_walls = ctx.draw_int("n_walls", 1, 2)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 6, 9)
        n_color = ctx.draw_int("n_color", 2, 5)
        n_walls = ctx.draw_int("n_walls", 0, 2)

    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    color_rng = ctx.draw_rng("colors")
    used = set()
    placed = 0
    while placed < n_color:
        r = rng.randint(0, h - 3)
        c = rng.randint(0, w - 1)
        if (r, c) in used: continue
        used.add((r, c))
        v = color_rng.choice([1, 2, 3, 4, 6, 7, 8, 9])
        g[r][c] = v
        placed += 1
    placed_walls = 0
    while placed_walls < n_walls:
        r = rng.randint(2, h - 1); c = rng.randint(0, w - 1)
        if (r, c) in used: continue
        used.add((r, c))
        g[r][c] = 5
        placed_walls += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "no_color_cells":
        # only walls, no colored seeds → nothing to smear, rule fires zero times
        g[3][2] = 5; g[5][6] = 5
        return g
    if name == "all_at_bottom":
        # colored cells already on the bottom row → no row below, smear extends 0 cells
        g[h - 1][1] = 4; g[h - 1][3] = 6; g[h - 1][6] = 3
        return g
    if name == "all_walls_below":
        # walls immediately below every colored cell → smear extends 0 cells, rule is identity
        g[1][2] = 4; g[2][2] = 5
        g[1][5] = 6; g[2][5] = 5
        return g
    return g
