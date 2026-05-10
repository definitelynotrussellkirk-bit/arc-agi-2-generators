"""Generator for 15b:hard_104 — build shape × color cross-product gallery.

Rule: top row (row 0) holds 3 distinct colors. Three 3x3 mask panels
at rows 2-4 cols [0-2, 4-6, 8-10]. Output is a 3x3 gallery (mask ×
color) painted with 1-cell gaps into an 11x11 canvas.

Multi-panel family: fixed panel offsets, fixed top-row legend.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_panel_cells,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: empty_legend, empty_panels, full_panels.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2f4a0e633093"
VERSION = "1.1.0"
TASK_ID = "2f4a0e633093"

SUMMARY = "Top-row 3-color legend + 3 3x3 mask panels at fixed lower offsets."

INVARIANTS = [
    "background is 0",
    "row 0 holds 3 distinct non-bg colors at distinct columns",
    "3 3x3 panels at rows 2-4 cols [0..2], [4..6], [8..10]",
    "each panel holds 3-6 non-bg cells in a single non-legend color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("empty_legend", "empty_panels", "full_panels")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "5", "valid": "5..5"},
    "grid_w":         {"type": "int", "default": "11", "valid": "11..11"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_panel_cells":  {"type": "int", "default": "rng 3..6", "valid": "3..6"},
    "palette_size":   {"type": "int", "default": "6", "valid": "6..6"},
    "position_bias":  {"type": "str", "default": "fixed_panel_layout",
                       "valid": "fixed_panel_layout"},
    "n_distinct_colors": {"type": "int", "default": "6", "valid": "6..6"},
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
    rng = ctx.draw_rng("layout")
    h = 5; w = 11
    g = full_grid(h, w, 0)
    legend_palette = rng.sample([2, 3, 4, 6, 7, 8, 9], 3)
    legend_cols = rng.sample(range(0, w), 3)
    for col, color in zip(legend_cols, legend_palette):
        g[0][col] = color
    panel_starts = [0, 4, 8]
    panel_palette = rng.sample([c for c in [1, 2, 3, 4, 5, 6, 7, 8, 9]
                                if c not in legend_palette], 3)
    if difficulty == "easy":
        n_lo, n_hi = 3, 4
    elif difficulty == "hard":
        n_lo, n_hi = 5, 6
    else:
        n_lo, n_hi = 3, 6
    for c0, color in zip(panel_starts, panel_palette):
        cells = [(r, c0 + dc) for r in range(2, 5) for dc in range(3)]
        n = rng.randint(n_lo, n_hi)
        for r, c in rng.sample(cells, n):
            g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 5, 11
    g = full_grid(h, w, 0)
    if name == "empty_legend":
        # no top-row colors → no legend to cross-product against
        for c0, color in zip([0, 4, 8], [4, 6, 8]):
            for r, c in [(2, c0), (3, c0), (3, c0 + 1)]:
                g[r][c] = color
        return g
    if name == "empty_panels":
        # legend present but no panel masks → empty gallery
        for col, color in zip([1, 5, 9], [2, 3, 4]):
            g[0][col] = color
        return g
    if name == "full_panels":
        # all 9 cells of each panel filled → degenerate solid masks
        for col, color in zip([1, 5, 9], [2, 3, 4]):
            g[0][col] = color
        for c0, color in zip([0, 4, 8], [6, 7, 8]):
            for r in range(2, 5):
                for dc in range(3):
                    g[r][c0 + dc] = color
        return g
    return g
