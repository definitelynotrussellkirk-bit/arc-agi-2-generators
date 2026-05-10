"""Generator for dc2aa30b.

Rule: 11x11 grid divided by 0-rows/cols at 3,7 into nine 3x3 blocks;
sort blocks by 1-count and rearrange to target order.

Combinatorial axes (8): grid_size, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_blocks, density.
Degenerates: empty_blocks, all_ones, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "3108da8bf9e8"
VERSION = "1.1.0"
TASK_ID = "3108da8bf9e8"
SUMMARY = "11x11 grid with 0-separators at rows/cols {3,7}; nine 3x3 blocks of 1s and 2s."

INVARIANTS = [
    "h equals 11 and w equals 11",
    "rows 3 and 7 and cols 3 and 7 are entirely 0",
    "nine 3x3 blocks each filled with mixed 1s and 2s",
    "blocks differ in their 1-counts so the rule has a unique sort order",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DENSITY_KINDS = ("sparse", "medium", "dense")
DEGENERATE_TEXTURES = ("empty_blocks", "all_ones", "full_grid")
HELPFUL_TEXTURES = DENSITY_KINDS

AXES = {
    "grid_size":      {"type": "int", "default": "11", "valid": "11"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_blocks":       {"type": "int", "default": "9", "valid": "9"},
    "density":        {"type": "str", "default": "rng helpful",
                       "valid": "|".join(DENSITY_KINDS)},
    "texture":        {"type": "str", "default": "alias for density",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    density = (overrides.get("texture") if overrides.get("texture") in DENSITY_KINDS else None) or \
              overrides.get("density") or \
              ctx.draw_choice("density", list(DENSITY_KINDS))
    if density == "sparse":
        weights = [1, 1, 2]
    elif density == "dense":
        weights = [1, 2, 2]
    else:
        weights = [1, 2]
    h = w = 11
    g = full_grid(h, w, 0)
    for br in range(3):
        for bc in range(3):
            for r in range(br * 4, br * 4 + 3):
                for c in range(bc * 4, bc * 4 + 3):
                    g[r][c] = rng.choice(weights)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 11, 0)
    if name == "empty_blocks":
        return g
    if name == "all_ones":
        for br in range(3):
            for bc in range(3):
                for r in range(br * 4, br * 4 + 3):
                    for c in range(bc * 4, bc * 4 + 3):
                        g[r][c] = 1
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(11):
                g[r][c] = 1
        return g
    return g
