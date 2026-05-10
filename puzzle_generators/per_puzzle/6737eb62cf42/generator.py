"""Generator for arc_puzzle_bank_eighth_21_bundle:easy_51_crop_nonzero_bbox.

Rule: sparse colored cells padded by background; the rule crops the
nonzero bbox.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_cells,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_cells, single_cell, full_grid_filled.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "6737eb62cf42"
VERSION = "1.1.0"
TASK_ID = "6737eb62cf42"
SUMMARY = "Sparse colored cells padded by background; the rule crops the nonzero bbox."

INVARIANTS = [
    "background is 0",
    "there are at least two nonzero cells",
    "nonzero cells are strictly inside the grid border",
    "the nonzero bounding box is smaller than the input grid",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_cells", "single_cell", "full_grid_filled")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..11", "valid": "5..16"},
    "grid_w":         {"type": "int", "default": "rng 7..11", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_cells":        {"type": "int", "default": "rng 3..6", "valid": "2..12"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "interior_padded",
                       "valid": "interior_padded"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
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
        w = ctx.draw_int("grid_w", 7, 8)
        n_cells = ctx.draw_int("n_cells", 3, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 10, 11)
        n_cells = ctx.draw_int("n_cells", 5, 6)
    else:
        h = ctx.draw_int("grid_h", 7, 11)
        w = ctx.draw_int("grid_w", 7, 11)
        n_cells = ctx.draw_int("n_cells", 3, 6)
    colors = ctx.draw_distinct_colors("colors", n=3, exclude={0})
    rng = ctx.draw_rng("cells")
    g = full_grid(h, w, 0)
    cells = [(r, c) for r in range(1, h - 1) for c in range(1, w - 1)]
    rng.shuffle(cells)
    for i, (r, c) in enumerate(cells[:n_cells]):
        g[r][c] = colors[i % len(colors)]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "no_cells":
        # empty grid → bbox is undefined, rule has no crop target
        return g
    if name == "single_cell":
        # one cell → bbox is 1×1, rule crops to a single pixel (trivial)
        g[3][4] = 5
        return g
    if name == "full_grid_filled":
        # every interior cell painted → bbox spans the whole grid, crop is identity
        for r in range(1, h - 1):
            for c in range(1, w - 1):
                g[r][c] = ((r + c) % 3) + 1
        return g
    return g
