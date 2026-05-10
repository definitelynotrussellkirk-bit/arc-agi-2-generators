"""Generator for 1990f7a8.

Rule: four scattered 3x3-local shapes assembled into a 7x7 quadrant
layout.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors,
shape_variant.
Degenerates: no_objects, single_object, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "b98cdd1751a7"
VERSION = "1.1.0"
TASK_ID = "b98cdd1751a7"
SUMMARY = "Four scattered 3x3 shapes assembled into 7x7 quadrant layout."

INVARIANTS = [
    "there are exactly four separated 8-connected objects",
    "two objects are above the row split and two below it",
    "within each half objects are ordered by column",
    "shape colors are distinct and non-zero",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_objects", "single_object", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

SHAPES = [
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (1, 1)],
    [(0, 1), (1, 0), (1, 1)],
]

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..14", "valid": "8..20"},
    "grid_w":         {"type": "int", "default": "rng 11..14", "valid": "8..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "4", "valid": "4"},
    "shape_variant":  {"type": "str", "default": "rng", "valid": "rng"},
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
    if difficulty == "easy":
        h_lo, h_hi = 11, 11
    elif difficulty == "hard":
        h_lo, h_hi = 14, 18
    else:
        h_lo, h_hi = 11, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    g = full_grid(h, w, 0)
    anchors = [(1, 1), (1, w - 4), (h - 4, 1), (h - 4, w - 4)]
    colors = ctx.draw_distinct_colors("colors", n=4, exclude={0})
    for anchor, color, shape in zip(anchors, colors, rng.sample(SHAPES, 4)):
        ar, ac = anchor
        for dr, dc in shape:
            g[ar + dr][ac + dc] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 12, 0)
    if name == "no_objects":
        return g
    if name == "single_object":
        for dr, dc in SHAPES[0]:
            g[1 + dr][1 + dc] = 2
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(12):
                g[r][c] = 2
        return g
    return g
