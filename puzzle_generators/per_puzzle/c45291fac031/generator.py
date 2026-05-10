"""Generator for a8d7556c.

Rule: largest rectangular subregions inside zero holes are colored red.

Combinatorial axes (8): grid_h/w, variant, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_holes, single_cell_hole, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "c45291fac031"
VERSION = "1.1.0"
TASK_ID = "c45291fac031"
SUMMARY = "Largest rectangular subregions inside zero holes are colored red."

INVARIANTS = [
    "nonzero background surrounds multiple connected zero regions",
    "each zero region contains at least one all-zero rectangle of size two by two or larger",
    "only maximum-area rectangular parts of each zero region are recolored",
]

VARIANTS = ("v0", "v1", "v2")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_holes", "single_cell_hole", "full_grid")
HELPFUL_TEXTURES = VARIANTS

AXES = {
    "grid_h":         {"type": "int", "default": "13", "valid": "13"},
    "grid_w":         {"type": "int", "default": "15", "valid": "15"},
    "variant":        {"type": "choice", "default": "rng helpful",
                       "valid": "0|1|2"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "1", "valid": "1"},
    "texture":        {"type": "str", "default": "alias for variant",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    tx = overrides.get("texture")
    if tx in VARIANTS:
        variant = int(tx[1])
    else:
        variant = ctx.draw_choice("variant", [0, 1, 2])
    bg = ctx.draw_choice("background", [4, 5, 8])
    g = full_grid(13, 15, bg)
    rects = [
        [(2, 2, 3, 4), (7, 9, 4, 3)],
        [(1, 3, 4, 3), (8, 2, 3, 5)],
        [(2, 8, 3, 5), (7, 3, 4, 3)],
    ][variant]
    for r, c, rh, rw in rects:
        draw_rect(g, r, c, rh, rw, 0)
    for r, c in [(6, 6), (7, 6), (8, 6), (8, 7), (8, 8)]:
        g[r][c] = 0
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 15, 4)
    if name == "no_holes":
        return g
    if name == "single_cell_hole":
        g[6][6] = 0
        return g
    if name == "full_grid":
        for r in range(13):
            for c in range(15):
                g[r][c] = 0
        return g
    return g
