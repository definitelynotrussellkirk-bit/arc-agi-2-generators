"""Generator for arc_additional_puzzles_21_set22_bundle:E149.

Rule: a small nonzero glyph is surrounded by blank rows and columns;
output is the bbox crop of all nonzero cells.

Combinatorial axes (8): grid_h/w, palette_kind, glyph_position,
palette_size, position_bias, n_distinct_colors, padding, texture.
Degenerates: glyph_at_edge, glyph_fills_grid, no_glyph.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c35effd8e6bc"
VERSION = "1.1.0"
TASK_ID = "c35effd8e6bc"
SUMMARY = "A small nonzero glyph is surrounded by blank rows and columns before cropping."

INVARIANTS = [
    "all nonzero cells are inside a smaller bounding box",
    "at least one full blank row and column remain outside the glyph",
]

PALETTE_KINDS = ("default", "warm", "cool", "rainbow")
DEGENERATE_TEXTURES = ("glyph_at_edge", "glyph_fills_grid", "no_glyph")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..13"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "7..13"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "glyph_position": {"type": "str", "default": "interior",
                       "valid": "interior"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "interior",
                       "valid": "interior"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
    "padding":        {"type": "int", "default": "rng 1..3", "valid": "1..3"},
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
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 8, 11)
    colors = list(ctx.draw_distinct_colors("colors", n=2, exclude=[0]))
    g = full_grid(h, w, 0)
    top = ctx.draw_int("top", 1, h - 5)
    left = ctx.draw_int("left", 1, w - 5)
    for dr, dc in [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)]:
        g[top + dr][left + dc] = colors[0]
    g[top + 1][left + 3] = colors[1]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    if name == "glyph_at_edge":
        # glyph touches grid edge — no blank padding to strip
        for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            g[dr][dc] = 4
        return g
    if name == "glyph_fills_grid":
        # nonzero in every row/col — bbox crop = full grid (rule no-op)
        for r in range(h):
            for c in range(w):
                g[r][c] = 4 if (r + c) % 2 == 0 else 0
        # ensure border rows/cols also have nonzero
        for r in range(h):
            g[r][0] = 5
            g[r][w - 1] = 5
        return g
    if name == "no_glyph":
        return g
    return g
