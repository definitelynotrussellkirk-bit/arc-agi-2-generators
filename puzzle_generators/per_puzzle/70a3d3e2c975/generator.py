"""Generator for arc_puzzle_bank_eighteenth21:E123.

Rule: reflect all colored cells on the left side across the full 9-axis.

Combinatorial axes (8): grid_h, half_w, palette_kind, marks,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: empty_left, full_left, no_axis.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "70a3d3e2c975"
VERSION = "1.1.0"
TASK_ID = "70a3d3e2c975"
SUMMARY = "Reflect all colored cells on the left side across the full 9-axis."

INVARIANTS = [
    "background is 0",
    "one full column of 9s is the mirror axis",
    "left-side colored cells are copied to symmetric right-side positions",
    "the original left half and 9-axis remain unchanged",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("empty_left", "full_left", "no_axis")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "5..14"},
    "half_w":         {"type": "int", "default": "rng 3..5", "valid": "2..8"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "marks":          {"type": "int", "default": "rng 4..7", "valid": "1..20"},
    "palette_size":   {"type": "int", "default": "rng 1..6", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "left_half", "valid": "left_half"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..6", "valid": "1..9"},
    "density":        {"type": "str", "default": "mixed", "valid": "mixed"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        half_w = ctx.draw_int("half_w", 3, 4)
        marks = ctx.draw_int("marks", 3, 5)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        half_w = ctx.draw_int("half_w", 4, 5)
        marks = ctx.draw_int("marks", 6, 8)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        half_w = ctx.draw_int("half_w", 3, 5)
        marks = ctx.draw_int("marks", 4, 7)
    w = half_w * 2 + 1
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    for r in range(h):
        g[r][half_w] = 9
    cells = [(r, c) for r in range(h) for c in range(half_w)]
    for r, c in rng.sample(cells, min(marks, len(cells))):
        g[r][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8])
    return g


def _draw_from_degenerate(name, rng):
    h, half_w = 8, 4
    w = half_w * 2 + 1
    g = full_grid(h, w, 0)
    if name == "empty_left":
        # 9-axis but no left-side cells → mirror produces empty right
        for r in range(h):
            g[r][half_w] = 9
        return g
    if name == "full_left":
        # entire left half filled → mirror copies a dense block
        for r in range(h):
            g[r][half_w] = 9
            for c in range(half_w):
                g[r][c] = ((r + c) % 7) + 1
        return g
    if name == "no_axis":
        # left-side cells without the 9-axis → mirror axis undefined
        for r, c in [(1, 1), (3, 2), (5, 0)]:
            g[r][c] = 4
        return g
    return g
