"""Generator for arc_puzzle_bank_21_set14_bundle:easy_n07.

Several nonzero colors appear, with one strict majority. The solver keeps only
that majority color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, majority_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_majority, single_color, all_minority.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e4e80c9fad18"
VERSION = "1.1.0"
TASK_ID = "e4e80c9fad18"
SUMMARY = "Multicolor sparse grids with a unique nonzero majority color."

INVARIANTS = [
    "background is 0",
    "at least two nonzero colors appear",
    "one nonzero color has strictly highest frequency",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_majority", "single_color", "all_minority")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "4..12"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "majority_count": {"type": "int", "default": "rng 6..10", "valid": "2..30"},
    "palette_size":   {"type": "int", "default": "3", "valid": "2..5"},
    "position_bias":  {"type": "str", "default": "scattered_majority",
                       "valid": "scattered_majority"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "2..5"},
    "density":        {"type": "str", "default": "scattered", "valid": "scattered"},
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
        w = ctx.draw_int("grid_w", 8, 9)
        majority_count = ctx.draw_int("majority_count", 5, 7)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 11, 12)
        majority_count = ctx.draw_int("majority_count", 9, 12)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 8, 12)
        majority_count = ctx.draw_int("majority_count", 6, 10)
    colors = ctx.draw_distinct_colors("colors", n=3, exclude={0})
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    positions = [(r, c) for r in range(h) for c in range(w)]
    rng.shuffle(positions)
    counts = [majority_count, rng.randint(1, 3), rng.randint(1, 3)]
    idx = 0
    for color, count in zip(colors, counts):
        for r, c in positions[idx:idx + count]:
            g[r][c] = color
        idx += count
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_majority":
        # all colors tied → ambiguous which color to keep
        for (r, c) in [(1, 1), (2, 3), (3, 5)]: g[r][c] = 4
        for (r, c) in [(4, 1), (5, 3), (6, 5)]: g[r][c] = 6
        for (r, c) in [(1, 7), (2, 8), (3, 9)]: g[r][c] = 3
        return g
    if name == "single_color":
        # only one nonzero color → "majority" is trivial, rule is identity
        for (r, c) in [(1, 1), (2, 3), (3, 5), (4, 7), (5, 2)]: g[r][c] = 4
        return g
    if name == "all_minority":
        # all colors appear exactly once → no majority defined
        for (r, c, v) in [(1, 1, 4), (2, 3, 6), (3, 5, 3), (4, 7, 8)]: g[r][c] = v
        return g
    return g
