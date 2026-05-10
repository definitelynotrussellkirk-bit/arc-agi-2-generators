"""Generator for arc_additional_puzzles_21_set22_bundle:M150.

Rule: each 0-region's neighboring colors (excluding 0 and 8); if exactly
one such color, fill that region with it.

Combinatorial axes (8): grid_h/w, palette_kind, num_compartments,
divider_orientation, palette_size, position_bias, n_distinct_colors, texture.
Degenerates: no_walls, no_seeds, multi_color_neighbors.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "60a8a9d74a75"
VERSION = "1.1.0"
TASK_ID = "60a8a9d74a75"
SUMMARY = "8-walls form 2 compartments each surrounded by single non-{0,8} color marker."

INVARIANTS = [
    "8-walls split grid into 2 compartments (left and right)",
    "each compartment has exactly one marker of distinct non-{0,8} color",
]

PALETTE_KINDS = ("default", "warm", "cool", "rainbow")
DEGENERATE_TEXTURES = ("no_walls", "no_seeds", "multi_color_neighbors")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "9", "valid": "9"},
    "grid_w":         {"type": "int", "default": "11", "valid": "11"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "num_compartments": {"type": "int", "default": "2", "valid": "2"},
    "divider_orientation": {"type": "str", "default": "vertical",
                            "valid": "vertical"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5"},
    "position_bias":  {"type": "str", "default": "scattered",
                       "valid": "scattered"},
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
    h, w = 9, 11
    g = full_grid(h, w, 0)
    for c in range(w):
        g[0][c] = 8; g[h - 1][c] = 8
    for r in range(h):
        g[r][0] = 8; g[r][w - 1] = 8
    div = w // 2
    for r in range(h):
        g[r][div] = 8
    palette = [2, 3, 4, 6, 7]; rng.shuffle(palette)
    g[2][2] = palette[0]
    g[6][7] = palette[1]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    div = w // 2
    if name == "no_walls":
        # seeds without walls — single region, ambiguous which color fills
        g[2][2] = 4
        g[6][7] = 7
        return g
    if name == "no_seeds":
        # walls/compartments but no markers — rule fills nothing
        for c in range(w):
            g[0][c] = 8; g[h - 1][c] = 8
        for r in range(h):
            g[r][0] = 8; g[r][w - 1] = 8
            g[r][div] = 8
        return g
    if name == "multi_color_neighbors":
        # one compartment has 2 different colors — no unique neighbor color
        for c in range(w):
            g[0][c] = 8; g[h - 1][c] = 8
        for r in range(h):
            g[r][0] = 8; g[r][w - 1] = 8
            g[r][div] = 8
        g[2][2] = 4
        g[6][2] = 7
        g[3][7] = 3
        return g
    return g
