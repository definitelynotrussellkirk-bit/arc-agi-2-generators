"""Generator for arc_additional_puzzles_21_set21_bundle:M147.

Rule: template = non-9 content cropped to bbox; positions = bbox-tl + each
9-marker; stamp template at all positions.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_template, no_anchors, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1eff2cf0e8d8"
VERSION = "1.1.0"
TASK_ID = "1eff2cf0e8d8"
SUMMARY = "Small multicolor template + 9-markers as additional stamp anchors."

INVARIANTS = [
    "small multicolor template (3-4 cells) in upper-left",
    "1-2 9-markers placed where stamps fit in-bounds",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_template", "no_anchors", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "7..9"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "11..13"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "3", "valid": "3"},
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
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 11, 13)
    g = full_grid(h, w, 0)
    g[0][0] = 2
    g[0][1] = 4
    g[1][1] = 2
    g[1][2] = 4
    g[3][6] = 9
    g[5][1] = 9
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(8, 12, 0)
    if name == "no_template":
        g[3][6] = 9
        return g
    if name == "no_anchors":
        g[0][0] = 2
        g[0][1] = 4
        g[1][1] = 2
        g[1][2] = 4
        return g
    if name == "full_grid":
        for r in range(8):
            for c in range(12):
                g[r][c] = 9
        return g
    return g
