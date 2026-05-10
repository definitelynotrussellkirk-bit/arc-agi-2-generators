"""Generator for arc_puzzle_bank_next21:H13.

Rule: each hollow object contributes its enclosed hole pattern,
recolored by the object color. Hole patterns are packed left-to-right
by source object column.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_objects,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: solid_objects, single_object, no_objects.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "4e05481a2c21"
VERSION = "1.1.0"
TASK_ID = "4e05481a2c21"
SUMMARY = "Hollow objects provide colored hole patterns packed horizontally."

INVARIANTS = [
    "all foreground objects are hollow enough to enclose background holes",
    "objects are separated and ordered by their left column",
    "hole patterns are non-empty",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("solid_objects", "single_object", "no_objects")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "10", "valid": "10"},
    "grid_w":         {"type": "int", "default": "20", "valid": "20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_objects":      {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "position_bias":  {"type": "str", "default": "row_aligned",
                       "valid": "row_aligned"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..4"},
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
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        n_objects = ctx.draw_int("n_objects", 2, 2)
    elif difficulty == "hard":
        n_objects = ctx.draw_int("n_objects", 3, 3)
    else:
        n_objects = ctx.draw_int("n_objects", 2, 3)
    g = full_grid(10, 20, 0)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], n_objects)
    origins = [(1, 1), (1, 8), (1, 14)]
    sizes = [(5, 5), (6, 5), (5, 6)]
    for i in range(n_objects):
        r0, c0 = origins[i]
        h, w = sizes[i]
        draw_frame(g, r0, c0, r0 + h - 1, c0 + w - 1, colors[i])
        if h > 5:
            g[r0 + 2][c0 + 2] = 0
        if w > 5:
            g[r0 + 2][c0 + 3] = 0
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 20, 0)
    if name == "solid_objects":
        # solid (non-hollow) objects → no hole pattern to extract
        for r in range(1, 6):
            for c in range(1, 6):
                g[r][c] = 4
        for r in range(1, 6):
            for c in range(8, 13):
                g[r][c] = 6
        return g
    if name == "single_object":
        # one hollow object → no horizontal packing comparison
        draw_frame(g, 2, 5, 6, 9, 4)
        return g
    if name == "no_objects":
        # empty grid → nothing to extract or pack
        return g
    return g
