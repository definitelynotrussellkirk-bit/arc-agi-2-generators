"""Generator for arc_additional_puzzle_bank_volume11:M75 — pack by descending area.

Rule: colored objects are cropped and packed left-to-right by
descending area.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_objects,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_objects, single_object, tied_areas.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "843e122e2e8a"
VERSION = "1.1.0"
TASK_ID = "843e122e2e8a"
SUMMARY = "Colored objects are cropped and packed left to right by descending area."

INVARIANTS = [
    "background is 0",
    "non-background objects are separated connected components",
    "object areas are distinct",
    "objects use stable simple shapes whose crops are nonempty",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_objects", "single_object", "tied_areas")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..14", "valid": "6..24"},
    "grid_w":         {"type": "int", "default": "rng 11..16", "valid": "6..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_objects":      {"type": "int", "default": "3", "valid": "3..3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "diagonal_distinct_areas",
                       "valid": "diagonal_distinct_areas"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
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
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 14)
        w = ctx.draw_int("grid_w", 15, 16)
    else:
        h = ctx.draw_int("grid_h", 10, 14)
        w = ctx.draw_int("grid_w", 11, 16)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    top = rng.randint(0, h - 8)
    left = rng.randint(0, w - 10)
    specs = [
        (2, [(top, left), (top, left + 1), (top + 1, left)]),
        (3, [(top + 3, left + 3), (top + 3, left + 4), (top + 4, left + 3), (top + 4, left + 4)]),
        (6, [(top + 6, left + 6), (top + 6, left + 7), (top + 6, left + 8),
             (top + 7, left + 6), (top + 7, left + 7), (top + 7, left + 8)]),
    ]
    rng.shuffle(specs)
    for color, cells in specs:
        for r, c in cells:
            g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 13
    g = full_grid(h, w, 0)
    if name == "no_objects":
        # blank → nothing to pack
        return g
    if name == "single_object":
        # only one object → packing is trivially identity
        for r, c in [(2, 2), (2, 3), (3, 2), (3, 3)]:
            g[r][c] = 4
        return g
    if name == "tied_areas":
        # two objects with equal area → "descending area" ambiguous
        for r, c in [(2, 2), (2, 3), (3, 2)]: g[r][c] = 3
        for r, c in [(6, 7), (6, 8), (7, 7)]: g[r][c] = 6
        return g
    return g
