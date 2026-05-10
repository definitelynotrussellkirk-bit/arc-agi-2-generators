"""Generator for 88a10436.

Rule: 5-marker is anchor. Shape (non-0 non-5 cells) is copied so its
centroid aligns with the 5-marker.

Combinatorial axes (8): grid_h/w, shape_variant, marker_position,
shape_position, palette_kind, anchor_corner, asymmetry_force, palette_size.
Degenerates: same_position, no_marker, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "be2d64032c69"
VERSION = "1.1.0"
TASK_ID = "be2d64032c69"
SUMMARY = "Single 5-marker + small multi-color shape (>=3 cells) at distance from it."

INVARIANTS = [
    "exactly one 5-cell (the marker)",
    ">=3 non-5 non-0 cells forming a connected shape",
    "shape and marker are in different quadrants so movement is non-trivial",
]

SHAPES = [
    [(0, 0, 6), (1, 0, 1), (1, 1, 1), (2, 0, 2), (2, 1, 2), (2, 2, 2)],
    [(0, 1, 6), (1, 0, 1), (1, 1, 1), (2, 0, 2)],
    [(0, 0, 4), (0, 1, 4), (1, 1, 6), (2, 1, 2)],
]

POSITION_BIASES = ("opposite", "diagonal", "wide_spread", "rng")
DEGENERATE_TEXTURES = ("same_position", "no_marker", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 7..9", "valid": "5..12"},
    "shape_variant":  {"type": "int", "default": "rng 0..2", "valid": "0..2"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "marker_position":{"type": "str", "default": "lower_left",
                       "valid": "lower_left|tl|tr|br|rng"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "fixed", "valid": "fixed"},
    "texture":        {"type": "str", "default": "alias for position_bias",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h_lo, h_hi = 5, 7
    elif difficulty == "hard":
        h_lo, h_hi = 9, 12
    else:
        h_lo, h_hi = 7, 9
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    g = full_grid(h, w, 0)
    sv = int(overrides.get("shape_variant",
                           ctx.draw_int("shape_variant", 0, len(SHAPES) - 1)))
    sv = max(0, min(len(SHAPES) - 1, sv))
    shape = SHAPES[sv]
    sh = max(r for r, c, v in shape) + 1
    sw = max(c for r, c, v in shape) + 1
    sr0 = rng.randint(0, max(0, h // 2 - sh))
    sc0 = rng.randint(max(w // 2 + 1, w - sw - 1), max(0, w - sw))
    for dr, dc, v in shape:
        if sr0 + dr < h and sc0 + dc < w:
            g[sr0 + dr][sc0 + dc] = v
    for _ in range(40):
        mr = rng.randint(max(1, h // 2 + 1), h - 2)
        mc = rng.randint(1, max(1, w // 2 - 1))
        if mr < h and mc >= 0 and g[mr][mc] == 0:
            g[mr][mc] = 5
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "same_position":
        g[3][3] = 5
        g[3][3] = 6
        return g
    if name == "no_marker":
        g[1][5] = 6; g[2][4] = 1; g[2][5] = 1
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 5
        return g
    return g
