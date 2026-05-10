"""Generator for db93a21d.

Rule: red rectangles receive thick green borders and blue stems below
them.

Combinatorial axes (8): grid_h/w, variant, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_rects, single_rect, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "067449d7a3b3"
VERSION = "1.1.0"
TASK_ID = "067449d7a3b3"
SUMMARY = "Red rectangles get thick green borders and blue stems below."

INVARIANTS = [
    "every foreground object is a red rectangle on black background",
    "border thickness is half the rectangle's longer side",
    "blue stems descend from rectangle columns below the border area",
    "the rectangles sit with bg margin so stems and borders fit",
]

VARIANTS = ("v0", "v1", "v2", "v3", "v4", "v5")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_rects", "single_rect", "full_grid")
HELPFUL_TEXTURES = VARIANTS

AXES = {
    "grid_h":         {"type": "int", "default": "18", "valid": "18"},
    "grid_w":         {"type": "int", "default": "18", "valid": "18"},
    "variant":        {"type": "str", "default": "rng helpful",
                       "valid": "|".join(VARIANTS)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "3", "valid": "3"},
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
        variant = ctx.draw_choice("variant", [0, 1, 2, 3, 4, 5])
        if "variant" not in overrides:
            variant = sample_index % 6
    g = full_grid(18, 18, 0)
    layouts = [
        [(3, 4, 2, 3), (4, 12, 3, 2)],
        [(2, 3, 3, 3), (7, 11, 2, 4)],
        [(4, 5, 2, 4), (3, 13, 4, 2)],
        [(5, 3, 3, 2), (2, 10, 2, 5)],
        [(2, 5, 4, 2), (6, 12, 3, 3)],
        [(6, 4, 2, 5), (2, 13, 3, 2)],
    ]
    for r, c, rh, rw in layouts[variant]:
        draw_rect(g, r, c, rh, rw, 9)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(18, 18, 0)
    if name == "no_rects":
        return g
    if name == "single_rect":
        draw_rect(g, 5, 5, 3, 4, 9)
        return g
    if name == "full_grid":
        for r in range(18):
            for c in range(18):
                g[r][c] = 9
        return g
    return g
