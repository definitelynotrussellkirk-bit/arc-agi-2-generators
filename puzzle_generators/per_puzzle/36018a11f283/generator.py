"""Generator for arc_additional_puzzle_bank_volume3:H21.

Rule: 5-walls divide grid; for each non-5 region, count {2,3,4} cells
and fill with the majority color (ties go to smallest).

Combinatorial axes (8): grid_h/w, palette_kind, n_compartments,
palette_size, position_bias, n_distinct_colors, marker_density, texture.
Degenerates: no_walls, no_markers, all_tied.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "36018a11f283"
VERSION = "1.1.0"
TASK_ID = "36018a11f283"
SUMMARY = "5-walls form 4 compartments; each has 1-2 markers from {2,3,4}."

INVARIANTS = [
    "5-walls form 2x2 compartments",
    "each has 1-2 markers from {2,3,4}",
]

PALETTE_KINDS = ("default", "warm_markers", "cool_markers", "varied")
DEGENERATE_TEXTURES = ("no_walls", "no_markers", "all_tied")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "9", "valid": "9"},
    "grid_w":         {"type": "int", "default": "12", "valid": "12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_compartments": {"type": "int", "default": "4", "valid": "4"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4"},
    "marker_density": {"type": "str", "default": "low", "valid": "low"},
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
    h, w = 9, 12
    g = full_grid(h, w, 5)
    for ri, r0 in enumerate([1, 5]):
        for ci, c0 in enumerate([1, 7]):
            for r in range(r0, r0 + 3):
                for c in range(c0, c0 + 4):
                    g[r][c] = 0
    palette = [2, 3, 4]; rng.shuffle(palette)
    g[2][2] = palette[0]; g[2][3] = palette[0]
    g[5][2] = palette[1]; g[6][2] = palette[1]
    g[2][8] = palette[2]; g[2][9] = palette[2]
    g[6][8] = 2; g[6][9] = 4
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 12
    if name == "no_walls":
        # no 5-walls → no compartments, rule has nothing to fill
        g = full_grid(h, w, 0)
        g[2][2] = 2; g[2][3] = 2
        g[5][2] = 3; g[6][2] = 3
        return g
    if name == "no_markers":
        # walls + compartments but no {2,3,4} markers — all majority counts zero
        g = full_grid(h, w, 5)
        for ri, r0 in enumerate([1, 5]):
            for ci, c0 in enumerate([1, 7]):
                for r in range(r0, r0 + 3):
                    for c in range(c0, c0 + 4):
                        g[r][c] = 0
        return g
    if name == "all_tied":
        # every compartment has all three markers tied (1 each) — fill ambiguous
        g = full_grid(h, w, 5)
        for ri, r0 in enumerate([1, 5]):
            for ci, c0 in enumerate([1, 7]):
                for r in range(r0, r0 + 3):
                    for c in range(c0, c0 + 4):
                        g[r][c] = 0
        for r0, c0 in [(1, 1), (1, 7), (5, 1), (5, 7)]:
            g[r0][c0] = 2
            g[r0 + 1][c0 + 1] = 3
            g[r0 + 2][c0 + 2] = 4
        return g
    return full_grid(h, w, 0)
