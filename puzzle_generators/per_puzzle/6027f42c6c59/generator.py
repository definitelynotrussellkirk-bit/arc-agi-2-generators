"""Generator for arc_puzzle_bank_21_set4_d:easy_d01.

Rule: each row keeps only its leftmost nonzero cell.

Combinatorial axes (8): grid_h, grid_w, palette_kind, active_rows,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: empty_grid, single_per_row, all_filled.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "6027f42c6c59"
VERSION = "1.1.0"
TASK_ID = "6027f42c6c59"
SUMMARY = "Each row keeps only its leftmost nonzero cell."

INVARIANTS = [
    "background is 0",
    "some rows contain multiple nonzero cells",
    "row colors may vary independently",
    "empty rows remain empty",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("empty_grid", "single_per_row", "all_filled")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..8", "valid": "3..14"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "4..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "active_rows":    {"type": "int", "default": "rng 4..7", "valid": "1..12"},
    "palette_size":   {"type": "int", "default": "rng 1..6", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "rows", "valid": "rows"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..6", "valid": "1..9"},
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
        w = ctx.draw_int("grid_w", 7, 8)
        active = ctx.draw_int("active_rows", min(3, h), h)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 9, 10)
        active = ctx.draw_int("active_rows", min(5, h), h)
    else:
        h = ctx.draw_int("grid_h", 5, 8)
        w = ctx.draw_int("grid_w", 7, 10)
        active = ctx.draw_int("active_rows", min(4, h), h)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    rows = rng.sample(range(h), active)
    multi_row = rng.choice(rows)
    for r in rows:
        k = rng.randint(2, 3) if r == multi_row else rng.randint(1, 3)
        cols = sorted(rng.sample(range(w), k))
        for c in cols:
            g[r][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 8
    g = full_grid(h, w, 0)
    if name == "empty_grid":
        # nothing to keep — output is identical empty grid
        return g
    if name == "single_per_row":
        # every row has at most one nonzero → rule is trivially identity
        for r, c, v in [(0, 2, 4), (2, 1, 6), (4, 5, 7)]:
            g[r][c] = v
        return g
    if name == "all_filled":
        # every cell of every row is nonzero → only column 0 survives
        for r in range(h):
            for c in range(w):
                g[r][c] = ((r + c) % 7) + 1
        return g
    return g
