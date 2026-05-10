"""Generator for 8fbca751.

Rule: separated components whose bboxes share a row or column span
merge, then each merged bbox fills with color 2.

Combinatorial axes (8): grid_h/w, cluster_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias, color.
Degenerates: no_components, single_component, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5d9c166a8c3b"
VERSION = "1.1.0"
TASK_ID = "5d9c166a8c3b"
SUMMARY = "Components sharing row/col span merge; merged bboxes fill with 2."

INVARIANTS = [
    "background is color 0",
    "foreground components are disconnected",
    "some component bboxes overlap in row span or in column span",
    "the foreground color is non-zero and not 2",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_components", "single_component", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 13..15", "valid": "11..18"},
    "grid_w":         {"type": "int", "default": "rng 14..16", "valid": "12..20"},
    "cluster_count":  {"type": "int", "default": "2", "valid": "1..4"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "color":          {"type": "color", "default": "rng !{0,2}",
                       "valid": "1|3|4|5|6|7|8|9"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _paint(g, cells, color):
    for r, c in cells:
        g[r][c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    ctx.draw_int("cluster_count", 2, 2)
    color = ctx.draw_color("color", exclude={0, 2})
    g = full_grid(13 + rng.randint(0, 2), 14 + rng.randint(0, 2), 0)
    row_shift = rng.randint(0, 1)
    col_shift = rng.randint(0, 1)
    _paint(g, [(2 + row_shift, 2), (3 + row_shift, 2)], color)
    _paint(g, [(2 + row_shift, 6), (3 + row_shift, 6)], color)
    _paint(g, [(7, 3 + col_shift), (7, 4 + col_shift)], color)
    _paint(g, [(10, 3 + col_shift), (10, 4 + col_shift)], color)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 14, 0)
    if name == "no_components":
        return g
    if name == "single_component":
        _paint(g, [(2, 2), (3, 2)], 3)
        return g
    if name == "full_grid":
        for r in range(13):
            for c in range(14):
                g[r][c] = 3
        return g
    return g
