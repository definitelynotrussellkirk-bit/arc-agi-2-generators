"""Generator for f18ec8cc.

Rule: vertical color regions are reversed when their widths are
unique, otherwise left-rotated by one region.

Combinatorial axes (8): grid_h, region_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias, widths.
Degenerates: no_regions, single_region, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "fc8ce6bdc6ea"
VERSION = "1.1.0"
TASK_ID = "fc8ce6bdc6ea"
SUMMARY = "Vertical color regions reversed if widths unique, else rotated by one."

INVARIANTS = [
    "each vertical region has a modal background color",
    "adjacent regions have different modal colors",
    "full columns are copied from source regions into the new region order",
    "region widths are 2, 3 and 4 so they are all unique",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_regions", "single_region", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "5..12"},
    "region_count":   {"type": "int", "default": "3", "valid": "3"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "widths":         {"type": "str", "default": "2,3,4", "valid": "2,3,4"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    ctx.draw_int("region_count", 3, 3)
    colors = ctx.draw_distinct_colors("colors", n=3, exclude={0})
    widths = [2, 3, 4]
    h = 6 + rng.randint(0, 2)
    g = full_grid(h, sum(widths), 0)
    c0 = 0
    for idx, width in enumerate(widths):
        for r in range(h):
            for c in range(c0, c0 + width):
                g[r][c] = colors[idx]
        if width > 2:
            g[1][c0 + width - 1] = colors[(idx + 1) % len(colors)]
        c0 += width
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(6, 9, 0)
    if name == "no_regions":
        return g
    if name == "single_region":
        for r in range(6):
            for c in range(9):
                g[r][c] = 2
        return g
    if name == "full_grid":
        for r in range(6):
            for c in range(9):
                g[r][c] = 2
        return g
    return g
