"""Generator for arc_puzzle_bank_seventh_21_bundle:hard_48_local_rotate_object_to_key_center.

Combinatorial axes (8): grid_h, grid_w, palette_kind, key,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_key, no_frame, no_object.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "f2dbde875127"
VERSION = "1.1.0"
TASK_ID = "f2dbde875127"
SUMMARY = "Rotate each framed object according to its key marker and center it within the frame interior."

INVARIANTS = [
    "color-1 frames define local object work areas",
    "a key marker above each frame is one of 2, 3, 4, or 5",
    "each frame interior contains one single-color object crop",
    "the object is cleared, rotated by the key, and centered back into the same interior",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_key", "no_frame", "no_object")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "8", "valid": "8..8"},
    "grid_w":         {"type": "int", "default": "15", "valid": "15..15"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "key":            {"type": "int", "default": "rng 2..5", "valid": "2..5"},
    "shape":          {"type": "int", "default": "rng 0..3", "valid": "0..3"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "two_frames_with_keys_and_objects",
                       "valid": "two_frames_with_keys_and_objects"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = [
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    [(0, 0), (0, 1), (1, 1), (2, 1)],
    [(0, 1), (1, 0), (1, 1), (1, 2)],
    [(0, 0), (1, 0), (2, 0), (2, 1)],
]


def _paint(g, top, left, cells, color):
    for r, c in cells:
        g[top + r][left + c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        key = ctx.draw_int("key", 2, 2)
        shape = ctx.draw_int("shape", 0, 1)
    elif difficulty == "hard":
        key = ctx.draw_int("key", 4, 5)
        shape = ctx.draw_int("shape", 2, 3)
    else:
        key = ctx.draw_int("key", 2, 5)
        shape = ctx.draw_int("shape", 0, len(_SHAPES) - 1)
    g = full_grid(8, 15, 0)
    draw_frame(g, 1, 1, 7, 7, 1)
    g[0][3] = key
    _paint(g, 2, 2, _SHAPES[shape], 7)
    draw_frame(g, 1, 9, 7, 14, 1)
    g[0][11] = 2 + ((key - 1) % 4)
    _paint(g, 3, 10, _SHAPES[-1 - shape], 8)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(8, 15, 0)
    if name == "no_key":
        # frames + objects but no key marker → no rotation count specified
        draw_frame(g, 1, 1, 7, 7, 1)
        _paint(g, 2, 2, _SHAPES[0], 7)
        return g
    if name == "no_frame":
        # key + object without frame → no work-area boundary defined
        g[0][3] = 3
        _paint(g, 2, 2, _SHAPES[0], 7)
        return g
    if name == "no_object":
        # frame + key but empty interior → nothing to rotate
        draw_frame(g, 1, 1, 7, 7, 1)
        g[0][3] = 3
        return g
    return g
