"""Generator for arc_additional_puzzle_bank_volume17:E116.

Rule: output is the bounding box crop enclosing all color-6 cells.

Combinatorial axes (8): grid_h/w, palette_kind, fill_color, marker_position,
palette_size, position_bias, n_distinct_colors, padding, texture.
Degenerates: only_one_six, no_six, six_at_corners.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "07a647c5c28d"
VERSION = "1.1.0"
TASK_ID = "07a647c5c28d"
SUMMARY = "The output is the bounding box enclosing all color-6 cells."

INVARIANTS = [
    "color 6 cells define a smaller bounding box inside the grid",
    "other colors may appear inside that box but not outside as targets",
]

PALETTE_KINDS = ("default", "warm_fill", "cool_fill", "primary_fill")
DEGENERATE_TEXTURES = ("only_one_six", "no_six", "six_at_corners")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "fill_color":     {"type": "int", "default": "rng", "valid": "1..9 except 6"},
    "marker_position": {"type": "str", "default": "interior",
                        "valid": "interior"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "interior",
                       "valid": "interior"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
    "padding":        {"type": "int", "default": "rng 1..3", "valid": "1..3"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 8, 12)
    fill_color = ctx.draw_color("fill_color", exclude=[0, 6])
    g = full_grid(h, w, 0)
    top = ctx.draw_int("top", 1, h - 5)
    left = ctx.draw_int("left", 1, w - 5)
    for dr, dc in [(0, 0), (0, 3), (2, 0), (2, 3)]:
        g[top + dr][left + dc] = 6
    g[top + 1][left + 1] = fill_color
    g[top + 1][left + 2] = fill_color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    if name == "only_one_six":
        # bbox is a 1×1 — degenerate crop
        g[3][4] = 6
        g[3][5] = 4
        return g
    if name == "no_six":
        # no markers — bbox is undefined, rule has nothing to crop
        g[3][4] = 4
        g[4][5] = 4
        return g
    if name == "six_at_corners":
        # 6s in all 4 grid corners — bbox = full grid (rule no-op)
        g[0][0] = 6
        g[0][w - 1] = 6
        g[h - 1][0] = 6
        g[h - 1][w - 1] = 6
        g[4][4] = 4
        return g
    return g
