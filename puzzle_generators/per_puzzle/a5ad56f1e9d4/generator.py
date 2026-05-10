"""Generator for arc_puzzle_bank_twentysecond21:M154 — recolor 5-shape cells to nearest marker.

Rule: a 5-color solid rectangle (often 3×3) sits with two single-cell
markers (distinct colors) outside it. Each 5-cell is recolored to
whichever marker is closer (Euclidean tie → first by precedence).

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_rectangle, no_markers, equidistant_markers.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, fill_box
from puzzle_generators.helpers.palette import random_palette

GENERATOR_ID = "a5ad56f1e9d4"
VERSION = "1.1.0"
TASK_ID = "a5ad56f1e9d4"
SUMMARY = "5-color solid rectangle (2-3×2-3) + two distinct-color markers outside it."

INVARIANTS = [
    "background is 0",
    "exactly one solid rectangle in color 5 (size 2×3 to 3×3)",
    "exactly two single-cell markers in distinct non-0/non-5 colors outside the rectangle",
    "markers don't touch the rectangle or each other",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_rectangle", "no_markers", "equidistant_markers")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "5..10"},
    "grid_w":         {"type": "int", "default": "rng 6..8", "valid": "5..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "rect_center_two_markers_outside",
                       "valid": "rect_center_two_markers_outside"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
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
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 6, 7)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 8, 11)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 6, 8)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    rh = rng.randint(2, 3)
    rw = rng.randint(2, 3)
    r1 = rng.randint(1, h - rh - 1)
    c1 = rng.randint(1, w - rw - 1)
    r2 = r1 + rh - 1
    c2 = c1 + rw - 1
    fill_box(g, r1, c1, r2, c2, 5)
    palette = list(random_palette(rng, 2, exclude={5}))
    m1_r = rng.randint(0, max(0, r1 - 1))
    m1_c = rng.randint(c1, c2)
    g[m1_r][m1_c] = palette[0]
    m2_r = rng.randint(r1, r2)
    m2_c = rng.randint(c2 + 2, w - 1) if w - 1 >= c2 + 2 else c2 + 1
    if 0 <= m2_r < h and 0 <= m2_c < w and g[m2_r][m2_c] == 0:
        g[m2_r][m2_c] = palette[1]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 7
    g = full_grid(h, w, 0)
    if name == "no_rectangle":
        # Two markers but no 5-rectangle — rule has no cells to recolor.
        g[0][3] = 3; g[3][6] = 7
        return g
    if name == "no_markers":
        # 5-rectangle but no markers — rule has nothing to assign each
        # 5-cell to.
        fill_box(g, 2, 2, 3, 4, 5)
        return g
    if name == "equidistant_markers":
        # Both markers exactly equidistant from every 5-cell — ties are
        # everywhere, no strictly-nearest marker exists.
        fill_box(g, 2, 2, 3, 4, 5)
        g[0][3] = 3
        g[5][3] = 7
        return g
    return g
