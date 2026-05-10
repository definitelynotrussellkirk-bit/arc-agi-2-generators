"""Generator for arc_puzzle_bank_21_set4:S4_M5 — solid rectangles to center crosses.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_rects,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_rects, even_dims, hollow_rect.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "13507b4f7614"
VERSION = "1.1.0"
TASK_ID = "13507b4f7614"

SUMMARY = "One or two odd-sized solid yellow rectangles that reduce to center crosses."

INVARIANTS = [
    "background is 0",
    "all color-4 objects are solid rectangles",
    "each rectangle has odd height and odd width",
    "rectangles are separated by at least one blank cell",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_rects", "even_dims", "hollow_rect")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..14", "valid": "9..18"},
    "grid_w":         {"type": "int", "default": "rng 13..17", "valid": "9..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_rects":        {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "separated_odd_rects",
                       "valid": "separated_odd_rects"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _clear(g, r, c, rh, rw):
    h, w = len(g), len(g[0])
    if r < 0 or c < 0 or r + rh > h or c + rw > w:
        return False
    for rr in range(max(0, r - 1), min(h, r + rh + 1)):
        for cc in range(max(0, c - 1), min(w, c + rw + 1)):
            if g[rr][cc] != 0:
                return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 13, 14)
        n_rects_lo, n_rects_hi = 1, 1
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 14)
        w = ctx.draw_int("grid_w", 16, 17)
        n_rects_lo, n_rects_hi = 2, 2
    else:
        h = ctx.draw_int("grid_h", 11, 14)
        w = ctx.draw_int("grid_w", 13, 17)
        n_rects_lo, n_rects_hi = 1, 2
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    for _ in range(rng.randint(n_rects_lo, n_rects_hi)):
        for _attempt in range(80):
            rh = rng.choice([3, 5])
            rw = rng.choice([3, 5, 7])
            r = rng.randint(1, h - rh - 1)
            c = rng.randint(1, w - rw - 1)
            if _clear(g, r, c, rh, rw):
                draw_rect(g, r, c, rh, rw, 4)
                break
        else:
            raise ValueError("could not place odd rectangle")
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 13
    g = full_grid(h, w, 0)
    if name == "no_rects":
        # blank → no rectangles to reduce to crosses
        return g
    if name == "even_dims":
        # 4x4 even rect → no single center cell, cross undefined
        for r in range(2, 6):
            for c in range(2, 6):
                g[r][c] = 4
        return g
    if name == "hollow_rect":
        # outline-only rectangle → not solid, fails precondition
        for c in range(2, 7): g[2][c] = 4; g[6][c] = 4
        for r in range(2, 7): g[r][2] = 4; g[r][6] = 4
        return g
    return g
