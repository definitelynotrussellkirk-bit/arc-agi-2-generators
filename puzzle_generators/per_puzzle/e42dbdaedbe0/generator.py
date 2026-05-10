"""Generator for arc_puzzle_bank_eighteenth21:M123 — recolor 8-shapes by size legend.

Rule: row 0 holds a legend (e.g., [2, 4, 6] at cols 0-2). Each
8-color shape elsewhere is recolored according to its cell count:
1-cell → legend[0], 2-cell → legend[1], 3-cell → legend[2].

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_legend (row 0 is bg → rule's size→color lookup is
empty, all 8s stay 8), no_shapes (legend present, no 8-shapes →
rule has nothing to recolor), tied_sizes (all 8-shapes share same
size → rule maps every shape to one legend slot, no contrast).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.palette import random_palette
from puzzle_generators.helpers.blobs import bbox_overlaps

GENERATOR_ID = "e42dbdaedbe0"
VERSION = "1.1.0"
TASK_ID = "e42dbdaedbe0"
SUMMARY = "Row-0 legend (3 colors) + 1-cell, 2-cell, 3-cell 8-shapes elsewhere."

INVARIANTS = [
    "background is 0",
    "row 0 cols 0-2 hold 3 distinct legend colors (none is 8)",
    "below row 0: a 1-cell 8, a 2-cell 8-line, and a 3-cell 8-L (each at a distinct location)",
    "8-shapes don't touch each other or row 0",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_legend", "no_shapes", "tied_sizes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":            {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "grid_w":            {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 3..3", "valid": "3..3"},
    "position_bias":     {"type": "str", "default": "row0_legend_plus_8shapes",
                          "valid": "row0_legend_plus_8shapes"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..4", "valid": "4..4"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_3CELL = [
    [(0, 0), (0, 1), (1, 1)],
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (0, 2)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 7, 10)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    legend = list(random_palette(rng, 3, exclude={8}))
    for i, c in enumerate(legend):
        g[0][i] = c
    placed: list[tuple[int, int, int, int]] = [(0, 0, 0, w - 1)]
    for _ in range(80):
        r0 = rng.randint(2, h - 2)
        c0 = rng.randint(0, w - 1)
        bb = (r0 - 1, c0 - 1, r0 + 1, c0 + 1)
        if any(bbox_overlaps(bb, p) for p in placed): continue
        g[r0][c0] = 8
        placed.append((r0, c0, r0, c0))
        break
    two = rng.choice([[(0, 0), (0, 1)], [(0, 0), (1, 0)]])
    sh = max(c[0] for c in two) + 1
    sw = max(c[1] for c in two) + 1
    for _ in range(80):
        r0 = rng.randint(2, h - sh - 1)
        c0 = rng.randint(0, w - sw)
        bb = (r0 - 1, c0 - 1, r0 + sh, c0 + sw)
        if any(bbox_overlaps(bb, p) for p in placed): continue
        paint_at(g, r0, c0, two, 8)
        placed.append((r0, c0, r0 + sh - 1, c0 + sw - 1))
        break
    three = rng.choice(_3CELL)
    sh = max(c[0] for c in three) + 1
    sw = max(c[1] for c in three) + 1
    for _ in range(80):
        r0 = rng.randint(2, h - sh - 1)
        c0 = rng.randint(0, w - sw)
        bb = (r0 - 1, c0 - 1, r0 + sh, c0 + sw)
        if any(bbox_overlaps(bb, p) for p in placed): continue
        paint_at(g, r0, c0, three, 8)
        placed.append((r0, c0, r0 + sh - 1, c0 + sw - 1))
        break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_legend":
        # Row 0 is bg → rule's size→color map empty; 8s stay 8.
        g[3][2] = 8
        g[3][5] = 8; g[3][6] = 8
        g[5][2] = 8; g[6][2] = 8; g[6][3] = 8
        return g
    if name == "no_shapes":
        # Legend present but no 8-shapes → rule has nothing to recolor.
        g[0][0] = 2; g[0][1] = 4; g[0][2] = 6
        return g
    if name == "tied_sizes":
        # All 8-shapes are 1-cell → all map to legend[0]; no contrast.
        g[0][0] = 2; g[0][1] = 4; g[0][2] = 6
        g[3][2] = 8
        g[4][6] = 8
        g[6][4] = 8
        return g
    return g
