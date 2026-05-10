"""Generator for arc_puzzle_bank_21_set2:S2_M7 — diagonal corner rect fill.

Rule: each color appearing exactly twice → fill the bbox between those
two cells (treated as opposite corners) with that color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_pairs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, collinear_pair, single_color_only.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a2156a5a4d26"
VERSION = "1.1.0"
TASK_ID = "a2156a5a4d26"
SUMMARY = "2-3 colors, each appearing exactly twice with diagonal bbox; rects don't overlap."

INVARIANTS = [
    "background is 0",
    "each non-zero color appears exactly twice",
    "the two cells of each color define a diagonal (different rows AND cols)",
    "filled bboxes don't overlap each other",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "collinear_pair", "single_color_only")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pairs":        {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "diagonal_corner_pairs",
                       "valid": "diagonal_corner_pairs"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..9"},
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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 10, 13)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    n = rng.randint(2, 3)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], n)
    reserved: set[tuple[int, int]] = set()
    for color in palette:
        for _ in range(60):
            r1 = rng.randint(0, h - 3)
            c1 = rng.randint(0, w - 3)
            r2 = rng.randint(r1 + 2, min(h - 1, r1 + 4))
            c2 = rng.randint(c1 + 2, min(w - 1, c1 + 4))
            cells = {(r, c) for r in range(r1, r2 + 1) for c in range(c1, c2 + 1)}
            if cells & reserved:
                continue
            if rng.random() < 0.5:
                g[r1][c1] = color
                g[r2][c2] = color
            else:
                g[r1][c2] = color
                g[r2][c1] = color
            reserved |= cells
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 11
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # blank → no colors with two cells, rule has no rectangles to fill
        return g
    if name == "collinear_pair":
        # both cells same row → degenerate rect (zero height), rule undefined
        g[2][1] = 4; g[2][5] = 4
        g[5][2] = 6; g[5][7] = 6
        return g
    if name == "single_color_only":
        # only one color appears twice → output has just one rectangle
        g[2][2] = 4
        g[6][7] = 4
        return g
    return g
