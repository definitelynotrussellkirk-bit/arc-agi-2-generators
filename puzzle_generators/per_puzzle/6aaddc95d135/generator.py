"""Generator for arc_puzzle_bank_21_set11_bundle:medium_k11.

Rule: each column has scattered same-color cells that become a
bottom-aligned bar of equal count.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_cols,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: empty_grid, mixed_colors_per_column, already_packed.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "6aaddc95d135"
VERSION = "1.1.0"
TASK_ID = "6aaddc95d135"
SUMMARY = "Each column has scattered same-color cells that become a bottom-aligned bar of equal count."

INVARIANTS = [
    "each nonempty column uses one nonzero color",
    "column counts vary",
    "background is zero",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("empty_grid", "mixed_colors_per_column", "already_packed")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..10", "valid": "4..14"},
    "grid_w":         {"type": "int", "default": "rng 6..10", "valid": "4..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_cols":         {"type": "int", "default": "rng 3..6", "valid": "1..10"},
    "palette_size":   {"type": "int", "default": "rng 3..6", "valid": "1..10"},
    "position_bias":  {"type": "str", "default": "scattered_columns",
                       "valid": "scattered_columns"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..6", "valid": "1..10"},
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
        w = ctx.draw_int("grid_w", 6, 7)
        n = min(ctx.draw_int("n_cols", 3, 4), w)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
        n = min(ctx.draw_int("n_cols", 5, 6), w)
    else:
        h = ctx.draw_int("grid_h", 6, 10)
        w = ctx.draw_int("grid_w", 6, 10)
        n = min(ctx.draw_int("n_cols", 3, 6), w)
    rng = ctx.draw_rng("layout")
    cols = list(range(w))
    rng.shuffle(cols)
    colors = list(ctx.draw_distinct_colors("colors", n=n, exclude={0}))
    g = full_grid(h, w, 0)
    for i, c in enumerate(cols[:n]):
        count = rng.randint(1, h - 1)
        rows = list(range(h))
        rng.shuffle(rows)
        for r in rows[:count]:
            g[r][c] = colors[i]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 8
    g = full_grid(h, w, 0)
    if name == "empty_grid":
        # nothing to compact — output equals input
        return g
    if name == "mixed_colors_per_column":
        # column has multiple nonzero colors → "one color per column" assumption violated
        for r, v in [(0, 3), (2, 5), (4, 7)]:
            g[r][2] = v
        for r, v in [(1, 4), (3, 6)]:
            g[r][5] = v
        return g
    if name == "already_packed":
        # every column already bottom-aligned → rule has no visible effect
        for c, count, color in [(1, 3, 4), (3, 5, 6), (5, 2, 7), (6, 4, 3)]:
            for r in range(h - count, h):
                g[r][c] = color
        return g
    return g
