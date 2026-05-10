"""Generator for arc_puzzle_bank_third21:E15.

Rule: a zero cell with matching nonzero up/down/left/right neighbors is
filled with that neighbor color (plus-arms → fill center).

Combinatorial axes (8): grid_h/w, palette_kind, n_pluses,
palette_size, position_bias, n_distinct_colors, plus_density, texture.
Degenerates: no_pluses, plus_arms_mismatched, plus_already_filled.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "68176b5eb124"
VERSION = "1.1.0"
TASK_ID = "68176b5eb124"
SUMMARY = "A zero cell with matching nonzero up/down/left/right neighbors is filled."

INVARIANTS = [
    "plus arms share one color",
    "plus centers begin as zero",
    "pluses are separated",
]

PALETTE_KINDS = ("default", "single_plus", "spread_pluses", "rainbow")
DEGENERATE_TEXTURES = ("no_pluses", "plus_arms_mismatched", "plus_already_filled")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pluses":       {"type": "int", "default": "rng 1..3", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "8", "valid": "8"},
    "position_bias":  {"type": "str", "default": "grid_aligned",
                       "valid": "grid_aligned"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..3",
                          "valid": "1..8"},
    "plus_density":   {"type": "str", "default": "medium",
                       "valid": "sparse|medium|dense"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 7, 10)
    n = ctx.draw_int("n_pluses", 1, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    centers = [(r, c) for r in range(1, h - 1, 3) for c in range(1, w - 1, 3)]
    rng.shuffle(centers)
    for i, (r, c) in enumerate(centers[:n]):
        color = (i % 8) + 1
        g[r - 1][c] = color
        g[r + 1][c] = color
        g[r][c - 1] = color
        g[r][c + 1] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "no_pluses":
        # scattered cells without plus pattern — rule fills nothing
        g[1][1] = 5
        g[3][5] = 7
        return g
    if name == "plus_arms_mismatched":
        # plus arms have different colors — center remains 0 (no match)
        g[0][3] = 4; g[2][3] = 5; g[1][2] = 6; g[1][4] = 7
        return g
    if name == "plus_already_filled":
        # plus center already nonzero — rule no-op for that plus
        g[0][3] = 5; g[2][3] = 5; g[1][2] = 5; g[1][4] = 5
        g[1][3] = 5
        return g
    return g
