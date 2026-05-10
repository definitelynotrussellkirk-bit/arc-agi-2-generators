"""Generator for arc_puzzle_bank_fourteenth21:E97.

Rule: scatter row-local color sequences that are stably packed to the
left of each row.

Combinatorial axes (8): grid_h, grid_w, palette_kind, active_rows,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: empty_grid, already_packed, single_color_per_row.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "709d506bd0aa"
VERSION = "1.1.0"
TASK_ID = "709d506bd0aa"
SUMMARY = "Scatter row-local color sequences that are stably packed to the left."

INVARIANTS = [
    "background is 0",
    "each active row contains one or more nonzero cells",
    "color order within each row matters",
    "at least one active row has leading or internal zeros",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("empty_grid", "already_packed", "single_color_per_row")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "3..14"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "3..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "active_rows":    {"type": "int", "default": "rng 2..4", "valid": "1..10"},
    "palette_size":   {"type": "int", "default": "rng 2..9", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "scattered_columns",
                       "valid": "scattered_columns"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..9", "valid": "1..9"},
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
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 8, 9)
        target = min(ctx.draw_int("active_rows", 2, 3), h)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 10, 11)
        target = min(ctx.draw_int("active_rows", 3, 4), h)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 8, 11)
        target = min(ctx.draw_int("active_rows", 2, 4), h)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    for r in rng.sample(range(h), target):
        count = rng.randint(1, min(4, w - 1))
        cols = sorted(rng.sample(range(1, w), count))
        colors = rng.choices([1, 2, 3, 4, 5, 6, 7, 8, 9], k=count)
        for c, color in zip(cols, colors):
            g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 10
    g = full_grid(h, w, 0)
    if name == "empty_grid":
        # no nonzero cells → packing is a no-op
        return g
    if name == "already_packed":
        # all rows already left-packed → rule has no visible effect
        for r, vals in [(1, [3, 5]), (3, [2, 7, 4]), (4, [6])]:
            for i, v in enumerate(vals):
                g[r][i] = v
        return g
    if name == "single_color_per_row":
        # each active row has only one nonzero cell → packing reduces to a 1-cell shift
        g[1][5] = 3
        g[3][7] = 6
        g[4][2] = 4
        return g
    return g
