"""Generator for arc_additional_puzzle_bank_volume20:E139 — Bbox crop of all non-zero cells.

Rule: subgrid bounded by min/max row/col of all non-bg cells.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: empty_grid, content_fills_grid, single_cell.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "045c3641f0eb"
VERSION = "1.1.0"
TASK_ID = "045c3641f0eb"
SUMMARY = "Two small distinct-color blobs in opposite quadrants."

INVARIANTS = [
    "exactly 2 small blobs in different corners",
    "padding rows/cols around them (so bbox crop is non-trivial)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("empty_grid", "content_fills_grid", "single_cell")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 10..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "2", "valid": "1..3"},
    "position_bias":  {"type": "str", "default": "opposite_corners",
                       "valid": "opposite_corners"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "1..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 8)
        w = ctx.draw_int("grid_w", 10, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 10, 12)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    shapes = [
        [(0, 0), (0, 1), (1, 0), (1, 1)],
        [(0, 0), (0, 1), (1, 1)],
        [(0, 0), (1, 0), (1, 1)],
        [(0, 0), (0, 1)],
    ]
    pal = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], 2)
    s1 = rng.choice(shapes); s2 = rng.choice(shapes)
    paint_at(g, rng.randint(1, 2), rng.randint(2, 4), s1, pal[0])
    paint_at(g, rng.randint(h - 4, h - 3), rng.randint(w - 4, w - 3), s2, pal[1])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "empty_grid":
        # no non-bg cells → bbox undefined, rule output is empty/ambiguous
        return g
    if name == "content_fills_grid":
        # non-bg content already fills entire grid → bbox crop = identity
        for r in range(h):
            for c in range(w):
                g[r][c] = 1 + ((r * 3 + c) % 5)
        return g
    if name == "single_cell":
        # exactly one non-bg cell → output is 1×1, trivial cropping
        g[4][5] = 7
        return g
    return g
