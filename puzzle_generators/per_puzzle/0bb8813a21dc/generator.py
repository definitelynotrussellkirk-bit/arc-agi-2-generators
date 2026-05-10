"""Generator for arc_puzzle_bank_21_set18_bundle:easy_p06.

Rule: leftmost nonzero cell in each active row is the row's leader color;
all other nonzero cells in that row are recolored to the leader's color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, row_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: single_cell_per_row, no_active_rows, all_same_color.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0bb8813a21dc"
VERSION = "1.1.0"
TASK_ID = "0bb8813a21dc"
SUMMARY = "Rows with a leftmost leader and later colored cells to recolor."

INVARIANTS = [
    "background is 0",
    "each active row has at least two nonzero cells",
    "the leftmost nonzero cell selects the row recolor",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("single_cell_per_row", "no_active_rows", "all_same_color")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "4..12"},
    "grid_w":         {"type": "int", "default": "rng 7..11", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "row_count":      {"type": "int", "default": "rng 3..5", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 4..7", "valid": "2..9"},
    "position_bias":  {"type": "str", "default": "leader_left",
                       "valid": "leader_left"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..7", "valid": "2..9"},
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
        row_count = min(ctx.draw_int("row_count", 3, 3), h)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 11)
        row_count = min(ctx.draw_int("row_count", 4, 5), h)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 7, 11)
        row_count = min(ctx.draw_int("row_count", 3, 5), h)
    colors = ctx.draw_distinct_colors("colors", n=8, exclude={0})
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    rows = rng.sample(range(h), row_count)
    for i, r in enumerate(rows):
        n = rng.randint(2, min(4, w))
        cols = sorted(rng.sample(range(w), n))
        g[r][cols[0]] = colors[i % len(colors)]
        for j, c in enumerate(cols[1:], start=1):
            g[r][c] = colors[(i + j) % len(colors)]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 9
    g = full_grid(h, w, 0)
    if name == "single_cell_per_row":
        # each active row has only one nonzero cell → no other cells to recolor, rule is identity
        for r, c, v in [(1, 2, 3), (3, 5, 4), (5, 1, 6)]:
            g[r][c] = v
        return g
    if name == "no_active_rows":
        # empty grid → no rows to process, rule no-op
        return g
    if name == "all_same_color":
        # all nonzero cells same color → leader recolor is identity, no contrast
        for r in [1, 3, 5]:
            for c in rng.sample(range(w), 3) if hasattr(rng, 'sample') else [1, 4, 6]:
                g[r][c] = 5
        return g
    return g
