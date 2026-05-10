"""Generator for arc_puzzle_bank_twentysecond21:M150 — pick K-th largest shape via 1-count.

Rule: top-left has K cells of color 1 (K = 1, 2, or 3). Below that:
several shapes in distinct colors and distinct sizes. Output is the
bbox crop of the shape ranked K-th largest.

Combinatorial axes (8): grid_h, grid_w, palette_kind, K,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_K, no_objects, equal_sizes.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.palette import random_palette
from puzzle_generators.helpers.blobs import bbox_overlaps

GENERATOR_ID = "fe4b917edd70"
VERSION = "1.1.0"
TASK_ID = "fe4b917edd70"
SUMMARY = "Top-left K 1-cells (K=1..3) + 3 shapes with distinct sizes."

INVARIANTS = [
    "background is 0",
    "row 0 cols 0..K-1 hold K cells of color 1 (K = 1, 2, or 3)",
    "exactly 3 connected non-bg objects below row 0, distinct colors and distinct sizes",
    "objects don't touch each other or the 1-marker",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_K", "no_objects", "equal_sizes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "K":              {"type": "int", "default": "rng 1..3", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "4", "valid": "3..5"},
    "position_bias":  {"type": "str", "default": "K_marker_topleft_objects_below",
                       "valid": "K_marker_topleft_objects_below"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "3..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SIZED = {
    2: [[(0, 0), (0, 1)], [(0, 0), (1, 0)]],
    3: [[(0, 0), (0, 1), (0, 2)], [(0, 0), (0, 1), (1, 0)]],
    4: [[(0, 0), (0, 1), (1, 0), (1, 1)], [(0, 0), (0, 1), (0, 2), (1, 1)]],
    5: [[(0, 0), (0, 1), (0, 2), (1, 0), (2, 0)]],
    6: [[(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]],
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 8, 9)
        K = ctx.draw_int("K", 1, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 11, 13)
        K = ctx.draw_int("K", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 8, 11)
        K = ctx.draw_int("K", 1, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    for c in range(K):
        g[0][c] = 1
    sizes = rng.sample(list(_SIZED.keys()), 3)
    palette = list(random_palette(rng, 3, exclude={1}))
    placed: list[tuple[int, int, int, int]] = [(0, 0, 0, K - 1)]
    for size, color in zip(sizes, palette):
        shape = rng.choice(_SIZED[size])
        sh = max(c[0] for c in shape) + 1
        sw = max(c[1] for c in shape) + 1
        for _ in range(80):
            r0 = rng.randint(2, h - sh)
            c0 = rng.randint(0, w - sw)
            bb = (r0 - 1, c0 - 1, r0 + sh, c0 + sw)
            if any(bbox_overlaps(bb, p) for p in placed): continue
            paint_at(g, r0, c0, shape, color)
            placed.append((r0, c0, r0 + sh - 1, c0 + sw - 1))
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 9
    g = full_grid(h, w, 0)
    if name == "no_K":
        # No 1-marker — rule has no rank K to pick.
        paint_at(g, 2, 1, [(0, 0), (0, 1)], 4)
        paint_at(g, 4, 1, [(0, 0), (0, 1), (1, 0)], 5)
        return g
    if name == "no_objects":
        # K marker present but no objects — rule has nothing to rank.
        g[0][0] = 1; g[0][1] = 1
        return g
    if name == "equal_sizes":
        # All objects same size — rank by size is ambiguous.
        g[0][0] = 1; g[0][1] = 1
        paint_at(g, 2, 1, [(0, 0), (0, 1)], 4)
        paint_at(g, 4, 1, [(0, 0), (0, 1)], 5)
        paint_at(g, 4, 5, [(0, 0), (0, 1)], 6)
        return g
    return g
