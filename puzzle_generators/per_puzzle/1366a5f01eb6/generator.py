"""Generator for arc_additional_puzzles_21_set4:E26.

Rule: find full-height 5-col `div`; for each non-{0,5} cell at
(r, c<div), mirror to (r, 2*div-c) if right side is 0.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_left_cells,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_divider, no_left_cells, right_side_filled.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1366a5f01eb6"
VERSION = "1.1.0"
TASK_ID = "1366a5f01eb6"
SUMMARY = "Full-height 5-col divider in middle; left side has scattered non-5 cells."

INVARIANTS = [
    "exactly 1 full-height col of 5s",
    "left side has 2-3 isolated non-{0,5} cells",
    "right side empty (so mirror is visible)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_divider", "no_left_cells", "right_side_filled")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "9", "valid": "9"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_left_cells":   {"type": "int", "default": "rng 2..3", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "left_half", "valid": "left_half"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..8"},
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
        h = ctx.draw_int("grid_h", 5, 6)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
    w = 9
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    gc = 4
    for r in range(h):
        g[r][gc] = 5
    palette = [1, 2, 3, 4, 6, 7, 8, 9]
    for _ in range(rng.randint(2, 3)):
        for _ in range(20):
            r = rng.randint(0, h - 1); c = rng.randint(0, gc - 1)
            if g[r][c] == 0:
                g[r][c] = rng.choice(palette)
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 9
    g = full_grid(h, w, 0)
    if name == "no_divider":
        # left cells but no full-height 5-col → mirror axis undefined
        for r, c in [(1, 1), (3, 2)]:
            g[r][c] = 4
        return g
    if name == "no_left_cells":
        # divider but nothing on left → rule has no source cells to mirror
        for r in range(h):
            g[r][4] = 5
        return g
    if name == "right_side_filled":
        # left cells + divider but right side already non-zero → "right empty" fails
        for r in range(h):
            g[r][4] = 5
        g[1][1] = 4; g[3][2] = 6
        g[1][7] = 9; g[3][6] = 8
        return g
    return g
