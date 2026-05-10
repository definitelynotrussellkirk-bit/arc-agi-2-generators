"""Generator for arc_additional_puzzles_21_set18_bundle:M121 — pack chosen objects in legend order.

Rule: row 0 holds N legend colors. Below row 0, for each legend
color, pick the largest object of that color and crop to its bbox.
Pack the crops horizontally with 1-col gap in legend order.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_legend, no_objects, color_mismatch.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.palette import random_palette
from puzzle_generators.helpers.blobs import bbox_overlaps

GENERATOR_ID = "192d2bc2de61"
VERSION = "1.1.0"
TASK_ID = "192d2bc2de61"
SUMMARY = "Row-0 legend (N colors) + N matching objects (one per color) below row 0."

INVARIANTS = [
    "row 0 holds N distinct non-bg legend colors at consecutive columns 0..N-1",
    "below row 0: exactly one object of each legend color",
    "objects don't touch each other or row 0",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_legend", "no_objects", "color_mismatch")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 13..16", "valid": "12..20"},
    "n_legend":       {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "position_bias":  {"type": "str", "default": "row0_legend_with_objects",
                       "valid": "row0_legend_with_objects"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = [
    [(0, 0), (0, 1), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 1)],
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    [(0, 0), (0, 1), (1, 1), (1, 2), (2, 2)],
    [(0, 0), (0, 1), (0, 2), (1, 0), (2, 0)],
    [(0, 0), (1, 0), (1, 1), (2, 0)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 13, 14)
        n = ctx.draw_int("n_legend", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 14)
        w = ctx.draw_int("grid_w", 15, 19)
        n = ctx.draw_int("n_legend", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 13, 16)
        n = ctx.draw_int("n_legend", 2, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    legend = list(random_palette(rng, n))
    for i, color in enumerate(legend):
        g[0][i] = color
    placed: list[tuple[int, int, int, int]] = [(0, 0, 0, w - 1)]
    for color in legend:
        shape = rng.choice(_SHAPES)
        sh = max(c[0] for c in shape) + 1
        sw = max(c[1] for c in shape) + 1
        for _ in range(80):
            r0 = rng.randint(2, h - sh - 1)
            c0 = rng.randint(0, w - sw)
            bb_pad = (r0 - 1, c0 - 1, r0 + sh, c0 + sw)
            if any(bbox_overlaps(bb_pad, p) for p in placed): continue
            paint_at(g, r0, c0, shape, color)
            placed.append((r0, c0, r0 + sh - 1, c0 + sw - 1))
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 14
    g = full_grid(h, w, 0)
    if name == "no_legend":
        # Objects but no row-0 legend — rule has no order/selection
        # to drive packing; output undefined.
        for r, c in [(3, 3), (4, 3), (4, 4)]: g[r][c] = 4
        for r, c in [(3, 9), (4, 9), (4, 10)]: g[r][c] = 6
        return g
    if name == "no_objects":
        # Legend but no body objects — rule has nothing to pack.
        g[0][0] = 4; g[0][1] = 6; g[0][2] = 7
        return g
    if name == "color_mismatch":
        # Legend lists colors not present in body — rule's
        # "largest object of color X" yields nothing for any X.
        g[0][0] = 4; g[0][1] = 6
        for r, c in [(3, 3), (4, 3), (4, 4)]: g[r][c] = 7
        return g
    return g
