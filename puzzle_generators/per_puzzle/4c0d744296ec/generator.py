"""Generator for arc_puzzle_bank_twentyfirst_21_bundle:easy_143_project_top_markers_down_columns.

Rule: top-row color markers project their colors down full columns.

Combinatorial axes (8): grid_h/w, palette_kind, n_markers, palette_size,
position_bias, n_distinct_colors, marker_density, texture.
Degenerates: no_markers, body_has_cells, full_top_row.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4c0d744296ec"
VERSION = "1.1.0"
TASK_ID = "4c0d744296ec"
SUMMARY = "Top-row color markers project their colors down full columns."

INVARIANTS = [
    "background is 0",
    "only the top row contains nonzero input markers",
    "marked columns are distinct",
    "all output cells outside marked columns are zero",
]

PALETTE_KINDS = ("default", "sparse", "dense", "varied_palette")
DEGENERATE_TEXTURES = ("no_markers", "body_has_cells", "full_top_row")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..12", "valid": "2..24"},
    "grid_w":         {"type": "int", "default": "rng 8..14", "valid": "2..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "markers":        {"type": "int", "default": "rng 3..6", "valid": "1..12"},
    "palette_size":   {"type": "int", "default": "rng 3..6", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "top_row",
                       "valid": "top_row"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..6", "valid": "1..9"},
    "marker_density": {"type": "str", "default": "mixed", "valid": "mixed"},
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
        w = ctx.draw_int("grid_w", 8, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 12, 14)
    else:
        h = ctx.draw_int("grid_h", 7, 12)
        w = ctx.draw_int("grid_w", 8, 14)
    target = min(ctx.draw_int("markers", 3, 6), w)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    for c in rng.sample(range(w), target):
        g[0][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_markers":
        # empty grid — no columns to project
        return g
    if name == "body_has_cells":
        # body has cells already → invariant violated, "only top" wrong
        g[0][2] = 4
        g[3][5] = 6  # body cell, should not exist
        g[5][8] = 7
        return g
    if name == "full_top_row":
        # every column has a marker — projection fills entire grid (trivial)
        for c in range(w):
            g[0][c] = ((c % 8) + 1)
        return g
    return g
