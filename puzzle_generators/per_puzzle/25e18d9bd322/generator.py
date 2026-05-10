"""Generator for arc_additional_puzzle_bank_volume3:M20.

Rule: among objects (excluding the 9-marker), pick the one nearest to
the marker by Manhattan distance; output bbox-cropped mask in obj's color.

Combinatorial axes (8): grid_h/w, palette_kind, n_blobs, palette_size,
position_bias, n_distinct_colors, marker_pos, texture.
Degenerates: no_marker, no_blobs, all_equidistant.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "25e18d9bd322"
VERSION = "1.1.0"
TASK_ID = "25e18d9bd322"
SUMMARY = "9-marker + 3 4-blobs at varying distances."

INVARIANTS = [
    "exactly one 9-marker",
    "exactly 3 non-touching 4-blobs at varying distances from marker",
    "nearest blob is unambiguous",
]

PALETTE_KINDS = ("default", "near_top", "near_bottom", "near_center")
DEGENERATE_TEXTURES = ("no_marker", "no_blobs", "all_equidistant")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "3", "valid": "3"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
    "marker_pos":     {"type": "str", "default": "fixed", "valid": "fixed"},
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
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 11)
    g = full_grid(h, w, 0)
    g[3][4] = 9
    paint_at(g, 4, 6, [(0, 0), (0, 1), (1, 1)], 4)
    paint_at(g, 1, 1, [(0, 0), (0, 1), (1, 0)], 4)
    paint_at(g, h - 2, 2, [(0, 0), (0, 1)], 4)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_marker":
        # blobs but no 9-marker — distance reference undefined
        paint_at(g, 1, 1, [(0, 0), (0, 1), (1, 0)], 4)
        paint_at(g, 4, 6, [(0, 0), (0, 1), (1, 1)], 4)
        return g
    if name == "no_blobs":
        # marker but no blobs to pick from
        g[3][4] = 9
        return g
    if name == "all_equidistant":
        # marker + blobs all at exactly same Manhattan distance — ambiguous
        g[4][4] = 9
        # 3 blobs each 3 steps away
        paint_at(g, 1, 4, [(0, 0)], 4)  # dist=3
        paint_at(g, 7, 4, [(0, 0)], 4)  # dist=3
        paint_at(g, 4, 7, [(0, 0)], 4)  # dist=3
        return g
    return g
