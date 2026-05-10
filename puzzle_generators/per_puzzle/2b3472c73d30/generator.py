"""Generator for arc_puzzle_bank_ninth21:E57.

Rule: rows contain exactly two same-color endpoints with blank intervals.

Combinatorial axes (8): grid_h, grid_w, palette_kind, rows,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_rows, mismatched_endpoints, three_endpoints.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2b3472c73d30"
VERSION = "1.1.0"
TASK_ID = "2b3472c73d30"
SUMMARY = "Rows contain exactly two same-color endpoints with blank intervals."

INVARIANTS = [
    "background is 0",
    "each active row has one color appearing exactly twice",
    "the span between those endpoints is blank",
    "other rows remain empty",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_rows", "mismatched_endpoints", "three_endpoints")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "3..16"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "4..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "rows":           {"type": "int", "default": "rng 2..4", "valid": "1..10"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "row_endpoints",
                       "valid": "row_endpoints"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..9"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 8, 10)
        target = min(ctx.draw_int("rows", 2, 3), h)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 11, 12)
        target = min(ctx.draw_int("rows", 3, 4), h)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 8, 12)
        target = min(ctx.draw_int("rows", 2, 4), h)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    rows = rng.sample(range(h), target)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], min(target, 9))
    for i, r in enumerate(rows):
        left = rng.randint(0, w - 4)
        right = rng.randint(left + 2, w - 1)
        color = colors[i % len(colors)]
        g[r][left] = color
        g[r][right] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 10
    g = full_grid(h, w, 0)
    if name == "no_rows":
        # empty grid — no endpoints anywhere
        return g
    if name == "mismatched_endpoints":
        # two endpoints with different colors → "same-color" predicate fails
        g[2][1] = 4
        g[2][6] = 6
        return g
    if name == "three_endpoints":
        # three same-color cells in a row → predicate "exactly twice" fails
        g[2][1] = 4; g[2][3] = 4; g[2][7] = 4
        return g
    return g
