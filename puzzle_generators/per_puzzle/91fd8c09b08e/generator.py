"""Generator for arc_puzzle_bank_ninth21:E58.

Rule: rows with a 9 anchor contain colored cells mirrored across it.

Combinatorial axes (8): grid_h, grid_w, palette_kind, rows,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_anchor, anchor_at_edge, no_other_cells.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "91fd8c09b08e"
VERSION = "1.1.0"
TASK_ID = "91fd8c09b08e"
SUMMARY = "Rows with a 9 anchor contain colored cells mirrored across it."

INVARIANTS = [
    "background is 0",
    "each active row has exactly one 9 anchor",
    "other nonzero row cells are not color 9",
    "reflected positions are in bounds and initially empty",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_anchor", "anchor_at_edge", "no_other_cells")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "3..16"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "5..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "rows":           {"type": "int", "default": "rng 2..4", "valid": "1..10"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "row_anchor",
                       "valid": "row_anchor"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..8"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 9, 10)
        target = min(ctx.draw_int("rows", 2, 2), h)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 11, 13)
        target = min(ctx.draw_int("rows", 3, 4), h)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 9, 13)
        target = min(ctx.draw_int("rows", 2, 4), h)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    rows = rng.sample(range(h), target)
    colors = [1, 2, 3, 4, 5, 6, 7, 8]
    for r in rows:
        anchor = rng.randint(2, w - 3)
        g[r][anchor] = 9
        offsets = rng.sample(range(1, min(anchor, w - 1 - anchor) + 1), rng.randint(1, 2))
        side = rng.choice([-1, 1])
        for off in offsets:
            c = anchor + side * off
            g[r][c] = rng.choice(colors)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 10
    g = full_grid(h, w, 0)
    if name == "no_anchor":
        # cells but no 9-anchor on any row → rule has no mirror axis
        g[2][3] = 4; g[2][6] = 5
        g[5][1] = 6; g[5][7] = 7
        return g
    if name == "anchor_at_edge":
        # anchor at column 0 → no left side to mirror; right cells can't reflect in-bounds
        g[2][0] = 9; g[2][3] = 4; g[2][5] = 5
        return g
    if name == "no_other_cells":
        # anchor present but no other cells to mirror → rule is identity
        g[3][5] = 9
        g[5][4] = 9
        return g
    return g
