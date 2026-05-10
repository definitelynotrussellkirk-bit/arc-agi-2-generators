"""Generator for arc_additional_puzzle_bank_volume12:M80.

Rule: control = first non-{0,1,2} ∈ {6,7,8,9}; rot_count = control - 6.
Rotate 2-template cw rot_count times; stamp at 1-anchor in color 4.

Combinatorial axes (8): grid_h, grid_w, palette_kind, control,
palette_size, position_bias, n_distinct_colors, anchor_pos, texture.
Degenerates: no_control, no_template, no_anchor.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f34f99f28c2d"
VERSION = "1.1.0"
TASK_ID = "f34f99f28c2d"
SUMMARY = "Control ∈ {6,7,8,9} at top-left + 2-template + 1-anchor for stamping."

INVARIANTS = [
    "(0,0) is control ∈ {6,7,8,9}",
    "exactly one 2-template (size 3-4) in upper-left",
    "exactly one 1-anchor where stamps fit in-bounds",
]

PALETTE_KINDS = ("default", "rot_0_or_1", "rot_2", "rot_3")
DEGENERATE_TEXTURES = ("no_control", "no_template", "no_anchor")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..12", "valid": "8..16"},
    "grid_w":         {"type": "int", "default": "rng 12..14", "valid": "10..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "control":        {"type": "int", "default": "rng 6..9", "valid": "6..9"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "anchor_pos":     {"type": "str", "default": "interior", "valid": "interior"},
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
        w = ctx.draw_int("grid_w", 12, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 10, 12)
        w = ctx.draw_int("grid_w", 12, 14)
    control = ctx.draw_int("control", 6, 9)
    g = full_grid(h, w, 0)
    g[0][0] = control
    g[1][1] = 2
    g[2][1] = 2
    g[3][1] = 2; g[3][2] = 2
    g[6][8] = 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 13
    g = full_grid(h, w, 0)
    if name == "no_control":
        # template + anchor but no control → rotation count undefined
        g[1][1] = 2; g[2][1] = 2
        g[3][1] = 2; g[3][2] = 2
        g[6][8] = 1
        return g
    if name == "no_template":
        # control + anchor but no 2-template → nothing to rotate or stamp
        g[0][0] = 7
        g[6][8] = 1
        return g
    if name == "no_anchor":
        # control + template but no 1-anchor → stamp position undefined
        g[0][0] = 7
        g[1][1] = 2; g[2][1] = 2
        g[3][1] = 2; g[3][2] = 2
        return g
    return g
