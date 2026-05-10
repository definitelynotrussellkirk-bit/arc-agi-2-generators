"""Generator for arc_puzzle_bank_tenth_21_bundle:easy_70_expand_diagonal_pairs_into_xs.

Two opposite 3x3-box corners expand into a full X.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_pairs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, single_endpoint, axis_aligned.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "74e83caa0660"
VERSION = "1.1.0"
TASK_ID = "74e83caa0660"

SUMMARY = "Two opposite 3x3-box corners expand into a full X."

INVARIANTS = [
    "background is 0",
    "each active color appears exactly twice",
    "the two cells are opposite corners of a 3x3 box",
    "output draws both diagonals of that box",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "single_endpoint", "axis_aligned")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "5..20"},
    "grid_w":         {"type": "int", "default": "rng 10..14", "valid": "5..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pairs":        {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "3x3_corner_pairs",
                       "valid": "3x3_corner_pairs"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 11)
        target = ctx.draw_int("pairs", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 13, 14)
        target = ctx.draw_int("pairs", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 10, 14)
        target = ctx.draw_int("pairs", 2, 4)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    colors = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(colors)
    used: set[tuple[int, int]] = set()
    placed = 0
    for color in colors:
        if placed >= target:
            break
        for _ in range(120):
            r0 = rng.randint(0, h - 3)
            c0 = rng.randint(0, w - 3)
            corners = [(r0, c0), (r0 + 2, c0 + 2)]
            if rng.randrange(2):
                corners = [(r0, c0 + 2), (r0 + 2, c0)]
            box = {(r, c) for r in range(r0, r0 + 3) for c in range(c0, c0 + 3)}
            if box & used:
                continue
            for r, c in corners:
                g[r][c] = color
            used.update(box)
            placed += 1
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # blank → no diagonal pairs to expand into Xs
        return g
    if name == "single_endpoint":
        # 1 cell per color → can't form pair, no X to draw
        g[2][2] = 4
        g[5][7] = 6
        return g
    if name == "axis_aligned":
        # 2 cells in same row → not 3x3 corners, rule won't fire
        g[3][1] = 4; g[3][7] = 4
        return g
    return g
