"""Generator for arc_additional_puzzles_21_set20_bundle:M139 — Pairwise mask-equal matrix from 8-separated panels.

Rule: 8-cols separate panels. Crop each to mask. n×n matrix: 1 if masks
equal, 0 else.

Combinatorial axes (8): grid_h, grid_w, palette_kind, panel_w,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_dividers, all_distinct_panels, all_equal_panels.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e45c4519a714"
VERSION = "1.1.0"
TASK_ID = "e45c4519a714"
SUMMARY = "3 8-separator-cols panels; some share masks."

INVARIANTS = [
    "2 full-column 8-dividers split grid into 3 panels",
    "each panel has 3-4 non-zero cells",
    "two panels share the same normalized mask",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_dividers", "all_distinct_panels", "all_equal_panels")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "derived", "valid": "4..7"},
    "grid_w":         {"type": "int", "default": "derived", "valid": "11..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "panel_w":        {"type": "int", "default": "rng 4..5", "valid": "3..6"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "8col_separated_panels",
                       "valid": "8col_separated_panels"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
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
        pw = ctx.draw_int("panel_w", 4, 4)
        h = ctx.draw_int("n_rows", 4, 4)
    elif difficulty == "hard":
        pw = ctx.draw_int("panel_w", 5, 5)
        h = ctx.draw_int("n_rows", 5, 5)
    else:
        pw = ctx.draw_int("panel_w", 4, 5)
        h = ctx.draw_int("n_rows", 4, 5)
    w = pw * 3 + 2
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    d1 = pw
    d2 = pw * 2 + 1
    for r in range(h):
        g[r][d1] = 8; g[r][d2] = 8
    palette = [2, 3, 4, 5, 6, 7, 9]; rng.shuffle(palette)
    # Panel A and B share same shape but different colors
    shape_ab = rng.choice([
        [(0, 0), (1, 0), (1, 1)],
        [(0, 0), (0, 1), (1, 1)],
        [(0, 0), (0, 1), (1, 0), (1, 1)],
    ])
    for r, c in shape_ab:
        g[1 + r][1 + c] = palette[0]
        g[1 + r][d1 + 1 + c] = palette[1]
    # Panel C different
    shape_c = [(0, 0), (1, 0), (1, 1), (2, 1)]
    for r, c in shape_c:
        if 1 + r < h and d2 + 1 + c < w:
            g[1 + r][d2 + 1 + c] = palette[2]
    return g


def _draw_from_degenerate(name, rng):
    pw = 4; h = 4
    w = pw * 3 + 2
    g = full_grid(h, w, 0)
    d1 = pw; d2 = pw * 2 + 1
    if name == "no_dividers":
        # missing 8-cols → can't split into panels
        for r, c in [(0, 0), (1, 0), (1, 1)]:
            g[r][c] = 2
        for r, c in [(0, 5), (1, 5), (1, 6)]:
            g[r][c] = 3
        return g
    if name == "all_distinct_panels":
        # all 3 panels have unique masks → identity matrix only
        for r in range(h):
            g[r][d1] = 8; g[r][d2] = 8
        for r, c in [(1, 1)]:
            g[r][c] = 2
        for r, c in [(1, d1 + 1), (2, d1 + 1)]:
            g[r][c] = 3
        for r, c in [(1, d2 + 1), (1, d2 + 2), (2, d2 + 1)]:
            g[r][c] = 4
        return g
    if name == "all_equal_panels":
        # all 3 panels share mask → matrix is all 1s
        for r in range(h):
            g[r][d1] = 8; g[r][d2] = 8
        shape = [(0, 0), (1, 0), (1, 1)]
        for r, c in shape:
            g[1 + r][1 + c] = 2
            g[1 + r][d1 + 1 + c] = 3
            g[1 + r][d2 + 1 + c] = 4
        return g
    return g
