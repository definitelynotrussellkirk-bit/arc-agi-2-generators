"""Generator for arc_additional_puzzle_bank_volume12:M82 — L-path between same-color pairs.

Rule: matching color pairs are joined by row-first L-shaped paths.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_pairs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, same_row_pair, single_endpoint.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "3065bdeaa7b0"
VERSION = "1.1.0"
TASK_ID = "3065bdeaa7b0"
SUMMARY = "Matching color pairs are joined by row-first L-shaped paths."

INVARIANTS = [
    "background is 0",
    "each active color appears exactly twice",
    "endpoint pairs are offset in both row and column",
    "generated L-paths are separated from other endpoint pairs",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "same_row_pair", "single_endpoint")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..14", "valid": "5..24"},
    "grid_w":         {"type": "int", "default": "rng 9..14", "valid": "5..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pairs":        {"type": "int", "default": "rng 1..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "rng 1..3", "valid": "1..5"},
    "position_bias":  {"type": "str", "default": "lpath_color_pairs",
                       "valid": "lpath_color_pairs"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..3", "valid": "1..5"},
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
        w = ctx.draw_int("grid_w", 9, 10)
        n_pairs = ctx.draw_int("n_pairs", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 14)
        w = ctx.draw_int("grid_w", 12, 14)
        n_pairs = ctx.draw_int("n_pairs", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 9, 14)
        w = ctx.draw_int("grid_w", 9, 14)
        n_pairs = ctx.draw_int("n_pairs", 1, 3)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    colors = list(range(1, 10))
    rng.shuffle(colors)
    rows = list(range(1, h - 2, 3))
    for i, r1 in enumerate(rows[:n_pairs]):
        color = colors[i]
        r2 = min(h - 1, r1 + rng.randint(1, 2))
        c1 = rng.randint(0, max(0, w // 3 - 1))
        c2 = rng.randint((2 * w) // 3, w - 1)
        g[r1][c1] = color
        g[r2][c2] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 11
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # singletons only → no pair to L-connect
        g[2][1] = 4
        g[5][7] = 6
        g[8][3] = 3
        return g
    if name == "same_row_pair":
        # endpoints share row → no row-then-col offset, L-path collapses to a straight line
        g[3][1] = 4; g[3][8] = 4   # same row (no row offset)
        g[7][2] = 6; g[7][9] = 6   # same row
        return g
    if name == "single_endpoint":
        # one color has only 1 endpoint → "matching pair" precondition fails
        g[2][1] = 4; g[5][8] = 4   # proper pair
        g[7][3] = 6                # singleton (no partner)
        return g
    return g
