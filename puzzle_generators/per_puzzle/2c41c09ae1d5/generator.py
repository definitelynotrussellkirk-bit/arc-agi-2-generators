"""Generator for arc_puzzle_bank_twelfth21:H81 — repeat object along marker vector by counter.

Rule: repeat an object along the vector from marker 1 to marker 2, once
per color-3 counter cell.

Combinatorial axes (8): grid_h, grid_w, palette_kind, variant,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_markers, no_object, no_counter.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2c41c09ae1d5"
VERSION = "1.1.0"
TASK_ID = "2c41c09ae1d5"
SUMMARY = "Repeat an object along the vector from marker 1 to marker 2, once per color-3 counter cell."

INVARIANTS = [
    "there is one marker 1 and one marker 2",
    "the marker vector is small enough for all repeated copies to stay in bounds",
    "the number of color-3 cells gives the number of additional copies",
    "the moved object uses a non-marker color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_markers", "no_object", "no_counter")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "8", "valid": "8..8"},
    "grid_w":         {"type": "int", "default": "10", "valid": "10..10"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "variant":        {"type": "int", "default": "rng 0..5", "valid": "0..5"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "markers_object_counter",
                       "valid": "markers_object_counter"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_VARIANTS = [
    ((0, 2), 2, [(0, 0), (1, 0), (1, 1)], (3, 0)),
    ((1, 1), 2, [(0, 0), (0, 1), (1, 1)], (2, 0)),
    ((0, 1), 3, [(0, 0), (1, 0), (1, 1), (2, 1)], (2, 0)),
    ((1, 0), 2, [(0, 0), (0, 1), (1, 0)], (1, 4)),
    ((1, 2), 1, [(0, 0), (1, 0), (1, 1)], (2, 0)),
    ((0, 2), 3, [(0, 0), (0, 1), (1, 0), (2, 0)], (2, 0)),
]


def _paint(g, top, left, cells, color):
    for r, c in cells:
        g[top + r][left + c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        idx = ctx.draw_int("variant", 0, 1)
    elif difficulty == "hard":
        idx = ctx.draw_int("variant", 4, 5)
    else:
        idx = ctx.draw_int("variant", 0, len(_VARIANTS) - 1)
    (dr, dc), count, cells, start = _VARIANTS[idx]
    color = rng.choice([4, 5, 6, 7, 8, 9])
    g = full_grid(8, 10, 0)
    g[0][0] = 1
    g[dr][dc] = 2
    for c in range(count):
        g[7][c] = 3
    _paint(g, start[0], start[1], cells, color)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(8, 10, 0)
    if name == "no_markers":
        # object + counter but no 1/2 markers → no vector defined
        _paint(g, 2, 2, [(0, 0), (1, 0), (1, 1)], 4)
        for c in range(2): g[7][c] = 3
        return g
    if name == "no_object":
        # markers + counter but no object to repeat
        g[0][0] = 1
        g[1][2] = 2
        for c in range(2): g[7][c] = 3
        return g
    if name == "no_counter":
        # markers + object but no 3-counter → no copies to make
        g[0][0] = 1
        g[1][2] = 2
        _paint(g, 2, 2, [(0, 0), (1, 0), (1, 1)], 4)
        return g
    return g
