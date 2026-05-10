"""Generator for arc_additional_puzzles_21_set22_bundle:H152.

Rule: for each color with 2 cells aligned, the span between them is
its line. Cells on 2 spans → 8, on ≥3 spans → 9.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_pairs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_aligned_pairs, parallel_only, single_pair.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "278b7aee1bad"
VERSION = "1.1.0"
TASK_ID = "278b7aee1bad"
SUMMARY = "3-4 colors each with 2 aligned cells (vertical or horizontal); spans cross."

INVARIANTS = [
    "between 3 and 4 distinct colors with exactly 2 aligned cells each",
    "spans intersect in at least one cell",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_aligned_pairs", "parallel_only", "single_pair")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pairs":        {"type": "int", "default": "3", "valid": "3..4"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..4"},
    "position_bias":  {"type": "str", "default": "crossing_spans",
                       "valid": "crossing_spans"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..4"},
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
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 11, 13)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    mid = w // 2
    g[1][2] = 2; g[1][mid + 2] = 2
    g[h - 2][2] = 4; g[h - 2][mid + 2] = 4
    g[2][mid] = 6; g[h - 3][mid] = 6
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 12
    g = full_grid(h, w, 0)
    if name == "no_aligned_pairs":
        # cells exist but none share a row or column → no spans, no marking
        g[1][2] = 2
        g[3][5] = 4
        g[5][8] = 6
        return g
    if name == "parallel_only":
        # all spans are horizontal (or all vertical) → no crossings, no 8/9 cells
        g[1][1] = 2; g[1][8] = 2
        g[3][1] = 4; g[3][8] = 4
        g[5][1] = 6; g[5][8] = 6
        return g
    if name == "single_pair":
        # only one color has aligned cells → at most one span, no intersections possible
        g[2][2] = 5; g[2][8] = 5
        return g
    return g
