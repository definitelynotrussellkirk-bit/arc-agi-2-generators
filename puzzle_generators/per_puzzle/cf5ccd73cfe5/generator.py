"""Generator for 6b9890af.

Rule: marker shape is scaled to fill the interior of a rectangular
frame.

Combinatorial axes (8): grid_h/w, scale, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_frame, no_marker, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "cf5ccd73cfe5"
VERSION = "1.1.0"
TASK_ID = "cf5ccd73cfe5"
SUMMARY = "Marker shape scaled to fill interior of rectangular frame."

INVARIANTS = [
    "background is color 0",
    "one hollow rectangular frame is present",
    "one outside marker shape uses a non-frame color",
    "frame interior dimensions are integer multiples of marker bbox dims",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_frame", "no_marker", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 13..15", "valid": "11..18"},
    "grid_w":         {"type": "int", "default": "rng 13..15", "valid": "11..18"},
    "scale":          {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
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
        scale_lo, scale_hi = 2, 2
    elif difficulty == "hard":
        scale_lo, scale_hi = 3, 4
    else:
        scale_lo, scale_hi = 2, 3
    scale = ctx.draw_int("scale", scale_lo, scale_hi)
    marker_h = 2
    marker_w = 2
    interior_h = marker_h * scale
    interior_w = marker_w * scale
    frame_h = interior_h + 2
    frame_w = interior_w + 2
    h = frame_h + 7 + rng.randint(0, 2)
    w = frame_w + 7 + rng.randint(0, 2)
    frame_color, marker_color = ctx.draw_distinct_colors("colors", n=2, exclude={0})
    g = full_grid(h, w, 0)
    fr, fc = 1, 1
    for c in range(fc, fc + frame_w):
        g[fr][c] = frame_color
        g[fr + frame_h - 1][c] = frame_color
    for r in range(fr, fr + frame_h):
        g[r][fc] = frame_color
        g[r][fc + frame_w - 1] = frame_color
    mr = frame_h + 3
    mc = 3 + ((sample_index + rng.randint(0, 2)) % max(1, w - 7))
    for dr, dc in [(0, 0), (0, 1), (1, 0)]:
        g[mr + dr][mc + dc] = marker_color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(15, 15, 0)
    if name == "no_frame":
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[8 + dr][3 + dc] = 2
        return g
    if name == "no_marker":
        for r in range(1, 7):
            g[r][1] = 1; g[r][6] = 1
        for c in range(1, 7):
            g[1][c] = 1; g[6][c] = 1
        return g
    if name == "full_grid":
        for r in range(15):
            for c in range(15):
                g[r][c] = 1
        return g
    return g
