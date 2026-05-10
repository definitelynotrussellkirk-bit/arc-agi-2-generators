"""Generator for set12:E78 — Sort objects by size desc, pack horizontally with 1-col gaps.

Rule: sort objects by size desc, then h asc, then w asc, then color asc.
Output: pack sorted objects from left in their original orientation,
separated by 1-col gaps.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_shapes,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_objects, all_same_size, single_object.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.shape import RING_3X3
from puzzle_generators.helpers.place import place_no_overlap

GENERATOR_ID = "0ff4b77946cc"
VERSION = "1.1.0"
TASK_ID = "0ff4b77946cc"
SUMMARY = "Random h×w grid with 3-4 distinct-shape, distinct-color, distinct-size objects."

INVARIANTS = [
    "3-4 connected objects of distinct sizes",
    "each object has a distinct color",
    "objects don't touch",
    "total packed width fits within w",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_objects", "all_same_size", "single_object")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "7..16"},
    "grid_w":         {"type": "int", "default": "rng 11..14", "valid": "10..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_shapes":       {"type": "int", "default": "rng 3..4", "valid": "2..6"},
    "palette_size":   {"type": "int", "default": "= n_shapes", "valid": "2..6"},
    "position_bias":  {"type": "str", "default": "scattered_distinct_sizes",
                       "valid": "scattered_distinct_sizes"},
    "n_distinct_colors": {"type": "int", "default": "= n_shapes", "valid": "2..6"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_SHAPES = [
    [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)],
    RING_3X3,
    [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 1)],
    [(0, 0), (0, 1), (1, 1)],
    [(0, 0)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 16)
        w = ctx.draw_int("grid_w", 14, 18)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 11, 14)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    n_shapes = rng.randint(3, 4)
    sizes_pool = sorted({len(s) for s in _SHAPES}, reverse=True)
    chosen_sizes = sorted(rng.sample(sizes_pool, n_shapes), reverse=True)
    chosen_shapes = [rng.choice([s for s in _SHAPES if len(s) == sz])
                     for sz in chosen_sizes]
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], n_shapes)
    for i, shape in enumerate(chosen_shapes):
        place_no_overlap(rng, g, shape, palette[i], padding=1, max_tries=40)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 12
    g = full_grid(h, w, 0)
    if name == "no_objects":
        # Empty grid — rule has nothing to sort or pack.
        return g
    if name == "all_same_size":
        # All objects are the same size — rule's primary sort key
        # (size desc) doesn't break ties, sort becomes ambiguous.
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[1 + dr][1 + dc] = 4
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[5 + dr][6 + dc] = 6
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[1 + dr][8 + dc] = 7
        return g
    if name == "single_object":
        # Just one object — sort is trivial, no multi-object pack
        # evidence is shown.
        for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            g[3 + dr][4 + dc] = 5
        return g
    return g
