"""Generator for arc_puzzle_bank_21_more:medium_b01.

Rule: cell (0, 0) names a marker color; all other cells of that color
are cropped as a mask.

Combinatorial axes (8): grid_h, grid_w, palette_kind, marker_color,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: missing_marker, no_target_cells, marker_only_at_origin.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "85c59d39af56"
VERSION = "1.1.0"
TASK_ID = "85c59d39af56"
SUMMARY = "Cell (0,0) names a marker color; all other cells of that color are cropped as a mask."

INVARIANTS = [
    "marker color appears at (0,0) and in a separated motif",
    "non-marker distractor colors are ignored",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("missing_marker", "no_target_cells", "marker_only_at_origin")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "marker_color":   {"type": "color", "default": "rng nonzero", "valid": "1..9"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "marker_top_left",
                       "valid": "marker_top_left"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 8, 12)
    marker = ctx.draw_color("marker_color", exclude=[0])
    other = ctx.draw_color("other_color", exclude=[0, marker])
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    g[0][0] = marker
    top = rng.randint(2, h - 4)
    left = rng.randint(2, w - 4)
    for dr, dc in [(0, 0), (0, 1), (1, 1), (2, 0)]:
        g[top + dr][left + dc] = marker
    g[h - 2][w - 2] = other
    g[h - 3][w - 2] = other
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "missing_marker":
        # cell (0,0) is bg → no marker color named, target is undefined
        g[3][3] = 4; g[3][4] = 4; g[4][4] = 4; g[5][3] = 4
        g[h - 2][w - 2] = 6
        return g
    if name == "no_target_cells":
        # marker named but only the (0,0) cell carries that color → mask is empty
        g[0][0] = 4
        g[h - 2][w - 2] = 6
        g[h - 3][w - 2] = 6
        return g
    if name == "marker_only_at_origin":
        # only the origin cell is marker color and rest are distractor → cropped mask trivial
        g[0][0] = 5
        for r in range(2, 6):
            for c in range(2, 6):
                g[r][c] = 8
        return g
    return g
