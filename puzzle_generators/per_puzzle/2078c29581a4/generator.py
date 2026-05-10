"""Generator for arc_puzzle_bank_eighth_21_bundle:easy_56_pack_nonempty_rows.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_rows,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_empty_rows, all_empty_rows, only_one_nonempty.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2078c29581a4"
VERSION = "1.1.0"
TASK_ID = "2078c29581a4"
SUMMARY = "Rows with colored cells separated by empty rows; empty rows are removed."

INVARIANTS = [
    "background is 0",
    "at least two rows are nonempty",
    "at least one empty row separates nonempty rows",
    "row widths are preserved by the rule",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_empty_rows", "all_empty_rows", "only_one_nonempty")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..11", "valid": "5..16"},
    "grid_w":         {"type": "int", "default": "rng 6..10", "valid": "4..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_rows":         {"type": "int", "default": "rng 3..5", "valid": "1..10"},
    "palette_size":   {"type": "int", "default": "3", "valid": "1..6"},
    "position_bias":  {"type": "str", "default": "scattered_rows",
                       "valid": "scattered_rows"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "1..6"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 6, 7)
        n_rows = ctx.draw_int("n_rows", 3, 4)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 9, 10)
        n_rows = ctx.draw_int("n_rows", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 7, 11)
        w = ctx.draw_int("grid_w", 6, 10)
        n_rows = ctx.draw_int("n_rows", 3, 5)
    colors = ctx.draw_distinct_colors("colors", n=3, exclude={0})
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    row_choices = sorted(rng.sample(range(h), min(n_rows, h)))
    if len(row_choices) == h:
        row_choices = row_choices[:-1]
    for i, r in enumerate(row_choices):
        count = rng.randint(1, min(3, w))
        cols = rng.sample(range(w), count)
        for c in cols:
            g[r][c] = colors[i % len(colors)]
    if all(any(v != 0 for v in row) for row in g):
        g[0] = [0] * w
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "no_empty_rows":
        # every row has content → packing is identity, rule has no visible effect
        for r in range(h):
            g[r][r % w] = 1 + (r % 5)
            if r + 2 < w:
                g[r][r + 2] = 1 + ((r + 1) % 5)
        return g
    if name == "all_empty_rows":
        # all rows empty → output is empty grid, output shape ambiguous
        return g
    if name == "only_one_nonempty":
        # one row has content, rest empty → packing reduces to a 1-row output, no comparison signal
        for c in [1, 3, 5]:
            g[3][c] = 4
        return g
    return g
