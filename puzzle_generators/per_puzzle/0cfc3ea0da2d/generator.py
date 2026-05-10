"""Generator for v0_original:medium_05 — recolor each object by size: 3 cells → 1, 2 → 2, 1 → 3.

Rule: each connected non-bg object is recolored by its cell-count:
3 → 1, 2 → 2, 1 → 3.

Combinatorial axes (8): grid_h, grid_w, palette_kind, shape_3,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_objects, equal_sizes, objects_touching.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.palette import random_palette
from puzzle_generators.helpers.blobs import bbox_overlaps

GENERATOR_ID = "0cfc3ea0da2d"
VERSION = "1.1.0"
TASK_ID = "0cfc3ea0da2d"
SUMMARY = "1 3-cell L + 1 2-cell line + 1 single-cell, each in distinct colors."

INVARIANTS = [
    "background is 0",
    "exactly one 3-cell object, one 2-cell object, one 1-cell object",
    "each object a distinct color (so the rule's color tracking is unambiguous)",
    "objects don't touch each other",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_objects", "equal_sizes", "objects_touching")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..8", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 6..9", "valid": "5..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "shape_3":        {"type": "int", "default": "rng 0..3", "valid": "0..3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..4"},
    "position_bias":  {"type": "str", "default": "non_overlapping_objects",
                       "valid": "non_overlapping_objects"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "3..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_3 = [
    [(0, 0), (0, 1), (0, 2)],
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (1, 0), (2, 0)],
]
_2 = [
    [(0, 0), (0, 1)],
    [(0, 0), (1, 0)],
]
_1 = [[(0, 0)]]


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
        h = ctx.draw_int("grid_h", 5, 8)
        w = ctx.draw_int("grid_w", 6, 9)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = list(random_palette(rng, 3))
    placed: list[tuple[int, int, int, int]] = []
    for size_set, color in zip([_3, _2, _1], palette):
        shape = rng.choice(size_set)
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
    h, w = 7, 8
    g = full_grid(h, w, 0)
    if name == "no_objects":
        # Empty grid — rule has no objects to recolor.
        return g
    if name == "equal_sizes":
        # Three 2-cell objects — rule's size→color map has no 1- or 3-cell input.
        paint_at(g, 1, 1, [(0, 0), (0, 1)], 4)
        paint_at(g, 3, 1, [(0, 0), (0, 1)], 5)
        paint_at(g, 5, 1, [(0, 0), (0, 1)], 6)
        return g
    if name == "objects_touching":
        # Objects touch — connected-component merge changes the size groups.
        paint_at(g, 1, 1, [(0, 0), (0, 1), (0, 2)], 4)
        paint_at(g, 1, 4, [(0, 0), (0, 1)], 5)
        return g
    return g
