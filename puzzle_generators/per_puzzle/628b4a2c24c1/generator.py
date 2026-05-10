"""Generator for arc_puzzle_bank_twentythird21:M157 — extend shape bbox toward 8-line.

Rule: a full-grid 8-line (vertical or horizontal) is on one side.
For the colored shape on the other side, fill every row of its bbox
that has at least one shape-cell, extending toward the 8-line until
just before the line.

Combinatorial axes (8): grid_h, grid_w, palette_kind, shape_idx,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_line, no_shape, shape_touches_line.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, fill_box, paint_at
from puzzle_generators.helpers.palette import random_palette

GENERATOR_ID = "628b4a2c24c1"
VERSION = "1.1.0"
TASK_ID = "628b4a2c24c1"
SUMMARY = "8-line column on the right + a colored shape on the left."

INVARIANTS = [
    "background is 0",
    "exactly one full-height 8-line column",
    "exactly one connected colored shape on the left side, with room to extend",
    "shape extends partway toward the 8-line (not yet touching it)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_line", "no_shape", "shape_touches_line")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "shape_idx":      {"type": "int", "default": "rng 0..5", "valid": "0..5"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..2"},
    "position_bias":  {"type": "str", "default": "shape_left_line_right",
                       "valid": "shape_left_line_right"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = [
    [(0, 0), (1, 0), (2, 0)],
    [(0, 0), (1, 0), (2, 0), (3, 0)],
    [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)],
    [(0, 0), (1, 0), (1, 1), (2, 0)],
    [(0, 0), (0, 1), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (1, 0), (2, 0), (3, 0)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 10, 13)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 8, 11)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    line_c = w - 4
    fill_box(g, 0, line_c, h - 1, line_c, 8)
    color = rng.choice(list(random_palette(rng, 4, exclude={8})))
    shape = rng.choice(_SHAPES)
    sh = max(c[0] for c in shape) + 1
    sw = max(c[1] for c in shape) + 1
    if sh > h or sw > line_c - 1:
        return g
    r0 = rng.randint(0, h - sh)
    c0 = rng.randint(0, line_c - sw - 1)
    paint_at(g, r0, c0, shape, color)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 10
    g = full_grid(h, w, 0)
    if name == "no_line":
        # No 8-line — rule has no anchor to extend toward.
        paint_at(g, 1, 1, [(0, 0), (1, 0), (2, 0)], 3)
        return g
    if name == "no_shape":
        # 8-line present but no shape — rule has nothing to extend.
        line_c = w - 4
        fill_box(g, 0, line_c, h - 1, line_c, 8)
        return g
    if name == "shape_touches_line":
        # Shape already adjacent to the line — already "extended" (rule no-op).
        line_c = w - 4
        fill_box(g, 0, line_c, h - 1, line_c, 8)
        paint_at(g, 1, line_c - 1, [(0, 0), (1, 0)], 3)
        return g
    return g
