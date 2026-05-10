"""Generator for arc_puzzle_bank_seventeenth_21_bundle:easy_117_crop_largest_object.

Combinatorial axes (8): grid_h, grid_w, palette_kind, large_variant,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_objects, all_same_size, single_object.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "db89dc496d45"
VERSION = "1.1.0"
TASK_ID = "db89dc496d45"

SUMMARY = "One unique largest object has a 3x3 bounding-box crop."

INVARIANTS = [
    "background is 0",
    "there is one unique largest connected component",
    "the largest component has a 3x3 bounding box",
    "all distractor components are smaller and separated",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_objects", "all_same_size", "single_object")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "6..18"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "6..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "large_variant":  {"type": "int", "default": "rng 0..2", "valid": "0..2"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "one_large_plus_distractors",
                       "valid": "one_large_plus_distractors"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _paint(g, top, left, shape, color):
    for dr, dc in shape:
        g[top + dr][left + dc] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 10, 13)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 4)
    large = rng.choice([
        [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
        [(0, 2), (1, 2), (2, 0), (2, 1), (2, 2)],
        [(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)],
    ])
    _paint(g, 2, 2, large, colors[0])
    _paint(g, 0, w - 3, [(0, 0), (0, 1)], colors[1])
    _paint(g, h - 2, 0, [(0, 0), (1, 0), (1, 1)], colors[2])
    _paint(g, h - 2, w - 2, [(0, 0), (1, 0)], colors[3])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 11
    g = full_grid(h, w, 0)
    if name == "no_objects":
        # blank → no largest object to crop
        return g
    if name == "all_same_size":
        # all components same size → no unique largest, ambiguous
        _paint(g, 1, 1, [(0, 0), (0, 1)], 4)
        _paint(g, 1, 5, [(0, 0), (0, 1)], 6)
        _paint(g, 5, 1, [(0, 0), (0, 1)], 7)
        return g
    if name == "single_object":
        # a single object → trivially "largest", no contrast distractors
        _paint(g, 3, 3, [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)], 4)
        return g
    return g
