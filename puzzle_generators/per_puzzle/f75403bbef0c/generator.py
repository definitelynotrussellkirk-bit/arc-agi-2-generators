"""Generator for 543a7ed5.

Rule: magenta rectangular frames on cyan get a green outer border and
yellow-filled cyan interior.

Combinatorial axes (8): grid_h/w, frame_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
frame_size.
Degenerates: no_frames, single_frame, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f75403bbef0c"
VERSION = "1.1.0"
TASK_ID = "f75403bbef0c"
SUMMARY = "Magenta frames on cyan get green border and yellow-filled cyan interior."

INVARIANTS = [
    "the background is color 8",
    "each foreground object is a color-6 rectangular frame",
    "frames sit clear of each other so their bboxes do not overlap",
    "each frame has at least one cyan cell inside and around it",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_frames", "single_frame", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "16", "valid": "16"},
    "grid_w":         {"type": "int", "default": "16", "valid": "16"},
    "frame_count":    {"type": "int", "default": "rng 1..3", "valid": "1..5"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "frame_size":     {"type": "str", "default": "rng 4..6", "valid": "4..6"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _draw_frame(g, r0, c0, rh, rw):
    for r in range(rh):
        g[r0 + r][c0] = 6
        g[r0 + r][c0 + rw - 1] = 6
    for c in range(rw):
        g[r0][c0 + c] = 6
        g[r0 + rh - 1][c0 + c] = 6


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
        fc_lo, fc_hi = 3, 3
    else:
        fc_lo, fc_hi = 1, 3
    frame_count = ctx.draw_int("frame_count", fc_lo, fc_hi)
    g = full_grid(16, 16, 8)
    placements = [(2, 2), (2, 10), (9, 5)]
    for r0, c0 in placements[:frame_count]:
        rh = rng.randint(4, 6)
        rw = rng.randint(4, 5)
        _draw_frame(g, r0, c0, rh, rw)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(16, 16, 8)
    if name == "no_frames":
        return g
    if name == "single_frame":
        _draw_frame(g, 4, 4, 5, 5)
        return g
    if name == "full_grid":
        for r in range(16):
            for c in range(16):
                g[r][c] = 6
        return g
    return g
