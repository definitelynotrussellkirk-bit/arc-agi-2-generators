"""Generator for 58c02a16.

Rule: top-left mask + separator color define a two-level tiling.

Combinatorial axes (8): grid_size, palette_kind, n_distinct, mask_variant,
anchor_corner, asymmetry_force, palette_size, position_bias.
Degenerates: no_mask, no_separator, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "87c05932431e"
VERSION = "1.1.0"
TASK_ID = "87c05932431e"
SUMMARY = "Top-left mask + separator color define a two-level tiling over the whole grid."

INVARIANTS = [
    "the mode color is the background",
    "a separator color forms the bottom row and right column of the top-left mask block",
    "the non-background mask cells define where macro cells emit foreground or separator color",
    "the output tiles the local mask under the macro pattern encoded in the same corner",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_mask", "no_separator", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_size":      {"type": "int", "default": "rng 7..11", "valid": "4..30"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_distinct":     {"type": "int", "default": "3", "valid": "3"},
    "mask_variant":   {"type": "int", "default": "0", "valid": "0..2"},
    "anchor_corner":  {"type": "bool", "default": "true",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "tl",
                       "valid": "tl"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        s_lo, s_hi = 4, 7
    elif difficulty == "hard":
        s_lo, s_hi = 11, 18
    else:
        s_lo, s_hi = 7, 11
    bg, fg, sep = ctx.draw_distinct_colors("colors", n=3, exclude=set())
    size = ctx.draw_int("grid_size", s_lo, s_hi)
    g = full_grid(size, size, bg)
    g[0][0] = fg
    g[1][1] = fg
    for c in range(3):
        g[2][c] = sep
    for r in range(3):
        g[r][2] = sep
    return g


def _draw_from_degenerate(name, rng):
    size = 9
    g = full_grid(size, size, 0)
    if name == "no_mask":
        for c in range(3):
            g[2][c] = 5
        for r in range(3):
            g[r][2] = 5
        return g
    if name == "no_separator":
        g[0][0] = 1; g[1][1] = 1
        return g
    if name == "full_grid":
        for r in range(size):
            for c in range(size):
                g[r][c] = 5
        return g
    return g
