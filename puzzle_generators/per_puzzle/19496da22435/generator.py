"""Generator for v3_rich_schema:hard_04_row_col_intersections_within_bbox.

Rule: fill blue-column / red-row intersections only inside the gray
frame.

Combinatorial axes (8): grid_h, grid_w, palette_kind, variant,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_frame, no_markers, all_intersections_outside.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "19496da22435"
VERSION = "1.1.0"
TASK_ID = "19496da22435"
SUMMARY = "Fill blue-column/red-row intersections only inside the gray frame."

INVARIANTS = [
    "top-row color-1 markers identify candidate columns",
    "left-column color-2 markers identify candidate rows",
    "a color-7 rectangular frame bounds valid intersections",
    "only strict interior intersections are filled with color 8",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frame", "no_markers", "all_intersections_outside")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "10", "valid": "10"},
    "grid_w":         {"type": "int", "default": "12", "valid": "12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "variant":        {"type": "int", "default": "rng 0..5", "valid": "0..5"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "framed_grid",
                       "valid": "framed_grid"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_LAYOUTS = [
    ([3, 5], [4, 7]),
    ([4, 6], [5, 8]),
    ([3, 6], [4, 6, 8]),
    ([4, 5], [5, 7]),
    ([3, 5, 6], [4, 8]),
    ([5, 6], [5, 6, 8]),
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        variant = ctx.draw_int("variant", 0, 1)
    elif difficulty == "hard":
        variant = ctx.draw_int("variant", 4, 5)
    else:
        variant = ctx.draw_int("variant", 0, 5)
    rows, cols = _LAYOUTS[variant]
    g = full_grid(10, 12, 0)
    for c in range(3, 10):
        g[2][c] = 7
        g[7][c] = 7
    for r in range(2, 8):
        g[r][3] = 7
        g[r][9] = 7
    for c in cols + [10]:
        g[0][c] = 1
    for r in rows + [8]:
        g[r][0] = 2
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 12, 0)
    if name == "no_frame":
        # no color-7 frame → no bounding box, all intersections look valid
        for c in [4, 7, 10]:
            g[0][c] = 1
        for r in [3, 5, 8]:
            g[r][0] = 2
        return g
    if name == "no_markers":
        # frame exists but no row/col markers → rule has no intersections to compute
        for c in range(3, 10):
            g[2][c] = 7; g[7][c] = 7
        for r in range(2, 8):
            g[r][3] = 7; g[r][9] = 7
        return g
    if name == "all_intersections_outside":
        # every marker pair intersects outside the frame → strict-interior filter empties out
        for c in range(3, 10):
            g[2][c] = 7; g[7][c] = 7
        for r in range(2, 8):
            g[r][3] = 7; g[r][9] = 7
        for c in [10, 11]:
            g[0][c] = 1
        for r in [8, 9]:
            g[r][0] = 2
        return g
    return g
