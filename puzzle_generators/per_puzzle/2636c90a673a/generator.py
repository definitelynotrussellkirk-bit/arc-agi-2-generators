"""Generator for arc_puzzle_bank_fifth21:M34.

Rule: row 0 is a column mask (color 1). Drop mask row, keep only body
columns whose mask value is 1.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_keep,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_mask, all_columns_masked, body_empty.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2636c90a673a"
VERSION = "1.1.0"
TASK_ID = "2636c90a673a"
SUMMARY = "A row-0 mask selects which body columns survive."

INVARIANTS = [
    "row 0 contains at least two color-1 mask cells",
    "not every column is selected",
    "the output is the body restricted to selected columns",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_mask", "all_columns_masked", "body_empty")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "4..12"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_keep":         {"type": "int", "default": "rng 2..5", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 4..7", "valid": "2..8"},
    "position_bias":  {"type": "str", "default": "row0_mask", "valid": "row0_mask"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..7", "valid": "2..8"},
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
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 8, 9)
        n_keep = min(ctx.draw_int("n_keep", 2, 3), w - 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 11, 12)
        n_keep = min(ctx.draw_int("n_keep", 4, 5), w - 1)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 8, 12)
        n_keep = min(ctx.draw_int("n_keep", 2, 5), w - 1)
    keep = sorted(rng.sample(range(w), n_keep))
    g = full_grid(h, w, 0)
    for c in keep:
        g[0][c] = 1
    palette = [2, 3, 4, 5, 6, 7, 8, 9]
    for r in range(1, h):
        for c in range(w):
            if rng.random() < 0.45:
                g[r][c] = rng.choice(palette)
    for i, c in enumerate(keep):
        g[1 + (i % (h - 1))][c] = palette[i % len(palette)]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 10
    g = full_grid(h, w, 0)
    palette = [2, 3, 4, 5, 6, 7, 8, 9]
    if name == "no_mask":
        # row 0 has no color-1 cells → output has zero columns, ambiguous shape
        for r in range(1, h):
            for c in range(w):
                if (r * 3 + c) % 3 == 0:
                    g[r][c] = palette[(r + c) % len(palette)]
        return g
    if name == "all_columns_masked":
        # every column selected → output equals input minus row 0, rule visible only via row drop
        for c in range(w):
            g[0][c] = 1
        for r in range(1, h):
            for c in range(w):
                if (r + c) % 2 == 0:
                    g[r][c] = palette[(r + c) % len(palette)]
        return g
    if name == "body_empty":
        # mask present but body is all zeros → output is all-zero shape, no information
        for c in [1, 4, 7]:
            g[0][c] = 1
        return g
    return g
