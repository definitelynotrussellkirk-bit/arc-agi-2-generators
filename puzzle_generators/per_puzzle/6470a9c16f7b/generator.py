"""Generator for arc_puzzle_bank_21_set11_s:S11_H1 — Fill nested frame interiors with frame color.

Rule: each rect-frame blob → fill 0-cells inside its bbox with the
frame's color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, frame_h, frame_w,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_frame, no_inner_shape, frame_too_small.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at, draw_rect_outline

GENERATOR_ID = "6470a9c16f7b"
VERSION = "1.1.0"
TASK_ID = "6470a9c16f7b"
SUMMARY = "Outer frame ≥5×5 with one inner shape preserved during fill."

INVARIANTS = [
    "1 outer hollow rect-frame ≥5×5",
    "1 inner shape (color != frame) inside the frame",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_frame", "no_inner_shape", "frame_too_small")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "frame_h":        {"type": "int", "default": "rng 5..h", "valid": "5..14"},
    "frame_w":        {"type": "int", "default": "rng 7..w", "valid": "5..16"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "frame_with_inner",
                       "valid": "frame_with_inner"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
    "density":        {"type": "str", "default": "frame", "valid": "frame"},
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
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 11, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 11, 13)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    pal = rng.sample([2, 3, 4, 5, 6, 7, 8, 9], 2)
    fr = rng.randint(5, h - 1); fc = rng.randint(7, w - 1)
    r0 = rng.randint(0, h - fr); c0 = rng.randint(0, w - fc)
    draw_rect_outline(g, r0, c0, fr, fc, pal[0])
    bar = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)]
    paint_at(g, r0 + rng.randint(1, fr - 2), c0 + 2, bar, pal[1])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 12
    g = full_grid(h, w, 0)
    if name == "no_frame":
        # only an inner shape, no outer frame → nothing to fill around
        bar = [(0, 0), (0, 1), (0, 2), (0, 3)]
        paint_at(g, 4, 3, bar, 6)
        return g
    if name == "no_inner_shape":
        # frame with empty interior → fill replaces all interior cells
        draw_rect_outline(g, 1, 1, 6, 8, 4)
        return g
    if name == "frame_too_small":
        # 3x3 frame has 1 interior cell, fill is trivially a single pixel
        draw_rect_outline(g, 2, 2, 3, 3, 4)
        return g
    return g
