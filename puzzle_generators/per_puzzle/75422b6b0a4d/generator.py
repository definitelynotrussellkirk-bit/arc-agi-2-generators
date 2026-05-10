"""Generator for arc_additional_puzzle_bank_volume2:H14.

Rule: each non-{0,5} cell is a seed. Flood-fill its 4-connected region
(cells with value 0 or matching seed color), painting 0 cells with seed
color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_compartments,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: missing_seed, conflicting_seeds, leaky_walls.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "75422b6b0a4d"
VERSION = "1.1.0"
TASK_ID = "75422b6b0a4d"
SUMMARY = "5-walls form 4 closed compartments; each holds one seed of distinct color {1,2,3,4}."

INVARIANTS = [
    "5-walls divide grid into 4 compartments",
    "each compartment has exactly one seed of distinct color from {1,2,3,4}",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("missing_seed", "conflicting_seeds", "leaky_walls")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "7", "valid": "7"},
    "grid_w":         {"type": "int", "default": "9", "valid": "9"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_compartments": {"type": "int", "default": "4", "valid": "4"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "compartment_corner",
                       "valid": "compartment_corner"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4"},
    "density":        {"type": "str", "default": "1_seed_per", "valid": "1_seed_per"},
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
    h = 7; w = 9
    g = full_grid(h, w, 5)
    # carve 2x3 compartments inside the 5-walls
    for ri, r0 in enumerate([1, 4]):
        for ci, c0 in enumerate([1, 5]):
            for r in range(r0, r0 + 2):
                for c in range(c0, c0 + 3):
                    g[r][c] = 0
    seeds_pal = [1, 2, 3, 4]
    rng.shuffle(seeds_pal)
    g[1][1] = seeds_pal[0]
    g[1][6] = seeds_pal[1]
    g[4][1] = seeds_pal[2]
    g[4][6] = seeds_pal[3]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 9
    g = full_grid(h, w, 5)
    for ri, r0 in enumerate([1, 4]):
        for ci, c0 in enumerate([1, 5]):
            for r in range(r0, r0 + 2):
                for c in range(c0, c0 + 3):
                    g[r][c] = 0
    if name == "missing_seed":
        # one compartment has no seed → that region's fill color is undefined
        g[1][1] = 1
        g[1][6] = 2
        g[4][1] = 3
        # bottom-right compartment empty
        return g
    if name == "conflicting_seeds":
        # one compartment carries 2 different seed colors → ambiguous fill
        g[1][1] = 1; g[1][3] = 2
        g[1][6] = 3
        g[4][1] = 4
        g[4][6] = 1
        return g
    if name == "leaky_walls":
        # missing wall segment lets two compartments merge → rule's
        # "one seed per chamber" assumption breaks
        g[1][1] = 1
        g[1][6] = 2
        g[4][1] = 3
        g[4][6] = 4
        g[3][4] = 0  # gap in horizontal divider
        return g
    return g
