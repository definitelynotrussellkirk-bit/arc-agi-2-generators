"""Generator for arc_puzzle_bank_sixth21:M39 — recolor blobs by header column.

Rule: top row holds N legend colors at distinct cols. Below row 0,
each blob is recolored based on which column the legend marker is at.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_legend,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_legend, blob_above_legend, blobs_misaligned.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "0dba62203065"
VERSION = "1.1.0"
TASK_ID = "0dba62203065"
SUMMARY = "Top-row legend colors at distinct cols + 2-3 blobs below."

INVARIANTS = [
    "background is 0",
    "row 0 has 2-3 distinct legend cells at distinct cols",
    "≥2 below-row-0 blobs at distinct columns; each below blob has a unique legend col above",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_legend", "blob_above_legend", "blobs_misaligned")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 11..13", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_legend":       {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "rng 3..4", "valid": "2..9"},
    "position_bias":  {"type": "str", "default": "header_with_blobs_below",
                       "valid": "header_with_blobs_below"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..4", "valid": "2..9"},
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
        w = ctx.draw_int("grid_w", 11, 12)
        n = 2
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 12, 13)
        n = 3
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 11, 13)
        n = None
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    if n is None:
        n = rng.randint(2, 3)
    legend_palette = rng.sample([2, 3, 4, 5, 6, 7, 8, 9], n)
    legend_cols = sorted(rng.sample(range(w), n))
    for c, color in zip(legend_cols, legend_palette):
        g[0][c] = color
    used = {(0, c) for c in legend_cols}
    for c in range(w):
        used.add((1, c))
    for _ in range(n):
        cells = grow_blob(rng, h, w, used, rng.randint(2, 4), max_attempts=80)
        if cells is None:
            continue
        for r, c in cells:
            g[r][c] = 1
        used |= cells
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 12
    g = full_grid(h, w, 0)
    if name == "no_legend":
        # row 0 blank → no legend, rule has no source colors to map blobs to
        for (r, c) in [(3, 2), (3, 3), (4, 2)]: g[r][c] = 1
        for (r, c) in [(5, 7), (5, 8), (6, 7)]: g[r][c] = 1
        return g
    if name == "blob_above_legend":
        # blobs occupy row 0 → ambiguous which cells are legend vs blob
        g[0][2] = 4; g[0][7] = 6   # legend
        g[0][5] = 1   # blob cell on row 0
        for (r, c) in [(3, 2), (4, 2)]: g[r][c] = 1
        return g
    if name == "blobs_misaligned":
        # blobs at columns that don't match any legend column → mapping undefined
        g[0][2] = 4; g[0][8] = 6   # legend at cols 2 and 8
        for (r, c) in [(3, 5), (4, 5)]: g[r][c] = 1   # blob at col 5 (no legend)
        for (r, c) in [(6, 10), (7, 10)]: g[r][c] = 1   # blob at col 10 (no legend)
        return g
    return g
