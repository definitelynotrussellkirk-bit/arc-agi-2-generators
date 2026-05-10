"""Generator for arc_puzzle_bank_eleventh21:M72 — recolor by size palette.

Rule: row 0 has N legend colors at cols 0..N-1 (size→color palette).
Below row 0, each blob's color is replaced by palette[size - 1].

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_legend,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_legend, no_blobs, blob_size_out_of_range.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "01f4294de005"
VERSION = "1.1.0"
TASK_ID = "01f4294de005"
SUMMARY = "Row 0 cols 0..N-1 hold a legend; below, blobs of size 1..N exist."

INVARIANTS = [
    "background is 0",
    "row 0 has exactly N legend cells at cols 0..N-1",
    "each blob below has size in 1..N (so palette lookup is well-defined)",
    "input blobs are all the same color (legend tells the rule which to use)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_legend", "no_blobs", "blob_size_out_of_range")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_legend":       {"type": "int", "default": "3", "valid": "2..4"},
    "palette_size":   {"type": "int", "default": "3", "valid": "2..4"},
    "position_bias":  {"type": "str", "default": "row0_legend_with_sized_blobs",
                       "valid": "row0_legend_with_sized_blobs"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "3..5"},
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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 9, 12)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    n = 3
    legend_palette = rng.sample([2, 3, 4, 5, 6, 8, 9], n)
    for i, color in enumerate(legend_palette):
        g[0][i] = color
    used = {(0, c) for c in range(n)}
    for c in range(w):
        used.add((1, c))
    sizes = [1, 2, 3]
    for size in sizes:
        cells = grow_blob(rng, h, w, used, size, max_attempts=80)
        if cells is None:
            continue
        for r, c in cells:
            g[r][c] = 7  # all same input color
        used |= cells
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_legend":
        # row 0 is empty → no palette, rule has nothing to look up
        for (r, c) in [(3, 2), (4, 2), (5, 2)]: g[r][c] = 7  # size-3 blob
        return g
    if name == "no_blobs":
        # legend present but no blobs → rule has nothing to recolor
        g[0][0] = 2; g[0][1] = 3; g[0][2] = 4
        return g
    if name == "blob_size_out_of_range":
        # blob of size 5, legend only has 3 entries → palette[4] undefined
        g[0][0] = 2; g[0][1] = 3; g[0][2] = 4
        for (r, c) in [(3, 5), (3, 6), (3, 7), (4, 5), (4, 6)]: g[r][c] = 7
        return g
    return g
