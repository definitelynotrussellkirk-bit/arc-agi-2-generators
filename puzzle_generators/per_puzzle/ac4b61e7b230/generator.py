"""Generator for puzzle 05f2a901.

Rule: 1 2-blob + 1 8-blob. Output is empty grid + 8 unchanged + 2
moved to abut 8 (in closer of row/col direction).

Combinatorial axes (8): grid_h/w, blob_2_size, blob_8_size,
blob_2_position, blob_8_position, anchor_corner, asymmetry_force,
include_decoy.
Degenerates: same_position, no_blobs, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.shape import H_LINE_3

GENERATOR_ID = "ac4b61e7b230"
VERSION = "1.1.0"
TASK_ID = "ac4b61e7b230"
SUMMARY = "1 red(2) blob + 1 cyan(8) blob; rule moves red to abut cyan."

INVARIANTS = [
    "background is 0",
    "exactly 1 connected 2-blob",
    "exactly 1 connected 8-blob",
    "blobs separated >=2 cells",
]

POSITION_BIASES = ("opposite_corners", "spread", "near_edge",
                   "diagonal", "row_aligned")
BLOB_2_SHAPES = ("h_line", "v_line", "single", "L_shape", "rect_2x2")
DEGENERATE_TEXTURES = ("same_position", "no_blobs", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..14", "valid": "6..18"},
    "grid_w":         {"type": "int", "default": "rng 9..14", "valid": "7..18"},
    "blob_2_shape":   {"type": "str", "default": "rng",
                       "valid": "|".join(BLOB_2_SHAPES)},
    "blob_8_shape":   {"type": "str", "default": "rng",
                       "valid": "h_line|plus|rect_2x2|cross"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "include_decoy":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "min_separation": {"type": "int", "default": "2", "valid": "2..6"},
    "texture":        {"type": "str", "default": "alias for position_bias",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_BLOB_2 = {
    "h_line":   list(H_LINE_3),
    "v_line":   [(0, 0), (1, 0), (2, 0)],
    "single":   [(0, 0)],
    "L_shape":  [(0, 0), (1, 0), (1, 1)],
    "rect_2x2": [(0, 0), (0, 1), (1, 0), (1, 1)],
}

_BLOB_8 = {
    "h_line":   [(0, 0), (0, 1), (0, 2)],
    "plus":     [(0, 0), (1, 0), (2, 0), (1, 1), (1, 2)],
    "rect_2x2": [(0, 0), (0, 1), (1, 0), (1, 1)],
    "cross":    [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)],
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 6, 9
    elif difficulty == "hard":
        h_lo, h_hi = 14, 18
    else:
        h_lo, h_hi = 8, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo + 1, h_hi + 1)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias",
                               list(POSITION_BIASES)))
    blob_2_kind = overrides.get("blob_2_shape",
                                ctx.draw_choice("blob_2_shape",
                                                list(BLOB_2_SHAPES)))
    blob_8_kind = overrides.get("blob_8_shape",
                                ctx.draw_choice("blob_8_shape",
                                                ["h_line", "plus",
                                                 "rect_2x2", "cross"]))
    blob_2 = list(_BLOB_2[blob_2_kind])
    blob_8 = list(_BLOB_8[blob_8_kind])
    g = full_grid(h, w, 0)
    r2_2, c2_2 = _pick_blob_2_pos(bias, h, w, blob_2, rng)
    r0_8, c0_8 = _pick_blob_8_pos(bias, h, w, blob_8, rng)
    paint_at(g, r2_2, c2_2, blob_2, 2)
    paint_at(g, r0_8, c0_8, blob_8, 8)
    return g


def _shape_dims(cells):
    h = max(r for r, _ in cells) + 1
    w = max(c for _, c in cells) + 1
    return h, w


def _pick_blob_2_pos(bias, h, w, cells, rng):
    bh, bw = _shape_dims(cells)
    if bias == "opposite_corners":
        return rng.randint(0, max(0, h // 3)), \
               rng.randint(0, max(0, w // 3))
    if bias == "near_edge":
        return rng.randint(0, 1), rng.randint(0, max(0, w - bw))
    if bias == "diagonal":
        return 0, 0
    if bias == "row_aligned":
        return h // 2, 0
    return rng.randint(0, max(0, h - bh - 2)), \
           rng.randint(0, max(0, w - bw - 2))


def _pick_blob_8_pos(bias, h, w, cells, rng):
    bh, bw = _shape_dims(cells)
    if bias == "opposite_corners":
        return rng.randint(2 * h // 3, max(2 * h // 3, h - bh)), \
               rng.randint(2 * w // 3, max(2 * w // 3, w - bw))
    if bias == "near_edge":
        return rng.randint(h - bh - 1, h - bh), \
               rng.randint(0, max(0, w - bw))
    if bias == "diagonal":
        return h - bh, w - bw
    if bias == "row_aligned":
        return h // 2, w - bw
    return rng.randint(h - bh - 2, max(h - bh - 2, h - bh)), \
           rng.randint(w - bw - 2, max(w - bw - 2, w - bw))


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "same_position":
        # 2 and 8 overlap (won't happen in valid input)
        g[h // 2][w // 2] = 2
        g[h // 2][w // 2 + 1] = 8
        return g
    if name == "no_blobs":
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 2 if (r + c) % 2 == 0 else 8
        return g
    return g
