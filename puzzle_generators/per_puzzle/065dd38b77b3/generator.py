"""Generator for arc_additional_puzzles_21_set21_bundle:E143 — Reflect across uniform guide-row.

Rule: find first row that is uniformly one non-zero color. For each
non-zero cell ABOVE the guide-row, paint a copy at the reflected row
position below.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_marks,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_guide, no_marks, marks_below_guide.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "065dd38b77b3"
VERSION = "1.1.0"
TASK_ID = "065dd38b77b3"
SUMMARY = "Uniform guide-row of one color; non-zero markers above it."

INVARIANTS = [
    "exactly one full-width row of a single non-bg color (the guide)",
    "≥3 non-zero non-guide cells above the guide-row",
    "rows below guide are all bg, with enough room for the reflection",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_guide", "no_marks", "marks_below_guide")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "5..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_marks":        {"type": "int", "default": "rng 4..6", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 2..5", "valid": "1..6"},
    "position_bias":  {"type": "str", "default": "marks_above_guide_row",
                       "valid": "marks_above_guide_row"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..5", "valid": "1..6"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 7, 10)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    # Pick guide_row in middle so reflection fits
    guide_row = rng.randint(3, h - 4)
    guide_color = rng.choice([5, 6, 8])
    for c in range(w):
        g[guide_row][c] = guide_color
    # Markers above
    palette = [v for v in [1, 2, 3, 4, 7, 9] if v != guide_color]
    n_marks = rng.randint(4, 6)
    placed = 0
    for _ in range(60):
        if placed >= n_marks:
            break
        r = rng.randint(0, guide_row - 1)
        c = rng.randint(0, w - 1)
        if g[r][c] == 0:
            g[r][c] = rng.choice(palette)
            placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 8
    g = full_grid(h, w, 0)
    if name == "no_guide":
        # markers but no full-width guide row → no axis to reflect across
        for r, c in [(1, 1), (2, 3), (3, 5)]: g[r][c] = 4
        return g
    if name == "no_marks":
        # only the guide row → nothing to reflect
        for c in range(w):
            g[5][c] = 6
        return g
    if name == "marks_below_guide":
        # markers below the guide → above region empty, rule has no source
        for c in range(w):
            g[3][c] = 6
        for r, c in [(5, 1), (6, 3), (7, 5)]: g[r][c] = 4
        return g
    return g
