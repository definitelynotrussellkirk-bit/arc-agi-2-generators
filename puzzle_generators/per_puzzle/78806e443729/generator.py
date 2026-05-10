"""Generator for arc_puzzle_bank_21_set15_bundle:easy_o03 — horizontal beams from seeds.

Rule: each nonzero seed emits horizontal beams through original zero
cells until an edge or original nonzero blocker.

Combinatorial axes (8): grid_h, grid_w, palette_kind, row_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_seeds, seeds_at_edge, multi_cell_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "78806e443729"
VERSION = "1.1.0"
TASK_ID = "78806e443729"
SUMMARY = "Rows with one or two colored seeds for horizontal beam casting."

INVARIANTS = [
    "background is 0",
    "all nonzero cells are singleton seeds",
    "each active row has one or two seeds",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_seeds", "seeds_at_edge", "multi_cell_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "4..12"},
    "grid_w":         {"type": "int", "default": "9..13", "valid": "5..15"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "row_count":      {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "rng 4..6", "valid": "2..8"},
    "position_bias":  {"type": "str", "default": "rows_with_1_2_seeds",
                       "valid": "rows_with_1_2_seeds"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..6", "valid": "2..8"},
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
        w = ctx.draw_int("grid_w", 9, 10)
        row_count = ctx.draw_int("row_count", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 12, 13)
        row_count = ctx.draw_int("row_count", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 9, 13)
        row_count = ctx.draw_int("row_count", 2, 4)
    colors = ctx.draw_distinct_colors("colors", n=row_count * 2, exclude={0})
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    rows = rng.sample(range(h), min(row_count, h))
    color_i = 0
    for r in rows:
        seed_count = rng.choice([1, 2])
        cols = sorted(rng.sample(range(1, w - 1), seed_count))
        for c in cols:
            g[r][c] = colors[color_i % len(colors)]
            color_i += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 10
    g = full_grid(h, w, 0)
    if name == "no_seeds":
        # blank → no beams to emit
        return g
    if name == "seeds_at_edge":
        # seeds at column 0 / w-1 → beam direction collapses (only one side has space)
        g[2][0] = 4
        g[4][w - 1] = 6
        return g
    if name == "multi_cell_blobs":
        # multi-cell blobs (not singletons) → "singleton seed" precondition fails
        g[1][2] = 4; g[1][3] = 4   # pair
        g[3][6] = 6; g[3][7] = 6   # pair
        return g
    return g
