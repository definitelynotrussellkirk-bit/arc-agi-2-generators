"""Generator for arc_puzzle_bank_21_set14_s:S14_M6.

Rule: a blue marker gives the top-left location for the anchor's
row-profile histogram stamp.

Combinatorial axes (8): grid_h, grid_w, palette_kind, marker_col,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_marker, no_anchor, marker_no_room.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "1d8a1c70332a"
VERSION = "1.1.0"
TASK_ID = "1d8a1c70332a"
SUMMARY = "A blue marker gives the top-left location for the anchor's row-profile histogram stamp."

INVARIANTS = [
    "background is 0",
    "there is exactly one blue marker cell",
    "the largest non-blue object supplies the row profile",
    "the marker has enough room for the stamped histogram footprint",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_marker", "no_anchor", "marker_no_room")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "8..15"},
    "grid_w":         {"type": "int", "default": "rng 12..15", "valid": "10..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "marker_col":     {"type": "int", "default": "rng", "valid": "fits histogram width"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "marker_top_right",
                       "valid": "marker_top_right"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

PROFILE_SHAPE = [(0, 0), (0, 2), (1, 0), (1, 1), (1, 2), (2, 1)]
SMALL_L = [(0, 0), (1, 0), (1, 1)]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("height", 9, 10)
        w = ctx.draw_int("width", 12, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("height", 11, 12)
        w = ctx.draw_int("width", 14, 15)
    else:
        h = ctx.draw_int("height", 9, 12)
        w = ctx.draw_int("width", 12, 15)
    marker_col = ctx.draw_int("marker_col", w - 5, w - 4)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)

    g[1][marker_col] = 1
    paint_at(g, rng.randint(3, 4), 1, PROFILE_SHAPE, 3)
    paint_at(g, h - 3, w - 4, SMALL_L, 6)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 13
    g = full_grid(h, w, 0)
    if name == "no_marker":
        # no blue marker → no destination for the histogram stamp
        paint_at(g, 3, 1, PROFILE_SHAPE, 3)
        paint_at(g, h - 3, w - 4, SMALL_L, 6)
        return g
    if name == "no_anchor":
        # only marker present → no anchor to read row profile from
        g[1][w - 5] = 1
        return g
    if name == "marker_no_room":
        # marker too close to the right edge → histogram footprint extends out of bounds
        g[1][w - 1] = 1
        paint_at(g, 3, 1, PROFILE_SHAPE, 3)
        return g
    return g
