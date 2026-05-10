"""Generator for arc_additional_puzzle_bank_volume19:E133.

Rule: each 4-blob with bbox 3×3 and size 8 (a 3×3 frame with hollow
center) → set the 1 interior cell to 1.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_3x3_frames,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_3x3_frames, all_4x4_frames, frame_already_filled.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect_outline

GENERATOR_ID = "0d863ca6dad6"
VERSION = "1.1.0"
TASK_ID = "0d863ca6dad6"
SUMMARY = "2-3 hollow 3×3 4-frames + 1 distractor non-3×3 4-blob."

INVARIANTS = [
    "≥2 hollow 3×3 4-frames",
    "1 non-3×3 4-blob (e.g. 4×4 frame, won't qualify)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_3x3_frames", "all_4x4_frames", "frame_already_filled")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 14..16", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_3x3_frames":   {"type": "int", "default": "2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "left_3x3_right_4x4",
                       "valid": "left_3x3_right_4x4"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
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
        h = ctx.draw_int("grid_h", 9, 9)
        w = ctx.draw_int("grid_w", 14, 14)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 15, 16)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 14, 16)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    r1 = rng.randint(0, h - 4)
    draw_rect_outline(g, r1, 0, 3, 3, 4)
    r2 = rng.randint(0, h - 4)
    draw_rect_outline(g, r2, 4, 3, 3, 4)
    r3 = rng.randint(0, h - 5)
    draw_rect_outline(g, r3, w - 5, 4, 4, 4)
    g[h - 1][9] = 7
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 15
    g = full_grid(h, w, 0)
    if name == "no_3x3_frames":
        # only 4x4 frames → no qualifying frame, rule has no targets
        draw_rect_outline(g, 1, 1, 4, 4, 4)
        draw_rect_outline(g, 1, 7, 4, 4, 4)
        g[h - 1][9] = 7
        return g
    if name == "all_4x4_frames":
        # alias for no qualifying frames
        draw_rect_outline(g, 1, 1, 4, 4, 4)
        draw_rect_outline(g, 5, 7, 4, 4, 4)
        return g
    if name == "frame_already_filled":
        # 3x3 frame with center already non-bg → rule is identity here
        draw_rect_outline(g, 2, 2, 3, 3, 4)
        g[3][3] = 1
        return g
    return g
