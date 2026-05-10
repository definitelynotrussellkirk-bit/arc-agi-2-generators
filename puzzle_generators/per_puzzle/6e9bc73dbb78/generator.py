"""Generator for arc_puzzle_bank_21_set3:S3_E7.

The only color with a single connected component is recolored yellow.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_repeat,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_unique, all_unique, no_components.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.place import place_no_overlap

GENERATOR_ID = "6e9bc73dbb78"
VERSION = "1.1.0"
TASK_ID = "6e9bc73dbb78"

SUMMARY = "The only color with a single connected component is recolored yellow."

INVARIANTS = [
    "background is 0",
    "one nonzero color appears in exactly one component",
    "another nonzero color appears in multiple components",
    "the unique-color component is not already yellow",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_unique", "all_unique", "no_components")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_repeat":       {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "unique_plus_repeated",
                       "valid": "unique_plus_repeated"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = [
    [(0, 0), (0, 1)],
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (1, 0), (1, 1)],
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
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 12)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    unique_color = rng.choice([2, 3, 5, 6, 7, 8, 9])
    repeat_color = rng.choice([c for c in [1, 2, 3, 5, 6, 7, 8, 9] if c != unique_color])
    if place_no_overlap(rng, g, rng.choice(_SHAPES), unique_color, padding=1, max_tries=400) is None:
        raise ValueError("could not place unique-color component")
    for _ in range(rng.randint(2, 3)):
        if place_no_overlap(rng, g, rng.choice(_SHAPES), repeat_color, padding=1, max_tries=400) is None:
            raise ValueError("could not place repeated-color component")
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_unique":
        # all colors have 2+ components → no color satisfies "exactly one component"
        for r, c in [(1, 1), (1, 2)]: g[r][c] = 4
        for r, c in [(4, 5), (5, 5)]: g[r][c] = 4
        for r, c in [(7, 7), (7, 8)]: g[r][c] = 6
        for r, c in [(2, 7), (3, 7)]: g[r][c] = 6
        return g
    if name == "all_unique":
        # every color has exactly one component → ambiguous winner
        for r, c in [(1, 1), (1, 2)]: g[r][c] = 4
        for r, c in [(4, 5), (5, 5)]: g[r][c] = 6
        for r, c in [(7, 7), (7, 8)]: g[r][c] = 7
        return g
    if name == "no_components":
        # blank → no nonzero components at all
        return g
    return g
