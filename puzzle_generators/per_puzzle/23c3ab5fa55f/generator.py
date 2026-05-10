"""Generator for arc_puzzle_bank_thirteenth_21_bundle:easy_87_compact_each_row_left.

Combinatorial axes (8): grid_h, grid_w, palette_kind, active_rows,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: already_left_packed, no_active_rows, fully_packed_rows.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "23c3ab5fa55f"
VERSION = "1.1.0"
TASK_ID = "23c3ab5fa55f"
SUMMARY = "Each row's nonzero cells slide left while preserving row order."

INVARIANTS = [
    "background is 0",
    "rows are independent",
    "nonzero colors keep their left-to-right order",
    "at least one row contains internal gaps",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("already_left_packed", "no_active_rows", "fully_packed_rows")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "2..18"},
    "grid_w":         {"type": "int", "default": "rng 8..13", "valid": "3..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "active_rows":    {"type": "int", "default": "rng 3..6", "valid": "1..12"},
    "palette_size":   {"type": "int", "default": "rng 3..6", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "with_internal_gaps",
                       "valid": "with_internal_gaps"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..6", "valid": "1..9"},
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
        w = ctx.draw_int("grid_w", 8, 10)
        target = min(ctx.draw_int("active_rows", 3, 4), h)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 11, 13)
        target = min(ctx.draw_int("active_rows", 5, 6), h)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 8, 13)
        target = min(ctx.draw_int("active_rows", 3, 6), h)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    for r in rng.sample(range(h), target):
        count = rng.randint(2, min(5, w - 1))
        cols = sorted(rng.sample(range(1, w), count))
        colors = [rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9]) for _ in range(count)]
        for c, color in zip(cols, colors):
            g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 10
    g = full_grid(h, w, 0)
    if name == "already_left_packed":
        # rows already have nonzeros packed at left → rule is identity, no movement visible
        for r, vs in [(1, [3, 4, 5]), (3, [6, 7]), (5, [8, 9, 2, 3])]:
            for i, v in enumerate(vs):
                g[r][i] = v
        return g
    if name == "no_active_rows":
        # empty grid → no rows to compact, rule no-op
        return g
    if name == "fully_packed_rows":
        # rows have no zeros at all → no gaps to close, rule is identity
        for r in [1, 3, 5]:
            for c in range(w):
                g[r][c] = 1 + ((r + c) % 7)
        return g
    return g
