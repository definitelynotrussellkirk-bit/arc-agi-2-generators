"""Generator for arc_puzzle_bank_nineteenth21:M131 — fill each shape's bbox to a solid rectangle.

Rule: each connected non-bg shape has its bounding-box filled with
the shape's color (output is solid rectangles).

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, n_objs, texture.
Degenerates: no_shapes, solid_rect, single_cell.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.palette import random_palette
from puzzle_generators.helpers.blobs import bbox_overlaps

GENERATOR_ID = "010ef9d0160b"
VERSION = "1.1.0"
TASK_ID = "010ef9d0160b"
SUMMARY = "1-2 hollow shapes in distinct colors; output fills each bbox."

INVARIANTS = [
    "background is 0",
    "1-2 connected shapes (3-5 cells, hollow within bbox) in distinct non-bg colors",
    "shapes don't touch each other",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_shapes", "solid_rect", "single_cell")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..8", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_objs":         {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "= n_objs", "valid": "1..3"},
    "position_bias":  {"type": "str", "default": "scattered_hollow_shapes",
                       "valid": "scattered_hollow_shapes"},
    "n_distinct_colors": {"type": "int", "default": "= n_objs", "valid": "1..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_HOLLOW = [
    [(0, 0), (0, 1), (1, 1)],
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    [(0, 1), (1, 0), (1, 1), (2, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 0)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 7, 8)
        n = ctx.draw_int("n_objs", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 10, 13)
        n = ctx.draw_int("n_objs", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 5, 8)
        w = ctx.draw_int("grid_w", 7, 10)
        n = ctx.draw_int("n_objs", 1, 2)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = list(random_palette(rng, n))
    placed: list[tuple[int, int, int, int]] = []
    for color in palette:
        shape = rng.choice(_HOLLOW)
        sh = max(c[0] for c in shape) + 1
        sw = max(c[1] for c in shape) + 1
        for _ in range(80):
            r0 = rng.randint(0, h - sh)
            c0 = rng.randint(0, w - sw)
            bb_pad = (r0 - 1, c0 - 1, r0 + sh, c0 + sw)
            if any(bbox_overlaps(bb_pad, p) for p in placed): continue
            paint_at(g, r0, c0, shape, color)
            placed.append((r0, c0, r0 + sh - 1, c0 + sw - 1))
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 8
    g = full_grid(h, w, 0)
    if name == "no_shapes":
        # Empty grid — rule has no shapes whose bboxes to fill.
        return g
    if name == "solid_rect":
        # Shape is already a solid rectangle (bbox fully filled) —
        # rule's bbox-fill is identity, output equals input.
        for dr in range(2):
            for dc in range(2): g[2 + dr][3 + dc] = 4
        return g
    if name == "single_cell":
        # Components are single cells — bbox is 1×1, already solid;
        # rule's effect is invisible.
        g[2][2] = 4; g[5][6] = 6
        return g
    return g
