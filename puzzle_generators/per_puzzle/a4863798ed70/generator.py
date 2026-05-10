"""Generator for ad173014.

Rule: interior colors inside red frames cycle clockwise around the
frame centroid.

Combinatorial axes (8): grid_h/w, frame_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_frames, single_frame, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "a4863798ed70"
VERSION = "1.1.0"
TASK_ID = "a4863798ed70"
SUMMARY = "Interior colors inside red frames cycle clockwise around centroid."

INVARIANTS = [
    "background is color 0",
    "red frame objects use color 2",
    "each red frame contains one non-red icon color",
    "icon colors are distinct from each other and from 0, 1 and 2",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_frames", "single_frame", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "12", "valid": "12"},
    "grid_w":         {"type": "int", "default": "12", "valid": "12"},
    "frame_count":    {"type": "int", "default": "rng 3..4", "valid": "3..4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "rng 3..4", "valid": "3..4"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "rng 3..4", "valid": "3..4"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
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
        c_lo, c_hi = 3, 3
    elif difficulty == "hard":
        c_lo, c_hi = 4, 4
    else:
        c_lo, c_hi = 3, 4
    count = ctx.draw_int("frame_count", c_lo, c_hi)
    colors = ctx.draw_distinct_colors("icon_colors", n=count, exclude={0, 1, 2})
    g = full_grid(12, 12, 0)
    anchors = [(1, 4), (4, 8), (8, 4), (4, 1)]
    for i in range(count):
        r, c = anchors[i]
        draw_frame(g, r, c, r + 2, c + 2, 2)
        g[r + 1][c + 1] = colors[i]
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 12, 0)
    if name == "no_frames":
        g[5][5] = 3
        return g
    if name == "single_frame":
        draw_frame(g, 4, 4, 6, 6, 2)
        g[5][5] = 3
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(12):
                g[r][c] = 2
        return g
    return g
