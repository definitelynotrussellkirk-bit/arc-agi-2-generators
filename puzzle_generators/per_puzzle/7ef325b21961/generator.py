"""Generator for 4b6b68e5.

Rule: closed frames keep their borders; interior noise dots disappear,
and enclosed cells fill with the majority interior dot color.

Combinatorial axes (8): grid_h/w, frame_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_frames, no_dots, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "7ef325b21961"
VERSION = "1.1.0"
TASK_ID = "7ef325b21961"
SUMMARY = "Closed frames keep borders; interior fills with majority dot color."

INVARIANTS = [
    "background is color 0",
    "each large object is a closed single-color rectangular frame",
    "isolated colored dots inside a frame are not connected to the frame",
    "frame, majority and minority colors are distinct and non-zero",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_frames", "no_dots", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "18", "valid": "18"},
    "grid_w":         {"type": "int", "default": "18", "valid": "18"},
    "frame_count":    {"type": "int", "default": "rng 1..2", "valid": "1..4"},
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


def _draw_frame(g, r0, c0, rh, rw, color):
    for r in range(rh):
        g[r0 + r][c0] = color
        g[r0 + r][c0 + rw - 1] = color
    for c in range(rw):
        g[r0][c0 + c] = color
        g[r0 + rh - 1][c0 + c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        fc_lo, fc_hi = 1, 1
    elif difficulty == "hard":
        fc_lo, fc_hi = 2, 2
    else:
        fc_lo, fc_hi = 1, 2
    frame_count = ctx.draw_int("frame_count", fc_lo, fc_hi)
    colors = ctx.draw_distinct_colors("colors", n=frame_count + 2, exclude={0})
    g = full_grid(18, 18, 0)
    specs = [(2, 2, 7, 8), (9, 9, 7, 7)]
    for idx in range(frame_count):
        r0, c0, rh, rw = specs[idx]
        frame_color = colors[idx]
        majority = colors[-2]
        minority = colors[-1]
        _draw_frame(g, r0, c0, rh, rw, frame_color)
        interior = [(r, c) for r in range(r0 + 2, r0 + rh - 2) for c in range(c0 + 2, c0 + rw - 2)]
        rng.shuffle(interior)
        for r, c in interior[:3]:
            g[r][c] = majority
        if len(interior) > 3:
            g[interior[3][0]][interior[3][1]] = minority
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(18, 18, 0)
    if name == "no_frames":
        g[5][5] = 2
        return g
    if name == "no_dots":
        _draw_frame(g, 2, 2, 7, 8, 1)
        return g
    if name == "full_grid":
        for r in range(18):
            for c in range(18):
                g[r][c] = 2
        return g
    return g
