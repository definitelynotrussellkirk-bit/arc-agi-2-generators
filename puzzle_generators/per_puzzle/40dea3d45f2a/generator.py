"""Generator for arc_puzzle_bank_twelfth_21_bundle:hard_79_dihedral_equivalence_matrix_ignoring_color.

Rule: 4 panels at 2x2 positions [(0,0), (0,5), (5,0), (5,5)] (4 wide
× 4 tall each). Output 4x4: 8 if panels j and i are dihedrally
equivalent, else 0.

Combinatorial axes (8): grid_h, grid_w, palette_kind, panel_cell_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: empty_panels, all_equivalent, all_distinct.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "40dea3d45f2a"
VERSION = "1.1.0"
TASK_ID = "40dea3d45f2a"
SUMMARY = "4 4x4 panels at fixed 2x2 grid positions [(0,0),(0,5),(5,0),(5,5)]."

INVARIANTS = [
    "background is 0",
    "grid is 9 rows tall and 9 cols wide",
    "4 panels at top-lefts [(0,0), (0,5), (5,0), (5,5)] each 4x4",
    "each panel holds 3-7 non-bg cells in any non-bg color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("empty_panels", "all_equivalent", "all_distinct")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "9", "valid": "9"},
    "grid_w":         {"type": "int", "default": "9", "valid": "9"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "panel_cell_count": {"type": "int", "default": "rng 3..7", "valid": "1..16"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "fixed_2x2_panels",
                       "valid": "fixed_2x2_panels"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4"},
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
    h = 9; w = 9
    g = full_grid(h, w, 0)
    starts = [(0, 0), (0, 5), (5, 0), (5, 5)]
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 4)
    if difficulty == "easy":
        lo, hi = 5, 7
    elif difficulty == "hard":
        lo, hi = 3, 5
    else:
        lo, hi = 3, 7
    for (r0, c0), color in zip(starts, palette):
        cells = [(r0 + dr, c0 + dc) for dr in range(4) for dc in range(4)]
        n = rng.randint(lo, hi)
        for r, c in rng.sample(cells, n):
            g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    starts = [(0, 0), (0, 5), (5, 0), (5, 5)]
    g = full_grid(h, w, 0)
    if name == "empty_panels":
        # all panels empty → every pair is trivially equivalent (uniform 8)
        return g
    if name == "all_equivalent":
        # all panels share one shape → matrix is all-8 with 4 different colors
        shape = [(0, 0), (1, 1), (2, 2), (3, 3)]
        for (r0, c0), color in zip(starts, [1, 2, 3, 4]):
            for dr, dc in shape:
                g[r0 + dr][c0 + dc] = color
        return g
    if name == "all_distinct":
        # every panel has a different (non-equivalent) shape → matrix is identity (only diag is 8)
        shapes = [
            [(0, 0), (0, 1), (1, 0)],
            [(0, 0), (1, 0), (2, 0), (3, 0)],
            [(0, 0), (0, 1), (0, 2), (1, 1)],
            [(0, 0), (0, 1), (1, 0), (2, 1), (3, 3)],
        ]
        for (r0, c0), color, shape in zip(starts, [1, 2, 3, 4], shapes):
            for dr, dc in shape:
                g[r0 + dr][c0 + dc] = color
        return g
    return g
