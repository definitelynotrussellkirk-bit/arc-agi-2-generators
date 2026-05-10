"""Generator for arc_additional_puzzles_21_set9:E61.

Rule: collect all distinct non-bg colors; for each color emit 1 row
per occurrence. Output is a single column of those colors.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_colors,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: empty_grid, single_color_only, equal_counts.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5ec08fa47c08"
VERSION = "1.1.0"
TASK_ID = "5ec08fa47c08"
SUMMARY = "Scattered single-cell markers in 2-3 distinct colors."

INVARIANTS = [
    "≥2 distinct non-bg colors",
    "1..3 cells per color, all isolated",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("empty_grid", "single_color_only", "equal_counts")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_colors":       {"type": "int", "default": "rng 2..4", "valid": "2..5"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "2..5"},
    "position_bias":  {"type": "str", "default": "scattered",
                       "valid": "scattered"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "2..5"},
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
        w = ctx.draw_int("grid_w", 5, 6)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 6, 7)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 5, 7)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    n_colors = rng.randint(2, 4)
    palette = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], n_colors)
    cells = [(r, c) for r in range(h) for c in range(w)]
    rng.shuffle(cells)
    idx = 0
    for color in palette:
        cnt = rng.randint(1, 2)
        for _ in range(cnt):
            r, c = cells[idx]; idx += 1
            g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 6
    g = full_grid(h, w, 0)
    if name == "empty_grid":
        # no cells → output is empty column, rule has nothing to count
        return g
    if name == "single_color_only":
        # only one color present → output is just that color repeated, no per-color signal
        for r, c in [(1, 2), (3, 4), (5, 1)]:
            g[r][c] = 6
        return g
    if name == "equal_counts":
        # every color has the same count → output rows have no rank/order signal
        for r, c, v in [(0, 1, 3), (1, 4, 3),
                        (2, 1, 5), (3, 4, 5),
                        (4, 1, 7), (5, 4, 7)]:
            g[r][c] = v
        return g
    return g
