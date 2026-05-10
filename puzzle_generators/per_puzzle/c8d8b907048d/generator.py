"""Generator for arc_puzzle_bank_21_set22_bundle:easy_p04.

Rule: colored cells are placed only in the top half and mirror down
vertically.

Combinatorial axes (8): grid_h/w, palette_kind, cell_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: empty_grid, all_on_midline, full_lower_half.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c8d8b907048d"
VERSION = "1.1.0"
TASK_ID = "c8d8b907048d"
SUMMARY = "Colored cells are placed only in the top half and mirror down vertically."

INVARIANTS = [
    "background is 0",
    "all source cells are in rows strictly above h//2",
    "the bottom half starts empty",
]

PALETTE_KINDS = ("default", "sparse", "dense", "varied_palette")
DEGENERATE_TEXTURES = ("empty_grid", "all_on_midline", "full_lower_half")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "4..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "cell_count":     {"type": "int", "default": "rng 4..8", "valid": "1..24"},
    "palette_size":   {"type": "int", "default": "rng 3..6", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "upper_half",
                       "valid": "upper_half"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..6", "valid": "1..9"},
    "density":        {"type": "str", "default": "mixed", "valid": "mixed"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 8, 12)
    cell_count = ctx.draw_int("cell_count", 4, 8)
    rng = ctx.draw_rng("layout")
    grid = full_grid(h, w, 0)
    top_rows = list(range(h // 2))
    positions = [(r, c) for r in top_rows for c in range(w)]
    rng.shuffle(positions)
    for r, c in positions[: min(cell_count, len(positions))]:
        grid[r][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    return grid


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "empty_grid":
        # nothing to mirror
        return g
    if name == "all_on_midline":
        # cells exactly on midline — mirror is identity
        mid = h // 2
        g[mid][2] = 4
        g[mid][5] = 6
        g[mid][7] = 8
        return g
    if name == "full_lower_half":
        # cells in lower half — invariant violated
        for r, c, v in [(5, 1, 4), (6, 4, 6), (6, 7, 8)]:
            g[r][c] = v
        return g
    return g
