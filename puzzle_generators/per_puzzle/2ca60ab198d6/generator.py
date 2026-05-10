"""Generator for arc_puzzle_bank_sixth21:M40.

The leftmost column is a row selector. Rows whose selector is color 7 are kept,
and the selector column itself is removed.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_keep,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_keepers, all_keepers, no_payload.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2ca60ab198d6"
VERSION = "1.1.0"
TASK_ID = "2ca60ab198d6"
SUMMARY = "Left-column 7 selectors choose payload rows to keep."

INVARIANTS = [
    "column 0 is a selector guide",
    "at least two rows have selector color 7",
    "the payload is every column except the selector column",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_keepers", "all_keepers", "no_payload")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..10", "valid": "4..14"},
    "grid_w":         {"type": "int", "default": "rng 7..11", "valid": "4..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_keep":         {"type": "int", "default": "rng 2..5", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 4..7", "valid": "2..8"},
    "position_bias":  {"type": "str", "default": "left_col_selector",
                       "valid": "left_col_selector"},
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
        w = ctx.draw_int("grid_w", 7, 8)
        n_keep = min(ctx.draw_int("n_keep", 2, 3), h - 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
        n_keep = min(ctx.draw_int("n_keep", 4, 5), h - 1)
    else:
        h = ctx.draw_int("grid_h", 6, 10)
        w = ctx.draw_int("grid_w", 7, 11)
        n_keep = min(ctx.draw_int("n_keep", 2, 5), h - 1)
    keep_rows = set(rng.sample(range(h), n_keep))
    g = full_grid(h, w, 0)
    palette = [1, 2, 3, 4, 5, 6, 8, 9]
    for r in range(h):
        g[r][0] = 7 if r in keep_rows else rng.choice([0, 1, 2, 3])
        for c in range(1, w):
            if rng.random() < 0.45:
                g[r][c] = rng.choice(palette)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    palette = [1, 2, 3, 4, 5, 6, 8, 9]
    if name == "no_keepers":
        # no row carries selector 7 → output is empty list of rows, ambiguous shape
        for r in range(h):
            g[r][0] = (r % 4) + 1
            for c in range(1, w):
                if (r * 3 + c) % 3 == 0:
                    g[r][c] = palette[(r + c) % len(palette)]
        return g
    if name == "all_keepers":
        # every row's selector is 7 → output is the whole grid minus col 0, rule is identity-like
        for r in range(h):
            g[r][0] = 7
            for c in range(1, w):
                if (r + c) % 3 == 0:
                    g[r][c] = palette[(r + c) % len(palette)]
        return g
    if name == "no_payload":
        # selector column has 7s but payload columns are all 0 → output is all-zero rows
        for r in range(h):
            g[r][0] = 7 if r % 2 == 0 else 0
        return g
    return g
