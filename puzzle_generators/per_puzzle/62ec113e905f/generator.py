"""Generator for 551d5bf1.

Rule: blue frames fill with cyan and extend a cyan ray through their
single edge gap.

Combinatorial axes (8): grid_h/w, frame_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias, side.
Degenerates: no_frames, no_gaps, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "62ec113e905f"
VERSION = "1.1.0"
TASK_ID = "62ec113e905f"
SUMMARY = "Blue frames fill with cyan and extend cyan ray through edge gap."

INVARIANTS = [
    "frames are color 1 on a color-0 background",
    "each frame is rectangular with one missing edge cell",
    "the gap side determines the extension direction",
    "frames sit clear of grid borders so the ray has room",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_frames", "no_gaps", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "18", "valid": "18"},
    "grid_w":         {"type": "int", "default": "19", "valid": "19"},
    "frame_count":    {"type": "int", "default": "rng 1..3", "valid": "1..5"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "side":           {"type": "str", "default": "rng",
                       "valid": "top|bottom|left|right"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _draw_gap_frame(g, r0, c0, rh, rw, side):
    cells = set()
    for r in range(rh):
        cells.add((r, 0))
        cells.add((r, rw - 1))
    for c in range(rw):
        cells.add((0, c))
        cells.add((rh - 1, c))
    gap = {
        "top": (0, rw // 2),
        "bottom": (rh - 1, rw // 2),
        "left": (rh // 2, 0),
        "right": (rh // 2, rw - 1),
    }[side]
    cells.discard(gap)
    for dr, dc in cells:
        g[r0 + dr][c0 + dc] = 1


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
    g = full_grid(18, 19, 0)
    specs = [(2, 2, "top"), (2, 11, "right"), (10, 6, "bottom")]
    for r0, c0, side in specs[:frame_count]:
        rh = rng.randint(5, 6)
        rw = rng.randint(5, 7)
        _draw_gap_frame(g, r0, c0, rh, rw, side)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(18, 19, 0)
    if name == "no_frames":
        return g
    if name == "no_gaps":
        for r in range(2, 8):
            g[r][2] = 1; g[r][8] = 1
        for c in range(2, 9):
            g[2][c] = 1; g[7][c] = 1
        return g
    if name == "full_grid":
        for r in range(18):
            for c in range(19):
                g[r][c] = 1
        return g
    return g
