"""Generator for arc_puzzle_bank_21_set2:S2_E6.

Rule: yellow L-triominoes recolor green; straight yellow bars remain.

Combinatorial axes (8): grid_h, grid_w, palette_kind, l_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: only_lines, only_Ls, single_object.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.place import place_no_overlap
from puzzle_generators.helpers.shape import L_TROMINOES

GENERATOR_ID = "42ed09bd039d"
VERSION = "1.1.0"
TASK_ID = "42ed09bd039d"
SUMMARY = "Yellow L-triominoes recolor green while straight yellow bars remain."

INVARIANTS = [
    "background is 0",
    "all input objects are yellow and have size 3",
    "some objects are L-triominoes",
    "straight length-3 bars remain yellow",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("only_lines", "only_Ls", "single_object")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "5..15"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "5..15"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "l_count":        {"type": "int", "default": "rng 1..3", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..2"},
    "position_bias":  {"type": "str", "default": "L_plus_lines",
                       "valid": "L_plus_lines"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_LINES = [
    [(0, 0), (0, 1), (0, 2)],
    [(0, 0), (1, 0), (2, 0)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 9, 10)
        l_count = ctx.draw_int("l_count", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 11, 12)
        l_count = ctx.draw_int("l_count", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 9, 12)
        l_count = ctx.draw_int("l_count", 1, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    shapes = [rng.choice(L_TROMINOES) for _ in range(l_count)]
    shapes.extend(rng.choice(_LINES) for _ in range(rng.randint(1, 2)))
    rng.shuffle(shapes)
    for cells in shapes:
        if place_no_overlap(rng, g, cells, 4, padding=1, max_tries=400) is None:
            raise ValueError("could not place yellow triomino")
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "only_lines":
        # only straight bars → no L → no recolor → output equals input
        paint_at(g, 1, 1, _LINES[0], 4)   # horizontal
        paint_at(g, 5, 5, _LINES[1], 4)   # vertical
        return g
    if name == "only_Ls":
        # only L-triominoes → all become green; no comparison/contrast against bars
        paint_at(g, 1, 1, L_TROMINOES[0], 4)
        paint_at(g, 5, 5, L_TROMINOES[1], 4)
        return g
    if name == "single_object":
        # one shape only → no contrast between L-recolor and line-keep
        paint_at(g, 3, 3, L_TROMINOES[0], 4)
        return g
    return g
