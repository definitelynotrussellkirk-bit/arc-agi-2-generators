"""Generator for 6b:m38 — legend ordered gallery.

Rule: top row legend defines color order. Below, blobs in those colors
are arranged in legend order, gallery-packed.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_legend,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_legend, no_blobs, missing_legend_blob.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "4e53f3cd64e8"
VERSION = "1.1.0"
TASK_ID = "4e53f3cd64e8"
SUMMARY = "Top legend (3-4 distinct colors at low cols) + below blobs in those colors."

INVARIANTS = [
    "background is 0",
    "row 0 has 3-4 legend cells in a contiguous prefix",
    "≥1 blob per legend color exists below (so output uses each)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_legend", "no_blobs", "missing_legend_blob")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 12..15", "valid": "10..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_legend":       {"type": "int", "default": "rng 3..4", "valid": "2..6"},
    "palette_size":   {"type": "int", "default": "rng 3..4", "valid": "2..6"},
    "position_bias":  {"type": "str", "default": "row0_legend_plus_below_blobs",
                       "valid": "row0_legend_plus_below_blobs"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..4", "valid": "2..6"},
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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 12, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 14, 15)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 12, 15)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    n = rng.randint(3, 4)
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], n)
    rng.shuffle(palette)
    for i, color in enumerate(palette):
        g[0][i] = color
    used = {(0, c) for c in range(n)}
    for c in range(w):
        used.add((1, c))
    for color in palette:
        cells = grow_blob(rng, h, w, used, rng.randint(2, 4), max_attempts=80)
        if cells:
            for r, c in cells: g[r][c] = color
            used |= cells
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 13
    g = full_grid(h, w, 0)
    if name == "no_legend":
        # blobs without row-0 legend → no order signal for gallery
        for r, c in [(3, 1), (3, 2), (4, 1)]: g[r][c] = 4
        for r, c in [(5, 5), (5, 6), (6, 5)]: g[r][c] = 6
        return g
    if name == "no_blobs":
        # legend alone → nothing to arrange
        for i, color in enumerate([4, 6, 7]):
            g[0][i] = color
        return g
    if name == "missing_legend_blob":
        # legend has color 7 but no blob of color 7 → gallery has missing slot
        for i, color in enumerate([4, 6, 7]):
            g[0][i] = color
        for r, c in [(3, 1), (3, 2), (4, 1)]: g[r][c] = 4
        for r, c in [(5, 5), (5, 6), (6, 5)]: g[r][c] = 6
        return g
    return g
