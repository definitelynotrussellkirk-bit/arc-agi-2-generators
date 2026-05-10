"""Generator for arc_puzzle_bank_21_set8_s:S8_H2.

A small nonzero 2D tile repeats across the full grid, except for one rectangular
zero hole that the rule repairs from the surrounding periodic pattern.

Combinatorial axes (8): grid_h, grid_w, palette_kind, tile_w,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_hole, no_periodicity, multiple_holes.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "54b040e4bd08"
VERSION = "1.1.0"
TASK_ID = "54b040e4bd08"
SUMMARY = "Recover a 2D periodic tile and fill one zero rectangle hole."

INVARIANTS = [
    "the intact cells follow a 2x2 or 2x3 nonzero tile",
    "one rectangular region is replaced by zeros",
    "the missing region is strictly inside the grid",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_hole", "no_periodicity", "multiple_holes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "6..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "tile_w":         {"type": "int", "default": "rng 2|3", "valid": "2 or 3"},
    "palette_size":   {"type": "int", "default": "rng 4..6", "valid": "4..6"},
    "position_bias":  {"type": "str", "default": "periodic_with_hole",
                       "valid": "periodic_with_hole"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..6", "valid": "4..6"},
    "density":        {"type": "str", "default": "dense", "valid": "dense"},
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
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 12)
    tw = ctx.draw_choice("tile_w", [2, 3])
    colors = rng.sample([2, 3, 4, 5, 6, 7, 8, 9], 2 * tw)
    tile = [colors[:tw], colors[tw:]]
    g = full_grid(h, w, 0)
    for r in range(h):
        for c in range(w):
            g[r][c] = tile[r % 2][c % tw]
    hole_h = rng.randint(2, 3)
    hole_w = rng.randint(3, 4)
    top = rng.randint(2, h - hole_h - 1)
    left = rng.randint(2, w - hole_w - 1)
    for r in range(top, top + hole_h):
        for c in range(left, left + hole_w):
            g[r][c] = 0
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_hole":
        # full periodic tile with no hole → rule has nothing to fill
        tile = [[2, 3], [4, 5]]
        for r in range(h):
            for c in range(w):
                g[r][c] = tile[r % 2][c % 2]
        return g
    if name == "no_periodicity":
        # random non-periodic content → rule cannot infer the tile
        for r in range(h):
            for c in range(w):
                g[r][c] = ((r * 7 + c * 11) % 8) + 2
        for r in range(3, 5):
            for c in range(4, 7):
                g[r][c] = 0  # hole, but no period to fill from
        return g
    if name == "multiple_holes":
        # multiple disjoint holes → rule's "one hole" precondition fails
        tile = [[2, 3], [4, 5]]
        for r in range(h):
            for c in range(w):
                g[r][c] = tile[r % 2][c % 2]
        for r in range(2, 4):
            for c in range(2, 4):
                g[r][c] = 0
        for r in range(5, 7):
            for c in range(6, 8):
                g[r][c] = 0
        return g
    return g
