"""Generator for arc_additional_puzzle_bank_volume13:M88.

Rule: wall chambers containing exactly one 1-4 seed are filled with
that seed color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_chambers,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_seed, conflicting_seeds, no_chambers.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "9e6e338d0ca7"
VERSION = "1.1.0"
TASK_ID = "9e6e338d0ca7"
SUMMARY = "Wall chambers containing exactly one 1-4 seed are filled with that seed color."

INVARIANTS = [
    "background is 0",
    "gray cells form closed chamber boundaries",
    "one chamber contains exactly one seed color from 1 through 4",
    "at least one chamber has no qualifying seed and remains blank",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_seed", "conflicting_seeds", "no_chambers")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..13", "valid": "6..24"},
    "grid_w":         {"type": "int", "default": "rng 9..15", "valid": "7..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_chambers":     {"type": "int", "default": "2", "valid": "2"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "framed_split",
                       "valid": "framed_split"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
    "density":        {"type": "str", "default": "1_seed", "valid": "1_seed"},
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
        w = ctx.draw_int("grid_w", 9, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 13, 15)
    else:
        h = ctx.draw_int("grid_h", 8, 13)
        w = ctx.draw_int("grid_w", 9, 15)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    for r in range(h):
        g[r][0] = 5
        g[r][w - 1] = 5
    for c in range(w):
        g[0][c] = 5
        g[h - 1][c] = 5
    wall = rng.randint(3, w - 4)
    for r in range(1, h - 1):
        g[r][wall] = 5
    color = rng.choice([1, 2, 3, 4])
    g[rng.randint(1, h - 2)][rng.randint(1, wall - 1)] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    for r in range(h):
        g[r][0] = 5; g[r][w - 1] = 5
    for c in range(w):
        g[0][c] = 5; g[h - 1][c] = 5
    wall = 5
    for r in range(1, h - 1):
        g[r][wall] = 5
    if name == "no_seed":
        # neither chamber has a seed → no chamber qualifies for fill
        return g
    if name == "conflicting_seeds":
        # one chamber has 2 different seed colors → fill color ambiguous
        g[2][2] = 1; g[5][3] = 3
        g[2][7] = 4
        return g
    if name == "no_chambers":
        # remove the divider → just one big region, "chamber" partition is trivial
        for r in range(1, h - 1):
            g[r][wall] = 0
        g[3][3] = 2
        return g
    return g
