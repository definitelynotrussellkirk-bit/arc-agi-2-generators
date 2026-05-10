"""Generator for arc_puzzle_bank_21_set3:S3_E1.

Rule: singleton blue components recolor red; larger blue objects remain.

Combinatorial axes (8): grid_h, grid_w, palette_kind, singleton_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: only_singletons, only_big, no_blobs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.place import place_no_overlap

GENERATOR_ID = "410fb6b72f16"
VERSION = "1.1.0"
TASK_ID = "410fb6b72f16"
SUMMARY = "Singleton blue components recolor red while larger blue objects remain."

INVARIANTS = [
    "background is 0",
    "all input objects are blue",
    "at least one component is a singleton",
    "at least one component has size greater than one",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("only_singletons", "only_big", "no_blobs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "singleton_count": {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..2"},
    "position_bias":  {"type": "str", "default": "singletons_plus_big",
                       "valid": "singletons_plus_big"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_BIG = [
    [(0, 0), (0, 1)],
    [(0, 0), (1, 0), (2, 0)],
    [(0, 0), (0, 1), (1, 0), (1, 1)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
        singleton_count = ctx.draw_int("singleton_count", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
        singleton_count = ctx.draw_int("singleton_count", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 8, 11)
        singleton_count = ctx.draw_int("singleton_count", 2, 4)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    for _ in range(singleton_count):
        if place_no_overlap(rng, g, [(0, 0)], 1, padding=1, max_tries=300) is None:
            raise ValueError("could not place singleton")
    for _ in range(rng.randint(1, 2)):
        if place_no_overlap(rng, g, rng.choice(_BIG), 1, padding=1, max_tries=300) is None:
            raise ValueError("could not place larger object")
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "only_singletons":
        # all components singletons → all recolored to red, no big-blob contrast
        g[1][1] = 1; g[3][5] = 1; g[5][2] = 1; g[6][8] = 1
        return g
    if name == "only_big":
        # only multi-cell blobs → no singletons, rule is identity
        for (r, c) in [(1, 1), (1, 2), (2, 1), (2, 2)]: g[r][c] = 1
        for (r, c) in [(5, 5), (5, 6), (6, 5)]: g[r][c] = 1
        return g
    if name == "no_blobs":
        # blank grid → no blue cells, rule fires zero times
        return g
    return g
