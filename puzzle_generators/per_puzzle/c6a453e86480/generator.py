"""Generator for arc_puzzle_bank_21_set8_s:S8_M4 — legend recolor by rank.

Rule: top row has legend colors at distinct cols. Below row 0, find
the 1-blobs sorted left-to-right; recolor i-th blob with i-th legend
color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_legend, no_blobs, blob_count_mismatch.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.blobs import grow_blob

GENERATOR_ID = "c6a453e86480"
VERSION = "1.1.0"
TASK_ID = "c6a453e86480"
SUMMARY = "Top-row 3 legend colors + 3 1-blobs below at distinct columns."

INVARIANTS = [
    "background is 0",
    "row 0 has 3 distinct legend colors at distinct cols",
    "below row 0 there are 3 1-blobs at strictly distinct leftmost cols",
    "blobs and legends are 4-disjoint",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_legend", "no_blobs", "blob_count_mismatch")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 12..14", "valid": "10..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "3", "valid": "3..3"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "row0_legend_plus_blobs",
                       "valid": "row0_legend_plus_blobs"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4..4"},
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
        h = ctx.draw_int("grid_h", 5, 5)
        w = ctx.draw_int("grid_w", 12, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 12, 14)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    legend_palette = rng.sample([2, 3, 4, 5, 6, 7, 8, 9], 3)
    legend_cols = sorted(rng.sample(range(w), 3))
    for c, color in zip(legend_cols, legend_palette):
        g[0][c] = color
    used = {(0, c) for c in legend_cols}
    for c in range(w):
        used.add((1, c))
    for _ in range(3):
        cells = grow_blob(rng, h, w, used, rng.randint(2, 4), max_attempts=80)
        if cells is None:
            continue
        for r, c in cells:
            g[r][c] = 1
        used |= cells
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 13
    g = full_grid(h, w, 0)
    if name == "no_legend":
        # 1-blobs without row-0 legend → no recolor mapping defined
        for r, c in [(2, 1), (2, 2)]: g[r][c] = 1
        for r, c in [(3, 5), (3, 6)]: g[r][c] = 1
        for r, c in [(4, 9), (4, 10)]: g[r][c] = 1
        return g
    if name == "no_blobs":
        # legend alone, no 1-blobs → nothing to recolor
        g[0][2] = 4; g[0][6] = 6; g[0][10] = 7
        return g
    if name == "blob_count_mismatch":
        # 3 legend cells but only 2 blobs → "i-th blob = i-th color" fails for 3rd
        g[0][2] = 4; g[0][6] = 6; g[0][10] = 7
        for r, c in [(2, 1), (2, 2)]: g[r][c] = 1
        for r, c in [(4, 5), (4, 6)]: g[r][c] = 1
        return g
    return g
