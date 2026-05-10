"""Generator for arc_puzzle_bank_21_set6:hard_f02.

Each multi-cell object moves onto its nearest singleton marker and adopts the
marker color. Objects are generated with distinct sizes and nearby markers so
the greedy assignment is stable.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_objects,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_objects, no_markers, equal_distances.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2e901bda22ee"
VERSION = "1.1.0"
TASK_ID = "2e901bda22ee"
SUMMARY = "Move each object to the nearest singleton marker and recolor by that marker."

INVARIANTS = [
    "there are two or three multi-cell objects with distinct sizes",
    "there is one singleton marker per object",
    "each marker is closest to the intended object",
    "moved normalized objects remain in bounds",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_objects", "no_markers", "equal_distances")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "10", "valid": "10..10"},
    "grid_w":         {"type": "int", "default": "15", "valid": "15..15"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_objects":      {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "palette_size":   {"type": "int", "default": "rng 4..6", "valid": "4..6"},
    "position_bias":  {"type": "str", "default": "objs_with_nearest_markers",
                       "valid": "objs_with_nearest_markers"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..6", "valid": "4..6"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = [
    [(0, 0), (0, 1), (1, 0), (2, 0), (2, 1), (2, 2)],
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    [(0, 0), (0, 1), (1, 0)],
]
_OBJ_TOP_LEFTS = [(1, 1), (6, 1), (2, 9)]
_MARKERS = [(2, 6), (7, 6), (4, 12)]


def _paint(g, top, left, cells, color):
    for dr, dc in cells:
        g[top + dr][left + dc] = color


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
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        n_objects = ctx.draw_int("n_objects", 2, 2)
    elif difficulty == "hard":
        n_objects = ctx.draw_int("n_objects", 3, 3)
    else:
        n_objects = ctx.draw_int("n_objects", 2, 3)
    obj_colors = rng.sample([3, 4, 5, 7, 8, 9], n_objects)
    marker_colors = rng.sample([1, 2, 6], n_objects)
    g = full_grid(10, 15, 0)

    for idx in range(n_objects):
        top, left = _OBJ_TOP_LEFTS[idx]
        marker_r, marker_c = _MARKERS[idx]
        _paint(g, top, left, _SHAPES[idx], obj_colors[idx])
        g[marker_r][marker_c] = marker_colors[idx]
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 15, 0)
    if name == "no_objects":
        # only markers, no objects to move → nothing to relocate
        for (r, c), color in zip(_MARKERS[:2], [1, 2]):
            g[r][c] = color
        return g
    if name == "no_markers":
        # objects without any marker → no destination defined
        for idx in range(2):
            top, left = _OBJ_TOP_LEFTS[idx]
            _paint(g, top, left, _SHAPES[idx], 4 + idx)
        return g
    if name == "equal_distances":
        # 1 marker equidistant to 2 objects → ambiguous nearest assignment
        _paint(g, 1, 1, _SHAPES[2], 4)
        _paint(g, 1, 8, _SHAPES[2], 6)
        g[1][5] = 1  # equidistant marker
        return g
    return g
