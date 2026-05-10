"""Generator for arc_puzzle_bank_21_set24_s:S24_E3.

Rule: a row reports the maximum onion depth of each component.

Combinatorial axes (8): grid_h, grid_w, palette_kind, object_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_objects, single_object, all_unit_depth.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2c4efc97c37d"
VERSION = "1.1.0"
TASK_ID = "2c4efc97c37d"
SUMMARY = "A row reports the maximum onion depth of each component."

INVARIANTS = [
    "background is 0",
    "components are separated solid rectangles",
    "component reading order is stable by left edge then top edge",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_objects", "single_object", "all_unit_depth")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "7..18"},
    "grid_w":         {"type": "int", "default": "rng 16..20", "valid": "10..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "object_count":   {"type": "int", "default": "rng 3..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 3..4", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "left_to_right_packed",
                       "valid": "left_to_right_packed"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..4", "valid": "1..8"},
    "density":        {"type": "str", "default": "rectangles", "valid": "rectangles"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 16, 17)
        count = ctx.draw_int("object_count", 3, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 18, 20)
        count = ctx.draw_int("object_count", 4, 4)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 16, 20)
        count = ctx.draw_int("object_count", 3, 4)
    rng = ctx.draw_rng("layout")
    grid = full_grid(h, w, 0)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8], count)
    col = 0
    for i, color in enumerate(colors):
        rh = rng.randint(3, min(7, h - 2))
        rw = rng.randint(3, 6)
        if col + rw > w:
            break
        r0 = rng.randint(0, h - rh)
        for r in range(r0, r0 + rh):
            for c in range(col, col + rw):
                grid[r][c] = color
        col += rw + rng.randint(2, 3)
    return grid


def _draw_from_degenerate(name, rng):
    h, w = 10, 18
    g = full_grid(h, w, 0)
    if name == "no_objects":
        # empty grid → no components, depth report empty
        return g
    if name == "single_object":
        # one component → trivial single-entry report
        for r in range(2, 6):
            for c in range(2, 6):
                g[r][c] = 4
        return g
    if name == "all_unit_depth":
        # all components are 1×1 → onion depth uniformly 1, no contrast
        for r, c in [(2, 2), (3, 5), (5, 8), (4, 12)]: g[r][c] = (r + c) % 8 + 1
        return g
    return g
