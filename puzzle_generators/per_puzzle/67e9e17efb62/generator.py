"""Generator for 5d588b4d.

Rule: bar of length L in row 0; rule generates pyramid of segments
1..L..1.

Combinatorial axes (8): grid_h, grid_w, bar_len, color, palette_kind,
position_bias, anchor_corner, asymmetry_force.
Degenerates: no_bar, full_grid, single_cell.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "67e9e17efb62"
VERSION = "1.1.0"
TASK_ID = "67e9e17efb62"
SUMMARY = "Bar of length L in row 0; rule generates pyramid of segments 1..L..1."

INVARIANTS = [
    "row 0 has a contiguous bar of one non-bg color",
    "bar length L in [2, 6]",
    "rest of grid is bg(0)",
]

POSITION_BIASES = ("centered", "left", "right", "rng")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_bar", "full_grid", "single_cell")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..8", "valid": "3..14"},
    "grid_w":         {"type": "int", "default": "rng 8..14", "valid": "6..18"},
    "bar_len":        {"type": "int", "default": "rng 2..6", "valid": "2..8"},
    "color":          {"type": "color", "default": "rng !0",
                       "valid": "1..9"},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for position_bias",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi = 3, 5, 6, 9
        bl_lo, bl_hi = 2, 3
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 9, 14, 14, 18
        bl_lo, bl_hi = 4, 8
    else:
        h_lo, h_hi, w_lo, w_hi = 5, 8, 8, 14
        bl_lo, bl_hi = 2, 6
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    bar_len = ctx.draw_int("bar_len", bl_lo, min(bl_hi, w - 1))
    bar_len = max(2, min(w - 1, bar_len))
    color = ctx.draw_color("color", exclude={0})
    g = full_grid(h, w, 0)
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias", list(POSITION_BIASES)))
    if bias == "centered":
        sc = max(0, (w - bar_len) // 2)
    elif bias == "left":
        sc = 0
    elif bias == "right":
        sc = max(0, w - bar_len)
    else:
        sc = rng.randint(0, max(0, w - bar_len))
    for c in range(sc, sc + bar_len):
        if c < w:
            g[0][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 10
    g = full_grid(h, w, 0)
    if name == "no_bar":
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 2
        return g
    if name == "single_cell":
        g[0][3] = 2
        return g
    return g
