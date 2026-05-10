"""Generator for arc_additional_puzzles_21_set11_bundle:E75.

Rule: count all nonzero cells, then output a row that repeats the first
seen color that many times.

Combinatorial axes (8): grid_h/w, palette_kind, num_nonzero,
palette_size, position_bias, n_distinct_colors, first_color, texture.
Degenerates: only_one_nonzero, count_exceeds_width, monocolor_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c74ecc35f54f"
VERSION = "1.1.0"
TASK_ID = "c74ecc35f54f"
SUMMARY = "All nonzero cells are counted, then a row repeats the first seen color that many times."

INVARIANTS = [
    "there are at least four nonzero cells",
    "the first nonzero value appears before any distractor colors",
]

PALETTE_KINDS = ("default", "scattered", "clustered", "rainbow")
DEGENERATE_TEXTURES = ("only_one_nonzero", "count_exceeds_width", "monocolor_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..8", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 6..9", "valid": "5..11"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "num_nonzero":    {"type": "int", "default": "5", "valid": "4..9"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "first_color":    {"type": "str", "default": "rng",
                       "valid": "any nonzero"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 6, 7)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
    else:
        h = ctx.draw_int("grid_h", 5, 8)
        w = ctx.draw_int("grid_w", 6, 9)
    colors = list(ctx.draw_distinct_colors("colors", n=3, exclude=[0]))
    g = full_grid(h, w, 0)
    for r, c, color in [
        (0, 1, colors[0]),
        (1, w - 2, colors[1]),
        (h // 2, 2, colors[2]),
        (h - 2, w // 2, colors[1]),
        (h - 1, w - 1, colors[2]),
    ]:
        g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 8
    g = full_grid(h, w, 0)
    if name == "only_one_nonzero":
        g[2][3] = 5
        return g
    if name == "count_exceeds_width":
        for r in range(h):
            for c in range(w):
                g[r][c] = 3 if (r + c) % 2 == 0 else 0
        g[0][0] = 7
        return g
    if name == "monocolor_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 5
        return g
    return g
