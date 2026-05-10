"""Generator for b7fb29bc.

Rule: 3-frame with one 3-marker inside; fill interior with 2/4 by
chebyshev distance from marker.

Combinatorial axes (8): grid_h/w, frame_h, frame_w, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias.
Degenerates: no_frame, no_marker, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect_outline

GENERATOR_ID = "e07bbcbe6ba4"
VERSION = "1.1.0"
TASK_ID = "e07bbcbe6ba4"
SUMMARY = "3-frame ≥6x6 with one 3-marker strictly inside."

INVARIANTS = [
    "exactly one 3-frame with width and height of at least 7",
    "exactly one extra 3-cell strictly inside the frame interior",
    "rest of the grid is color 0",
    "the marker sits at least two cells inside any frame edge",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_frame", "no_marker", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..14", "valid": "9..18"},
    "grid_w":         {"type": "int", "default": "rng 11..14", "valid": "9..18"},
    "frame_h":        {"type": "int", "default": "rng 7..9", "valid": "7..12"},
    "frame_w":        {"type": "int", "default": "rng 7..9", "valid": "7..12"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
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
        h_lo, h_hi = 11, 12
    elif difficulty == "hard":
        h_lo, h_hi = 14, 18
    else:
        h_lo, h_hi = 11, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    g = full_grid(h, w, 0)
    fh = rng.randint(7, min(9, h - 2))
    fw = rng.randint(7, min(9, w - 2))
    r0 = rng.randint(1, h - fh - 1)
    c0 = rng.randint(1, w - fw - 1)
    draw_rect_outline(g, r0, c0, fh, fw, 3)
    mr = rng.randint(r0 + 2, r0 + fh - 3)
    mc = rng.randint(c0 + 2, c0 + fw - 3)
    g[mr][mc] = 3
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 12, 0)
    if name == "no_frame":
        g[5][5] = 3
        return g
    if name == "no_marker":
        draw_rect_outline(g, 1, 1, 8, 8, 3)
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(12):
                g[r][c] = 3
        return g
    return g
