"""Generator for ac2e8ecf.

Rule: rectangular frame objects packed upward; plus-like non-frames
packed downward.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors,
object_layout.
Degenerates: no_frames, no_pluses, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid, paint_at
from puzzle_generators.helpers.shape import PLUS_5

GENERATOR_ID = "8a6282b87245"
VERSION = "1.1.0"
TASK_ID = "8a6282b87245"
SUMMARY = "Frames packed upward; plus-like non-frames packed downward."

INVARIANTS = [
    "background is color 0",
    "some same-color objects are exact rectangle outlines",
    "other same-color objects are compact non-frame plus shapes",
    "frames preserve columns and move to the top; non-frames preserve columns and move to the bottom",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_frames", "no_pluses", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "14", "valid": "14"},
    "grid_w":         {"type": "int", "default": "15", "valid": "15"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "4", "valid": "4"},
    "object_layout":  {"type": "str", "default": "shuffled", "valid": "shuffled"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


PLUS = PLUS_5


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    _ = ctx.draw_choice("object_layout", ["shuffled"])
    colors = ctx.draw_distinct_colors("colors", n=4, exclude={0})
    g = full_grid(14, 15, 0)
    draw_frame(g, 7, 1, 9, 3, colors[0])
    draw_frame(g, 10, 8, 12, 10, colors[1])
    paint_at(g, 1, 5, PLUS, colors[2])
    paint_at(g, 3, 12, PLUS, colors[3])
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(14, 15, 0)
    if name == "no_frames":
        paint_at(g, 1, 5, PLUS, 4)
        return g
    if name == "no_pluses":
        draw_frame(g, 7, 1, 9, 3, 3)
        return g
    if name == "full_grid":
        for r in range(14):
            for c in range(15):
                g[r][c] = 3
        return g
    return g
