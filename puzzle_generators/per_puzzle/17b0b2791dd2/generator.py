"""Generator for arc_puzzle_bank_21_set2:S2_E1.

Rule: exact 3-cell vertical blue bars recolor red; horizontal bars stay blue.

Combinatorial axes (8): grid_h, grid_w, palette_kind, vertical_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: only_horizontal, only_vertical, no_bars.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.place import place_no_overlap

GENERATOR_ID = "17b0b2791dd2"
VERSION = "1.1.0"
TASK_ID = "17b0b2791dd2"
SUMMARY = "Exact 3-cell vertical blue bars recolor red; horizontal bars stay blue."

INVARIANTS = [
    "background is 0",
    "all input objects are blue",
    "at least one object is exactly a vertical length-3 line",
    "horizontal blue bars are present as distractors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("only_horizontal", "only_vertical", "no_bars")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "vertical_count": {"type": "int", "default": "rng 1..3", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "vertical_plus_horizontal_bars",
                       "valid": "vertical_plus_horizontal_bars"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_VERTICAL = [(0, 0), (1, 0), (2, 0)]
_HORIZONTAL = [(0, 0), (0, 1), (0, 2)]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
        vertical_count = ctx.draw_int("vertical_count", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
        vertical_count = ctx.draw_int("vertical_count", 2, 3)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 8, 11)
        vertical_count = ctx.draw_int("vertical_count", 1, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    shapes = [_VERTICAL for _ in range(vertical_count)]
    shapes.extend(_HORIZONTAL for _ in range(rng.randint(1, 2)))
    rng.shuffle(shapes)
    for cells in shapes:
        if place_no_overlap(rng, g, cells, 1, padding=1, max_tries=400) is None:
            raise ValueError("could not place blue bar")
    return g


def _draw_from_degenerate(name, rng):
    from puzzle_generators.helpers.grid import paint_at
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "only_horizontal":
        # only horizontal bars → no vertical to recolor, rule is identity
        paint_at(g, 1, 1, _HORIZONTAL, 1)
        paint_at(g, 4, 5, _HORIZONTAL, 1)
        return g
    if name == "only_vertical":
        # only vertical bars → all recolored to red, no contrast against horizontal stays-blue
        paint_at(g, 1, 1, _VERTICAL, 1)
        paint_at(g, 5, 6, _VERTICAL, 1)
        return g
    if name == "no_bars":
        # blank grid → no bars to inspect, rule is identity
        return g
    return g
