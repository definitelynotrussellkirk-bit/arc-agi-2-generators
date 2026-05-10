"""Generator for arc_additional_puzzles_21_set4:E25.

Rule: keep only columns that have ≥1 non-zero cell; drop fully-zero
columns. Output rows project to those kept columns.

Combinatorial axes (8): grid_h/w, palette_kind, n_keep, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_zero_cols, no_kept_cols, all_zero.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e52b8ee307e1"
VERSION = "1.1.0"
TASK_ID = "e52b8ee307e1"
SUMMARY = "Sparse non-bg cells leaving ≥2 fully-zero columns."

INVARIANTS = [
    "≥3 cols are fully zero (will be dropped)",
    "≥3 cols have ≥1 non-zero cell (will be kept)",
]

PALETTE_KINDS = ("default", "warm", "cool", "rainbow")
DEGENERATE_TEXTURES = ("no_zero_cols", "no_kept_cols", "all_zero")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 4..6", "valid": "3..10"},
    "grid_w":         {"type": "int", "default": "rng 7..9", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_keep":         {"type": "int", "default": "rng 3..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 3..6", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..6", "valid": "1..9"},
    "density":        {"type": "str", "default": "low", "valid": "low"},
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
        h = ctx.draw_int("grid_h", 4, 5)
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 8, 9)
    else:
        h = ctx.draw_int("grid_h", 4, 6)
        w = ctx.draw_int("grid_w", 7, 9)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    n_keep = rng.randint(3, 4)
    keep_cols = rng.sample(range(w), n_keep)
    palette = [2, 3, 4, 5, 6, 7, 8, 9]
    for c in keep_cols:
        cnt = rng.randint(1, 2)
        rs = rng.sample(range(h), cnt)
        for r in rs:
            g[r][c] = rng.choice(palette)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 5, 8
    g = full_grid(h, w, 0)
    if name == "no_zero_cols":
        # every column has a cell — output equals input (rule trivial)
        for c in range(w):
            g[c % h][c] = ((c % 7) + 2)
        return g
    if name == "no_kept_cols":
        # all columns fully zero — output has zero columns (degenerate shape)
        return g
    if name == "all_zero":
        # alias of empty — extreme of the no_kept case
        return g
    return g
