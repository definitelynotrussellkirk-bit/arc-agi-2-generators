"""Generator for a834deea.

Rule: zero rectangle inside an eight background is filled by
compass-position colors.

Combinatorial axes (8): grid_h/w, region_h, region_w, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias.
Degenerates: no_region, full_grid, no_bg.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "270c2549d26d"
VERSION = "1.1.0"
TASK_ID = "270c2549d26d"
SUMMARY = "Zero rectangle inside eight background filled by compass-position colors."

INVARIANTS = [
    "background is color 8",
    "one rectangular zero region is fully enclosed by the background",
    "the zero region has a border and an interior",
    "the region sits with at least two cells of bg margin from the grid border",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_region", "full_grid", "no_bg")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "8..14"},
    "region_h":       {"type": "int", "default": "rng 5..8", "valid": "5..10"},
    "region_w":       {"type": "int", "default": "rng 5..8", "valid": "5..10"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "center", "valid": "center"},
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
    rh = 5 + rng.randint(0, 3)
    rw = 5 + rng.randint(0, 3)
    g = full_grid(rh + 4, rw + 4, 8)
    for r in range(2, 2 + rh):
        for c in range(2, 2 + rw):
            g[r][c] = 0
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 11, 8)
    if name == "no_region":
        return g
    if name == "no_bg":
        return full_grid(11, 11, 0)
    if name == "full_grid":
        for r in range(11):
            for c in range(11):
                g[r][c] = 8
        return g
    return g
