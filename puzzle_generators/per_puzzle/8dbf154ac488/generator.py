"""Generator for ARC task 794b24be.

Rule: 3×3 binary grid; output is 3×3 with 2s placed at first n positions
of fixed fill (n = count of 1s, capped at 4).

Combinatorial axes (8): one_count, cell_layout, position_bias,
include_decoy_color, decoy_density, anchor_corners, asymmetry,
fg_distribution.
Degenerates: all_zero, all_ones, mixed_with_other_color.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8dbf154ac488"
VERSION = "1.1.0"
TASK_ID = "8dbf154ac488"
SUMMARY = "3×3 binary grid; rule encodes count of 1s into fixed 2-cell pattern."

INVARIANTS = [
    "input is 3×3",
    "only colors 0 and 1 appear",
    "count of 1s in [0, 9]",
]

CELL_LAYOUTS = ("scattered", "diagonal", "row", "col", "corners",
                "center", "L_shape")
DEGENERATE_TEXTURES = ("all_zero", "all_ones", "mixed_with_other_color")
HELPFUL_TEXTURES = CELL_LAYOUTS

AXES = {
    "one_count":         {"type": "int", "default": "rng 0..6", "valid": "0..9"},
    "cell_layout":       {"type": "str", "default": "rng helpful",
                          "valid": "|".join(CELL_LAYOUTS)},
    "position_bias":     {"type": "str", "default": "rng top|bottom|spread",
                          "valid": "top|bottom|spread"},
    "anchor_corners":    {"type": "bool", "default": "false",
                          "valid": "true|false"},
    "anchor_center":     {"type": "bool", "default": "false",
                          "valid": "true|false"},
    "fg_distribution":   {"type": "str", "default": "rng even|skewed",
                          "valid": "even|skewed"},
    "include_zero_bg":   {"type": "bool", "default": "true",
                          "valid": "true|false"},
    "noise_overlay":     {"type": "float", "default": "0", "valid": "0..0.05"},
    "texture":           {"type": "str", "default": "alias for cell_layout",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        c_lo, c_hi = 0, 2
    elif difficulty == "hard":
        c_lo, c_hi = 5, 9
    else:
        c_lo, c_hi = 0, 6
    rng = ctx.draw_rng("cells")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    count = int(overrides.get("one_count",
                              ctx.draw_int("one_count", c_lo, c_hi)))
    count = max(0, min(9, count))
    layout = (overrides.get("texture") or overrides.get("cell_layout")
              or ctx.draw_choice("cell_layout", list(CELL_LAYOUTS)))
    bias = overrides.get("position_bias",
                         ctx.draw_choice("position_bias",
                                         ["top", "bottom", "spread"]))
    g = full_grid(3, 3, 0)
    cells = _layout_cells(layout, bias, rng)
    for r, c in cells[:count]:
        g[r][c] = 1
    return g


def _layout_cells(layout, bias, rng):
    if layout == "diagonal":
        cells = [(0, 0), (1, 1), (2, 2), (0, 2), (2, 0), (0, 1), (1, 0), (1, 2), (2, 1)]
    elif layout == "row":
        cells = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
    elif layout == "col":
        cells = [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2)]
    elif layout == "corners":
        cells = [(0, 0), (0, 2), (2, 0), (2, 2), (1, 1), (0, 1), (1, 0), (1, 2), (2, 1)]
    elif layout == "center":
        cells = [(1, 1), (0, 1), (1, 0), (1, 2), (2, 1), (0, 0), (0, 2), (2, 0), (2, 2)]
    elif layout == "L_shape":
        cells = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (1, 1), (0, 1), (0, 2), (1, 2)]
    else:
        cells = [(r, c) for r in range(3) for c in range(3)]
    if bias == "top":
        cells = sorted(cells, key=lambda rc: rc[0])
    elif bias == "bottom":
        cells = sorted(cells, key=lambda rc: -rc[0])
    elif layout == "scattered":
        rng.shuffle(cells)
    return cells


def _draw_from_degenerate(name, rng):
    if name == "all_zero":
        return [[0] * 3 for _ in range(3)]
    if name == "all_ones":
        return [[1] * 3 for _ in range(3)]
    if name == "mixed_with_other_color":
        # Rule will see this as "non-zero" but it's not 1; falls through differently
        g = [[0] * 3 for _ in range(3)]
        g[0][0] = 1
        g[1][1] = 1
        return g
    return [[0] * 3 for _ in range(3)]
