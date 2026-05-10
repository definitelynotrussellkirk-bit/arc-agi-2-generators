"""Generator for arc_additional_puzzle_bank_volume23:E157.

Rule: yellow L-triominoes receive an orientation-coded missing-corner
color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_shapes,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_l_triominoes, all_complete_2x2, single_cells.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1221ce96e758"
VERSION = "1.1.0"
TASK_ID = "1221ce96e758"
SUMMARY = "Yellow L-triominoes receive an orientation-coded missing-corner color."

INVARIANTS = [
    "background is 0",
    "each yellow component is a three-cell L inside a 2x2 box",
    "L-triominoes are separated from each other",
    "the missing corner is initially blank",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_l_triominoes", "all_complete_2x2", "single_cells")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..12", "valid": "4..24"},
    "grid_w":         {"type": "int", "default": "rng 7..12", "valid": "4..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_shapes":       {"type": "int", "default": "rng 2..5", "valid": "1..12"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "grid_aligned_3_step",
                       "valid": "grid_aligned_3_step"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
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
        n_shapes = ctx.draw_int("n_shapes", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 12)
        w = ctx.draw_int("grid_w", 10, 12)
        n_shapes = ctx.draw_int("n_shapes", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 7, 12)
        w = ctx.draw_int("grid_w", 7, 12)
        n_shapes = ctx.draw_int("n_shapes", 2, 5)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    anchors = [(r, c) for r in range(0, h - 1, 3) for c in range(0, w - 1, 3)]
    rng.shuffle(anchors)
    local = [(0, 0), (0, 1), (1, 0), (1, 1)]
    for r, c in anchors[:n_shapes]:
        missing = rng.choice(local)
        for dr, dc in local:
            if (dr, dc) != missing:
                g[r + dr][c + dc] = 4
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_l_triominoes":
        # empty grid → no L-triominoes to mark
        return g
    if name == "all_complete_2x2":
        # all 2x2 blocks complete (no missing corner) → orientation undefined
        for r, c in [(1, 1), (1, 2), (2, 1), (2, 2)]: g[r][c] = 4
        for r, c in [(4, 5), (4, 6), (5, 5), (5, 6)]: g[r][c] = 4
        return g
    if name == "single_cells":
        # single 4-cells, not L-triominoes → invariant violated
        g[1][1] = 4
        g[4][5] = 4
        return g
    return g
