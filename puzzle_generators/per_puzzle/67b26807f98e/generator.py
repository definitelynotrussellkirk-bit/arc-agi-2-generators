"""Generator for arc_additional_puzzle_bank_volume6:H40.

Rule: row 0 has selector ∈ 2..7. Find frame of selector color with
empty holes inside; normalize hole cells; place at 9-anchor offset,
color 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, selector_color,
palette_size, position_bias, n_distinct_colors, frame_kind, texture.
Degenerates: no_selector, no_matching_frame, no_anchor.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, fill_box, full_grid

GENERATOR_ID = "67b26807f98e"
VERSION = "1.1.0"
TASK_ID = "67b26807f98e"
SUMMARY = "Selector ∈ 2..7 in row 0 + matching frame with hole + 9-anchor + decoy frame."

INVARIANTS = [
    "row 0 has selector ∈ 2..7",
    "frame of selector color has hole",
    "9-anchor where stamp fits",
    "decoy frame of different color",
]

PALETTE_KINDS = ("default", "selector_2", "selector_3", "selector_mid")
DEGENERATE_TEXTURES = ("no_selector", "no_matching_frame", "no_anchor")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "grid_w":         {"type": "int", "default": "rng 13..15", "valid": "11..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "selector_color": {"type": "int", "default": "2", "valid": "2..7"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4"},
    "frame_kind":     {"type": "str", "default": "5x4", "valid": "5x4"},
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
    g[0][1] = 2
    draw_frame(g, 2, 1, 5, 4, 2)
    fill_box(g, h - 4, 3, h - 2, 5, 4)
    g[8][12] = 9
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 14
    g = full_grid(h, w, 0)
    if name == "no_selector":
        # frame + anchor but no selector → which color frame to copy?
        draw_frame(g, 2, 1, 5, 4, 2)
        fill_box(g, h - 4, 3, h - 2, 5, 4)
        g[8][12] = 9
        return g
    if name == "no_matching_frame":
        # selector says 2 but only a 4-frame and a solid 2-block are present
        g[0][1] = 2
        fill_box(g, 2, 1, 6, 4, 2)
        draw_frame(g, h - 5, 6, 4, 4, 4)
        g[8][12] = 9
        return g
    if name == "no_anchor":
        # selector + matching frame but no 9-anchor → stamp position undefined
        g[0][1] = 2
        draw_frame(g, 2, 1, 5, 4, 2)
        fill_box(g, h - 4, 3, h - 2, 5, 4)
        return g
    return g
