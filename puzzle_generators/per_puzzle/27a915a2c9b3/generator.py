"""Generator for a04b2602.

Rule: interior color-2 cells inside valid color-3 components receive a
surrounding 3x3 box of color 1.

Combinatorial axes (8): grid_h/w, marker_count, rect_h, rect_w,
position_bias, palette_kind, anchor_corner, asymmetry_force.
Degenerates: no_markers, no_rect, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import fill_box, full_grid

GENERATOR_ID = "27a915a2c9b3"
VERSION = "1.1.0"
TASK_ID = "27a915a2c9b3"
SUMMARY = "Interior color-2 cells in color-3 components receive 3x3 box of color 1."

INVARIANTS = [
    "background is color 0",
    "a color-3 component's bbox contains only colors 3 and 2",
    "the color-2 cells inside that bbox are the marked interiors",
    "the rule paints color 1 around each marked cell except on other marked interiors",
]

POSITION_BIASES = ("centered", "corner", "near_edge", "scattered")
DEGENERATE_TEXTURES = ("no_markers", "no_rect", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..12", "valid": "8..16"},
    "grid_w":         {"type": "int", "default": "rng 10..12", "valid": "8..16"},
    "marker_count":   {"type": "int", "default": "2", "valid": "1..4"},
    "rect_h":         {"type": "int", "default": "rng 4..5", "valid": "3..7"},
    "rect_w":         {"type": "int", "default": "rng 4..5", "valid": "3..7"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
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
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h_lo, h_hi = 8, 10
        rh_lo, rh_hi = 3, 4
    elif difficulty == "hard":
        h_lo, h_hi = 12, 16
        rh_lo, rh_hi = 5, 7
    else:
        h_lo, h_hi = 10, 12
        rh_lo, rh_hi = 4, 5
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    g = full_grid(h, w, 0)
    rh = int(overrides.get("rect_h",
                           rng.randint(rh_lo, rh_hi)))
    rw = int(overrides.get("rect_w",
                           rng.randint(rh_lo, rh_hi)))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias", list(POSITION_BIASES)))
    if bias == "centered":
        r1 = max(1, (h - rh) // 2)
        c1 = max(1, (w - rw) // 2)
    elif bias == "corner":
        r1 = rng.choice([1, max(1, h - rh - 2)])
        c1 = rng.choice([1, max(1, w - rw - 2)])
    elif bias == "near_edge":
        if rng.random() < 0.5:
            r1 = rng.choice([1, max(1, h - rh - 2)])
            c1 = rng.randint(1, max(1, w - rw - 2))
        else:
            r1 = rng.randint(1, max(1, h - rh - 2))
            c1 = rng.choice([1, max(1, w - rw - 2)])
    else:
        r1 = 1 + rng.randint(0, max(0, h - rh - 2))
        c1 = 1 + rng.randint(0, max(0, w - rw - 2))
    r1 = max(1, min(r1, h - rh - 1))
    c1 = max(1, min(c1, w - rw - 1))
    r2 = min(h - 2, r1 + rh - 1)
    c2 = min(w - 2, c1 + rw - 1)
    fill_box(g, r1, c1, r2, c2, 3)
    if r1 + 2 <= r2 and c1 + 2 <= c2:
        g[r1 + 2][c1 + 2] = 2
    if r1 + 1 <= r2 and c2 - 1 >= c1:
        g[r1 + 1][c2 - 1] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 11
    g = full_grid(h, w, 0)
    if name == "no_markers":
        fill_box(g, 2, 2, 6, 7, 3)
        return g
    if name == "no_rect":
        g[5][5] = 2
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 3
        return g
    return g
