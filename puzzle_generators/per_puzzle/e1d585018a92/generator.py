"""Generator for arc_additional_puzzles_21_set21_bundle:M143.

Rule: cell (0, 0) names a color; the largest object of that color is
cropped to its bbox.

Combinatorial axes (8): grid_h, grid_w, palette_kind, target_color,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: missing_marker, no_target_objects, equal_target_sizes.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e1d585018a92"
VERSION = "1.1.0"
TASK_ID = "e1d585018a92"
SUMMARY = "Cell (0,0) names a color; the largest object of that color is cropped to its bbox."

INVARIANTS = [
    "there are at least two target-color objects",
    "the largest target-color object is separated from all other objects",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("missing_marker", "no_target_objects", "equal_target_sizes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "7..16"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "7..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "target_color":   {"type": "color", "default": "rng nonzero", "valid": "1..9"},
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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 9, 12)
    target = ctx.draw_color("target_color", exclude=[0])
    other = ctx.draw_color("other_color", exclude=[0, target])
    g = full_grid(h, w, 0)
    g[0][0] = target
    for dr, dc in [(0, 0), (0, 1), (1, 0), (2, 0), (2, 1)]:
        g[2 + dr][2 + dc] = target
    g[h - 3][w - 3] = target
    g[h - 2][w - 3] = target
    g[1][w - 2] = other
    g[2][w - 2] = other
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "missing_marker":
        # no (0,0) target color → target is undefined, no object to crop
        for dr, dc in [(0, 0), (0, 1), (1, 0), (2, 0), (2, 1)]:
            g[2 + dr][2 + dc] = 4
        g[h - 3][w - 3] = 4
        return g
    if name == "no_target_objects":
        # marker present but no other cells of that color → "largest" has no candidates
        g[0][0] = 5
        g[3][3] = 7; g[3][4] = 7
        return g
    if name == "equal_target_sizes":
        # multiple target objects all the same size → "largest" is ambiguous, tie-break needed
        g[0][0] = 4
        g[2][2] = 4; g[2][3] = 4
        g[5][5] = 4; g[5][6] = 4
        g[7][7] = 4; g[7][8] = 4
        return g
    return g
