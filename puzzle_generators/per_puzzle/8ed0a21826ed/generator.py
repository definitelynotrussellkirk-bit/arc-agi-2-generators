"""Generator for 2c608aff.

Rule: small colored dots aligned to the largest rectangle draw beams
toward it.

Combinatorial axes (8): grid_h/w, dot_count, palette_kind, rect_h,
rect_w, anchor_corner, asymmetry_force, palette_size.
Degenerates: no_dots, no_rect, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "8ed0a21826ed"
VERSION = "1.1.0"
TASK_ID = "8ed0a21826ed"
SUMMARY = "Small dots aligned to largest rectangle draw beams toward it."

INVARIANTS = [
    "the top-left cell is the background color",
    "the largest non-background object is a solid rectangle",
    "small non-rectangle-color dots sit outside the rectangle",
    "aligned dots beam horizontally or vertically through background cells to the rectangle",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_dots", "no_rect", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 14..16", "valid": "12..20"},
    "grid_w":         {"type": "int", "default": "rng 14..16", "valid": "12..20"},
    "dot_count":      {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "rect_h":         {"type": "int", "default": "rng 3..5", "valid": "3..7"},
    "rect_w":         {"type": "int", "default": "rng 4..6", "valid": "3..8"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "5", "valid": "3..6"},
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
        h_lo, h_hi = 12, 14
        dc_lo, dc_hi = 1, 2
    elif difficulty == "hard":
        h_lo, h_hi = 16, 20
        dc_lo, dc_hi = 4, 8
    else:
        h_lo, h_hi = 14, 16
        dc_lo, dc_hi = 2, 4
    dot_count = ctx.draw_int("dot_count", dc_lo, dc_hi)
    rect_color = ctx.draw_color("rect_color", exclude={0})
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind")
                    or ctx.draw_choice("palette_kind",
                                       list(PALETTE_KINDS)))
    pool = _build_palette(palette_kind, rect_color, rng)
    if len(pool) < 4:
        pool = pool + [c for c in [1, 2, 3, 4, 5, 6, 7, 8, 9]
                       if c not in pool and c != rect_color]
    dot_colors = pool[:4]
    h = rng.randint(h_lo, h_hi)
    w = rng.randint(h_lo, h_hi)
    rh = int(overrides.get("rect_h", rng.randint(3, 5)))
    rw = int(overrides.get("rect_w", rng.randint(4, 6)))
    rh = max(3, min(rh, h - 6))
    rw = max(3, min(rw, w - 6))
    r0 = rng.randint(4, h - rh - 3)
    c0 = rng.randint(4, w - rw - 3)
    g = full_grid(h, w, 0)
    draw_rect(g, r0, c0, rh, rw, rect_color)
    candidates = [
        (r0 - 3, c0 + 1),
        (r0 + rh + 2, c0 + rw - 2),
        (r0 + 1, c0 - 3),
        (r0 + rh - 2, c0 + rw + 2),
    ]
    rng.shuffle(candidates)
    for i, (r, c) in enumerate(candidates[:dot_count]):
        if 0 <= r < h and 0 <= c < w:
            g[r][c] = dot_colors[i % len(dot_colors)]
    return g


def _build_palette(kind, rect_color, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    pool = [c for c in pool if c != 0 and c != rect_color]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    h, w = 14, 14
    g = full_grid(h, w, 0)
    if name == "no_dots":
        draw_rect(g, 5, 5, 3, 4, 2)
        return g
    if name == "no_rect":
        for _ in range(4):
            r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
            g[r][c] = rng.choice([3, 4, 5, 6])
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 2
        return g
    return g
