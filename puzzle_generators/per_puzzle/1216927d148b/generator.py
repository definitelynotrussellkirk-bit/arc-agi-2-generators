"""Generator for arc_puzzle_bank_fourteenth_21_bundle:hard_96_build_pairwise_intersection_gallery.

Rule: 3 panels at fixed cols [0..4, 6..10, 12..16], each 5 wide.
Output hstacks the 3 pairwise intersections of their binary masks.

Combinatorial axes (8): grid_h, grid_w, palette_kind, panel_cell_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: empty_panels, full_panels, single_panel.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1216927d148b"
VERSION = "1.1.0"
TASK_ID = "1216927d148b"
SUMMARY = "3 5-wide panels with binary content; pairwise intersection."

INVARIANTS = [
    "background is 0",
    "grid is 5 rows tall and 17 cols wide",
    "3 panels at cols [0..4], [6..10], [12..16]; each holds 3-7 non-bg cells",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("empty_panels", "full_panels", "single_panel")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "5", "valid": "5"},
    "grid_w":         {"type": "int", "default": "17", "valid": "17"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "panel_cell_count": {"type": "int", "default": "rng 3..7 per panel", "valid": "1..25"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed_panels", "valid": "fixed_panels"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "density":        {"type": "str", "default": "varied", "valid": "varied"},
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
    h = 5; w = 17
    starts = [0, 6, 12]
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)
    g = full_grid(h, w, 0)
    if difficulty == "easy":
        lo, hi = 5, 7
    elif difficulty == "hard":
        lo, hi = 3, 5
    else:
        lo, hi = 3, 7
    for c0, color in zip(starts, palette):
        cells = [(r, c0 + dc) for r in range(5) for dc in range(5)]
        n = rng.randint(lo, hi)
        for r, c in rng.sample(cells, n):
            g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 5, 17
    starts = [0, 6, 12]
    g = full_grid(h, w, 0)
    if name == "empty_panels":
        # all 3 panels empty → every pairwise intersection is empty, output all-bg
        return g
    if name == "full_panels":
        # all 3 panels fully filled → every intersection equals the panel mask
        for c0, color in zip(starts, [1, 2, 3]):
            for r in range(5):
                for dc in range(5):
                    g[r][c0 + dc] = color
        return g
    if name == "single_panel":
        # only the first panel populated → second/third intersections are vacuously empty
        for r, c in [(0, 0), (1, 1), (2, 2), (3, 3), (4, 0)]:
            g[r][c] = 4
        return g
    return g
