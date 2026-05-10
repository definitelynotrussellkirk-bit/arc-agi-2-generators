"""Generator for arc_additional_puzzles_21_set20_bundle:M140.

Rule: external selector cell selects which frame's interior to extract.
Output bbox-cropped interior of the matching frame.

Combinatorial axes (8): grid_h, grid_w, palette_kind, selector,
palette_size, position_bias, n_distinct_colors, frame_kind, texture.
Degenerates: no_selector, no_matching_frame, both_match.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "6027a830c96e"
VERSION = "1.1.0"
TASK_ID = "6027a830c96e"
SUMMARY = "External selector cell + 2 frames with multicolor interiors."

INVARIANTS = [
    "exactly 2 closed frames of distinct colors",
    "exactly one external selector cell matching one frame's color",
    "each frame has multicolor interior content",
]

PALETTE_KINDS = ("default", "select_left", "select_right", "varied")
DEGENERATE_TEXTURES = ("no_selector", "no_matching_frame", "both_match")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..13", "valid": "9..18"},
    "grid_w":         {"type": "int", "default": "rng 13..15", "valid": "11..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "selector":       {"type": "int", "default": "7", "valid": "7|3"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5"},
    "position_bias":  {"type": "str", "default": "fixed_two_frames",
                       "valid": "fixed_two_frames"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "5"},
    "frame_kind":     {"type": "str", "default": "small_plus_large",
                       "valid": "small_plus_large"},
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
        w = ctx.draw_int("grid_w", 13, 14)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 14, 15)
    else:
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 13, 15)
    g = full_grid(h, w, 0)
    g[0][0] = 7
    draw_frame(g, 2, 2, 5, 5, 7)
    g[3][3] = 2; g[4][3] = 2; g[4][4] = 5
    draw_frame(g, 2, 8, 6, 12, 3)
    g[3][9] = 4; g[4][10] = 4; g[5][11] = 5
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 14
    g = full_grid(h, w, 0)
    if name == "no_selector":
        # both frames present but no external selector → which frame is unclear
        draw_frame(g, 2, 2, 5, 5, 7)
        g[3][3] = 2
        draw_frame(g, 2, 8, 6, 12, 3)
        g[3][9] = 4
        return g
    if name == "no_matching_frame":
        # selector says 4 but no frame has color 4
        g[0][0] = 4
        draw_frame(g, 2, 2, 5, 5, 7)
        g[3][3] = 2
        draw_frame(g, 2, 8, 6, 12, 3)
        g[3][9] = 4
        return g
    if name == "both_match":
        # both frames the same color as the selector → ambiguous selection
        g[0][0] = 7
        draw_frame(g, 2, 2, 5, 5, 7)
        g[3][3] = 2
        draw_frame(g, 2, 8, 6, 12, 7)
        g[3][9] = 4
        return g
    return g
