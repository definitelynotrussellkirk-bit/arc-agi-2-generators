"""Generator for 42f14c03.

Rule: hollow 3x3 template frame has one one-cell filler whose area
exactly matches the hole.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors,
filler_color.
Degenerates: no_template, no_filler, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, draw_frame

GENERATOR_ID = "ce7050977ab7"
VERSION = "1.1.0"
TASK_ID = "ce7050977ab7"
SUMMARY = "Hollow 3x3 template frame has one one-cell filler matching the hole."

INVARIANTS = [
    "background is 0",
    "largest object is a 3x3 frame with one-cell hole",
    "one singleton filler object supplies the hole color",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_template", "no_filler", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "7", "valid": "7"},
    "grid_w":         {"type": "int", "default": "8", "valid": "8"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "filler_color":   {"type": "color", "default": "rng !{0}",
                       "valid": "1..9"},
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
    template_color = ctx.draw_color("template_color", exclude={0})
    filler_color = ctx.draw_color("filler_color", exclude={0, template_color})
    g = full_grid(7, 8, 0)
    draw_frame(g, 1, 1, 3, 3, template_color)
    g[rng.randint(4, 6)][rng.randint(5, 7)] = filler_color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(7, 8, 0)
    if name == "no_template":
        g[5][5] = 4
        return g
    if name == "no_filler":
        draw_frame(g, 1, 1, 3, 3, 3)
        return g
    if name == "full_grid":
        for r in range(7):
            for c in range(8):
                g[r][c] = 3
        return g
    return g
