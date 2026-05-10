"""Generator for arc_additional_puzzles_21_set19_bundle:M127 — Slide non-9 blobs east in 9-walled compartments.

Rule: 9-cells = walls. Each non-9 connected blob slides east until
adjacent to a wall or another (already-moved) blob.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_compartments,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_walls, no_blobs, blob_at_east_wall.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "f0d16ecf2012"
VERSION = "1.1.0"
TASK_ID = "f0d16ecf2012"
SUMMARY = "9-walls split a 13x12 grid into 3 compartments, each holding 1 small blob."

INVARIANTS = [
    "9-walls form left/right cols + 4 horizontal dividers",
    "exactly 3 compartments, each with one small non-9 blob",
    "blob has room to slide east",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_walls", "no_blobs", "blob_at_east_wall")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "13", "valid": "13..13"},
    "grid_w":         {"type": "int", "default": "12", "valid": "12..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_compartments": {"type": "int", "default": "3", "valid": "3..3"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "horizontal_compartments_with_blobs",
                       "valid": "horizontal_compartments_with_blobs"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4..4"},
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
    rng = ctx.draw_rng("layout")
    h, w = 13, 12
    g = full_grid(h, w, 0)
    for r in range(h):
        g[r][0] = 9; g[r][w - 1] = 9
    for r in (0, 4, 8, 12):
        for c in range(w):
            g[r][c] = 9
    shapes = [
        [(0, 0), (0, 1), (1, 0), (1, 1)],
        [(0, 0), (0, 1), (1, 1)],
        [(0, 0), (1, 0), (1, 1)],
        [(0, 0), (0, 1)],
        [(0, 0), (1, 0)],
    ]
    palette = rng.sample([2, 3, 4, 6, 7, 8], 3)
    for i, (r0, r1) in enumerate([(1, 3), (5, 7), (9, 11)]):
        s = rng.choice(shapes)
        cs = [c for _, c in s]
        max_c0 = w - 4 - max(cs)
        c0 = rng.randint(1, max(1, max_c0))
        max_dr = (r1 - r0) - max(r for r, _ in s)
        dr = rng.randint(0, max(0, max_dr))
        paint_at(g, r0 + dr, c0, s, palette[i])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 13, 12
    g = full_grid(h, w, 0)
    if name == "no_walls":
        # blobs without 9-walls → no compartments to slide within
        paint_at(g, 1, 2, [(0, 0), (0, 1), (1, 0)], 4)
        paint_at(g, 5, 3, [(0, 0), (0, 1)], 6)
        paint_at(g, 9, 4, [(0, 0), (1, 0)], 7)
        return g
    if name == "no_blobs":
        # walls alone, no blobs to slide
        for r in range(h):
            g[r][0] = 9; g[r][w - 1] = 9
        for r in (0, 4, 8, 12):
            for c in range(w):
                g[r][c] = 9
        return g
    if name == "blob_at_east_wall":
        # blob already touching east wall → slide is identity
        for r in range(h):
            g[r][0] = 9; g[r][w - 1] = 9
        for r in (0, 4, 8, 12):
            for c in range(w):
                g[r][c] = 9
        paint_at(g, 1, w - 3, [(0, 0), (0, 1)], 4)
        paint_at(g, 5, w - 3, [(0, 0), (1, 0)], 6)
        paint_at(g, 9, w - 3, [(0, 0), (0, 1)], 7)
        return g
    return g
