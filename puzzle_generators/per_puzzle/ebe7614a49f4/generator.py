"""Generator for arc_puzzle_bank_fifth21:M32 — row × col activation map.

Rule: 2-cells mark active rows; 1-cells mark active cols. Output: 3
at every (active-row, active-col) intersection cell.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_active_rows, n_active_cols,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_2_markers, no_1_markers, marker_color_swap.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ebe7614a49f4"
VERSION = "1.1.0"
TASK_ID = "ebe7614a49f4"
SUMMARY = "Scattered 2-cells (active rows) + 1-cells (active cols)."

INVARIANTS = [
    "background is 0",
    "≥2 cells of color 2 (each marking its row as active)",
    "≥2 cells of color 1 (each marking its col as active)",
    "2-cells and 1-cells are at distinct positions",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_2_markers", "no_1_markers", "marker_color_swap")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..8", "valid": "4..12"},
    "grid_w":         {"type": "int", "default": "rng 6..9", "valid": "5..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_active_rows":  {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "n_active_cols":  {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..3"},
    "position_bias":  {"type": "str", "default": "scattered_markers",
                       "valid": "scattered_markers"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..3"},
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
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 6, 7)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
    else:
        h = ctx.draw_int("grid_h", 5, 8)
        w = ctx.draw_int("grid_w", 6, 9)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    n_2 = rng.randint(2, 3)
    rows = rng.sample(range(h), n_2)
    for r in rows:
        c = rng.randint(0, w - 1)
        g[r][c] = 2
    n_1 = rng.randint(2, 3)
    used_cells = {(r, c) for r, row in enumerate(g) for c, v in enumerate(row) if v != 0}
    placed = 0
    for _ in range(40):
        if placed >= n_1: break
        r = rng.randint(0, h - 1)
        c = rng.randint(0, w - 1)
        if (r, c) in used_cells: continue
        g[r][c] = 1
        used_cells.add((r, c))
        placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 8
    g = full_grid(h, w, 0)
    if name == "no_2_markers":
        # only 1-cells → no active rows → output is all bg, rule trivial
        g[1][2] = 1; g[3][5] = 1; g[4][1] = 1
        return g
    if name == "no_1_markers":
        # only 2-cells → no active cols → output is all bg, rule trivial
        g[1][2] = 2; g[3][5] = 2; g[4][6] = 2
        return g
    if name == "marker_color_swap":
        # used color 8 instead of 1 or 2 → markers don't match expected role
        g[1][2] = 8; g[3][5] = 8
        g[2][3] = 7; g[4][6] = 7
        return g
    return g
