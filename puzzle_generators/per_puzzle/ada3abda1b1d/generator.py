"""Generator for arc_puzzle_bank_21_set5_e:easy_e03.

Rule: keep only cells whose color appears exactly twice.

Combinatorial axes (8): grid_h, grid_w, palette_kind, kept_colors,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, all_pairs, all_singletons.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ada3abda1b1d"
VERSION = "1.1.0"
TASK_ID = "ada3abda1b1d"
SUMMARY = "Keep only cells whose color appears exactly twice."

INVARIANTS = [
    "background is 0",
    "at least one color appears exactly twice",
    "at least one distractor color appears once or at least three times",
    "output keeps exact-two colors and erases all others",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "all_pairs", "all_singletons")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..12"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "kept_colors":    {"type": "int", "default": "rng 1..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "rng 4..6", "valid": "2..9"},
    "position_bias":  {"type": "str", "default": "scattered", "valid": "scattered"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..6", "valid": "2..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _place(g, rng, color, count):
    h, w = len(g), len(g[0])
    cells = [(r, c) for r in range(h) for c in range(w) if g[r][c] == 0]
    for r, c in rng.sample(cells, count):
        g[r][c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 5, 5)
        w = ctx.draw_int("grid_w", 7, 8)
        kept = ctx.draw_int("kept_colors", 1, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 9, 10)
        kept = ctx.draw_int("kept_colors", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 7, 10)
        kept = ctx.draw_int("kept_colors", 1, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], kept + 3)
    for color in palette[:kept]:
        _place(g, rng, color, 2)
    for color in palette[kept:]:
        _place(g, rng, color, rng.choice([1, 3, 4]))
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 8
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # no color appears exactly twice → output is all zeros, rule erases everything
        for r, c, v in [(1, 1, 3), (2, 4, 4), (3, 6, 5), (4, 2, 6)]:
            g[r][c] = v
        for r, c in [(0, 0), (0, 5), (5, 7)]:
            g[r][c] = 7
        return g
    if name == "all_pairs":
        # every color appears exactly twice → output equals input, rule is identity
        for color, cells in [(3, [(1, 1), (4, 6)]), (4, [(2, 3), (3, 5)]),
                              (5, [(0, 4), (5, 0)])]:
            for r, c in cells:
                g[r][c] = color
        return g
    if name == "all_singletons":
        # every color appears once → output is all zeros, rule erases everything
        for r, c, v in [(1, 1, 3), (2, 4, 4), (3, 6, 5), (4, 2, 6), (0, 5, 7), (5, 7, 8)]:
            g[r][c] = v
        return g
    return g
