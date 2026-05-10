"""Generator for arc_additional_puzzles_21_set11_bundle:E72 — Bbox outline from each color.

Rule: for each non-bg color, find the bbox of its cells and draw the
rectangle outline in that color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_colors,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_colors, single_cell_per_color, collinear_cells.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a452b4b4f04a"
VERSION = "1.1.0"
TASK_ID = "a452b4b4f04a"
SUMMARY = "1-3 distinct colors, each with 2-3 cells forming a non-degenerate bbox."

INVARIANTS = [
    "1-3 colors",
    "each color's bbox is ≥3×3",
    "cells per color: ≥2 corners",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_colors", "single_cell_per_color", "collinear_cells")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_colors":       {"type": "int", "default": "rng 2..3", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..3"},
    "position_bias":  {"type": "str", "default": "non_degenerate_bboxes",
                       "valid": "non_degenerate_bboxes"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..3"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 8, 12)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    n_colors = rng.randint(2, 3)
    palette = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], n_colors)
    occupied = [[False] * w for _ in range(h)]
    for color in palette:
        for _ in range(40):
            r1 = rng.randint(0, h - 4); c1 = rng.randint(0, w - 4)
            r2 = rng.randint(r1 + 2, min(h - 1, r1 + 5))
            c2 = rng.randint(c1 + 2, min(w - 1, c1 + 5))
            if any(occupied[rr][cc] for rr in range(r1, r2 + 1) for cc in range(c1, c2 + 1)):
                continue
            for rr in range(r1, r2 + 1):
                for cc in range(c1, c2 + 1):
                    occupied[rr][cc] = True
            g[r1][c1] = color
            g[r2][c2] = color
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    if name == "no_colors":
        # blank → no colors, no bboxes to outline
        return g
    if name == "single_cell_per_color":
        # each color has 1 cell → degenerate 1×1 bbox, no outline
        g[1][1] = 4
        g[5][5] = 6
        return g
    if name == "collinear_cells":
        # cells in a single row → 1xN bbox, no rectangular outline
        g[3][1] = 4; g[3][5] = 4
        g[6][2] = 6; g[6][7] = 6
        return g
    return g
