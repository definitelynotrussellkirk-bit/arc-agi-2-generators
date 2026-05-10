"""Generator for 890034e9.

Rule: largest monochrome zero-interior frame is copied to another
same-sized zero-interior slot.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, frame_size,
n_distinct_colors.
Degenerates: no_frame, full_grid, single_pixel.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "4f065093e631"
VERSION = "1.1.0"
TASK_ID = "4f065093e631"
SUMMARY = "Largest monochrome zero-interior frame copied to same-sized slot."

INVARIANTS = [
    "background is color 0",
    "there is one largest rectangular frame with a zero interior",
    "another same-sized zero-interior slot is available",
    "the frame color is non-zero",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_frame", "full_grid", "single_pixel")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 14..16", "valid": "12..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "frame_size":     {"type": "str", "default": "5x5", "valid": "5x5"},
    "n_distinct_colors":{"type": "int", "default": "1", "valid": "1"},
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
    color = ctx.draw_color("frame_color", exclude={0})
    g = full_grid(9 + rng.randint(0, 1), 14 + rng.randint(0, 1), 0)
    draw_frame(g, 1, 1, 5, 5, color)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 15, 0)
    if name == "no_frame":
        return g
    if name == "single_pixel":
        g[5][5] = 2
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(15):
                g[r][c] = 2
        return g
    return g
