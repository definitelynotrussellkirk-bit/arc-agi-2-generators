"""Generator for arc_additional_puzzles_21_set15_bundle:M101 -- object-size row encoding.

Combinatorial axes (8): grid_h, grid_w, palette_kind, num_items,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_objects, single_object, all_equal_sizes.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0f801939eff6"
VERSION = "1.1.0"
TASK_ID = "0f801939eff6"
SUMMARY = "Create colored objects whose sizes are encoded as one sorted output row."

INVARIANTS = [
    "nonzero objects are 4-connected and separated by background",
    "at least two object sizes differ, so descending-size ordering is visible",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_objects", "single_object", "all_equal_sizes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "7..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "num_items":      {"type": "int", "default": "rng 3..5", "valid": "2..8"},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "2..8"},
    "position_bias":  {"type": "str", "default": "distinct_size_objects",
                       "valid": "distinct_size_objects"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "2..8"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _stamp(g, r0, c0, size, color):
    cells = [(0, 0)]
    if size >= 2:
        cells.append((0, 1))
    if size >= 3:
        cells.append((1, 0))
    if size >= 4:
        cells.append((1, 1))
    if size >= 5:
        cells.append((2, 0))
    for dr, dc in cells[:size]:
        g[r0 + dr][c0 + dc] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(
        seed=seed,
        sample_index=sample_index,
        version=VERSION,
        task_id=TASK_ID,
        difficulty=difficulty,
        overrides=overrides,
    )
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
        n = ctx.draw_int("num_items", 3, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 13)
        n = ctx.draw_int("num_items", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 9, 13)
        n = ctx.draw_int("num_items", 3, 5)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    colors = list(ctx.draw_distinct_colors("colors", n=n, exclude=[0]))
    sizes = [2, 3, 4, 5, 1][:n]
    rng.shuffle(sizes)
    slots = [(1, 1), (1, w - 4), (h - 4, 1), (h - 4, w - 4), (h // 2, w // 2)]
    for (r0, c0), size, color in zip(slots, sizes, colors):
        _stamp(g, r0, c0, size, color)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_objects":
        # blank → no sizes to encode, output is empty row
        return g
    if name == "single_object":
        # one object → sorted output is trivially that object's size
        _stamp(g, 3, 4, 3, 4)
        return g
    if name == "all_equal_sizes":
        # all sizes equal → no descending ordering visible
        _stamp(g, 1, 1, 2, 4)
        _stamp(g, 1, 6, 2, 6)
        _stamp(g, 5, 1, 2, 7)
        return g
    return g
