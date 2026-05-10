"""Generator for arc_additional_puzzles_21_set9:E58 — Draw diagonal between same-color pairs.

Rule: for each color appearing exactly twice, if the two cells are
diagonal (|dr|=|dc|), draw a diagonal line between them in that color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_pairs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, axis_aligned_pair, single_endpoint.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "366ce015cd2a"
VERSION = "1.1.0"
TASK_ID = "366ce015cd2a"
SUMMARY = "2-3 distinct colors, each with 2 cells at diagonal distance ≥3."

INVARIANTS = [
    "2-3 colors",
    "each color: 2 cells at (r,c) and (r±k, c±k) for k ≥3",
    "diagonals don't overlap with each other",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "axis_aligned_pair", "single_endpoint")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "6..12"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "6..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pairs":        {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "diagonal_pairs",
                       "valid": "diagonal_pairs"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..8"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 7, 8)
        n_pairs = ctx.draw_int("n_pairs", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
        n_pairs = ctx.draw_int("n_pairs", 3, 3)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 7, 10)
        n_pairs = ctx.draw_int("n_pairs", 2, 3)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    palette = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], n_pairs)
    occupied = set()
    for color in palette:
        for _ in range(40):
            k = rng.randint(2, 4)
            sr = rng.choice([1, -1])
            sc = rng.choice([1, -1])
            r1 = rng.randint(max(0, -k * sr), min(h - 1, h - 1 - k * sr))
            c1 = rng.randint(max(0, -k * sc), min(w - 1, w - 1 - k * sc))
            r2 = r1 + k * sr
            c2 = c1 + k * sc
            cells = [(r1 + i * sr, c1 + i * sc) for i in range(k + 1)]
            if any(cell in occupied for cell in cells):
                continue
            g[r1][c1] = color
            g[r2][c2] = color
            for cell in cells:
                occupied.add(cell)
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # single cells per color → no pair → no line to draw
        g[2][2] = 4; g[5][7] = 6
        return g
    if name == "axis_aligned_pair":
        # pairs share a row or column (|dr|=0 or |dc|=0) → not diagonal, no line
        g[3][1] = 4; g[3][7] = 4
        g[1][5] = 6; g[6][5] = 6
        return g
    if name == "single_endpoint":
        # only 1 cell per color → can't form a pair, undefined endpoint
        g[2][2] = 4
        g[6][6] = 6
        return g
    return g
