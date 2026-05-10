"""Generator for arc_puzzle_bank_eleventh_21_bundle:easy_74_compact_nonzero_rows_up.

Combinatorial axes (8): grid_h, grid_w, palette_kind, active_rows,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: already_top_packed, no_blank_rows, all_blank.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2a928a0f8378"
VERSION = "1.1.0"
TASK_ID = "2a928a0f8378"
SUMMARY = "Scatter nonzero rows with gaps; output compacts those rows upward."

INVARIANTS = [
    "background is 0",
    "some rows contain colored cells and other rows are blank",
    "relative order of nonzero rows is preserved",
    "at least one blank row appears before or between kept rows",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("already_top_packed", "no_blank_rows", "all_blank")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "4..16"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "4..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "active_rows":    {"type": "int", "default": "rng 2..4", "valid": "1..10"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "scattered_with_gaps",
                       "valid": "scattered_with_gaps"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..9"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
        k = min(ctx.draw_int("active_rows", 2, 3), h - 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
        k = min(ctx.draw_int("active_rows", 3, 4), h - 1)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 8, 11)
        k = min(ctx.draw_int("active_rows", 2, 4), h - 1)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    for _ in range(80):
        rows = sorted(rng.sample(range(h), k))
        if rows != list(range(k)):
            break
    palette = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for r in rows:
        color = rng.choice(palette)
        width = rng.randint(1, min(4, w))
        cols = sorted(rng.sample(range(w), width))
        for c in cols:
            g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "already_top_packed":
        # nonzero rows already at top → rule is identity, no movement visible
        for r, cols, color in [(0, [1, 3, 5], 4), (1, [2, 6], 5), (2, [0, 7], 6)]:
            for c in cols:
                g[r][c] = color
        return g
    if name == "no_blank_rows":
        # every row has content → no row drops, rule has no visible effect
        for r in range(h):
            for c in [r % w, (r + 3) % w]:
                g[r][c] = 1 + (r % 7)
        return g
    if name == "all_blank":
        # all rows blank → output is an empty stack, ambiguous shape
        return g
    return g
