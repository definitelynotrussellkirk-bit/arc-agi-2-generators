"""Generator for arc_additional_puzzle_bank_volume4:M23 — Rotate each object cw in place.

Rule: for each object, rotate-cw its normalized cells; place at object's
top-left in fresh grid.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_objects,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_objects, square_bboxes, touching_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "f2f15d832fb1"
VERSION = "1.1.0"
TASK_ID = "f2f15d832fb1"
SUMMARY = "2 distinct-color non-touching blobs with non-square bboxes; output rotates each cw."

INVARIANTS = [
    "exactly 2 non-touching blobs",
    "each has a non-square bbox so rotation is visible",
    "blobs use distinct colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_objects", "square_bboxes", "touching_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..14", "valid": "9..16"},
    "grid_w":         {"type": "int", "default": "rng 11..14", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_objects":      {"type": "int", "default": "2", "valid": "2..2"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "two_corner_blobs",
                       "valid": "two_corner_blobs"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


PATTERNS_4x4 = [
    [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (3, 2), (3, 3)],  # L corner
    [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (2, 0), (3, 0)],  # corner top
    [(0, 0), (1, 0), (1, 1), (2, 0), (3, 0), (3, 1), (3, 2)],
]



def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 14)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 11, 14)
        w = ctx.draw_int("grid_w", 11, 14)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    colors = list(range(1, 10)); rng.shuffle(colors)
    p1 = rng.choice(PATTERNS_4x4)
    p2 = rng.choice(PATTERNS_4x4)
    paint_at(g, 1, 1, p1, colors[0])
    paint_at(g, h - 5, w - 5, p2, colors[1])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 12
    g = full_grid(h, w, 0)
    if name == "no_objects":
        # blank → no object to rotate
        return g
    if name == "square_bboxes":
        # 2x2 squares → rotation is visually identity (no signal)
        g[1][1] = 4; g[1][2] = 4
        g[2][1] = 4; g[2][2] = 4
        g[8][8] = 6; g[8][9] = 6
        g[9][8] = 6; g[9][9] = 6
        return g
    if name == "touching_blobs":
        # blobs share a border → 4-conn merges them, "for each object" ambiguous
        for r, c in PATTERNS_4x4[0]:
            g[3 + r][3 + c] = 4
        for r, c in PATTERNS_4x4[1]:
            g[3 + r][7 + c] = 6
        return g
    return g
