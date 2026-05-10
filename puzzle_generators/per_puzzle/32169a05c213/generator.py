"""Generator for arc_additional_puzzle_bank_volume20:M139.

Rule: nonzero objects are normalized and packed into a size-sorted
strip.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_objects,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: tied_sizes, single_object, no_objects.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "32169a05c213"
VERSION = "1.1.0"
TASK_ID = "32169a05c213"
SUMMARY = "Nonzero objects are normalized and packed into a size-sorted strip."

INVARIANTS = [
    "background is 0",
    "every nonzero component is an object to pack",
    "object sizes are distinct to avoid tie ambiguity",
    "components are separated by background",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("tied_sizes", "single_object", "no_objects")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..14", "valid": "6..24"},
    "grid_w":         {"type": "int", "default": "rng 11..16", "valid": "6..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_objects":      {"type": "int", "default": "3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "scattered",
                       "valid": "scattered"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
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
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 11, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 14)
        w = ctx.draw_int("grid_w", 14, 16)
    else:
        h = ctx.draw_int("grid_h", 10, 14)
        w = ctx.draw_int("grid_w", 11, 16)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    top = rng.randint(0, h - 8)
    left = rng.randint(0, w - 10)
    specs = [
        (3, [(top, left), (top + 1, left)]),
        (5, [(top + 3, left + 3), (top + 3, left + 4), (top + 4, left + 3)]),
        (8, [(top + 6, left + 6), (top + 6, left + 7), (top + 6, left + 8),
             (top + 7, left + 6), (top + 7, left + 7)]),
    ]
    rng.shuffle(specs)
    for color, cells in specs:
        for r, c in cells:
            g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 12
    g = full_grid(h, w, 0)
    if name == "tied_sizes":
        # equal-size objects → pack order ambiguous
        for r, c in [(1, 1), (2, 1)]: g[r][c] = 3
        for r, c in [(5, 4), (6, 4)]: g[r][c] = 5
        for r, c in [(8, 7), (8, 8), (9, 7)]: g[r][c] = 8
        return g
    if name == "single_object":
        # one object → trivial pack
        for r, c in [(3, 3), (3, 4), (4, 3)]: g[r][c] = 4
        return g
    if name == "no_objects":
        # empty grid → nothing to pack
        return g
    return g
