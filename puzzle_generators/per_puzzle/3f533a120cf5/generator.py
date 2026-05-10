"""Generator for 278e5215.

Rule: gray mask selects colors from adjacent key row, with non-mask
cells filled by separator color.

Combinatorial axes (8): mask_h, mask_w, sep_color, palette_kind,
position_bias, anchor_corner, asymmetry_force, n_holes.
Degenerates: no_mask, no_key, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "3f533a120cf5"
VERSION = "1.1.0"
TASK_ID = "3f533a120cf5"
SUMMARY = "Gray mask + key row + separator; rule fills mask with key colors."

INVARIANTS = [
    "gray cells define the output mask and bounding box",
    "a uniform nonzero separator row sits outside the gray mask",
    "the key row adjacent to the separator provides one color per mask column",
    "gray mask cells become key colors and mask holes become separator color",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_mask", "no_key", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "mask_height":    {"type": "int", "default": "rng 3..5", "valid": "2..8"},
    "mask_width":     {"type": "int", "default": "rng 3..5", "valid": "2..8"},
    "sep_color":      {"type": "color", "default": "rng !{0,5}",
                       "valid": "1..9"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "position_bias":  {"type": "str", "default": "rng",
                       "valid": "centered|rng"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "n_holes":        {"type": "int", "default": "rng 1..3", "valid": "0..5"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
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
        mh_lo, mh_hi = 2, 3
        mw_lo, mw_hi = 2, 3
    elif difficulty == "hard":
        mh_lo, mh_hi = 5, 8
        mw_lo, mw_hi = 5, 8
    else:
        mh_lo, mh_hi = 3, 5
        mw_lo, mw_hi = 3, 5
    mh = ctx.draw_int("mask_height", mh_lo, mh_hi)
    mw = ctx.draw_int("mask_width", mw_lo, mw_hi)
    sep_color = ctx.draw_color("separator", exclude={0, 5})
    key_colors = ctx.draw_distinct_colors("key_colors", n=mw,
                                          exclude={0, 5, sep_color})
    h = mh + 6
    w = max(mw + 4, 8)
    c0 = rng.randint(1, w - mw - 1)
    r0 = 4
    g = full_grid(h, w, 0)
    for i, color in enumerate(key_colors):
        g[0][c0 + i] = color
    for c in range(w):
        g[1][c] = sep_color
    for r in range(mh):
        for c in range(mw):
            g[r0 + r][c0 + c] = 5
    n_holes = int(overrides.get("n_holes",
                                rng.randint(1, max(1, (mh * mw) // 4))))
    n_holes = max(0, min(mh * mw, n_holes))
    for _ in range(n_holes):
        hr = rng.randrange(mh)
        hc = rng.randrange(mw)
        if 0 < hr < mh - 1 or 0 < hc < mw - 1:
            g[r0 + hr][c0 + hc] = 0
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 9
    g = full_grid(h, w, 0)
    if name == "no_mask":
        for c in range(w):
            g[1][c] = 3
        for c, color in enumerate([2, 4, 6]):
            if 1 + c < w:
                g[0][1 + c] = color
        return g
    if name == "no_key":
        for c in range(w):
            g[1][c] = 3
        for r in range(4, 7):
            for c in range(2, 5):
                g[r][c] = 5
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 5
        return g
    return g
