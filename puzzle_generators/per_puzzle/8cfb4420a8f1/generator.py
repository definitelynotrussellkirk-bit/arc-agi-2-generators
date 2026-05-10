"""Generator for arc_puzzle_bank_21_set6:easy_f04.

Rule: a top-row marker selects the color whose cells are erased below.

Combinatorial axes (8): grid_h, grid_w, palette_kind, marked_cells,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_marker, marker_color_absent_below, all_marker_color.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8cfb4420a8f1"
VERSION = "1.1.0"
TASK_ID = "8cfb4420a8f1"
SUMMARY = "A top-row marker selects the color to delete below."

INVARIANTS = [
    "background is 0",
    "row 0 contains one nonzero marker",
    "all non-top cells of the marker color are erased",
    "other colors remain unchanged",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_marker", "marker_color_absent_below", "all_marker_color")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "3..12"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "5..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "marked_cells":   {"type": "int", "default": "rng 2..4", "valid": "1..10"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "marker_top_body_below",
                       "valid": "marker_top_body_below"},
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
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 8, 9)
        n = ctx.draw_int("marked_cells", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 10, 11)
        n = ctx.draw_int("marked_cells", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 8, 11)
        n = ctx.draw_int("marked_cells", 2, 4)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    marker = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    g[0][rng.randrange(w)] = marker
    cells = [(r, c) for r in range(1, h) for c in range(w)]
    for r, c in rng.sample(cells, n):
        g[r][c] = marker
    for r, c in rng.sample([p for p in cells if g[p[0]][p[1]] == 0], rng.randint(3, 6)):
        g[r][c] = rng.choice([x for x in [1, 2, 3, 4, 5, 6, 7, 8, 9] if x != marker])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 9
    g = full_grid(h, w, 0)
    if name == "no_marker":
        # row 0 is empty → no color selector for deletion
        g[2][3] = 4; g[3][7] = 6; g[4][1] = 7
        return g
    if name == "marker_color_absent_below":
        # marker selects a color that doesn't appear below → rule is identity
        g[0][2] = 4
        g[2][3] = 6; g[3][7] = 7; g[4][1] = 9
        return g
    if name == "all_marker_color":
        # all body cells are the marker color → rule erases everything below
        g[0][2] = 4
        for r, c in [(2, 3), (3, 7), (4, 1), (5, 5), (5, 8)]:
            g[r][c] = 4
        return g
    return g
