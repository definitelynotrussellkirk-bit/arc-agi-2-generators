"""Generator for arc_puzzle_bank_21_set5_s:S5_M5.

The top-row count of blue markers selects the orange object with that many
enclosed holes; the rule outputs that object's bounding-box crop.

Combinatorial axes (8): grid_h, grid_w, palette_kind, hole_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_markers, no_matching_holes, tied_holes.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "49a0b77dcc7f"
VERSION = "1.1.0"
TASK_ID = "49a0b77dcc7f"
SUMMARY = "Blue count selects among orange components by enclosed-hole count."

INVARIANTS = [
    "row 0 contains one or two color-1 count markers",
    "orange components have distinct enclosed-hole counts",
    "the selected component is color 7",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_markers", "no_matching_holes", "tied_holes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "13", "valid": "13..13"},
    "grid_w":         {"type": "int", "default": "18", "valid": "18..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "hole_count":     {"type": "int", "default": "rng 1..2", "valid": "1..2"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "top_markers_holed_objects",
                       "valid": "top_markers_holed_objects"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _paint_holed_rect(g, top, left, h, w, holes):
    for r in range(h):
        for c in range(w):
            g[top + r][left + c] = 7
    for r, c in holes:
        g[top + r][left + c] = 0


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        k = ctx.draw_int("hole_count", 1, 1)
    elif difficulty == "hard":
        k = ctx.draw_int("hole_count", 2, 2)
    else:
        k = ctx.draw_int("hole_count", 1, 2)
    g = full_grid(13, 18, 0)
    marker_cols = rng.sample(range(1, 8), k)
    for c in marker_cols:
        g[0][c] = 1
    if k == 1:
        _paint_holed_rect(g, 3, 1, 5, 5, [(2, 2)])
        _paint_holed_rect(g, 3, 10, 5, 7, [(2, 2), (2, 4)])
    else:
        _paint_holed_rect(g, 3, 1, 5, 5, [(2, 2)])
        _paint_holed_rect(g, 3, 10, 5, 7, [(2, 2), (2, 4)])
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 18, 0)
    if name == "no_markers":
        # no blue markers in row 0 → no count to select with
        _paint_holed_rect(g, 3, 1, 5, 5, [(2, 2)])
        _paint_holed_rect(g, 3, 10, 5, 7, [(2, 2), (2, 4)])
        return g
    if name == "no_matching_holes":
        # markers say 3 but no orange component has 3 holes
        g[0][1] = 1; g[0][3] = 1; g[0][5] = 1
        _paint_holed_rect(g, 3, 1, 5, 5, [(2, 2)])
        _paint_holed_rect(g, 3, 10, 5, 7, [(2, 2), (2, 4)])
        return g
    if name == "tied_holes":
        # both orange components have the same hole count → ambiguous select
        g[0][1] = 1
        _paint_holed_rect(g, 3, 1, 5, 5, [(2, 2)])
        _paint_holed_rect(g, 3, 10, 5, 5, [(2, 2)])
        return g
    return g
