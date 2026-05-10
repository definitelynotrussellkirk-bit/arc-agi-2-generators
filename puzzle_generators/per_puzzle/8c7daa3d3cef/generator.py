"""Generator for arc_additional_puzzle_bank_volume2:H12.

Rule: a 4-frame surrounds a 1-frame; the rule fills the annular region
between the two frames with color 8.

Combinatorial axes (8): grid_h/w, palette_kind, annular_thickness,
palette_size, position_bias, n_distinct_colors, frame_offset, texture.
Degenerates: frames_touching, no_inner_frame, no_outer_frame.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "8c7daa3d3cef"
VERSION = "1.1.0"
TASK_ID = "8c7daa3d3cef"
SUMMARY = "4-frame surrounding 1-frame surrounding empty interior."

INVARIANTS = [
    "outer frame is color 4 (h≥7, w≥7)",
    "inner frame is color 1 inside outer with at least 2-cell margin",
    "interior of inner frame is empty",
]

PALETTE_KINDS = ("default", "thin_annular", "thick_annular", "tight")
DEGENERATE_TEXTURES = ("frames_touching", "no_inner_frame", "no_outer_frame")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "9..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "9..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "annular_thickness": {"type": "int", "default": "1", "valid": "1..2"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "centered", "valid": "centered"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
    "frame_offset":   {"type": "int", "default": "1", "valid": "1"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 9, 11)
    g = full_grid(h, w, 0)
    draw_frame(g, 1, 1, h - 2, w - 2, 4)
    draw_frame(g, 3, 3, h - 4, w - 4, 1)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "frames_touching":
        draw_frame(g, 1, 1, h - 2, w - 2, 4)
        draw_frame(g, 2, 2, h - 3, w - 3, 1)
        return g
    if name == "no_inner_frame":
        draw_frame(g, 1, 1, h - 2, w - 2, 4)
        return g
    if name == "no_outer_frame":
        draw_frame(g, 3, 3, h - 4, w - 4, 1)
        return g
    return g
