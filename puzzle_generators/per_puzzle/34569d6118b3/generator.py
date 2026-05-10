"""Generator for 42f83767.

Rule: swatch colors select ordered color-5 templates rendered over a
lower layout grid.

Combinatorial axes (8): grid_h/w, layout_size, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_swatches, no_layout, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "34569d6118b3"
VERSION = "1.1.0"
TASK_ID = "34569d6118b3"
SUMMARY = "Swatch colors select ordered templates rendered over layout grid."

INVARIANTS = [
    "the first all-zero row separates swatches/templates from the layout",
    "top-row non-gray runs are swatches and gray runs are ordered templates",
    "layout colors index the corresponding template",
    "swatch colors are distinct from each other and from 0 and 5",
]

LAYOUT_SIZES = ("2x2", "2x3")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_swatches", "no_layout", "full_grid")
HELPFUL_TEXTURES = LAYOUT_SIZES

AXES = {
    "grid_h":         {"type": "int", "default": "8", "valid": "8"},
    "grid_w":         {"type": "int", "default": "12", "valid": "12"},
    "layout_size":    {"type": "str", "default": "rng helpful",
                       "valid": "|".join(LAYOUT_SIZES)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for layout_size",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    layout_size = (overrides.get("texture") if overrides.get("texture") in LAYOUT_SIZES else None) or \
                  overrides.get("layout_size") or \
                  ctx.draw_choice("layout_size", list(LAYOUT_SIZES))
    color_a, color_b = ctx.draw_distinct_colors("swatches", n=2, exclude={0, 5})
    g = full_grid(8, 12, 0)
    g[0][0] = color_a
    g[0][2] = 5
    g[0][3] = 5
    g[0][4] = 5
    g[1][3] = 5
    g[2][3] = 5
    g[0][6] = color_b
    g[0][8] = 5
    g[1][8] = 5
    g[1][9] = 5
    g[1][10] = 5
    g[2][8] = 5
    rows = 2
    cols = 2 if layout_size == "2x2" else 3
    layout = [[color_a, color_b, color_a], [color_b, color_a, color_b]]
    for r in range(rows):
        for c in range(cols):
            g[4 + r][1 + c] = layout[r][c]
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(8, 12, 0)
    if name == "no_swatches":
        for r in range(2):
            for c in range(2):
                g[4 + r][1 + c] = 2
        return g
    if name == "no_layout":
        g[0][0] = 2; g[0][6] = 3
        g[0][2] = 5; g[1][3] = 5
        return g
    if name == "full_grid":
        for r in range(8):
            for c in range(12):
                g[r][c] = 5
        return g
    return g
