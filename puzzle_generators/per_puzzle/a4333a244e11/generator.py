"""Generator for arc_puzzle_bank_21_set6_s:S6_H5 — Voronoi fill from two seeds in 8-frame.

Rule: inside an 8-frame, two colored seeds induce a Manhattan-distance
Voronoi fill. Ties remain black.

Combinatorial axes (8): grid_h, grid_w, palette_kind, frame_h,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_frame, no_seeds, single_seed.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a4333a244e11"
VERSION = "1.1.0"
TASK_ID = "a4333a244e11"
SUMMARY = "Fill the interior of an 8-frame by nearest of two colored seeds."

INVARIANTS = [
    "color 8 is the rectangular frame",
    "there are exactly two non-8 colored seeds inside the frame",
    "empty interior cells choose the nearest seed by Manhattan distance",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frame", "no_seeds", "single_seed")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..12"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "frame_h":        {"type": "int", "default": "rng 6..8", "valid": "5..10"},
    "frame_w":        {"type": "int", "default": "rng 8..11", "valid": "6..14"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "frame_with_two_seeds",
                       "valid": "frame_with_two_seeds"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _draw_frame(g, top, left, bottom, right):
    for c in range(left, right + 1):
        g[top][c] = 8
        g[bottom][c] = 8
    for r in range(top, bottom + 1):
        g[r][left] = 8
        g[r][right] = 8


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        fh = ctx.draw_int("frame_h", 6, 6)
        fw = ctx.draw_int("frame_w", 8, 9)
    elif difficulty == "hard":
        fh = ctx.draw_int("frame_h", 7, 8)
        fw = ctx.draw_int("frame_w", 10, 11)
    else:
        fh = ctx.draw_int("frame_h", 6, 8)
        fw = ctx.draw_int("frame_w", 8, 11)
    h = fh + 2
    w = fw + 2
    g = full_grid(h, w, 0)
    _draw_frame(g, 1, 1, fh, fw)
    seed_a = (rng.randint(2, fh - 1), rng.randint(2, max(2, fw // 2)))
    seed_b = (rng.randint(2, fh - 1), rng.randint(max(3, fw // 2 + 1), fw - 1))
    g[seed_a[0]][seed_a[1]] = 2
    g[seed_b[0]][seed_b[1]] = 3
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 12
    g = full_grid(h, w, 0)
    if name == "no_frame":
        # seeds but no 8-frame → no interior to Voronoi-partition
        g[3][3] = 2
        g[5][8] = 3
        return g
    if name == "no_seeds":
        # frame but no seeds → no Voronoi partition possible
        _draw_frame(g, 1, 1, 7, 10)
        return g
    if name == "single_seed":
        # only one seed inside frame → entire interior is "nearest" to that seed
        _draw_frame(g, 1, 1, 7, 10)
        g[4][5] = 2
        return g
    return g
