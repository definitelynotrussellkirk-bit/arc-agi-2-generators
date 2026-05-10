"""Generator for arc_additional_puzzles_21_set20_bundle:M138 — Flood single-color compartments.

Rule: 8-walls divide grid into compartments. For each compartment, if it
has exactly one non-{0,8} color, fill that compartment with that color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_seeds,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_walls, no_seeds, multi_color_compartment.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "058ae70e4bdb"
VERSION = "1.1.0"
TASK_ID = "058ae70e4bdb"
SUMMARY = "8-walls divide canvas into 4 compartments; 3 have single seed colors, 1 is empty."

INVARIANTS = [
    "8-walls form a 2x2 grid of compartments",
    "exactly 3 compartments have a single non-{0,8} seed",
    "1 compartment is empty (no fill)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_walls", "no_seeds", "multi_color_compartment")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "9", "valid": "9..9"},
    "grid_w":         {"type": "int", "default": "11", "valid": "11..11"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_seeds":        {"type": "int", "default": "3", "valid": "3..3"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4..4"},
    "position_bias":  {"type": "str", "default": "four_walled_compartments",
                       "valid": "four_walled_compartments"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "5..5"},
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
    h = 9; w = 11
    g = full_grid(h, w, 8)
    rows = [(1, 3), (5, 7)]
    cols = [(1, 4), (6, 9)]
    seeds = [(2, 2), (3, 6), (6, 7), None]
    rng.shuffle(seeds)
    for ri, (r0, r1) in enumerate(rows):
        for ci, (c0, c1) in enumerate(cols):
            for r in range(r0, r1 + 1):
                for c in range(c0, c1 + 1):
                    g[r][c] = 0
    palette = [2, 3, 4, 6]; rng.shuffle(palette)
    placements = [(2, 2), (2, 7), (6, 2), (6, 7)]
    chosen_idx = rng.randint(0, 3)
    for i, pos in enumerate(placements):
        if i == chosen_idx: continue
        g[pos[0]][pos[1]] = palette[i]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_walls":
        # seeds but no 8-walls → compartments not defined
        g[2][2] = 4
        g[3][7] = 6
        g[6][3] = 7
        return g
    if name == "no_seeds":
        # walls form 4 compartments but no seeds → no color to fill any compartment
        g = full_grid(h, w, 8)
        rows = [(1, 3), (5, 7)]
        cols = [(1, 4), (6, 9)]
        for r0, r1 in rows:
            for c0, c1 in cols:
                for r in range(r0, r1 + 1):
                    for c in range(c0, c1 + 1):
                        g[r][c] = 0
        return g
    if name == "multi_color_compartment":
        # one compartment has TWO different seed colors → ambiguous fill color
        g = full_grid(h, w, 8)
        rows = [(1, 3), (5, 7)]
        cols = [(1, 4), (6, 9)]
        for r0, r1 in rows:
            for c0, c1 in cols:
                for r in range(r0, r1 + 1):
                    for c in range(c0, c1 + 1):
                        g[r][c] = 0
        g[2][2] = 4; g[3][3] = 6   # two colors in same compartment
        g[2][7] = 7
        g[6][2] = 3
        return g
    return g
