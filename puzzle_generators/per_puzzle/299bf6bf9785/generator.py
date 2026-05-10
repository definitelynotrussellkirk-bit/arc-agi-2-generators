"""Generator for arc_additional_puzzle_bank_volume9:M63 — Mark median solid 1-rectangle.

Rule: among solid 1-rectangles, sort by size asc; recolor the middle one
(index = len/2) to 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_rects,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_rects, tied_sizes, even_count.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "299bf6bf9785"
VERSION = "1.1.0"
TASK_ID = "299bf6bf9785"
SUMMARY = "3 solid 1-rectangles of distinct sizes + decoration; output recolors median to 8."

INVARIANTS = [
    "exactly 3 non-touching solid 1-rectangles",
    "all distinct sizes",
    "decoration is a non-1 colored blob",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_rects", "tied_sizes", "even_count")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..14", "valid": "10..16"},
    "grid_w":         {"type": "int", "default": "rng 12..14", "valid": "10..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_rects":        {"type": "int", "default": "3", "valid": "3..5"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "distinct_size_solid_rects",
                       "valid": "distinct_size_solid_rects"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _occupied_or_adjacent(used, r1, c1, r2, c2):
    for r in range(r1 - 1, r2 + 2):
        for c in range(c1 - 1, c2 + 2):
            if (r, c) in used: return True
    return False


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 12, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 14)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 12, 14)
        w = ctx.draw_int("grid_w", 12, 14)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    used = set()
    # 3 solid rectangles of distinct sizes
    dims = [(2, 2), (2, 4), (4, 4)]
    rng.shuffle(dims)
    for bh, bw in dims:
        for _ in range(40):
            r1 = rng.randint(0, h - bh)
            c1 = rng.randint(0, w - bw)
            r2 = r1 + bh - 1; c2 = c1 + bw - 1
            if _occupied_or_adjacent(used, r1, c1, r2, c2): continue
            for r in range(r1, r2 + 1):
                for c in range(c1, c2 + 1):
                    g[r][c] = 1; used.add((r, c))
            break
    # decoration (non-1, non-solid)
    for _ in range(15):
        r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
        if (r, c) in used: continue
        g[r][c] = 5; used.add((r, c))
        break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 13, 13
    g = full_grid(h, w, 0)
    if name == "no_rects":
        # no rectangles → rule has no median to mark
        g[5][5] = 5  # decoration only
        return g
    if name == "tied_sizes":
        # all 3 rects same size (2x2) → median is ambiguous (sort key tied)
        for r in range(2):
            for c in range(2): g[1 + r][1 + c] = 1
        for r in range(2):
            for c in range(2): g[1 + r][7 + c] = 1
        for r in range(2):
            for c in range(2): g[7 + r][4 + c] = 1
        return g
    if name == "even_count":
        # 4 rects → no clear "middle" (index len/2 = 2 is upper-mid, ambiguous)
        for r in range(2):
            for c in range(2): g[1 + r][1 + c] = 1     # 2x2 (size 4)
        for r in range(2):
            for c in range(3): g[1 + r][7 + c] = 1     # 2x3 (size 6)
        for r in range(3):
            for c in range(3): g[6 + r][1 + c] = 1     # 3x3 (size 9)
        for r in range(3):
            for c in range(4): g[6 + r][8 + c] = 1     # 3x4 (size 12)
        return g
    return g
