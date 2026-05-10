"""Generator for arc_puzzle_bank_ninth_21_bundle:easy_59_drop_single_object_to_floor.

Rule: a single connected object falls to the bottom of the grid.

Combinatorial axes (8): grid_h, grid_w, palette_kind, shape_idx,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_object, object_on_floor, multiple_objects.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c84e2a641055"
VERSION = "1.1.0"
TASK_ID = "c84e2a641055"

SUMMARY = "A single connected object starts above the bottom and drops to the floor."

INVARIANTS = [
    "background is 0",
    "there is exactly one connected nonzero object",
    "the object does not initially touch the bottom row",
    "the object shape is preserved by a downward translation",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_object", "object_on_floor", "multiple_objects")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "5..18"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "5..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "shape_idx":      {"type": "int", "default": "rng 0..3", "valid": "0..3"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..2"},
    "position_bias":  {"type": "str", "default": "object_above_floor",
                       "valid": "object_above_floor"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_SHAPES = [
    [(0, 0), (0, 1), (1, 0), (2, 0)],
    [(0, 0), (0, 1), (0, 2), (1, 1)],
    [(0, 1), (1, 0), (1, 1), (2, 1)],
    [(0, 0), (1, 0), (1, 1), (1, 2)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 7, 10)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    shape = rng.choice(_SHAPES)
    sh = max(r for r, _ in shape) + 1
    sw = max(c for _, c in shape) + 1
    top = rng.randint(0, h - sh - 1)
    left = rng.randint(0, w - sw)
    color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    for dr, dc in shape:
        g[top + dr][left + dc] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 8
    g = full_grid(h, w, 0)
    if name == "no_object":
        # blank → no object to drop, rule has no effect
        return g
    if name == "object_on_floor":
        # object already touches bottom row → rule is identity (no further drop possible)
        for (r, c) in [(h - 1, 2), (h - 1, 3), (h - 2, 2)]: g[r][c] = 4
        return g
    if name == "multiple_objects":
        # two separated objects → rule's "single object" predicate fails
        for (r, c) in [(1, 1), (1, 2), (2, 1)]: g[r][c] = 4
        for (r, c) in [(3, 5), (3, 6), (4, 6)]: g[r][c] = 6
        return g
    return g
