"""Generator for arc_puzzle_bank_21_set8_s:S8_H1.

Two cyan markers identify a horizontal or vertical reflection axis. Colored
cells on one side are mirrored across that axis by the rule.

Combinatorial axes (8): grid_h, grid_w, palette_kind, orientation,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_axis, no_content, content_on_both_sides.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0a54983176e5"
VERSION = "1.1.0"
TASK_ID = "0a54983176e5"
SUMMARY = "Cyan markers define a reflection axis for completing colored cells."

INVARIANTS = [
    "exactly two color-8 cells mark one reflection axis",
    "all other colored cells lie on one side of the axis",
    "their mirrored positions are initially empty",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_axis", "no_content", "content_on_both_sides")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "orientation":    {"type": "int", "default": "rng 0..1", "valid": "0..1"},
    "palette_size":   {"type": "int", "default": "rng 4..5", "valid": "3..6"},
    "position_bias":  {"type": "str", "default": "axis_plus_one_side_content",
                       "valid": "axis_plus_one_side_content"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..5", "valid": "3..6"},
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
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        orientation = ctx.draw_int("orientation", 0, 0)
        h = ctx.draw_int("grid_h", 7, 7)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        orientation = ctx.draw_int("orientation", 1, 1)
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        orientation = ctx.draw_int("orientation", 0, 1)
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 9, 11)
    g = full_grid(h, w, 0)
    colors = [2, 3, 4, 5, 6]
    if orientation == 0:
        axis = w // 2
        g[0][axis] = 8
        g[h - 1][axis] = 8
        cells = [(r, c) for r in range(1, h - 1) for c in range(0, axis - 1)]
    else:
        axis = h // 2
        g[axis][0] = 8
        g[axis][w - 1] = 8
        cells = [(r, c) for r in range(0, axis - 1) for c in range(1, w - 1)]
    rng.shuffle(cells)
    for i, (r, c) in enumerate(cells[:6]):
        g[r][c] = colors[i % len(colors)]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_axis":
        # content without 8-marker pair → no axis to mirror across
        g[2][2] = 4
        g[3][1] = 6
        g[4][3] = 7
        return g
    if name == "no_content":
        # axis markers alone, no content → nothing to mirror
        g[0][5] = 8
        g[h - 1][5] = 8
        return g
    if name == "content_on_both_sides":
        # content on both sides of axis → "one side only" precondition fails
        g[0][5] = 8
        g[h - 1][5] = 8
        g[2][2] = 4
        g[3][8] = 6  # also right side
        return g
    return g
