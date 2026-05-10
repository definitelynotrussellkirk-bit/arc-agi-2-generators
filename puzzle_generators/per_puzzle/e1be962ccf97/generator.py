"""Generator for arc_additional_puzzle_bank_volume23:M158 — Fill compartment with most 2-cells.

Rule: 5-walls divide grid. Find non-5 region with most 2-cells; fill 0
cells in that region with 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, count_split,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_divider, no_2_cells, tied_compartment_counts.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e1be962ccf97"
VERSION = "1.1.0"
TASK_ID = "e1be962ccf97"
SUMMARY = "5-walls divide grid horizontally + 2-cells in different compartments with varied counts."

INVARIANTS = [
    "1 full-row 5-divider",
    "top compartment has 2-3 2-cells",
    "bottom compartment has 4-5 2-cells (more than top)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_divider", "no_2_cells", "tied_compartment_counts")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "count_split":    {"type": "str", "default": "top_lt_bot", "valid": "top_lt_bot"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "horizontal_divider",
                       "valid": "horizontal_divider"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
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
        h = ctx.draw_int("grid_h", 11, 11)
        w = ctx.draw_int("grid_w", 11, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 11, 13)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    div = h // 2
    for c in range(w):
        g[div][c] = 5
    n_top = rng.randint(2, 3)
    placed = 0
    while placed < n_top:
        r = rng.randint(0, div - 1); c = rng.randint(0, w - 1)
        if g[r][c] == 0:
            g[r][c] = 2; placed += 1
    n_bot = rng.randint(4, 5)
    placed = 0
    while placed < n_bot:
        r = rng.randint(div + 1, h - 1); c = rng.randint(0, w - 1)
        if g[r][c] == 0:
            g[r][c] = 2; placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 12
    g = full_grid(h, w, 0)
    if name == "no_divider":
        # 2-cells but no 5-divider → no compartments to compare
        g[2][2] = 2; g[3][5] = 2; g[7][8] = 2
        return g
    if name == "no_2_cells":
        # divider exists but no 2-cells in either compartment → no count to compare
        for c in range(w): g[5][c] = 5
        return g
    if name == "tied_compartment_counts":
        # both compartments have the same number of 2-cells → ambiguous winner
        for c in range(w): g[5][c] = 5
        g[1][1] = 2; g[2][3] = 2; g[3][7] = 2     # top: 3
        g[7][1] = 2; g[8][4] = 2; g[9][8] = 2     # bot: 3 (tied)
        return g
    return g
