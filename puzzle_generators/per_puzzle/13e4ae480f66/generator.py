"""Generator for arc_puzzle_bank_21_set4:S4_E6.

Rule: blue objects touching the left border are recolored yellow; interior
blue objects stay blue.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_left, n_interior,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_left_objects, no_interior_objects, all_at_left.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.place import place_no_overlap

GENERATOR_ID = "13e4ae480f66"
VERSION = "1.1.0"
TASK_ID = "13e4ae480f66"

SUMMARY = "Blue objects touching the left border are recolored yellow."

INVARIANTS = [
    "background is 0",
    "all objects are blue",
    "at least one blue object touches the left edge",
    "at least one blue object does not touch the left edge",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_left_objects", "no_interior_objects", "all_at_left")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_left":         {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "n_interior":     {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "left_edge_plus_interior",
                       "valid": "left_edge_plus_interior"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_LEFT_SHAPES = [
    [(0, 0), (1, 0), (2, 0)],
    [(0, 0), (0, 1), (1, 0), (1, 1)],
    [(0, 0), (1, 0), (2, 0), (2, 1)],
]

_INTERIOR = [
    [(0, 0), (0, 1), (1, 0), (1, 1)],
    [(0, 0), (1, 0), (2, 0), (2, 1)],
    [(0, 0), (0, 1), (0, 2)],
]


def _paint(g, cells, r0, c0):
    for dr, dc in cells:
        g[r0 + dr][c0 + dc] = 1


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 12)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    for _ in range(rng.randint(1, 2)):
        cells = rng.choice(_LEFT_SHAPES)
        sh = max(r for r, _ in cells) + 1
        r0 = rng.randint(0, h - sh)
        if all(g[r0 + r][c] == 0 for r, c in cells):
            _paint(g, cells, r0, 0)
    for _ in range(rng.randint(1, 2)):
        if place_no_overlap(rng, g, rng.choice(_INTERIOR), 1, padding=1, margin=1, max_tries=400) is None:
            raise ValueError("could not place interior blue object")
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_left_objects":
        # only interior objects → rule fires zero times; output identical to input
        for (r, c) in [(2, 4), (2, 5), (3, 4), (3, 5)]: g[r][c] = 1
        for (r, c) in [(6, 7), (7, 7), (7, 8)]: g[r][c] = 1
        return g
    if name == "no_interior_objects":
        # only left-edge objects → all blues become yellow; output is uniform yellow
        for (r, c) in [(1, 0), (2, 0), (3, 0)]: g[r][c] = 1
        for (r, c) in [(5, 0), (5, 1), (6, 0), (6, 1)]: g[r][c] = 1
        return g
    if name == "all_at_left":
        # every object touches left edge → "interior vs edge" distinction collapses
        for (r, c) in [(1, 0), (2, 0)]: g[r][c] = 1
        for (r, c) in [(4, 0), (5, 0), (5, 1)]: g[r][c] = 1
        for (r, c) in [(7, 0), (8, 0)]: g[r][c] = 1
        return g
    return g
