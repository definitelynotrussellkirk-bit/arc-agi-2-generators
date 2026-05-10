"""Generator for arc_puzzle_bank_21_set6:easy_f02.

Rule: keep only the four corners of each filled rectangle.

Combinatorial axes (8): grid_h, grid_w, palette_kind, rectangles,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: line_rects, single_cell_rects, no_rects.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "7fd453cd0339"
VERSION = "1.1.0"
TASK_ID = "7fd453cd0339"
SUMMARY = "Keep only the four corners of each filled rectangle."

INVARIANTS = [
    "background is 0",
    "objects are solid monochrome rectangles",
    "rectangles are separated by background",
    "output preserves only rectangle corner cells",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("line_rects", "single_cell_rects", "no_rects")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "4..14"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "5..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "rectangles":     {"type": "int", "default": "rng 2..3", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "spaced_solid_rects",
                       "valid": "spaced_solid_rects"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _free(g, r1, c1, r2, c2):
    h, w = len(g), len(g[0])
    for r in range(max(0, r1 - 1), min(h, r2 + 2)):
        for c in range(max(0, c1 - 1), min(w, c2 + 2)):
            if g[r][c] != 0:
                return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 8, 9)
        target = ctx.draw_int("rectangles", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 10, 11)
        target = ctx.draw_int("rectangles", 3, 3)
    else:
        h = ctx.draw_int("grid_h", 6, 8)
        w = ctx.draw_int("grid_w", 8, 11)
        target = ctx.draw_int("rectangles", 2, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    placed = 0
    for _ in range(180):
        if placed >= target:
            break
        rh = rng.randint(2, min(4, h))
        rw = rng.randint(2, min(5, w))
        r0 = rng.randint(0, h - rh)
        c0 = rng.randint(0, w - rw)
        if not _free(g, r0, c0, r0 + rh - 1, c0 + rw - 1):
            continue
        color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
        for r in range(r0, r0 + rh):
            for c in range(c0, c0 + rw):
                g[r][c] = color
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 10
    g = full_grid(h, w, 0)
    if name == "line_rects":
        # 1×N or N×1 lines → bbox has only 2 distinct corners; rule keeps endpoints
        for c in range(1, 6): g[2][c] = 4   # 1x5 horizontal
        for r in range(4, 7): g[r][8] = 6   # 3x1 vertical
        return g
    if name == "single_cell_rects":
        # 1x1 rects → bbox has 1 distinct corner; rule keeps the cell, identity
        g[2][3] = 4; g[5][7] = 6; g[6][1] = 3
        return g
    if name == "no_rects":
        # blank grid → rule has nothing to corner-extract
        return g
    return g
