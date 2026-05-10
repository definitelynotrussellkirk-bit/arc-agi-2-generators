"""Generator for arc_additional_puzzle_bank_volume4:H23 — Flood compartments by single seed.

Rule: 5-walls divide grid into compartments. For each compartment, if it
has exactly one seed (color ∈ {1,2,3}), fill the compartment with seed color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_seeds,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_walls, no_seeds, multiple_seeds_per_compartment.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "529bd4803bcc"
VERSION = "1.1.0"
TASK_ID = "529bd4803bcc"
SUMMARY = "5-walls form 4 compartments; some have 1 seed (filled), some 0/2+ (skipped)."

INVARIANTS = [
    "5-walls form 2x2 compartments",
    "between 2 and 3 compartments have exactly one seed of color {1,2,3}",
    "remaining compartments have 0 or ≥2 seeds (kept empty/unchanged)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_walls", "no_seeds", "multiple_seeds_per_compartment")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "9", "valid": "9..9"},
    "grid_w":         {"type": "int", "default": "9", "valid": "9..9"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_seeds":        {"type": "int", "default": "3", "valid": "3..3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "five_walls_with_seeds",
                       "valid": "five_walls_with_seeds"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
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
    h = 9; w = 9
    g = full_grid(h, w, 5)
    for ri, r0 in enumerate([0, 5]):
        for ci, c0 in enumerate([0, 5]):
            for r in range(r0, r0 + 4):
                for c in range(c0, c0 + 4):
                    if r < 4 and c < 4: g[r][c] = 0
                    elif r < 4 and c >= 5: g[r][c] = 0
                    elif r >= 5 and c < 4: g[r][c] = 0
                    elif r >= 5 and c >= 5: g[r][c] = 0
    palette = [1, 2, 3]; rng.shuffle(palette)
    seeds = [(1, 1), (1, 6), (6, 1), (6, 6)]
    rng.shuffle(seeds)
    g[seeds[0][0]][seeds[0][1]] = palette[0]
    g[seeds[1][0]][seeds[1][1]] = palette[1]
    g[seeds[2][0]][seeds[2][1]] = palette[2]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    if name == "no_walls":
        # seeds without 5-walls → no compartment boundaries to flood within
        g = full_grid(h, w, 0)
        g[1][1] = 1; g[1][6] = 2; g[6][1] = 3
        return g
    if name == "no_seeds":
        # walls and compartments but no seeds → nothing to flood
        g = full_grid(h, w, 5)
        for ri, r0 in enumerate([0, 5]):
            for ci, c0 in enumerate([0, 5]):
                for r in range(r0, r0 + 4):
                    for c in range(c0, c0 + 4):
                        if (r < 4 or r >= 5) and (c < 4 or c >= 5): g[r][c] = 0
        return g
    if name == "multiple_seeds_per_compartment":
        # one compartment has 2+ seeds → "exactly one seed" precondition fails
        g = full_grid(h, w, 5)
        for ri, r0 in enumerate([0, 5]):
            for ci, c0 in enumerate([0, 5]):
                for r in range(r0, r0 + 4):
                    for c in range(c0, c0 + 4):
                        if (r < 4 or r >= 5) and (c < 4 or c >= 5): g[r][c] = 0
        g[1][1] = 1; g[2][2] = 2  # both in TL compartment
        g[6][6] = 3
        return g
    return full_grid(h, w, 0)
