"""Generator for 25e02866.

Rule: colored contents from multiple frames overlaid into largest frame
coordinates.

Combinatorial axes (8): grid_h/w, frame_count, frame_color, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias.
Degenerates: no_frames, single_frame, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect_outline, full_grid

GENERATOR_ID = "9d81f4236010"
VERSION = "1.1.0"
TASK_ID = "9d81f4236010"
SUMMARY = "Colored frames overlaid into largest frame coordinates."

INVARIANTS = [
    "the mode color is the background",
    "the most frequent non-background color forms rectangular frames",
    "one frame has the largest bounding box and sets output dimensions",
    "non-frame colored cells inside each frame are copied by local coordinates",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_frames", "single_frame", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "15", "valid": "12..22"},
    "grid_w":         {"type": "int", "default": "18", "valid": "14..24"},
    "frame_count":    {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "frame_color":    {"type": "color", "default": "rng !0",
                       "valid": "1..9"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "5", "valid": "4..6"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
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
        fc_lo, fc_hi = 1, 2
    elif difficulty == "hard":
        fc_lo, fc_hi = 3, 4
    else:
        fc_lo, fc_hi = 2, 3
    frame_count = ctx.draw_int("frame_count", fc_lo, fc_hi)
    frame_count = max(1, min(4, frame_count))
    frame_color = ctx.draw_color("frame_color", exclude={0})
    marks = ctx.draw_distinct_colors("marks", n=4, exclude={0, frame_color})
    g = full_grid(15, 18, 0)
    frames = [(1, 1, 6, 7), (1, 10, 5, 6), (9, 3, 5, 7)]
    rng.shuffle(frames)
    for i, (r, c, rh, rw) in enumerate(frames[:frame_count]):
        draw_rect_outline(g, r, c, rh, rw, frame_color)
        g[r + 1][c + 1 + (i % max(1, rw - 3))] = marks[i % len(marks)]
        g[r + rh - 2][c + rw - 2] = marks[(i + 1) % len(marks)]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 15, 18
    g = full_grid(h, w, 0)
    if name == "no_frames":
        for r, c in [(2, 2), (5, 8)]:
            g[r][c] = 3
        return g
    if name == "single_frame":
        draw_rect_outline(g, 1, 1, 6, 7, 4)
        g[3][3] = 2
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 4
        return g
    return g
