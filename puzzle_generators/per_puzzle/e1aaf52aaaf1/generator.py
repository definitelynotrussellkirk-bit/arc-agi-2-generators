"""Generator for arc_puzzle_bank_21_set6_s:S6_E5.

Rule: among several green components, the unique odd-area component
recolors blue.

Combinatorial axes (8): grid_h, grid_w, palette_kind, component_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: all_even_areas, all_odd_areas, single_component.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.place import place_no_overlap

GENERATOR_ID = "e1aaf52aaaf1"
VERSION = "1.1.0"
TASK_ID = "e1aaf52aaaf1"
SUMMARY = "Among several green components, the unique odd-area component recolors blue."

INVARIANTS = [
    "background is 0",
    "all input objects are color 3",
    "exactly one component has odd area",
    "the other components have even area",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("all_even_areas", "all_odd_areas", "single_component")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "7..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "component_count": {"type": "int", "default": "rng 3..4", "valid": "2..6"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "scattered", "valid": "scattered"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_ODD_SHAPES = [
    [(0, 0), (0, 1), (0, 2)],
    [(0, 0), (1, 0), (1, 1)],
    [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
]

_EVEN_SHAPES = [
    [(0, 0), (0, 1), (1, 0), (1, 1)],
    [(0, 0), (0, 1)],
    [(0, 0), (1, 0), (2, 0), (3, 0)],
    [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 9, 10)
        count = ctx.draw_int("component_count", 3, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 12, 13)
        count = ctx.draw_int("component_count", 4, 4)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 9, 13)
        count = ctx.draw_int("component_count", 3, 4)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    shapes = [rng.choice(_ODD_SHAPES)]
    shapes.extend(rng.choice(_EVEN_SHAPES) for _ in range(count - 1))
    rng.shuffle(shapes)
    for cells in shapes:
        if place_no_overlap(rng, g, cells, 3, padding=1, max_tries=300) is None:
            raise ValueError("could not place component")
    return g


def _draw_from_degenerate(name, rng):
    import random
    rng = random.Random(0)
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "all_even_areas":
        # all components have even area → no unique odd-area component, rule has no target
        shapes = [_EVEN_SHAPES[0], _EVEN_SHAPES[1], _EVEN_SHAPES[2]]
        for cells in shapes:
            place_no_overlap(rng, g, cells, 3, padding=1, max_tries=300)
        return g
    if name == "all_odd_areas":
        # all components have odd area → multiple "odd" components, ambiguous which to recolor
        for cells in [_ODD_SHAPES[0], _ODD_SHAPES[1], _ODD_SHAPES[2]]:
            place_no_overlap(rng, g, cells, 3, padding=1, max_tries=300)
        return g
    if name == "single_component":
        # one component → trivially the unique odd (if odd) or no odd (if even), rule degenerate
        place_no_overlap(rng, g, _ODD_SHAPES[1], 3, padding=1, max_tries=300)
        return g
    return g
