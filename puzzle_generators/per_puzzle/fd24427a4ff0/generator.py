"""Generator for 9772c176.

Rule: 8-trapezoid (narrower at top and bottom, wider in middle) gets
diamond apex extensions added above and below.

Combinatorial axes (8): grid_h/w, body_h, top_w, position_bias,
anchor_corner, asymmetry_force, palette_size, body_w_delta.
Degenerates: no_trapezoid, full_grid, single_row.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "fd24427a4ff0"
VERSION = "1.1.0"
TASK_ID = "fd24427a4ff0"
SUMMARY = "8-trapezoid narrower at top/bottom, wider in middle, gets apex extensions."

INVARIANTS = [
    "single 8-shape: trapezoid wider in middle than at top/bottom row",
    "trapezoid has at least three rows so top, body, bottom are distinct",
    "the shape sits clear of grid borders so apex extensions fit",
]

POSITION_BIASES = ("center", "top_left", "top_right", "bottom_left", "bottom_right")
DEGENERATE_TEXTURES = ("no_trapezoid", "full_grid", "single_row")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 18..22", "valid": "14..28"},
    "grid_w":         {"type": "int", "default": "rng 18..22", "valid": "14..28"},
    "body_h":         {"type": "int", "default": "rng 4..6", "valid": "3..8"},
    "top_w":          {"type": "int", "default": "rng 4..6", "valid": "3..8"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "body_w_delta":   {"type": "int", "default": "2", "valid": "1..3"},
    "texture":        {"type": "str", "default": "alias for position_bias",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h_lo, h_hi, b_lo, b_hi = 16, 18, 3, 4
    elif difficulty == "hard":
        h_lo, h_hi, b_lo, b_hi = 22, 26, 5, 7
    else:
        h_lo, h_hi, b_lo, b_hi = 18, 22, 4, 6
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    body_h = ctx.draw_int("body_h", b_lo, b_hi)
    top_w = ctx.draw_int("top_w", 4, 6)
    body_w = top_w + int(overrides.get("body_w_delta", 2))
    pos = (overrides.get("texture") if overrides.get("texture") in POSITION_BIASES else None) or \
          overrides.get("position_bias") or \
          ctx.draw_choice("position_bias", list(POSITION_BIASES))
    cr_max = h - 1 - body_h - 2
    cc_max = w - body_w - 3
    if pos == "top_left":
        cr, cc = 2, 3
    elif pos == "top_right":
        cr, cc = 2, max(3, cc_max)
    elif pos == "bottom_left":
        cr, cc = max(2, cr_max), 3
    elif pos == "bottom_right":
        cr, cc = max(2, cr_max), max(3, cc_max)
    else:
        cr = rng.randint(2, max(2, cr_max))
        cc = rng.randint(3, max(3, cc_max))
    g = full_grid(h, w, 0)
    top_off = (body_w - top_w) // 2
    for c in range(cc + top_off, cc + top_off + top_w):
        g[cr][c] = 8
    for r in range(cr + 1, cr + 1 + body_h):
        for c in range(cc, cc + body_w):
            g[r][c] = 8
    bot_off = (body_w - top_w) // 2
    for c in range(cc + bot_off, cc + bot_off + top_w):
        g[cr + 1 + body_h][c] = 8
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(20, 20, 0)
    if name == "no_trapezoid":
        return g
    if name == "single_row":
        for c in range(5, 12):
            g[10][c] = 8
        return g
    if name == "full_grid":
        for r in range(20):
            for c in range(20):
                g[r][c] = 8
        return g
    return g
