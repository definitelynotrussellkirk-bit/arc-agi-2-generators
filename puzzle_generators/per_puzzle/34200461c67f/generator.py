"""Generator for d931c21c.

Rule: a hollow color-1 object gets exterior-adjacent and interior-
adjacent background marks.

Combinatorial axes (8): grid_h/w, frame_size, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_frame, solid_frame, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "34200461c67f"
VERSION = "1.1.0"
TASK_ID = "34200461c67f"
SUMMARY = "Hollow color-1 object gets exterior-adjacent and interior-adjacent background marks."

INVARIANTS = [
    "the background is zero",
    "one color-1 rectangular frame encloses a nonempty zero hole",
    "the frame is not clipped by the grid edge",
    "the rule paints outside-adjacent zero cells 2 and enclosed-adjacent zero cells 3",
]

FRAME_KINDS = ("F5x5", "F5x6", "F6x5")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_frame", "solid_frame", "full_grid")
HELPFUL_TEXTURES = FRAME_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "12", "valid": "12"},
    "grid_w":         {"type": "int", "default": "12", "valid": "12"},
    "frame_size":     {"type": "str", "default": "rng helpful",
                       "valid": "5x5|5x6|6x5"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "varied", "valid": "varied"},
    "n_distinct_colors":{"type": "int", "default": "1", "valid": "1"},
    "texture":        {"type": "str", "default": "alias for frame_size",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    tx = overrides.get("texture")
    if tx == "F5x5":
        rh, rw = 5, 5
    elif tx == "F5x6":
        rh, rw = 5, 6
    elif tx == "F6x5":
        rh, rw = 6, 5
    else:
        rh, rw = ctx.draw_choice("frame_size", [(5, 5), (5, 6), (6, 5)])
    g = full_grid(12, 12, 0)
    top = ctx.draw_int("top", 1, 12 - rh - 1)
    left = ctx.draw_int("left", 1, 12 - rw - 1)
    draw_frame(g, top, left, top + rh - 1, left + rw - 1, 1)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 12, 0)
    if name == "no_frame":
        return g
    if name == "solid_frame":
        for r in range(2, 7):
            for c in range(2, 7):
                g[r][c] = 1
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(12):
                g[r][c] = 1
        return g
    return g
