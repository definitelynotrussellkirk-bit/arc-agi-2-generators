"""Generator for arc_puzzle_bank_twentyfirst21:M141 — fill shape's bbox up to the 8-line.

Rule: a full-grid 8-line (vertical or horizontal) divides the grid.
For the colored shape on one side, fill the entire bbox (between the
shape and the 8-line) with the shape's color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, shape_idx,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_line, no_shape, shape_touching_line.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, fill_box, paint_at
from puzzle_generators.helpers.palette import random_palette

GENERATOR_ID = "26ac80084566"
VERSION = "1.1.0"
TASK_ID = "26ac80084566"
SUMMARY = "8-line column divides grid; one side has a small colored shape."

INVARIANTS = [
    "background is 0",
    "exactly one full-height (or full-width) 8-line",
    "one side has a connected colored shape (3-5 cells)",
    "the shape extends partway toward the 8-line (not yet touching it)",
    "the other side is empty",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_line", "no_shape", "shape_touching_line")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "shape_idx":      {"type": "int", "default": "rng 0..3", "valid": "0..3"},
    "palette_size":   {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "position_bias":  {"type": "str", "default": "8line_divides_shape_offset",
                       "valid": "8line_divides_shape_offset"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = [
    [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],   # plus
    [(0, 0), (1, 0), (1, 1), (2, 0)],            # T-rotated
    [(0, 0), (0, 1), (1, 1), (2, 1)],            # zig
    [(0, 0), (0, 1), (1, 0), (1, 1)],            # 2x2
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 5, 5)
        w = ctx.draw_int("grid_w", 7, 8)
        idx = ctx.draw_int("shape_idx", 3, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 9, 12)
        idx = ctx.draw_int("shape_idx", 0, 3)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 7, 10)
        idx = ctx.draw_int("shape_idx", 0, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    line_c = w - 3
    fill_box(g, 0, line_c, h - 1, line_c, 8)
    color = rng.choice(list(random_palette(rng, 4, exclude={8})))
    shape = _SHAPES[idx]
    sh = max(c[0] for c in shape) + 1
    sw = max(c[1] for c in shape) + 1
    if sh > h or sw > line_c - 1:
        return g
    r0 = rng.randint(0, h - sh)
    c0 = rng.randint(0, line_c - sw - 1)
    paint_at(g, r0, c0, shape, color)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 9
    g = full_grid(h, w, 0)
    if name == "no_line":
        # Shape present but no 8-line — rule has no boundary to fill up to.
        paint_at(g, 1, 1, _SHAPES[0], 4)
        return g
    if name == "no_shape":
        # 8-line present but no shape — rule has nothing to extend.
        line_c = w - 3
        fill_box(g, 0, line_c, h - 1, line_c, 8)
        return g
    if name == "shape_touching_line":
        # Shape already touches the 8-line — bbox-to-line fill is empty.
        line_c = w - 3
        fill_box(g, 0, line_c, h - 1, line_c, 8)
        for r in range(2, 5):
            g[r][line_c - 1] = 4
        return g
    return g
