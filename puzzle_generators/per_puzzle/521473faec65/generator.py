"""Generator for arc_puzzle_bank_21_set12_bundle:easy_l03.

Rule: each filled (solid) rect blob in g — output cells where
(r-r1+c-c1) is even = blob color; odd = 0.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_rects,
palette_size, position_bias, n_distinct_colors, rect_aspect, texture.
Degenerates: no_rects, hollow_rect, rects_touching.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect

GENERATOR_ID = "521473faec65"
VERSION = "1.1.0"
TASK_ID = "521473faec65"
SUMMARY = "2-3 solid rectangle blobs in distinct colors."

INVARIANTS = [
    "≥2 solid rectangles, ≥2x2 each",
    "rectangles don't touch",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_rects", "hollow_rect", "rects_touching")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_rects":        {"type": "int", "default": "2", "valid": "2..3"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "2..8"},
    "position_bias":  {"type": "str", "default": "corners", "valid": "corners"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "2..8"},
    "rect_aspect":    {"type": "str", "default": "rng", "valid": "rng"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 9, 11)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    pal = rng.sample([2, 3, 4, 5, 6, 7, 8, 9], 3)
    rh1 = rng.randint(2, 3); rw1 = rng.randint(2, 4)
    draw_rect(g, 1, 1, rh1, rw1, pal[0])
    rh2 = rng.randint(2, 3); rw2 = rng.randint(2, 3)
    draw_rect(g, h - rh2 - 1, w - rw2 - 1, rh2, rw2, pal[1])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_rects":
        # empty grid — rule has no blob to checkerboard
        return g
    if name == "hollow_rect":
        # outline only (not solid) → predicate "solid rect" fails
        for c in range(1, 6):
            g[1][c] = 4; g[3][c] = 4
        for r in range(1, 4):
            g[r][1] = 4; g[r][5] = 4
        return g
    if name == "rects_touching":
        # two rects sharing a border → component-detection merges them
        draw_rect(g, 1, 1, 2, 3, 4)
        draw_rect(g, 1, 4, 2, 3, 6)
        return g
    return g
