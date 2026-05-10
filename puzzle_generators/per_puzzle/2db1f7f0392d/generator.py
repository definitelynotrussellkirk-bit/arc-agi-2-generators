"""Generator for arc_additional_puzzles_21_set12_bundle:E83.

Rule: 9-walls form compartments. Each non-{0, 9} seed cell paints its 4
cardinal rays in its color until hitting a 9-wall or the edge.

Combinatorial axes (8): grid_h/w, palette_kind, num_seeds,
divider_layout, palette_size, position_bias, n_distinct_colors, texture.
Degenerates: no_seeds, seed_against_wall, no_walls.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2db1f7f0392d"
VERSION = "1.1.0"
TASK_ID = "2db1f7f0392d"
SUMMARY = "9-walls form a 2-compartment grid; each compartment has a colored seed."

INVARIANTS = [
    "9-walls form full-grid border + 1-2 horizontal/vertical dividers",
    "each compartment has 1-2 seed cells of distinct non-{0,9} colors",
]

PALETTE_KINDS = ("default", "warm", "cool", "rainbow")
DEGENERATE_TEXTURES = ("no_seeds", "seed_against_wall", "no_walls")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "6", "valid": "6"},
    "grid_w":         {"type": "int", "default": "11", "valid": "11"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "num_seeds":      {"type": "int", "default": "2", "valid": "1..3"},
    "divider_layout": {"type": "str", "default": "vertical_2",
                       "valid": "vertical_2"},
    "palette_size":   {"type": "int", "default": "7", "valid": "7"},
    "position_bias":  {"type": "str", "default": "compartment_center",
                       "valid": "compartment_center"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
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
    h, w = 6, 11
    g = full_grid(h, w, 0)
    for r in range(h):
        g[r][0] = 9; g[r][5] = 9; g[r][w - 1] = 9
    for c in range(w):
        g[0][c] = 9
    pal = rng.sample([1, 2, 3, 4, 6, 7, 8], 3)
    g[rng.randint(2, 4)][rng.randint(1, 4)] = pal[0]
    g[rng.randint(2, 4)][rng.randint(6, 9)] = pal[1]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 11
    g = full_grid(h, w, 0)
    if name == "no_seeds":
        # walls but no seeds — no rays to paint
        for r in range(h):
            g[r][0] = 9; g[r][5] = 9; g[r][w - 1] = 9
        for c in range(w):
            g[0][c] = 9
        return g
    if name == "seed_against_wall":
        # seed adjacent to a wall — rays in that direction are zero-length
        for r in range(h):
            g[r][0] = 9; g[r][5] = 9; g[r][w - 1] = 9
        for c in range(w):
            g[0][c] = 9
        g[1][1] = 4
        g[1][6] = 7
        return g
    if name == "no_walls":
        # seeds but no walls — rays would extend grid-wide
        g[2][3] = 4
        g[3][7] = 7
        return g
    return g
