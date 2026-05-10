"""Generator for arc_puzzle_bank_twentieth_21_bundle:easy_138_project_markers_to_full_crosses.

Rule: markers project full same-color rows and columns.

Combinatorial axes (8): grid_h, grid_w, palette_kind, markers,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_markers, mixed_marker_colors, all_cells_marked.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8d45a1d4a531"
VERSION = "1.1.0"
TASK_ID = "8d45a1d4a531"
SUMMARY = "Markers project full same-color rows and columns."

INVARIANTS = [
    "background is 0",
    "all markers share one color so projected cross overlaps are unambiguous",
    "markers are singleton cells",
    "the output is the union of every selected row and column",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_markers", "mixed_marker_colors", "all_cells_marked")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..11", "valid": "3..20"},
    "grid_w":         {"type": "int", "default": "rng 8..13", "valid": "3..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "markers":        {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 10)
        target = ctx.draw_int("markers", 2, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 13)
        target = ctx.draw_int("markers", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 7, 11)
        w = ctx.draw_int("grid_w", 8, 13)
        target = ctx.draw_int("markers", 2, 4)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    for r, c in rng.sample([(r, c) for r in range(h) for c in range(w)], min(target, h * w)):
        g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_markers":
        # empty grid → no rows or columns to project
        return g
    if name == "mixed_marker_colors":
        # markers in different colors → cross-overlap cell color is ambiguous
        g[1][2] = 3
        g[5][7] = 6
        g[3][9] = 4
        return g
    if name == "all_cells_marked":
        # entire grid filled with marker color → projection has no visible delta
        for r in range(h):
            for c in range(w):
                g[r][c] = 4
        return g
    return g
