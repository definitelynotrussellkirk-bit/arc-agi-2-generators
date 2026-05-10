"""Generator for arc_puzzle_bank_fifteenth21:M100 — recolor by column header.

Rule: row 0 holds a per-column legend. Every non-zero cell at (r>0, c)
is recolored to row-0's color at column c. Row 0 itself becomes all 0s.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_legend,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_legend, no_below_content, content_outside_legend_cols.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "00b92ce63593"
VERSION = "1.1.0"
TASK_ID = "00b92ce63593"
SUMMARY = "Row 0 has 2-3 distinct legend colors at distinct cols + content below in single color."

INVARIANTS = [
    "background is 0",
    "row 0 has 2-3 non-zero cells (the legend)",
    "below row 0: scattered non-zero cells only at columns with a legend (so all get recolored)",
    "all below-row-0 non-zero cells start in the same color (e.g. 7)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_legend", "no_below_content", "content_outside_legend_cols")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_legend":       {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..7"},
    "position_bias":  {"type": "str", "default": "row0_legend",
                       "valid": "row0_legend"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..7"},
    "density":        {"type": "str", "default": "medium", "valid": "medium"},
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
        h = ctx.draw_int("grid_h", 5, 5)
        w = ctx.draw_int("grid_w", 5, 6)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 6, 7)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 5, 7)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    n = rng.randint(2, 3)
    legend_cols = rng.sample(range(w), n)
    legend_palette = rng.sample([2, 3, 4, 5, 6, 8, 9], n)
    for c, color in zip(legend_cols, legend_palette):
        g[0][c] = color
    for r in range(1, h):
        for c in legend_cols:
            if rng.random() < 0.5:
                g[r][c] = 7
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 6
    g = full_grid(h, w, 0)
    if name == "no_legend":
        # row 0 is all zeros → no recoloring possible, content below stays as 7
        for r in range(1, h):
            for c in [1, 3]:
                g[r][c] = 7
        return g
    if name == "no_below_content":
        # legend exists but nothing to recolor → output is just zeroed row 0 (no visible change)
        g[0][1] = 3
        g[0][3] = 5
        g[0][4] = 6
        return g
    if name == "content_outside_legend_cols":
        # below cells sit in cols with no legend → recolor target is undefined (0)
        g[0][1] = 4
        g[0][3] = 6
        for r in range(1, h):
            for c in [0, 2, 4, 5]:
                if (r + c) % 2 == 0:
                    g[r][c] = 7
        return g
    return g
