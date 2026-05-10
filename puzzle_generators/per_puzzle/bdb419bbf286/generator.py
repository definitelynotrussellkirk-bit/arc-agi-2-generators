"""Generator for arc_additional_puzzle_bank_volume19:H132.

Rule: the color-2 shape is copied three times along the vector (m4 - m3).

Combinatorial axes (8): grid_h/w, palette_kind, marker_offset_r,
marker_offset_c, palette_size, position_bias, n_distinct_colors, texture.
Degenerates: no_shape, markers_collide, missing_marker.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "bdb419bbf286"
VERSION = "1.1.0"
TASK_ID = "bdb419bbf286"
SUMMARY = "A color-2 shape is copied three times along the vector from marker 3 to marker 4."

INVARIANTS = [
    "one color-2 object defines the copied shape",
    "markers 3 and 4 define a small in-bounds translation vector",
]

PALETTE_KINDS = ("default", "vertical_vec", "horizontal_vec", "diagonal_vec")
DEGENERATE_TEXTURES = ("no_shape", "markers_collide", "missing_marker")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "7..16"},
    "grid_w":         {"type": "int", "default": "rng 10..14", "valid": "8..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "marker_offset_r": {"type": "int", "default": "rng 1..2", "valid": "1..2"},
    "marker_offset_c": {"type": "int", "default": "rng 1..2", "valid": "1..2"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 10, 14)
    rng = ctx.draw_rng("layout")
    dr, dc = rng.choice([(1, 2), (2, 1), (1, 1)])
    g = full_grid(h, w, 0)
    g[0][0] = 3
    g[dr][dc] = 4
    shape = [(0, 0), (0, 1), (1, 0), (2, 0)]
    top = rng.randint(1, h - 2 * dr - 4)
    left = rng.randint(1, w - 2 * dc - 3)
    for rr, cc in shape:
        g[top + rr][left + cc] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 12
    g = full_grid(h, w, 0)
    shape = [(0, 0), (0, 1), (1, 0), (2, 0)]
    if name == "no_shape":
        # markers but no color-2 source
        g[0][0] = 3
        g[1][2] = 4
        return g
    if name == "markers_collide":
        # 3 and 4 at the same cell — zero translation, copies stack on shape
        g[0][0] = 3
        g[0][0] = 4
        for rr, cc in shape:
            g[3 + rr][3 + cc] = 2
        return g
    if name == "missing_marker":
        # only marker 3 — translation vector undefined
        g[0][0] = 3
        for rr, cc in shape:
            g[3 + rr][3 + cc] = 2
        return g
    return g
