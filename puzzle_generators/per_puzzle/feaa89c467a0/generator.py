"""Generator for 14b:hard_93 — build dihedral equivalence matrix.

Rule: 4 panels at fixed cols [0..4, 6..10, 12..16, 18..22], each 5
wide. Output is a 4x4 matrix: 8 on diagonal, 2 if rotation-equivalent,
6 if dihedrally-equivalent (mirror), 0 otherwise.

Combinatorial axes (8): grid_h, grid_w, palette_kind, panel_cell_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: empty_panel, all_identical, all_unique.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "feaa89c467a0"
VERSION = "1.1.0"
TASK_ID = "feaa89c467a0"
SUMMARY = "4 5-wide panels with binary content."

INVARIANTS = [
    "background is 0",
    "grid is 5 rows tall and 23 cols wide",
    "4 panels at cols [0..4], [6..10], [12..16], [18..22]; each holds 3-7 non-bg cells",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("empty_panel", "all_identical", "all_unique")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "5", "valid": "5"},
    "grid_w":         {"type": "int", "default": "23", "valid": "23"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "panel_cell_count": {"type": "int", "default": "rng 3..7", "valid": "1..25"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "four_panels",
                       "valid": "four_panels"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4"},
    "density":        {"type": "str", "default": "panels", "valid": "panels"},
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
    if difficulty == "easy":
        n_lo, n_hi = 3, 4
    elif difficulty == "hard":
        n_lo, n_hi = 5, 7
    else:
        n_lo, n_hi = 3, 7
    h = 5; w = 23
    starts = [0, 6, 12, 18]
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 4)
    g = full_grid(h, w, 0)
    for c0, color in zip(starts, palette):
        cells = [(r, c0 + dc) for r in range(5) for dc in range(5)]
        n = rng.randint(n_lo, n_hi)
        for r, c in rng.sample(cells, n):
            g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 5, 23
    g = full_grid(h, w, 0)
    if name == "empty_panel":
        # 1 of 4 panels is blank → its row/col in the matrix is degenerate
        for r, c in [(0, 0), (1, 1), (2, 2)]:
            g[r][c] = 1
        for r, c in [(0, 12), (1, 13), (2, 14)]:
            g[r][c] = 3
        for r, c in [(0, 18), (1, 19), (2, 20), (3, 21)]:
            g[r][c] = 5
        return g
    if name == "all_identical":
        # all 4 panels are the same shape and same color → matrix saturates
        shape = [(0, 0), (1, 0), (2, 0), (1, 1)]
        for c0 in [0, 6, 12, 18]:
            for r, dc in shape:
                g[r][c0 + dc] = 4
        return g
    if name == "all_unique":
        # all 4 pairwise inequivalent → off-diagonal = all 0
        for r, c in [(0, 0), (0, 1), (0, 2)]:
            g[r][c] = 1
        for r, c in [(0, 6), (1, 6), (2, 6)]:
            g[r][c] = 3
        for r, c in [(0, 12), (1, 13), (2, 14), (3, 15)]:
            g[r][c] = 5
        for r, c in [(0, 18), (4, 18), (0, 22), (4, 22), (2, 20)]:
            g[r][c] = 7
        return g
    return g
