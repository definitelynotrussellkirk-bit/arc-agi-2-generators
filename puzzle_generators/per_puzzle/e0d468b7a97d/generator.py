"""Generator for arc_additional_puzzles_21_set20_bundle:E138 -- crop inside 9 frame.

Combinatorial axes (8): grid_h, grid_w, palette_kind, frame_h,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_frame, frame_open_side, multiple_frames.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e0d468b7a97d"
VERSION = "1.1.0"
TASK_ID = "e0d468b7a97d"
SUMMARY = "A color-9 rectangular frame encloses the crop returned as output."

INVARIANTS = [
    "color 9 marks the full outside frame of the target crop",
    "frame interior contains nonzero content",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frame", "frame_open_side", "multiple_frames")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "8..15"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "frame_h":        {"type": "int", "default": "rng 4..6", "valid": "3..8"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..4"},
    "position_bias":  {"type": "str", "default": "interior", "valid": "interior"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 9, 13)
    colors = list(ctx.draw_distinct_colors("colors", n=2, exclude=[0, 9]))
    g = full_grid(h, w, 0)
    fh = ctx.draw_int("frame_h", 4, min(6, h - 2))
    fw = ctx.draw_int("frame_w", 5, min(7, w - 2))
    top = ctx.draw_int("top", 1, h - fh - 1)
    left = ctx.draw_int("left", 1, w - fw - 1)
    for r in range(top, top + fh):
        g[r][left] = 9
        g[r][left + fw - 1] = 9
    for c in range(left, left + fw):
        g[top][c] = 9
        g[top + fh - 1][c] = 9
    g[top + 1][left + 1] = colors[0]
    g[top + 1][left + fw - 2] = colors[1]
    g[top + fh - 2][left + 2] = colors[0]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 11
    g = full_grid(h, w, 0)
    if name == "no_frame":
        # no color-9 frame → rule has no anchor for cropping
        for r, c, v in [(2, 3, 4), (4, 5, 6), (6, 7, 4)]:
            g[r][c] = v
        return g
    if name == "frame_open_side":
        # frame is missing one side → bbox of 9-cells is fine but enclosure invariant breaks
        top, left, fh, fw = 2, 2, 5, 6
        for r in range(top, top + fh):
            g[r][left] = 9
            g[r][left + fw - 1] = 9
        for c in range(left, left + fw):
            g[top + fh - 1][c] = 9  # top side missing
        g[top + 1][left + 1] = 4
        g[top + 1][left + fw - 2] = 6
        return g
    if name == "multiple_frames":
        # two color-9 frames → ambiguous which to crop
        for top, left, fh, fw, c1 in [(1, 1, 4, 4, 4), (5, 6, 4, 4, 6)]:
            for r in range(top, top + fh):
                g[r][left] = 9
                g[r][left + fw - 1] = 9
            for c in range(left, left + fw):
                g[top][c] = 9
                g[top + fh - 1][c] = 9
            g[top + 1][left + 1] = c1
        return g
    return g
