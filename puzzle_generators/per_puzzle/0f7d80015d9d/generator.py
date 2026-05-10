"""Generator for puzzle e4941b18.

Rule: bg=7, gray(5) rect at bottom rows, single 2-cell + single 8-cell
above. Output: 2↔8 swap (2→7, 8→2), then place new 8 at bottom-row of
gray rect, just outside the rect on the side opposite to the 2's
horizontal half.

Combinatorial axes (8): grid_h/w, rect_h, rect_w, rect_position,
twos_side, twos_row_offset, eights_position, asymmetry_force.
Degenerates: rect_at_top, no_above_space, twos_eights_same_col.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect

GENERATOR_ID = "0f7d80015d9d"
VERSION = "1.1.0"
TASK_ID = "0f7d80015d9d"
SUMMARY = "7-bg with 5-rect at bottom + single 2-cell and 8-cell above."

INVARIANTS = [
    "bg = 7",
    "exactly one solid 5-rectangle, >=3 wide, at bottom rows",
    "exactly one cell of color 2 above the rect, in rect's column span",
    "exactly one cell of color 8 above the rect, in rect's column span",
    "rect's mid-col defines a left/right half for the 2",
    "destination col for new 8 is in-bounds",
]

RECT_ASPECTS = ("wide", "tall", "square")
TWOS_SIDES = ("left", "right")
DEGENERATE_TEXTURES = ("rect_at_top", "no_above_space", "twos_eights_same_col")
HELPFUL_TEXTURES = RECT_ASPECTS

AXES = {
    "grid_h":        {"type": "int", "default": "rng 8..12", "valid": "6..14"},
    "grid_w":        {"type": "int", "default": "rng 9..13", "valid": "8..16"},
    "rect_aspect":   {"type": "str", "default": "rng helpful",
                      "valid": "|".join(RECT_ASPECTS)},
    "rect_h":        {"type": "int", "default": "rng 3..5", "valid": "3..6"},
    "rect_w":        {"type": "int", "default": "rng 4..6", "valid": "3..8"},
    "twos_side":     {"type": "str", "default": "rng left|right",
                      "valid": "|".join(TWOS_SIDES)},
    "twos_row_offset":{"type": "int", "default": "rng 0..rect_r-1",
                       "valid": "0..rect_r-1"},
    "anchor_corner": {"type": "bool", "default": "false",
                      "valid": "true|false"},
    "texture":       {"type": "str", "default": "alias for rect_aspect",
                      "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 6, 9
    elif difficulty == "hard":
        h_lo, h_hi = 11, 14
    else:
        h_lo, h_hi = 8, 12
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo + 1, h_hi + 2)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    aspect = (overrides.get("texture") or
              overrides.get("rect_aspect")
              or ctx.draw_choice("rect_aspect", list(RECT_ASPECTS)))
    if aspect == "wide":
        rect_h = rng.randint(2, 4)
        rect_w = rng.randint(min(5, w - 2), min(7, w - 2))
    elif aspect == "tall":
        rect_h = rng.randint(min(4, h - 3), min(6, h - 3))
        rect_w = rng.randint(3, 4)
    else:
        sz = rng.randint(3, min(min(h - 3, w - 2), 5))
        rect_h = sz; rect_w = sz
    rect_h = max(2, min(h - 3, rect_h))
    rect_w = max(3, min(w - 2, rect_w))
    rect_r = h - rect_h
    rect_c = rng.randint(1, w - rect_w - 1)
    g = [[7] * w for _ in range(h)]
    draw_rect(g, rect_r, rect_c, rect_h, rect_w, 5)
    twos_side = overrides.get("twos_side",
                              ctx.draw_choice("twos_side", list(TWOS_SIDES)))
    mid_c = (2 * rect_c + rect_w - 1) // 2
    rect_left = rect_c
    rect_right = rect_c + rect_w - 1
    if twos_side == "left":
        c2 = rng.randint(rect_left, mid_c)
    else:
        c2 = rng.randint(mid_c + 1, rect_right) if mid_c + 1 <= rect_right else rect_right
    above_row_2 = rng.randint(0, max(0, rect_r - 1))
    g[above_row_2][c2] = 2
    placed_8 = False
    for _ in range(40):
        ar = rng.randint(0, max(0, rect_r - 1))
        ac = rng.randint(rect_left, rect_right)
        if g[ar][ac] == 7 and (ar, ac) != (above_row_2, c2):
            g[ar][ac] = 8
            placed_8 = True
            break
    if not placed_8:
        for ar in range(0, rect_r):
            for ac in range(rect_left, rect_right + 1):
                if g[ar][ac] == 7 and (ar, ac) != (above_row_2, c2):
                    g[ar][ac] = 8
                    placed_8 = True
                    break
            if placed_8:
                break
    return g


def _draw_from_degenerate(name, h, w, rng):
    g = [[7] * w for _ in range(h)]
    if name == "rect_at_top":
        rect_h = 3; rect_w = 5
        draw_rect(g, 0, 1, rect_h, rect_w, 5)
        g[5][2] = 2
        g[5][4] = 8
        return g
    if name == "no_above_space":
        rect_h = h - 1; rect_w = w - 2
        draw_rect(g, 1, 1, rect_h, rect_w, 5)
        g[0][2] = 2
        g[0][3] = 8
        return g
    if name == "twos_eights_same_col":
        rect_h = 3; rect_w = 5
        rect_r = h - rect_h; rect_c = 1
        draw_rect(g, rect_r, rect_c, rect_h, rect_w, 5)
        g[1][rect_c + 2] = 2
        g[2][rect_c + 2] = 8
        return g
    return g
