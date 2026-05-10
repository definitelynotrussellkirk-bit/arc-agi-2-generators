"""Generator for arc_puzzle_bank_21_set3:S3_E5 — horizontal gray dominoes recolor cyan.

Rule: horizontal gray dominoes recolor cyan; vertical and longer gray
objects stay gray.

Combinatorial axes (8): grid_h, grid_w, palette_kind, domino_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_dominoes, all_dominoes, vertical_dominoes_only.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.place import place_no_overlap

GENERATOR_ID = "e46c2557ad08"
VERSION = "1.1.0"
TASK_ID = "e46c2557ad08"

SUMMARY = "Horizontal gray dominoes recolor cyan; vertical and longer gray objects stay gray."

INVARIANTS = [
    "background is 0",
    "all objects are gray",
    "at least one object is a horizontal 1x2 domino",
    "non-horizontal-domino gray objects remain gray",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_dominoes", "all_dominoes", "vertical_dominoes_only")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "domino_count":   {"type": "int", "default": "rng 1..3", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "h_dominoes_with_distractors",
                       "valid": "h_dominoes_with_distractors"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_H_DOMINO = [(0, 0), (0, 1)]
_OTHER = [
    [(0, 0), (1, 0)],
    [(0, 0), (0, 1), (0, 2)],
    [(0, 0), (1, 0), (2, 0)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
        domino_count = ctx.draw_int("domino_count", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
        domino_count = ctx.draw_int("domino_count", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 12)
        domino_count = ctx.draw_int("domino_count", 1, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    shapes = [_H_DOMINO for _ in range(domino_count)]
    shapes.extend(rng.choice(_OTHER) for _ in range(rng.randint(1, 2)))
    rng.shuffle(shapes)
    for cells in shapes:
        if place_no_overlap(rng, g, cells, 5, padding=1, max_tries=400) is None:
            raise ValueError("could not place gray object")
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_dominoes":
        # only non-domino gray objects → rule has nothing to recolor
        for r, c in [(1, 1), (2, 1)]:        g[r][c] = 5  # vertical pair
        for r, c in [(5, 5), (5, 6), (5, 7)]: g[r][c] = 5  # h-tromino (length 3)
        return g
    if name == "all_dominoes":
        # only horizontal dominoes → no distractor stays gray (no contrast)
        g[1][1] = 5; g[1][2] = 5
        g[3][5] = 5; g[3][6] = 5
        g[6][3] = 5; g[6][4] = 5
        return g
    if name == "vertical_dominoes_only":
        # all dominoes are vertical → none satisfy the "horizontal" precondition
        g[1][1] = 5; g[2][1] = 5
        g[1][5] = 5; g[2][5] = 5
        g[5][8] = 5; g[6][8] = 5
        return g
    return g
