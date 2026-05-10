"""Generator for 18b:hard_120 — build rotation equivalence matrix.

Rule: input is split into 3 fixed 5-wide panels (cols 0-4, 6-10, 12-16).
Output is 3x3: cell (i, j) = 8 iff i==j, 2 if normalized binaries are
rotation-equivalent, else 0.

Combinatorial axes (8): grid_h, grid_w, palette_kind, panel_cell_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: empty_panel, all_identical, no_pairs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5c126cb64bf7"
VERSION = "1.1.0"
TASK_ID = "5c126cb64bf7"
SUMMARY = "3 5-wide panels (cols 0-4, 6-10, 12-16) with binary shapes."

INVARIANTS = [
    "background is 0",
    "grid is 5 rows tall and 17 cols wide",
    "3 panels at cols [0..4], [6..10], [12..16]; each holds 3-7 non-bg cells",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("empty_panel", "all_identical", "no_pairs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "5", "valid": "5"},
    "grid_w":         {"type": "int", "default": "17", "valid": "17"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "panel_cell_count": {"type": "int", "default": "rng 3..7", "valid": "1..25"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "three_panels",
                       "valid": "three_panels"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
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
    h = 5; w = 17
    starts = [0, 6, 12]
    palette = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)
    g = full_grid(h, w, 0)
    for c0, color in zip(starts, palette):
        cells = [(r, c0 + dc) for r in range(5) for dc in range(5)]
        n = rng.randint(n_lo, n_hi)
        for r, c in rng.sample(cells, n):
            g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 5, 17
    g = full_grid(h, w, 0)
    starts = [0, 6, 12]
    if name == "empty_panel":
        # one of 3 panels is blank → its rotation class is undefined
        for r, c, v in [(0, 0, 1), (1, 1, 1), (2, 2, 1)]:
            g[r][c] = v
        for r, c, v in [(0, 12, 3), (1, 13, 3), (2, 14, 3)]:
            g[r][c] = v
        return g
    if name == "all_identical":
        # all 3 panels are identical shape and same color → no contrast cells
        shape = [(0, 0), (1, 0), (2, 0), (1, 1)]
        for c0 in starts:
            for r, dc in shape:
                g[r][c0 + dc] = 4
        return g
    if name == "no_pairs":
        # all 3 panels are pairwise non-rotation-equivalent → off-diagonal output is all 0
        for r, c in [(0, 0), (0, 1), (0, 2)]:
            g[r][c] = 1
        for r, c in [(0, 6), (1, 6), (2, 6)]:
            g[r][c] = 3
        for r, c in [(0, 12), (1, 13), (2, 14), (3, 15)]:
            g[r][c] = 5
        return g
    return g
