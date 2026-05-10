"""Generator for easy_k07: fill intersections from matching border markers.

Rule: top-row markers occupy columns; left-column markers occupy rows;
matching colors select interior intersections to fill.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_colors,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_top_markers, no_left_markers, no_color_match.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a546ac859141"
VERSION = "1.1.0"
TASK_ID = "a546ac859141"
SUMMARY = "Top-row and left-column markers with matching colors select filled intersections."
INVARIANTS = [
    "top-row markers occupy columns and left-column markers occupy rows",
    "at least one color appears on both borders",
    "interior starts as background",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_top_markers", "no_left_markers", "no_color_match")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..10", "valid": "4..14"},
    "grid_w":         {"type": "int", "default": "rng 6..10", "valid": "4..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_colors":       {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "position_bias":  {"type": "str", "default": "border_markers",
                       "valid": "border_markers"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..5"},
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
        w = ctx.draw_int("grid_w", 6, 7)
        n = ctx.draw_int("n_colors", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 8, 10)
        n = ctx.draw_int("n_colors", 3, 3)
    else:
        h = ctx.draw_int("grid_h", 6, 10)
        w = ctx.draw_int("grid_w", 6, 10)
        n = ctx.draw_int("n_colors", 2, 3)
    rng = ctx.draw_rng("layout")
    colors = list(ctx.draw_distinct_colors("colors", n=n, exclude={0}))
    row_slots = list(range(1, h))
    col_slots = list(range(1, w))
    rng.shuffle(row_slots)
    rng.shuffle(col_slots)
    g = full_grid(h, w, 0)
    for i, color in enumerate(colors):
        g[row_slots[i]][0] = color
        g[0][col_slots[i]] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 7
    g = full_grid(h, w, 0)
    if name == "no_top_markers":
        # only left-column markers → no column selectors, no intersections
        g[2][0] = 4
        g[5][0] = 6
        return g
    if name == "no_left_markers":
        # only top-row markers → no row selectors, no intersections
        g[0][3] = 4
        g[0][5] = 6
        return g
    if name == "no_color_match":
        # markers on both borders but no shared color → empty intersection set
        g[2][0] = 4; g[5][0] = 6
        g[0][3] = 7; g[0][5] = 9
        return g
    return g
