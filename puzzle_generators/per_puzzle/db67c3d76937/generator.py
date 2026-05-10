"""Generator for arc_additional_puzzles_21_set22_bundle:M152.

Rule: for each non-bg color with 2 aligned cells (same row or col),
paint the span between with that color. Cells in 2+ spans → 9.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_pairs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: parallel_only, single_pair, no_pairs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "db67c3d76937"
VERSION = "1.1.0"
TASK_ID = "db67c3d76937"
SUMMARY = "1 vertical pair + 1 horizontal pair that intersect."

INVARIANTS = [
    "1 color with 2 vertically-aligned cells",
    "1 color with 2 horizontally-aligned cells",
    "their spans cross at least 1 cell",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("parallel_only", "single_pair", "no_pairs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pairs":        {"type": "int", "default": "2", "valid": "2"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "crossing_axes",
                       "valid": "crossing_axes"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
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
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 9, 11)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    palette = [2, 3, 4, 6, 7]; rng.shuffle(palette)
    g[0][4] = palette[0]; g[h - 1][4] = palette[0]
    g[h // 2][1] = palette[1]; g[h // 2][w - 2] = palette[1]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "parallel_only":
        # both pairs horizontal (or both vertical) → spans don't cross, no 9 cell
        g[1][1] = 3; g[1][8] = 3
        g[5][1] = 7; g[5][8] = 7
        return g
    if name == "single_pair":
        # only 1 aligned pair → at most 1 span, no intersections possible
        g[2][2] = 4; g[2][7] = 4
        return g
    if name == "no_pairs":
        # cells exist but none share a row or column → no spans, output equals input
        g[1][2] = 3; g[3][5] = 6; g[5][8] = 7
        return g
    return g
