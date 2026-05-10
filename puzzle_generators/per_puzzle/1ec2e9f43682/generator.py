"""Generator for arc_puzzle_bank_nineteenth21:M128 — flood 5-walled chambers with marker color.

Rule: 5-walls divide the grid into chambers. Each chamber's
interior gets fully filled with the single non-0/non-5 marker
color present in it.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_chambers,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_walls, no_markers, multiple_markers_per_chamber.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, fill_box

GENERATOR_ID = "1ec2e9f43682"
VERSION = "1.1.0"
TASK_ID = "1ec2e9f43682"
SUMMARY = "5-walled 1×2 chamber layout (two side-by-side chambers) with one marker each."

INVARIANTS = [
    "background is 0",
    "5-walls form 2 chambers side-by-side: rows 0 and h-1 are 5; cols 0, mid, w-1 are 5",
    "each chamber holds exactly one marker in a distinct non-0/non-5 color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_walls", "no_markers", "multiple_markers_per_chamber")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "4", "valid": "4..6"},
    "grid_w":         {"type": "int", "default": "rng 7..9", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_chambers":     {"type": "int", "default": "2", "valid": "2..2"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "side_by_side_chambers",
                       "valid": "side_by_side_chambers"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
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
        h = ctx.draw_int("grid_h", 4, 4)
        w = ctx.draw_int("grid_w", 7, 7)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 4, 4)
        w = ctx.draw_int("grid_w", 8, 9)
    else:
        h = ctx.draw_int("grid_h", 4, 4)
        w = ctx.draw_int("grid_w", 7, 9)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    fill_box(g, 0, 0, 0, w - 1, 5)
    fill_box(g, h - 1, 0, h - 1, w - 1, 5)
    fill_box(g, 0, 0, h - 1, 0, 5)
    mid = (w - 1) // 2
    fill_box(g, 0, mid, h - 1, mid, 5)
    fill_box(g, 0, w - 1, h - 1, w - 1, 5)
    chambers = [(1, 1, h - 2, mid - 1), (1, mid + 1, h - 2, w - 2)]
    palette = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], 2)
    for (r1, c1, r2, c2), color in zip(chambers, palette):
        cells = [(r, c) for r in range(r1, r2 + 1) for c in range(c1, c2 + 1)]
        if not cells: continue
        r, c = rng.choice(cells)
        g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 4, 7
    g = full_grid(h, w, 0)
    if name == "no_walls":
        # markers without 5-walls → no chambers to flood, undefined
        g[1][2] = 4
        g[2][5] = 6
        return g
    if name == "no_markers":
        # walls form chambers but no markers → nothing to flood with
        fill_box(g, 0, 0, 0, w - 1, 5)
        fill_box(g, h - 1, 0, h - 1, w - 1, 5)
        fill_box(g, 0, 0, h - 1, 0, 5)
        mid = (w - 1) // 2
        fill_box(g, 0, mid, h - 1, mid, 5)
        fill_box(g, 0, w - 1, h - 1, w - 1, 5)
        return g
    if name == "multiple_markers_per_chamber":
        # one chamber has 2 different colors → ambiguous flood
        fill_box(g, 0, 0, 0, w - 1, 5)
        fill_box(g, h - 1, 0, h - 1, w - 1, 5)
        fill_box(g, 0, 0, h - 1, 0, 5)
        mid = (w - 1) // 2
        fill_box(g, 0, mid, h - 1, mid, 5)
        fill_box(g, 0, w - 1, h - 1, w - 1, 5)
        g[1][1] = 4; g[2][2] = 6  # both in left chamber
        g[1][mid + 1] = 7
        return g
    return g
