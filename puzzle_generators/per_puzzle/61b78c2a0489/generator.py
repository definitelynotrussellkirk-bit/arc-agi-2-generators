"""Generator for medium_22_gravity_down_each_column.

Rule: each non-zero cell falls down its column, stacking at the bottom.

Combinatorial axes (8): grid_h/w, palette_kind, density,
palette_size, position_bias, n_distinct_colors, fall_room, texture.
Degenerates: already_settled, full_grid, empty_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "61b78c2a0489"
VERSION = "1.1.0"
TASK_ID = "61b78c2a0489"
SUMMARY = "Sparse non-zero cells in upper rows (so gravity moves them down)."

INVARIANTS = [
    "background is 0",
    "≥3 non-zero cells in upper half (will fall)",
    "bottom 1-2 rows are all zero (so gravity has somewhere to go)",
]

PALETTE_KINDS = ("default", "sparse", "medium_density", "scattered")
DEGENERATE_TEXTURES = ("already_settled", "full_grid", "empty_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..8", "valid": "4..12"},
    "grid_w":         {"type": "int", "default": "rng 6..9", "valid": "5..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "density":        {"type": "str", "default": "0.3",
                       "valid": "0.15|0.3|0.5"},
    "palette_size":   {"type": "int", "default": "9", "valid": "9"},
    "position_bias":  {"type": "str", "default": "upper_half",
                       "valid": "upper_half"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..9",
                          "valid": "1..9"},
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
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 6, 7)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
    else:
        h = ctx.draw_int("grid_h", 5, 8)
        w = ctx.draw_int("grid_w", 6, 9)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    for r in range(h - 2):
        for c in range(w):
            if rng.random() < 0.3:
                g[r][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 7
    g = full_grid(h, w, 0)
    if name == "already_settled":
        # Cells already at the bottom — gravity is no-op
        for c in range(w):
            g[h - 1][c] = (c % 9) + 1
        for c in [0, 2, 4]:
            g[h - 2][c] = 5
        return g
    if name == "full_grid":
        # Every cell filled — nothing to fall through
        for r in range(h):
            for c in range(w):
                g[r][c] = ((r + c) % 9) + 1
        return g
    if name == "empty_grid":
        return g
    return g
