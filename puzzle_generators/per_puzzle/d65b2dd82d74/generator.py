"""Generator for arc_puzzle_bank_21_set4:S4_M2 — fill between parallel bars.

Rule: each color forms two parallel vertical bars; fill the rectangular
region between them (inclusive) with that color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_pairs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, single_bar, adjacent_bars.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d65b2dd82d74"
VERSION = "1.1.0"
TASK_ID = "d65b2dd82d74"
SUMMARY = "1-2 colors each forming two parallel vertical bars (same row range)."

INVARIANTS = [
    "background is 0",
    "each non-zero color forms 2 vertical bars at distinct cols, same row range",
    "different colors don't share rows or cols",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "single_bar", "adjacent_bars")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pairs":        {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "rng 1..2", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "parallel_vertical_bars",
                       "valid": "parallel_vertical_bars"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..2", "valid": "1..9"},
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
        w = ctx.draw_int("grid_w", 10, 11)
        n = ctx.draw_int("n_pairs", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 12, 13)
        n = ctx.draw_int("n_pairs", 2, 2)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 10, 13)
        n = ctx.draw_int("n_pairs", 1, 2)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], n)
    used_rows: set[int] = set()
    used_cols: set[int] = set()
    for color in palette:
        for _ in range(40):
            r1 = rng.randint(0, h - 4)
            r2 = rng.randint(r1 + 2, min(h - 1, r1 + 5))
            if any(r in used_rows for r in range(r1, r2 + 1)):
                continue
            c1 = rng.randint(1, w // 2 - 1)
            c2 = rng.randint(c1 + 2, min(w - 2, c1 + 4))
            if c1 in used_cols or c2 in used_cols:
                continue
            for r in range(r1, r2 + 1):
                g[r][c1] = color
                g[r][c2] = color
            for r in range(r1, r2 + 1):
                used_rows.add(r)
            used_cols.add(c1); used_cols.add(c2)
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 11
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # blank → no bars to fill between
        return g
    if name == "single_bar":
        # only one bar per color → no second bar to define the fill region
        for r in range(2, 6): g[r][3] = 4
        return g
    if name == "adjacent_bars":
        # bars are adjacent (gap=0) → no interior region between them
        for r in range(2, 6):
            g[r][3] = 4
            g[r][4] = 4
        return g
    return g
