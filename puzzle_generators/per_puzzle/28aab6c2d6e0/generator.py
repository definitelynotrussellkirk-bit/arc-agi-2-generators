"""Generator for v1_e_m_h_keys:M2 — complete each L-tromino to a 2x2 square.

Rule: each connected 3-cell L-tromino has its missing 4th corner
filled with the same color, forming a 2x2 square.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_objs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: already_2x2, non_l_shapes, no_objects.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.shape import L_TROMINOES
from puzzle_generators.helpers.palette import random_palette
from puzzle_generators.helpers.blobs import bbox_overlaps

GENERATOR_ID = "28aab6c2d6e0"
VERSION = "1.1.0"
TASK_ID = "28aab6c2d6e0"
SUMMARY = "1-2 L-trominoes in distinct colors, separated."

INVARIANTS = [
    "background is 0",
    "1-2 L-trominoes (3 cells in a 2x2 bbox), each a distinct non-bg color",
    "trominoes don't touch each other",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("already_2x2", "non_l_shapes", "no_objects")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_objs":         {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "position_bias":  {"type": "str", "default": "scattered", "valid": "scattered"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..2", "valid": "1..3"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 7, 8)
        n = ctx.draw_int("n_objs", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
        n = ctx.draw_int("n_objs", 2, 2)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 7, 10)
        n = ctx.draw_int("n_objs", 1, 2)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = list(random_palette(rng, n))
    placed: list[tuple[int, int, int, int]] = []
    for color in palette:
        shape = list(rng.choice(L_TROMINOES))
        for _ in range(80):
            r0 = rng.randint(0, h - 2)
            c0 = rng.randint(0, w - 2)
            bb_pad = (r0 - 1, c0 - 1, r0 + 2, c0 + 2)
            if any(bbox_overlaps(bb_pad, p) for p in placed): continue
            paint_at(g, r0, c0, shape, color)
            placed.append((r0, c0, r0 + 1, c0 + 1))
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 9
    g = full_grid(h, w, 0)
    if name == "already_2x2":
        # blobs already complete 2x2 squares → "missing 4th corner" never matches, rule no-op
        for r in range(1, 3):
            for c in range(1, 3):
                g[r][c] = 4
        for r in range(4, 6):
            for c in range(5, 7):
                g[r][c] = 6
        return g
    if name == "non_l_shapes":
        # blobs are non-L shapes (1x3 lines, single cells, etc.) → not L-trominoes, rule no-op
        for c in range(1, 4):
            g[2][c] = 4
        g[5][3] = 6
        return g
    if name == "no_objects":
        # empty grid → no L-trominoes, rule no-op
        return g
    return g
