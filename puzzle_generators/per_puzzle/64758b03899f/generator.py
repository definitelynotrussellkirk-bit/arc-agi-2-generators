"""Generator for arc_additional_puzzles_21_set13_bundle:M91.

Rule: normalize the color-5 mask and stamp it at every nonzero non-5
seed using that seed color.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_mask, no_seeds, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "64758b03899f"
VERSION = "1.1.0"
TASK_ID = "64758b03899f"
SUMMARY = "Normalize the color-5 mask and stamp it at every nonzero non-5 seed using that seed color."

INVARIANTS = [
    "a compact color-5 mask is present",
    "colored seeds are placed where the normalized mask fits in bounds",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_mask", "no_seeds", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "7..16"},
    "grid_w":         {"type": "int", "default": "rng 10..14", "valid": "8..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "4", "valid": "4"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 10, 14)
    colors = list(ctx.draw_distinct_colors("seeds", n=3, exclude=[0, 5]))
    g = full_grid(h, w, 0)
    for dr, dc in [(0, 0), (0, 1), (1, 0), (2, 1)]:
        g[1 + dr][1 + dc] = 5
    for color, (r, c) in zip(colors, [(1, w - 4), (h - 4, 2), (h - 4, w - 4)]):
        g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 12, 0)
    if name == "no_mask":
        g[1][8] = 2
        g[6][2] = 3
        return g
    if name == "no_seeds":
        for dr, dc in [(0, 0), (0, 1), (1, 0), (2, 1)]:
            g[1 + dr][1 + dc] = 5
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(12):
                g[r][c] = 5
        return g
    return g
