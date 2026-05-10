"""Generator for arc_puzzle_bank_21_set2:S2_E2.

Rule: the uniquely smallest green component is recolored magenta.

Combinatorial axes (8): grid_h, grid_w, palette_kind, small_size, n_large,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_components, tied_smallest, all_same_size.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.place import place_no_overlap

GENERATOR_ID = "04e2ffe8dc8e"
VERSION = "1.1.0"
TASK_ID = "04e2ffe8dc8e"

SUMMARY = "The uniquely smallest green component is recolored magenta."

INVARIANTS = [
    "background is 0",
    "all objects are green",
    "exactly one green component has the smallest size",
    "larger green components remain green",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_components", "tied_smallest", "all_same_size")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "6..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "small_size":     {"type": "choice", "default": "rng 1|2", "valid": "1|2"},
    "n_large":        {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..2"},
    "position_bias":  {"type": "str", "default": "smallest_plus_distractors",
                       "valid": "smallest_plus_distractors"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SMALL = {
    1: [(0, 0)],
    2: [(0, 0), (0, 1)],
}

_LARGE = [
    [(0, 0), (0, 1), (0, 2)],
    [(0, 0), (0, 1), (1, 1)],
    [(0, 0), (0, 1), (1, 0), (1, 1)],
    [(0, 0), (1, 0), (2, 0), (2, 1)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 9, 12)
    small_size = ctx.draw_choice("small_size", [1, 2])
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    if place_no_overlap(rng, g, _SMALL[small_size], 3, padding=1, max_tries=400) is None:
        raise ValueError("could not place smallest component")
    for _ in range(rng.randint(2, 3)):
        if place_no_overlap(rng, g, rng.choice(_LARGE), 3, padding=1, max_tries=400) is None:
            raise ValueError("could not place larger green component")
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 11
    g = full_grid(h, w, 0)
    if name == "no_components":
        # blank → no green components, rule has no smallest
        return g
    if name == "tied_smallest":
        # two components of equal smallest size → ambiguous which to recolor
        g[1][1] = 3
        g[5][5] = 3  # both 1-cell singletons
        for (r, c) in [(7, 7), (7, 8), (8, 7), (8, 8)]: g[r][c] = 3
        return g
    if name == "all_same_size":
        # all components share the same size → rule's "smallest" is ambiguous
        for (r, c) in [(1, 1), (1, 2)]: g[r][c] = 3
        for (r, c) in [(5, 4), (5, 5)]: g[r][c] = 3
        for (r, c) in [(8, 8), (8, 9)]: g[r][c] = 3
        return g
    return g
