"""Generator for arc_puzzle_bank_seventeenth_21_bundle:easy_114_draw_rectangle_borders_from_opposite_corners.

Rule: each color appearing twice as opposite rectangle corners
expands into the full rectangle border outline.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, rectangles, texture.
Degenerates: no_pairs, single_corner, collinear_corners.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "874aa60956cc"
VERSION = "1.1.0"
TASK_ID = "874aa60956cc"

SUMMARY = "Each color appears twice as opposite corners of a rectangle border."

INVARIANTS = [
    "background is 0",
    "each active color appears exactly twice",
    "the two cells are opposite rectangle corners",
    "rectangle regions are separated to avoid overlaps",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "single_corner", "collinear_corners")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "5..18"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "5..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "rectangles":     {"type": "int", "default": "rng 1..3", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "= rectangles", "valid": "1..6"},
    "position_bias":  {"type": "str", "default": "scattered_diagonal_corners",
                       "valid": "scattered_diagonal_corners"},
    "n_distinct_colors": {"type": "int", "default": "= rectangles", "valid": "1..6"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
        target = ctx.draw_int("rectangles", 1, 1)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 14)
        w = ctx.draw_int("grid_w", 12, 16)
        target = ctx.draw_int("rectangles", 3, 5)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 9, 12)
        target = ctx.draw_int("rectangles", 1, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    reserved: set[tuple[int, int]] = set()
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], min(target, 9))
    placed = 0
    for _ in range(300):
        if placed >= target:
            break
        height = rng.randint(3, 4)
        width = rng.randint(3, 5)
        r1 = rng.randint(0, h - height)
        c1 = rng.randint(0, w - width)
        r2 = r1 + height - 1
        c2 = c1 + width - 1
        guard = {
            (r, c)
            for r in range(max(0, r1 - 1), min(h, r2 + 2))
            for c in range(max(0, c1 - 1), min(w, c2 + 2))
        }
        if guard & reserved:
            continue
        color = colors[placed % len(colors)]
        if rng.randrange(2) == 0:
            g[r1][c1] = color
            g[r2][c2] = color
        else:
            g[r1][c2] = color
            g[r2][c1] = color
        reserved.update(guard)
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # Empty grid — rule has no corner pairs to expand.
        return g
    if name == "single_corner":
        # Color appears once — rule's "exactly twice" filter excludes;
        # rectangle is undefined.
        g[2][2] = 4
        return g
    if name == "collinear_corners":
        # Same color twice but on the same row/column — implied
        # rectangle is 1-D, rule's outline degenerates to a line.
        g[3][2] = 4; g[3][7] = 4
        return g
    return g
