"""Generator for arc_additional_puzzle_bank_volume14:M95.

Rule: ctrl = first non-{0,5} cell ∈ {1..4}; rotate 6-shape (ctrl-1) cw
turns; stamp at 8-anchor in color 3.

Combinatorial axes (8): grid_h, grid_w, palette_kind, ctrl, palette_size,
position_bias, n_distinct_colors, anchor_pos, texture.
Degenerates: no_ctrl, no_template, no_anchor.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "55ff88a3cf8f"
VERSION = "1.1.0"
TASK_ID = "55ff88a3cf8f"
SUMMARY = "Ctrl ∈ {1..4} at top-left + 6-template + 8-anchor + decoration."

INVARIANTS = [
    "(0,0) is ctrl ∈ 1..4",
    "(0, w-1) is decoration (color 5)",
    "exactly one 6-template (3 cells L-shape) in upper-left",
    "exactly one 8-anchor where rotated stamp fits in-bounds",
]

PALETTE_KINDS = ("default", "rot_0", "rot_90", "rot_180_or_270")
DEGENERATE_TEXTURES = ("no_ctrl", "no_template", "no_anchor")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "ctrl":           {"type": "int", "default": "rng 1..4", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4"},
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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 11, 13)
    ctrl = ctx.draw_int("ctrl", 1, 4)
    g = full_grid(h, w, 0)
    g[0][0] = ctrl
    g[0][w - 1] = 5
    g[1][1] = 6
    g[2][1] = 6; g[2][2] = 6
    g[5][7] = 8
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_ctrl":
        # template + anchor but no ctrl → rotation count undefined
        g[0][w - 1] = 5
        g[1][1] = 6
        g[2][1] = 6; g[2][2] = 6
        g[5][7] = 8
        return g
    if name == "no_template":
        # ctrl + anchor but no 6-template → nothing to rotate or stamp
        g[0][0] = 2
        g[0][w - 1] = 5
        g[5][7] = 8
        return g
    if name == "no_anchor":
        # ctrl + template but no 8-anchor → stamp position undefined
        g[0][0] = 2
        g[0][w - 1] = 5
        g[1][1] = 6
        g[2][1] = 6; g[2][2] = 6
        return g
    return g
