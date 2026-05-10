"""Generator for arc_puzzle_bank_21_set12_bundle:easy_l05.

Rule: each hollow rect-frame with both dims odd → set its bbox center
to the frame color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_frames,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: even_dims, no_frames, frame_too_small.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect_outline

GENERATOR_ID = "e5dc3d423bd9"
VERSION = "1.1.0"
TASK_ID = "e5dc3d423bd9"
SUMMARY = "1-2 hollow rect-frames with odd dimensions ≥3."

INVARIANTS = [
    "1-2 hollow rect-frames with both dims odd ≥3",
    "frames don't touch",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("even_dims", "no_frames", "frame_too_small")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 12..14", "valid": "10..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_frames":       {"type": "int", "default": "2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "left_right_frames",
                       "valid": "left_right_frames"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
    "density":        {"type": "str", "default": "frames", "valid": "frames"},
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
        h = ctx.draw_int("grid_h", 7, 7)
        w = ctx.draw_int("grid_w", 12, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 12, 14)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    pal = rng.sample([2, 3, 4, 5, 6, 7, 8, 9], 2)
    fr = rng.choice([3, 5]); fc = rng.choice([3, 5])
    r0 = rng.randint(0, h - fr); c0 = rng.randint(0, w // 2 - fc - 1)
    draw_rect_outline(g, r0, c0, fr, fc, pal[0])
    fr2 = rng.choice([3, 5]); fc2 = rng.choice([3, 5])
    r02 = rng.randint(0, h - fr2); c02 = rng.randint(w // 2 + 1, w - fc2)
    draw_rect_outline(g, r02, c02, fr2, fc2, pal[1])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 13
    g = full_grid(h, w, 0)
    if name == "even_dims":
        # frames with even dims → bbox has no integer center, rule has no target cell
        draw_rect_outline(g, 1, 1, 4, 4, 4)
        draw_rect_outline(g, 1, 8, 4, 4, 6)
        return g
    if name == "no_frames":
        # empty grid → no frames to mark centers of
        return g
    if name == "frame_too_small":
        # 1×1 frame → bbox is one cell, no hollow interior
        g[2][2] = 4
        g[5][8] = 6
        return g
    return g
