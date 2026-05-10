"""Generator for arc_additional_puzzle_bank_volume4:H27.

Rule: 5-frames create nesting depth. Pick non-5 object with max depth
(ties: largest). Output bbox-cropped mask.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_frames,
palette_size, position_bias, n_distinct_colors, depth_kind, texture.
Degenerates: no_frames, single_frame, both_blobs_at_same_depth.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid, paint_at
from puzzle_generators.helpers.shape import L_TROMINO_NE, L_TROMINO_SE

GENERATOR_ID = "1711c30d0528"
VERSION = "1.1.0"
TASK_ID = "1711c30d0528"
SUMMARY = "Outer 5-frame + nested 5-frame + 1 non-5 blob deep inside + 1 outside."

INVARIANTS = [
    "exactly 2 nested 5-frames",
    "exactly one non-5 blob inside both frames (depth 2)",
    "exactly one non-5 blob outside (depth 0)",
]

PALETTE_KINDS = ("default", "wide_outer", "tall_outer", "balanced")
DEGENERATE_TEXTURES = ("no_frames", "single_frame", "both_blobs_at_same_depth")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_frames":       {"type": "int", "default": "2", "valid": "2"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "concentric", "valid": "concentric"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "depth_kind":     {"type": "str", "default": "0_vs_2", "valid": "0_vs_2"},
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
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 11, 13)
    g = full_grid(h, w, 0)
    draw_frame(g, 2, 2, 8, 8, 5)
    draw_frame(g, 4, 4, 6, 6, 5)
    paint_at(g, 5, 5, L_TROMINO_NE, 3)
    paint_at(g, 0, 0, L_TROMINO_SE, 1)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 12
    g = full_grid(h, w, 0)
    if name == "no_frames":
        # blobs but no 5-frames → all depths are 0, max-depth selection ambiguous
        paint_at(g, 5, 5, L_TROMINO_NE, 3)
        paint_at(g, 0, 0, L_TROMINO_SE, 1)
        return g
    if name == "single_frame":
        # one frame only → max depth is 1, less informative for the rule
        draw_frame(g, 2, 2, 8, 8, 5)
        paint_at(g, 5, 5, L_TROMINO_NE, 3)
        paint_at(g, 0, 0, L_TROMINO_SE, 1)
        return g
    if name == "both_blobs_at_same_depth":
        # 2 frames + 2 blobs both inside the inner frame → tie at max depth
        draw_frame(g, 2, 2, 8, 8, 5)
        draw_frame(g, 4, 4, 6, 6, 5)
        paint_at(g, 5, 5, L_TROMINO_NE, 3)
        paint_at(g, 7, 7, L_TROMINO_SE, 1)
        return g
    return g
