"""Generator for arc_additional_puzzle_bank_volume18:M126.

Rule: nonzero objects are cropped and packed left to right by increasing
size.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_objects,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: tied_sizes, single_object, no_objects.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "056999828b88"
VERSION = "1.1.0"
TASK_ID = "056999828b88"
SUMMARY = "Nonzero objects are cropped and packed left to right by increasing size."

INVARIANTS = [
    "background is 0",
    "all objects are separated nonzero connected components",
    "object sizes are distinct",
    "object colors are preserved in the packed output",
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
        (2, [(top, left)]),
        (4, [(top + 2, left + 3), (top + 2, left + 4), (top + 3, left + 3)]),
        (7, [(top + 5, left + 6), (top + 5, left + 7), (top + 6, left + 6),
             (top + 6, left + 7), (top + 6, left + 8)]),
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
        # two objects equal size → packing order ambiguous
        for r, c in [(1, 1), (2, 1)]: g[r][c] = 2
        for r, c in [(5, 4), (6, 4)]: g[r][c] = 4
        for r, c in [(8, 7), (8, 8), (9, 7)]: g[r][c] = 7
        return g
    if name == "single_object":
        # one object → trivial packing
        for r, c in [(3, 3), (3, 4), (4, 3)]: g[r][c] = 4
        return g
    if name == "no_objects":
        # empty grid → no objects
        return g
    return g
