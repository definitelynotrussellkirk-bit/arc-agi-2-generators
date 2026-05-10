"""Generator for arc_additional_puzzles_21_set9:E62.

Rule: row 0 contains some 8s acting as column markers. Output is the
sub-grid (rows 1+, only the marked columns).

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_marks,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_markers, all_columns_marked, body_empty.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "73500a0803e5"
VERSION = "1.1.0"
TASK_ID = "73500a0803e5"
SUMMARY = "Row 0 has 2-4 column markers (8s); rest of grid has random non-8 colors."

INVARIANTS = [
    "row 0 has ≥2 cells of color 8 (others are 0)",
    "rows 1+ have varied non-8 colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_markers", "all_columns_marked", "body_empty")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 4..6", "valid": "3..10"},
    "grid_w":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_marks":        {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "rng 3..8", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "row0_markers",
                       "valid": "row0_markers"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..8", "valid": "1..8"},
    "density":        {"type": "str", "default": "noisy_body", "valid": "noisy_body"},
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
        w = ctx.draw_int("grid_w", 5, 6)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 6, 7)
    else:
        h = ctx.draw_int("grid_h", 4, 6)
        w = ctx.draw_int("grid_w", 5, 7)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    n_marks = rng.randint(2, min(4, w - 1))
    cols = rng.sample(range(w), n_marks)
    for c in cols:
        g[0][c] = 8
    palette = [1, 2, 3, 4, 5, 6, 7, 9]
    for r in range(1, h):
        for c in range(w):
            if rng.random() < 0.6:
                g[r][c] = rng.choice(palette)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 5, 6
    g = full_grid(h, w, 0)
    if name == "no_markers":
        # row 0 is empty → no columns selected, output is empty sub-grid
        for r in range(1, h):
            for c in range(w):
                g[r][c] = ((r + c) % 8) + 1
        return g
    if name == "all_columns_marked":
        # every column marked → sub-grid equals the entire body, no filtering
        for c in range(w):
            g[0][c] = 8
        for r in range(1, h):
            for c in range(w):
                g[r][c] = ((r + c) % 8) + 1
        return g
    if name == "body_empty":
        # markers exist but rows 1+ are all zero → output sub-grid is all zero
        g[0][1] = 8
        g[0][3] = 8
        return g
    return g
