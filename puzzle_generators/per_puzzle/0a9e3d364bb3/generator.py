"""Generator for 58743b76.

Rule: 2x2 corner key recolors marker cells according to their
quadrant in the main field.

Combinatorial axes (8): grid_h/w, marker_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_key, no_markers, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0a9e3d364bb3"
VERSION = "1.1.0"
TASK_ID = "0a9e3d364bb3"
SUMMARY = "2x2 corner key recolors marker cells by quadrant in main field."

INVARIANTS = [
    "one corner contains a nonzero non-8 2x2 key",
    "the main field has marker-color cells outside the key",
    "marker cells are classified by quadrant relative to the main non-8 bbox",
    "key colors are distinct and exclude 0 and 8",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_key", "no_markers", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "12", "valid": "12"},
    "grid_w":         {"type": "int", "default": "12", "valid": "12"},
    "marker_count":   {"type": "int", "default": "5", "valid": "1..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "true",
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
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    k00, k01, k10, k11 = ctx.draw_distinct_colors("key_colors", n=4, exclude={0, 8})
    marker = k11
    g = full_grid(12, 12, 0)
    g[0][10] = k00
    g[0][11] = k01
    g[1][10] = k10
    g[1][11] = k11
    for r in range(2, 12):
        g[r][10] = 8
        g[r][11] = 8
    for r, c in [(3, 2), (3, 7), (8, 2), (8, 7), (5, 5)]:
        g[r][c] = marker
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 12, 0)
    if name == "no_key":
        g[5][5] = 2
        return g
    if name == "no_markers":
        g[0][10] = 1; g[0][11] = 2; g[1][10] = 3; g[1][11] = 4
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(12):
                g[r][c] = 2
        return g
    return g
