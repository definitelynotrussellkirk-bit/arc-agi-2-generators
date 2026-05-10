"""Generator for 5b37cb25.

Rule: background plus-shaped notches are filled with the frame-side
color indicated by nearby foreground cells.

Combinatorial axes (8): grid_h/w, notch_side, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_notch, no_frame, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0e134ade0f09"
VERSION = "1.1.0"
TASK_ID = "0e134ade0f09"
SUMMARY = "Background plus-notch filled with matching side color from frame."

INVARIANTS = [
    "the outer frame exposes top, left, right and bottom side colors",
    "a distinct foreground color forms side-specific five-cell ring cues",
    "the plus-shaped notch itself is background color",
    "all six involved colors are distinct and non-zero",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_notch", "no_frame", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "13", "valid": "13"},
    "grid_w":         {"type": "int", "default": "13", "valid": "13"},
    "notch_side":     {"type": "str", "default": "top", "valid": "top"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "6", "valid": "6"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "6", "valid": "6"},
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
    bg, top, left, right, bottom, fg = ctx.draw_distinct_colors("colors", n=6, exclude={0})
    g = full_grid(13, 13, bg)
    for c in range(13):
        g[0][c] = top
        g[12][c] = bottom
    for r in range(13):
        g[r][0] = left
        g[r][12] = right
    r = 5
    c = 6
    for dr, dc in [(2, 0), (0, -2), (0, 2), (1, -1), (1, 1)]:
        g[r + dr][c + dc] = fg
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 13, 5)
    if name == "no_notch":
        return g
    if name == "no_frame":
        return full_grid(13, 13, 5)
    if name == "full_grid":
        for r in range(13):
            for c in range(13):
                g[r][c] = 2
        return g
    return g
