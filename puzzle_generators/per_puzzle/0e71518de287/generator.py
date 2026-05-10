"""Generator for arc_additional_puzzle_bank_volume18:M124.

Rule: a marker adjacent to one yellow frame selects that frame's
interior to fill in the marker's color.

Combinatorial axes (8): grid_h/w, palette_kind, marker_color,
palette_size, position_bias, n_distinct_colors, frame_count, texture.
Degenerates: no_marker, no_frame, marker_adjacent_to_two.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "0e71518de287"
VERSION = "1.1.0"
TASK_ID = "0e71518de287"
SUMMARY = "A marker adjacent to one yellow frame selects the frame interior to fill."

INVARIANTS = [
    "background is 0",
    "yellow components are hollow rectangular frames",
    "one external non-yellow marker is directly adjacent to one frame",
    "unmarked frames remain unchanged",
]

PALETTE_KINDS = ("default", "warm_marker", "cool_marker", "varied_marker")
DEGENERATE_TEXTURES = ("no_marker", "no_frame", "marker_adjacent_to_two")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..14", "valid": "8..24"},
    "grid_w":         {"type": "int", "default": "rng 13..17", "valid": "10..30"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "marker_color":   {"type": "int", "default": "rng", "valid": "1..9"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
    "frame_count":    {"type": "int", "default": "2", "valid": "2"},
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
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 13, 14)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 14)
        w = ctx.draw_int("grid_w", 16, 17)
    else:
        h = ctx.draw_int("grid_h", 10, 14)
        w = ctx.draw_int("grid_w", 13, 17)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    r0 = rng.randint(2, h - 7)
    r1 = r0 + rng.randint(4, 5)
    draw_frame(g, r0, 2, r1, 5, 4)
    draw_frame(g, r0, w - 5, r1, w - 2, 4)
    marker_color = rng.choice([1, 2, 3, 5, 6, 7, 8, 9])
    g[r0 - 1][rng.randint(2, 5)] = marker_color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 15
    g = full_grid(h, w, 0)
    if name == "no_marker":
        # frames but no marker — selection has no candidate
        draw_frame(g, 2, 2, 6, 5, 4)
        draw_frame(g, 2, w - 5, 6, w - 2, 4)
        return g
    if name == "no_frame":
        # marker but no yellow frame — fill target undefined
        g[2][3] = 6
        return g
    if name == "marker_adjacent_to_two":
        # marker between two frames → ambiguous which to fill
        draw_frame(g, 2, 2, 5, 5, 4)
        draw_frame(g, 2, 7, 5, 10, 4)
        g[3][6] = 7  # between both frames
        return g
    return g
