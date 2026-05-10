"""Generator for easy_68_read_column_markers_as_row.

Rule: columns containing markers are read left-to-right into a one-row
palette; empty columns are skipped.

Combinatorial axes (8): grid_h/w, palette_kind, markers,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_markers, multi_markers_per_col, all_columns_active.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "875ce5d835db"
VERSION = "1.1.0"
TASK_ID = "875ce5d835db"
SUMMARY = "Columns with markers are read left-to-right into a one-row palette."

INVARIANTS = [
    "background is 0",
    "each active column has exactly one marker",
    "empty columns are skipped",
    "output preserves active column order",
]

PALETTE_KINDS = ("default", "sparse", "dense", "rainbow")
DEGENERATE_TEXTURES = ("no_markers", "multi_markers_per_col", "all_columns_active")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "3..16"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "4..22"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "markers":        {"type": "int", "default": "rng 3..6", "valid": "1..12"},
    "density":        {"type": "str", "default": "medium",
                       "valid": "sparse|medium|dense"},
    "palette_size":   {"type": "int", "default": "9", "valid": "9"},
    "position_bias":  {"type": "str", "default": "scattered",
                       "valid": "scattered"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..6",
                          "valid": "1..9"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 9, 10)
        target_max = 4
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 12, 13)
        target_max = 6
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 9, 13)
        target_max = 6
    target = min(ctx.draw_int("markers", 3, target_max), w)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    for c in sorted(rng.sample(range(w), target)):
        g[rng.randrange(h)][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 10
    g = full_grid(h, w, 0)
    if name == "no_markers":
        return g
    if name == "multi_markers_per_col":
        # 2 markers in same column — palette ordering ambiguous
        g[1][3] = 4
        g[5][3] = 6
        g[2][7] = 5
        return g
    if name == "all_columns_active":
        # every column has a marker — output palette = full width
        for c in range(w):
            g[3][c] = (c % 9) + 1
        return g
    return g
