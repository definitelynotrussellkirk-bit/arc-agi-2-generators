"""Generator for easy_k03: turn solid rectangles into hollow frames.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_rects,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_rects, all_2x2, already_hollow.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ec491e97a5d5"
VERSION = "1.1.0"
TASK_ID = "ec491e97a5d5"
SUMMARY = "Separated solid monochrome rectangles are hollowed so only their borders remain."
INVARIANTS = [
    "rectangles are solid and monochrome",
    "rectangles are separated by at least one background cell",
    "background is zero",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_rects", "all_2x2", "already_hollow")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "5..16"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "5..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_rects":        {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "solid_monochrome_rects",
                       "valid": "solid_monochrome_rects"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _can_place(grid, top, left, rh, rw):
    h = len(grid)
    w = len(grid[0])
    if top < 1 or left < 1 or top + rh >= h or left + rw >= w:
        return False
    for r in range(top - 1, top + rh + 1):
        for c in range(left - 1, left + rw + 1):
            if grid[r][c] != 0:
                return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
        n = ctx.draw_int("n_rects", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 13)
        n = ctx.draw_int("n_rects", 3, 3)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 9, 13)
        n = ctx.draw_int("n_rects", 2, 3)
    rng = ctx.draw_rng("layout")
    colors = list(ctx.draw_distinct_colors("colors", n=n, exclude={0}))
    g = full_grid(h, w, 0)
    for i in range(n):
        for _ in range(40):
            rh = rng.randint(3, 5)
            rw = rng.randint(3, 5)
            top = rng.randint(1, h - rh - 1)
            left = rng.randint(1, w - rw - 1)
            if _can_place(g, top, left, rh, rw):
                for r in range(top, top + rh):
                    for c in range(left, left + rw):
                        g[r][c] = colors[i]
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_rects":
        # blank → no rects to hollow
        return g
    if name == "all_2x2":
        # 2x2 rects → border IS the rect, hollowing leaves nothing → identity
        for r in range(2):
            for c in range(2):
                g[1 + r][1 + c] = 4
                g[5 + r][6 + c] = 6
        return g
    if name == "already_hollow":
        # rects already hollow (frames) → rule has no work to do
        for c in range(2, 6): g[2][c] = 3; g[5][c] = 3
        for r in range(2, 6): g[r][2] = 3; g[r][5] = 3
        return g
    return g
