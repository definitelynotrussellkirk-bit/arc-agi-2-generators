"""Generator for arc_additional_puzzle_bank_volume3:M18.

Rule: pivot = first 2-cell. For each non-{0,2} cell at (r,c), compute
delta (r-pr, c-pc), place at (pr+dc, pc-dr).

Combinatorial axes (8): grid_h, grid_w, palette_kind, blob_kind,
palette_size, position_bias, n_distinct_colors, blob_color, texture.
Degenerates: no_pivot, two_pivots, no_blob.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "3279a0599dab"
VERSION = "1.1.0"
TASK_ID = "3279a0599dab"
SUMMARY = "1-blob in upper-left + 2-pivot in middle; output rotates blob 90° around pivot."

INVARIANTS = [
    "exactly one 2-pivot in middle",
    "1-blob is asymmetric, fits within grid after 90° rotation around pivot",
]

PALETTE_KINDS = ("default", "L_blob", "I_blob", "asymmetric")
DEGENERATE_TEXTURES = ("no_pivot", "two_pivots", "no_blob")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "grid_w":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "blob_kind":      {"type": "str", "default": "L_3cell", "valid": "L_3cell"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "pivot_centered",
                       "valid": "pivot_centered"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
    "blob_color":     {"type": "int", "default": "rng 1,4..9", "valid": "1|4|5|6|7|8|9"},
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
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 7, 9)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    pr = h // 2; pc = w // 2
    g[pr][pc] = 2
    color = rng.choice([1, 4, 5, 6, 7, 8, 9])
    g[pr - 2][pc - 1] = color
    g[pr - 1][pc - 1] = color
    g[pr - 1][pc - 2] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    pr, pc = h // 2, w // 2
    if name == "no_pivot":
        # blob present but no 2-pivot → rotation center undefined
        g[pr - 2][pc - 1] = 5
        g[pr - 1][pc - 1] = 5
        g[pr - 1][pc - 2] = 5
        return g
    if name == "two_pivots":
        # two 2-cells → which is the pivot?
        g[pr][pc] = 2
        g[1][1] = 2
        g[pr - 2][pc - 1] = 5
        g[pr - 1][pc - 1] = 5
        return g
    if name == "no_blob":
        # pivot but nothing to rotate → rule has no source cells
        g[pr][pc] = 2
        return g
    return g
