"""Generator for arc_puzzle_bank_21_set10_s:S10_E5 — Keep only blobs not touching border.

Rule: 4-connected non-bg blobs touching the border are erased; interior
blobs survive at their original color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_border_blobs, no_interior_blobs, all_border.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "899e2a4cfac9"
VERSION = "1.1.0"
TASK_ID = "899e2a4cfac9"
SUMMARY = "Mix of border-touching and interior blobs in distinct colors."

INVARIANTS = [
    "≥2 blobs touching the grid border",
    "≥2 blobs fully interior (will survive)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_border_blobs", "no_interior_blobs", "all_border")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "4", "valid": "2..6"},
    "palette_size":   {"type": "int", "default": "4", "valid": "2..6"},
    "position_bias":  {"type": "str", "default": "border_plus_interior_mix",
                       "valid": "border_plus_interior_mix"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "2..6"},
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
        h = ctx.draw_int("grid_h", 7, 7)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 8, 10)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    pal = rng.sample([2, 3, 4, 5, 6, 7, 8, 9], 4)
    L = [(0, 0), (1, 0), (1, 1)]
    sq = [(0, 0), (0, 1), (1, 0), (1, 1)]
    bar2 = [(0, 0), (1, 0)]
    paint_at(g, 0, rng.randint(0, w - 3), bar2, pal[0])
    paint_at(g, h - 2, w - 2, bar2, pal[1])
    paint_at(g, rng.randint(2, 3), rng.randint(2, w - 5), L, pal[2])
    paint_at(g, rng.randint(3, h - 3), rng.randint(w - 5, w - 4), L, pal[3])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    L = [(0, 0), (1, 0), (1, 1)]
    if name == "no_border_blobs":
        # only interior blobs → rule fires zero times, output identical to input
        paint_at(g, 2, 3, [(0, 0), (0, 1), (1, 0), (1, 1)], 4)
        paint_at(g, 5, 5, L, 6)
        return g
    if name == "no_interior_blobs":
        # only border-touching blobs → rule erases everything, output blank
        paint_at(g, 0, 1, [(0, 0), (1, 0)], 4)
        paint_at(g, h - 2, w - 2, [(0, 0), (1, 0)], 6)
        paint_at(g, 3, 0, [(0, 0), (1, 0)], 3)
        return g
    if name == "all_border":
        # every blob touches border → output blank, weakly tests rule
        paint_at(g, 0, 1, [(0, 0), (0, 1)], 4)
        paint_at(g, 0, 5, [(0, 0), (0, 1)], 6)
        paint_at(g, h - 1, 2, [(0, 0), (0, 1)], 3)
        return g
    return g
