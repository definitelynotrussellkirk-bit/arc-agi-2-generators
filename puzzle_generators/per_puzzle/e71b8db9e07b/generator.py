"""Generator for arc_puzzle_bank_seventeenth21:M114.

The only non-5 object is a prototype. Matching color-5 frames receive a copy of
that prototype in their interiors.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_frames,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_prototype, no_frames, frame_size_mismatch.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "e71b8db9e07b"
VERSION = "1.1.0"
TASK_ID = "e71b8db9e07b"
SUMMARY = "A non-5 prototype is stamped into every matching-size 5-frame."

INVARIANTS = [
    "exactly one non-5 prototype object is present outside the frames",
    "target frames are color-5 rectangular outlines",
    "matching frames have interior size equal to the prototype crop",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_prototype", "no_frames", "frame_size_mismatch")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "15", "valid": "15..15"},
    "grid_w":         {"type": "int", "default": "18", "valid": "18..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_frames":       {"type": "int", "default": "rng 1..3", "valid": "1..3"},
    "shape":          {"type": "int", "default": "rng 0..2", "valid": "0..2"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "prototype_plus_frames",
                       "valid": "prototype_plus_frames"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = [
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)],
    [(0, 1), (1, 0), (1, 1), (1, 2)],
]


def _paint(g, top, left, cells, color):
    for r, c in cells:
        g[top + r][left + c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    if difficulty == "easy":
        n_frames = ctx.draw_int("n_frames", 1, 1)
    elif difficulty == "hard":
        n_frames = ctx.draw_int("n_frames", 2, 3)
    else:
        n_frames = ctx.draw_int("n_frames", 1, 3)
    shape = _SHAPES[ctx.draw_int("shape", 0, len(_SHAPES) - 1)]
    ph = max(r for r, _c in shape) + 1
    pw = max(c for _r, c in shape) + 1
    color = rng.choice([1, 2, 3, 4, 6, 7, 8, 9])
    g = full_grid(15, 18, 0)
    _paint(g, 1, 1, shape, color)
    origins = [(1, 9), (7, 1), (7, 9)]
    for r0, c0 in origins[:n_frames]:
        draw_frame(g, r0, c0, r0 + ph + 1, c0 + pw + 1, 5)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(15, 18, 0)
    if name == "no_prototype":
        # frames without prototype → no template to stamp
        draw_frame(g, 1, 9, 5, 13, 5)
        draw_frame(g, 7, 1, 11, 5, 5)
        return g
    if name == "no_frames":
        # prototype alone, no frames to fill
        _paint(g, 1, 1, _SHAPES[0], 4)
        return g
    if name == "frame_size_mismatch":
        # frame interior ≠ prototype crop size → no matching frames
        _paint(g, 1, 1, _SHAPES[0], 4)  # 3x2 prototype
        draw_frame(g, 7, 1, 13, 7, 5)  # huge 7x7 frame, no match
        return g
    return g
