"""Generator for arc_additional_puzzles_21_set4:E27.

Rule: bbox of all 3-cells; fill that solid rectangle with 3 on a fresh
empty grid (everything else 0).

Combinatorial axes (8): grid_h/w, palette_kind, num_threes,
palette_size, position_bias, n_distinct_colors, bbox_aspect, texture.
Degenerates: only_one_three, no_threes, threes_aligned.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c7c6836fd350"
VERSION = "1.1.0"
TASK_ID = "c7c6836fd350"
SUMMARY = "2-3 isolated 3-cells defining a non-degenerate bbox."

INVARIANTS = [
    "exactly 2-3 cells of color 3",
    "their bbox spans ≥3 rows AND ≥3 cols",
]

PALETTE_KINDS = ("default", "tight_bbox", "wide_bbox", "diagonal_bbox")
DEGENERATE_TEXTURES = ("only_one_three", "no_threes", "threes_aligned")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "num_threes":     {"type": "int", "default": "rng 2..3", "valid": "2..3"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "diagonal",
                       "valid": "diagonal"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
    "bbox_aspect":    {"type": "str", "default": "rectangle",
                       "valid": "rectangle"},
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
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 8, 11)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    r1 = rng.randint(0, h - 5); r2 = rng.randint(r1 + 3, h - 1)
    c1 = rng.randint(0, w - 5); c2 = rng.randint(c1 + 3, w - 1)
    g[r1][c1] = 3
    g[r2][c2] = 3
    if rng.random() < 0.5:
        g[rng.randint(r1, r2)][rng.randint(c1, c2)] = 3
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "only_one_three":
        # 1×1 bbox — fills only the single cell, rule effectively no-op
        g[3][4] = 3
        return g
    if name == "no_threes":
        # zero 3-cells — bbox undefined
        return g
    if name == "threes_aligned":
        # 3-cells in same row → zero-height bbox
        g[3][1] = 3
        g[3][5] = 3
        g[3][7] = 3
        return g
    return g
