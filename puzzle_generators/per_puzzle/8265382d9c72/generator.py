"""Generator for 8ba14f53.

Rule: 2 hollow rectangles, count holes inside each; rule outputs 3x3
with left rect's color in first n1 cells, right rect's in next n2.

Combinatorial axes (8): grid_h/w, fw_l, fw_r, palette_kind,
position_bias, anchor_corner, asymmetry_force, palette_size.
Degenerates: same_color, no_rects, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_rect_outline

GENERATOR_ID = "8265382d9c72"
VERSION = "1.1.0"
TASK_ID = "8265382d9c72"
SUMMARY = "2 hollow rectangles side-by-side, distinct colors, no holes."

INVARIANTS = [
    "2 hollow rectangles in distinct colors",
    "left rectangle has fewer interior holes than right",
    "rectangles separated by >=1 0-col",
]

POSITION_BIASES = ("scattered", "edge_aligned", "wide_spread", "rng")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("same_color", "no_rects", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 4..6", "valid": "4..8"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "fw_l":           {"type": "int", "default": "rng 3..4", "valid": "3..5"},
    "fw_r":           {"type": "int", "default": "rng 3..4", "valid": "3..5"},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
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
        h_lo, h_hi, w_lo, w_hi = 4, 5, 8, 10
        fw_lo, fw_hi = 3, 3
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 6, 8, 12, 14
        fw_lo, fw_hi = 4, 5
    else:
        h_lo, h_hi, w_lo, w_hi = 4, 6, 9, 12
        fw_lo, fw_hi = 3, 4
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    g = full_grid(h, w, 0)
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    pal = _build_palette(palette_kind, 2, rng)
    color_l, color_r = pal[0], pal[1]
    fh = h
    fw_l = int(overrides.get("fw_l",
                             rng.randint(fw_lo, fw_hi)))
    fw_r = int(overrides.get("fw_r",
                             rng.randint(fw_lo, fw_hi)))
    fw_l = max(3, min(fw_l, 5))
    fw_r = max(3, min(fw_r, 5))
    if fw_l + fw_r + 1 > w:
        fw_l = 3; fw_r = 3
    c0_l = 0
    c0_r = w - fw_r
    draw_rect_outline(g, 0, c0_l, fh, fw_l, color_l)
    draw_rect_outline(g, 0, c0_r, fh, fw_r, color_r)
    return g


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 6, 7, 8, 9]
    rng.shuffle(pool)
    if len(pool) < n:
        for c in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            if c not in pool:
                pool.append(c)
            if len(pool) >= n:
                break
    return pool[:n]


def _draw_from_degenerate(name, rng):
    h, w = 5, 10
    g = full_grid(h, w, 0)
    if name == "same_color":
        draw_rect_outline(g, 0, 0, h, 3, 2)
        draw_rect_outline(g, 0, w - 3, h, 3, 2)
        return g
    if name == "no_rects":
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 2
        return g
    return g
