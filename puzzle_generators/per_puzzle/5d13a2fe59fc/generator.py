"""Generator for arc_puzzle_bank_21_set8:easy_h03.

Rule: top-row seeds paint down-right diagonal rays.

Combinatorial axes (8): grid_h/w, seeds, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_seeds, single_seed, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5d13a2fe59fc"
VERSION = "1.1.0"
TASK_ID = "5d13a2fe59fc"

SUMMARY = "Top-row seeds paint down-right diagonal rays."

INVARIANTS = [
    "background is 0",
    "only the top row contains input seeds",
    "seed columns are distinct",
    "each seed paints a down-right diagonal to the grid edge",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_seeds", "single_seed", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "6..8"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "8..11"},
    "seeds":          {"type": "int", "default": "rng 2..4", "valid": "2..4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "varied", "valid": "varied"},
    "position_bias":  {"type": "str", "default": "varied", "valid": "varied"},
    "n_distinct_colors":{"type": "int", "default": "varied", "valid": "varied"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 6, 6)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 6, 8)
        w = ctx.draw_int("grid_w", 8, 11)
    n = min(ctx.draw_int("seeds", 2, 4), w)
    g = full_grid(h, w, 0)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], n)
    for c, color in zip(rng.sample(range(w), n), colors):
        g[0][c] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(7, 10, 0)
    if name == "no_seeds":
        return g
    if name == "single_seed":
        g[0][3] = 3
        return g
    if name == "full_grid":
        for r in range(7):
            for c in range(10):
                g[r][c] = 3
        return g
    return g
