"""Generator for e619ca6e.

Rule: green rectangle seeds repeated horizontal blocks below it,
expanding left and right by block width.

Combinatorial axes (8): grid_h/w, rect_size, palette_kind,
position_bias, anchor_corner, asymmetry_force, palette_size, rect_color.
Degenerates: no_rect, full_grid, single_cell.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1856980929fe"
VERSION = "1.1.0"
TASK_ID = "1856980929fe"
SUMMARY = "Green rectangle seeds repeated horizontal blocks below it."

INVARIANTS = [
    "background is color 0",
    "one solid color-3 rectangle has a detectable top-left corner",
    "the rectangle height and width define the downward repeat spacing",
    "lower repetitions spread symmetrically left and right",
]

RECT_SIZES = ("2x2", "2x3", "3x2", "3x3")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_rect", "full_grid", "single_cell")
HELPFUL_TEXTURES = RECT_SIZES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "grid_w":         {"type": "int", "default": "rng 12..16", "valid": "10..20"},
    "rect_size":      {"type": "str", "default": "rng helpful",
                       "valid": "|".join(RECT_SIZES)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "position_bias":  {"type": "str", "default": "centered",
                       "valid": "centered|left|right|rng"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "texture":        {"type": "str", "default": "alias for rect_size",
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
    elif difficulty == "hard":
        h_lo, h_hi = 13, 16
    else:
        h_lo, h_hi = 10, 13
    size = (overrides.get("texture") if overrides.get("texture") in RECT_SIZES else None) or \
           overrides.get("rect_size") or \
           ctx.draw_choice("rect_size", list(RECT_SIZES))
    rh, rw = (int(x) for x in size.split("x"))
    h = rng.randint(h_lo, h_hi)
    w = rng.randint(h_lo + 2, h_hi + 4)
    g = full_grid(h, w, 0)
    bias = overrides.get("position_bias", "centered")
    if bias == "left":
        c0 = 1
    elif bias == "right":
        c0 = w - rw - 1
    else:
        c0 = w // 2 - rw // 2
    r0 = 1
    for r in range(r0, r0 + rh):
        for c in range(c0, c0 + rw):
            if 0 <= r < h and 0 <= c < w:
                g[r][c] = 3
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 14
    g = full_grid(h, w, 0)
    if name == "no_rect":
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 3
        return g
    if name == "single_cell":
        g[3][6] = 3
        return g
    return g
