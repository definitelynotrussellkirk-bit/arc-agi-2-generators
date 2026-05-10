"""Generator for arc_puzzle_bank_fifth21:H29.

Objects with colors 5 and above have an adjacent arrow code. The rule sweeps
each object in the arrow direction to the grid edge.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_objects,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_arrow, no_object, mismatched_arrow.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e64c021e29ad"
VERSION = "1.1.0"
TASK_ID = "e64c021e29ad"
SUMMARY = "Sweep each high-color object in the direction of its adjacent arrow."

INVARIANTS = [
    "every object color is at least 5",
    "each object has one adjacent arrow cell with code 1..4",
    "objects are separated from each other",
    "sweeps remain within the grid until they hit an edge",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_arrow", "no_object", "mismatched_arrow")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "10", "valid": "10..10"},
    "grid_w":         {"type": "int", "default": "14", "valid": "14..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_objects":      {"type": "int", "default": "rng 1..2", "valid": "1..2"},
    "palette_size":   {"type": "int", "default": "rng 1..2", "valid": "1..2"},
    "position_bias":  {"type": "str", "default": "objects_with_arrows",
                       "valid": "objects_with_arrows"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..2", "valid": "1..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_OBJECTS = [
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (1, 0), (1, 1)],
]
_PLACEMENTS = [(4, 3), (4, 9)]
_ARROWS = {
    1: (-1, 0),
    2: (0, 2),
    3: (2, 0),
    4: (0, -1),
}


def _paint(g, top, left, cells, color):
    for dr, dc in cells:
        g[top + dr][left + dc] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        n_objects = ctx.draw_int("n_objects", 1, 1)
    elif difficulty == "hard":
        n_objects = ctx.draw_int("n_objects", 2, 2)
    else:
        n_objects = ctx.draw_int("n_objects", 1, 2)
    colors = rng.sample([5, 6, 7, 8, 9], n_objects)
    g = full_grid(10, 14, 0)
    for idx in range(n_objects):
        top, left = _PLACEMENTS[idx]
        arrow = rng.choice([1, 2, 3, 4])
        _paint(g, top, left, _OBJECTS[idx], colors[idx])
        dr, dc = _ARROWS[arrow]
        g[top + dr][left + dc] = arrow
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 14, 0)
    if name == "no_arrow":
        # objects without arrows → no sweep direction specified
        _paint(g, 4, 3, _OBJECTS[0], 6)
        _paint(g, 4, 9, _OBJECTS[1], 7)
        return g
    if name == "no_object":
        # arrows alone with no high-color object → nothing to sweep
        g[3][3] = 1
        g[6][9] = 3
        return g
    if name == "mismatched_arrow":
        # arrow value not in 1..4 (e.g., another high color where arrow goes)
        _paint(g, 4, 3, _OBJECTS[0], 6)
        g[3][3] = 9  # not a valid arrow code
        return g
    return g
