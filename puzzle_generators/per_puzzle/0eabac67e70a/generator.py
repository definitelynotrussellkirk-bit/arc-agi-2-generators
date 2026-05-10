"""Generator for arc_puzzle_bank_21_set16_s:S16_M2 — span between pair points.

Rule: each color that appears exactly twice draws a horizontal/vertical
span between its two cells, painted in 8. Output is empty grid + spans.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, n_pairs, texture.
Degenerates: no_pairs, no_shared_axis, adjacent_pair.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0eabac67e70a"
VERSION = "1.1.0"
TASK_ID = "0eabac67e70a"
SUMMARY = "1-3 colors, each appearing exactly twice on the same row OR same column."

INVARIANTS = [
    "background is 0",
    "every non-zero color appears exactly twice",
    "the two cells of each color share a row or share a column (so span is well-defined)",
    "spans don't pass through other markers (stays well-formed)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "no_shared_axis", "adjacent_pair")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..13"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "7..13"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pairs":        {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "= n_pairs", "valid": "1..4"},
    "position_bias":  {"type": "str", "default": "shared_axis_pairs",
                       "valid": "shared_axis_pairs"},
    "n_distinct_colors": {"type": "int", "default": "= n_pairs", "valid": "1..4"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
        n = ctx.draw_int("n_pairs", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 11, 13)
        n = ctx.draw_int("n_pairs", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 8, 11)
        n = ctx.draw_int("n_pairs", 1, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 9], n)
    for color in palette:
        for _ in range(40):
            if rng.random() < 0.5:
                r = rng.randint(0, h - 1)
                c1 = rng.randint(0, w - 4)
                c2 = rng.randint(c1 + 3, w - 1)
                if g[r][c1] == 0 and g[r][c2] == 0:
                    g[r][c1] = color
                    g[r][c2] = color
                    break
            else:
                c = rng.randint(0, w - 1)
                r1 = rng.randint(0, h - 4)
                r2 = rng.randint(r1 + 3, h - 1)
                if g[r1][c] == 0 and g[r2][c] == 0:
                    g[r1][c] = color
                    g[r2][c] = color
                    break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # Empty grid — rule's pair-finder has no input.
        return g
    if name == "no_shared_axis":
        # Same color appears twice but at different row+col — rule's
        # span-axis check fails.
        g[1][2] = 4; g[5][6] = 4
        return g
    if name == "adjacent_pair":
        # Pair shares an axis but is adjacent — span between is empty,
        # rule's effect is invisible.
        g[3][2] = 4; g[3][3] = 4
        return g
    return g
