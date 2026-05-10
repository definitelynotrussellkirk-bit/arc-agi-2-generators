"""Generator for arc_puzzle_bank_21_set13_bundle:easy_m05.

The grid has exactly two nonzero colors with unequal frequencies. The rarer
color is recolored to the more frequent color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, dominant_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: monochrome, equal_freq, three_colors.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "73ab3e5ab7dc"
VERSION = "1.1.0"
TASK_ID = "73ab3e5ab7dc"
SUMMARY = "Two nonzero colors with a strict frequency winner and loser."

INVARIANTS = [
    "background is 0",
    "exactly two nonzero colors appear",
    "one color appears strictly more often than the other",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("monochrome", "equal_freq", "three_colors")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "4..12"},
    "grid_w":         {"type": "int", "default": "rng 7..11", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "dominant_count": {"type": "int", "default": "rng 4..8", "valid": "2..20"},
    "rare_count":     {"type": "int", "default": "rng 1..3", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "two_colors_unequal_freq",
                       "valid": "two_colors_unequal_freq"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
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
        w = ctx.draw_int("grid_w", 7, 9)
        dominant_count = ctx.draw_int("dominant_count", 4, 5)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 11)
        dominant_count = ctx.draw_int("dominant_count", 6, 8)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 7, 11)
        dominant_count = ctx.draw_int("dominant_count", 4, 8)
    rare_count = min(ctx.draw_int("rare_count", 1, 3), dominant_count - 1)
    dominant, rare = ctx.draw_distinct_colors("colors", n=2, exclude={0})
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    positions = [(r, c) for r in range(h) for c in range(w)]
    rng.shuffle(positions)
    for r, c in positions[:dominant_count]:
        g[r][c] = dominant
    for r, c in positions[dominant_count:dominant_count + rare_count]:
        g[r][c] = rare
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 9
    g = full_grid(h, w, 0)
    if name == "monochrome":
        # only one nonzero color → no rare color to recolor
        for r, c in [(1, 1), (1, 2), (3, 4), (5, 6)]:
            g[r][c] = 4
        return g
    if name == "equal_freq":
        # two colors at equal frequency → no winner/loser
        for r, c in [(1, 1), (2, 3), (4, 5)]:
            g[r][c] = 4
        for r, c in [(0, 0), (3, 7), (5, 2)]:
            g[r][c] = 6
        return g
    if name == "three_colors":
        # three nonzero colors → "exactly two" precondition fails
        for r, c in [(1, 1), (2, 3), (4, 5)]:
            g[r][c] = 4
        for r, c in [(0, 0), (3, 7)]:
            g[r][c] = 6
        for r, c in [(5, 2)]:
            g[r][c] = 7
        return g
    return g
