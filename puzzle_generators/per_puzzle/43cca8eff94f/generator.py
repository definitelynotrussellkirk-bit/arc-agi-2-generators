"""Generator for arc_puzzle_bank_21_set7_s:S7_M1.

A red object begins to the left of a cyan frame and slides right until it
touches the frame from outside.

Combinatorial axes (8): grid_h, grid_w, palette_kind, gap,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_frame, no_object, object_inside_frame.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "43cca8eff94f"
VERSION = "1.1.0"
TASK_ID = "43cca8eff94f"
SUMMARY = "Dock a red object to the outside-left edge of a fixed cyan frame."

INVARIANTS = [
    "the cyan object is a rectangular frame",
    "the red object lies completely left of the frame",
    "sliding right is the only direction that brings the object to the frame",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frame", "no_object", "object_inside_frame")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "10", "valid": "10..10"},
    "grid_w":         {"type": "int", "default": "14", "valid": "14..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "gap":            {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "object_left_of_frame",
                       "valid": "object_left_of_frame"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = [
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (1, 1)],
    [(0, 1), (1, 0), (1, 1)],
]


def _draw_frame(g, top, left, bottom, right):
    for c in range(left, right + 1):
        g[top][c] = 8
        g[bottom][c] = 8
    for r in range(top, bottom + 1):
        g[r][left] = 8
        g[r][right] = 8


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        gap = ctx.draw_int("gap", 1, 1)
    elif difficulty == "hard":
        gap = ctx.draw_int("gap", 2, 3)
    else:
        gap = ctx.draw_int("gap", 1, 3)
    frame_left = ctx.draw_int("frame_left", 6, 8)
    shape = _SHAPES[ctx.draw_int("shape", 0, len(_SHAPES) - 1)]
    shape_w = max(c for _, c in shape) + 1
    g = full_grid(10, 14, 0)
    top = 2
    bottom = 6
    frame_right = frame_left + 4
    _draw_frame(g, top, frame_left, bottom, frame_right)
    base_r = 3
    base_c = max(0, frame_left - gap - shape_w)
    for dr, dc in shape:
        g[base_r + dr][base_c + dc] = 2
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 14, 0)
    if name == "no_frame":
        # red object without cyan frame → no destination edge
        for dr, dc in [(0, 0), (1, 0), (1, 1)]:
            g[3 + dr][2 + dc] = 2
        return g
    if name == "no_object":
        # frame only, no red object → nothing to dock
        _draw_frame(g, 2, 6, 6, 10)
        return g
    if name == "object_inside_frame":
        # red object inside frame → "left of" precondition fails
        _draw_frame(g, 2, 6, 6, 10)
        for dr, dc in [(0, 0), (1, 0), (1, 1)]:
            g[3 + dr][7 + dc] = 2
        return g
    return g
