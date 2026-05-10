"""Generator for puzzle 18286ef8.

Rule: bg=anything; one yellow(9) cell + one magenta(6) cell. Compute
single-step direction from 9 toward 6. Output: paint old 9 position
gray(5), paint one-step-toward-6 cell as 9, paint 6 position as 9.

Combinatorial axes (8): grid_h/w, bg_color, frame_kind, frame_color,
distance_lo, distance_hi, position_bias, anchor_corner.
Degenerates: same_position, no_six, three_nines.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect_outline

GENERATOR_ID = "a85f5274d2ae"
VERSION = "1.1.0"
TASK_ID = "a85f5274d2ae"
SUMMARY = "9 + 6 markers; rule paints one-step-toward path with 5/9."

INVARIANTS = [
    "exactly one cell of color 9",
    "exactly one cell of color 6",
    "the 9 starts >=2 cells from the 6 (so the rule moves it)",
    "frame is rect outline of frame_color (default 3)",
]

FRAME_KINDS = ("rect_outline", "thick_rect", "diagonal_frame",
               "no_frame", "corner_marks")
DEGENERATE_TEXTURES = ("same_position", "no_six", "three_nines")
HELPFUL_TEXTURES = FRAME_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..14", "valid": "5..20"},
    "grid_w":         {"type": "int", "default": "rng 8..14", "valid": "5..20"},
    "bg_color":       {"type": "color", "default": "5",
                       "valid": "1..9 (≠6,9)"},
    "frame_kind":     {"type": "str", "default": "rng helpful",
                       "valid": "|".join(FRAME_KINDS)},
    "frame_color":    {"type": "color", "default": "3",
                       "valid": "1..9 (≠6,9,bg)"},
    "min_distance":   {"type": "int", "default": "2", "valid": "2..5"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "texture":        {"type": "str", "default": "alias for frame_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 5, 9
    elif difficulty == "hard":
        h_lo, h_hi = 14, 20
    else:
        h_lo, h_hi = 8, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    bg_color = int(overrides.get("bg_color", 5))
    frame_kind = (overrides.get("texture") or
                  overrides.get("frame_kind")
                  or ctx.draw_choice("frame_kind", list(FRAME_KINDS)))
    frame_color = int(overrides.get("frame_color", 3))
    if frame_color in (bg_color, 6, 9):
        frame_color = next((c for c in [3, 4, 7, 8, 1, 2]
                            if c not in (bg_color, 6, 9)), 3)
    min_dist = int(overrides.get("min_distance", 2))
    g = full_grid(h, w, bg_color)
    _draw_frame(g, frame_kind, h, w, frame_color)
    r9 = rng.randint(2, h - 3)
    c9 = rng.randint(2, w - 3)
    candidates = [
        (r, c)
        for r in range(1, h - 1)
        for c in range(1, w - 1)
        if abs(r - r9) >= min_dist or abs(c - c9) >= min_dist
        if (r, c) != (r9, c9)
    ]
    r6, c6 = rng.choice(candidates)
    g[r9][c9] = 9
    g[r6][c6] = 6
    return g


def _draw_frame(g, kind, h, w, color):
    if kind == "rect_outline":
        draw_rect_outline(g, 1, 1, h - 2, w - 2, color)
    elif kind == "thick_rect":
        draw_rect_outline(g, 0, 0, h, w, color)
        draw_rect_outline(g, 1, 1, h - 2, w - 2, color)
    elif kind == "diagonal_frame":
        for i in range(min(h, w)):
            if 0 <= i < h and 0 <= i < w:
                g[i][i] = color
    elif kind == "no_frame":
        pass
    elif kind == "corner_marks":
        for r, c in [(0, 0), (0, w - 1), (h - 1, 0), (h - 1, w - 1)]:
            g[r][c] = color
    else:
        draw_rect_outline(g, 1, 1, h - 2, w - 2, color)


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 5)
    if name == "same_position":
        # Rule's first cell is the only one; one cell can't be both
        g[h // 2][w // 2] = 9
        return g
    if name == "no_six":
        g[h // 2][w // 2] = 9
        return g
    if name == "three_nines":
        for r, c in [(2, 2), (h - 3, w - 3), (2, w - 3)]:
            g[r][c] = 9
        g[3][3] = 6
        return g
    return g
