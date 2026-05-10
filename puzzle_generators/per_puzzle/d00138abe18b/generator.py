"""Generator for arc_puzzle_bank_ninth_21_bundle:easy_61_read_nonempty_rows_as_column.

Rule: nonempty rows each carry one color → read into a color column.

Combinatorial axes (8): grid_h, grid_w, palette_kind, nonempty_rows,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: all_rows_empty, mixed_color_rows, no_empty_separators.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d00138abe18b"
VERSION = "1.1.0"
TASK_ID = "d00138abe18b"
SUMMARY = "Nonempty rows each carry one color that is read into a color column."

INVARIANTS = [
    "background is 0",
    "each nonempty row contains cells of exactly one color",
    "empty rows may appear between nonempty rows",
    "the output height equals the number of nonempty rows",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("all_rows_empty", "mixed_color_rows", "no_empty_separators")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "3..16"},
    "grid_w":         {"type": "int", "default": "rng 7..11", "valid": "3..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "nonempty_rows":  {"type": "int", "default": "rng 3..6", "valid": "1..12"},
    "palette_size":   {"type": "int", "default": "rng 3..6", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "row_separated",
                       "valid": "row_separated"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 7, 8)
        target = min(ctx.draw_int("nonempty_rows", 2, 3), h)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
        target = min(ctx.draw_int("nonempty_rows", 5, 6), h)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 7, 11)
        target = min(ctx.draw_int("nonempty_rows", 3, 6), h)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    rows = sorted(rng.sample(range(h), target))
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], min(target, 9))
    for i, r in enumerate(rows):
        color = colors[i % len(colors)]
        count = rng.randint(1, min(4, w))
        for c in rng.sample(range(w), count):
            g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "all_rows_empty":
        # blank grid → output is empty (zero rows)
        return g
    if name == "mixed_color_rows":
        # rows contain multiple colors → "one color per nonempty row" predicate fails
        g[1][2] = 4; g[1][5] = 6
        g[3][1] = 3; g[3][7] = 8
        g[5][4] = 2; g[5][6] = 9
        return g
    if name == "no_empty_separators":
        # every row is nonempty → output is a column of length h (no separator rows)
        for r in range(h):
            color = (r % 8) + 1
            g[r][r % w] = color
            if r % w + 2 < w:
                g[r][r % w + 2] = color
        return g
    return g
