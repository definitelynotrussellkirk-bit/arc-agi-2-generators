"""Generator for arc_puzzle_bank_eighth21:E50.

Rule: top-row column legends recolor body cells marked 8 — each 8 in
column c becomes the color sitting at row 0 of column c.

Combinatorial axes (8): grid_h, grid_w, palette_kind, legend_cols,
palette_size, position_bias, n_distinct_colors, marker_density, texture.
Degenerates: no_legend, no_8s, 8_outside_legend.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1a58c96bb078"
VERSION = "1.1.0"
TASK_ID = "1a58c96bb078"
SUMMARY = "Use top-row column legends to recolor body cells marked 8."

INVARIANTS = [
    "background is 0",
    "top row contains nonzero legend colors in selected columns",
    "body cells marked 8 appear only in legend columns",
    "each 8 is replaced by its column's legend color",
]

PALETTE_KINDS = ("default", "warm_legend", "cool_legend", "varied_legend")
DEGENERATE_TEXTURES = ("no_legend", "no_8s", "8_outside_legend")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "4..14"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "4..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "legend_cols":    {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "top_row", "valid": "top_row"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..5", "valid": "1..9"},
    "marker_density": {"type": "str", "default": "mixed", "valid": "mixed"},
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
        w = ctx.draw_int("grid_w", 7, 8)
        n = min(ctx.draw_int("legend_cols", 2, 3), w)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
        n = min(ctx.draw_int("legend_cols", 3, 4), w)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 7, 10)
        n = min(ctx.draw_int("legend_cols", 2, 4), w)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    cols = rng.sample(range(w), n)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 9], n)
    for c, color in zip(cols, colors):
        g[0][c] = color
        for r in rng.sample(range(1, h), rng.randint(1, min(3, h - 1))):
            g[r][c] = 8
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_legend":
        # 8 markers but no top-row legend → recolor source undefined
        for r, c in [(3, 2), (4, 5), (5, 7)]:
            g[r][c] = 8
        return g
    if name == "no_8s":
        # legend present but no body 8s → rule has nothing to recolor
        g[0][2] = 4; g[0][5] = 6; g[0][7] = 1
        return g
    if name == "8_outside_legend":
        # body 8 sits in a column with no top-row legend → ambiguous mapping
        g[0][2] = 4; g[0][5] = 6
        for r, c in [(3, 1), (4, 3)]:
            g[r][c] = 8
        return g
    return g
