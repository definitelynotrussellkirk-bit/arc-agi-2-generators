"""Generator for arc_puzzle_bank_21_set22_bundle:medium_p02 — aspect recolor.

Rule: each blob's bbox aspect determines color: w == h → 4 (square),
w > h → 2 (wide), h > w → 3 (tall).

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: all_squares, single_blob, all_same_aspect.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.shape import SQUARE_2X2, H_LINE_3, V_LINE_3

GENERATOR_ID = "67ec1565020d"
VERSION = "1.1.0"
TASK_ID = "67ec1565020d"
SUMMARY = "Three blobs: square + wide + tall (so all 3 branches fire)."

INVARIANTS = [
    "background is 0",
    "≥1 blob each: square (h=w), wide (w>h), tall (h>w)",
    "blobs don't 4-touch",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("all_squares", "single_blob", "all_same_aspect")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "9..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "3", "valid": "3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "spread",
                       "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _bbox(cells):
    rs = [r for r, _ in cells]; cs = [c for _, c in cells]
    return max(rs) + 1, max(cs) + 1


def _free(g, r0, c0, cells):
    h, w = len(g), len(g[0])
    for r, c in cells:
        rr, cc = r0 + r, c0 + c
        if not (0 <= rr < h and 0 <= cc < w):
            return False
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                nr, nc = rr + dr, cc + dc
                if 0 <= nr < h and 0 <= nc < w and g[nr][nc] != 0:
                    return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 10, 13)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    palette = rng.sample([5, 6, 7, 8, 9], 3)
    shapes = [SQUARE_2X2, H_LINE_3, V_LINE_3]
    rng.shuffle(palette)
    for shape, color in zip(shapes, palette):
        sh, sw = _bbox(shape)
        for _ in range(40):
            r0 = rng.randint(0, h - sh)
            c0 = rng.randint(0, w - sw)
            if _free(g, r0, c0, shape):
                paint_at(g, r0, c0, shape, color)
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 12
    g = full_grid(h, w, 0)
    if name == "all_squares":
        # all blobs are squares → only the w==h → 4 branch fires; uniform output
        paint_at(g, 1, 1, SQUARE_2X2, 5)
        paint_at(g, 1, 7, SQUARE_2X2, 6)
        paint_at(g, 5, 4, SQUARE_2X2, 7)
        return g
    if name == "single_blob":
        # only one blob → rule still fires but no comparison/contrast across aspects
        paint_at(g, 3, 5, SQUARE_2X2, 8)
        return g
    if name == "all_same_aspect":
        # all wide (h<w) → only the w>h → 2 branch fires; no tall or square
        paint_at(g, 1, 1, H_LINE_3, 5)
        paint_at(g, 4, 6, H_LINE_3, 6)
        paint_at(g, 7, 2, H_LINE_3, 7)
        return g
    return g
