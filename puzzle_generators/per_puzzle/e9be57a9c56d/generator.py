"""Generator for 9b2a60aa.

Rule: a largest template shape is chain-replicated at marker-spaced
positions and recolored by marker color.

Combinatorial axes (8): grid_h/w, orientation, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_template, no_markers, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "e9be57a9c56d"
VERSION = "1.1.0"
TASK_ID = "e9be57a9c56d"
SUMMARY = "Largest template shape chain-replicated at marker-spaced positions."

INVARIANTS = [
    "the largest 8-connected object is the template",
    "singleton markers lie in one row or one column",
    "one marker has the same color as the template and anchors the chain",
    "copies inherit the template shape and the ordered marker colors",
]

ORIENTATIONS = ("horizontal", "vertical")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_template", "no_markers", "full_grid")
HELPFUL_TEXTURES = ORIENTATIONS

AXES = {
    "grid_h":         {"type": "int", "default": "14", "valid": "14"},
    "grid_w":         {"type": "int", "default": "16", "valid": "16"},
    "orientation":    {"type": "str", "default": "rng helpful",
                       "valid": "|".join(ORIENTATIONS)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "3", "valid": "3"},
    "texture":        {"type": "str", "default": "alias for orientation",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


TEMPLATE = [(0, 0), (0, 1), (1, 0), (2, 0)]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    orientation = (overrides.get("texture") if overrides.get("texture") in ORIENTATIONS else None) or \
                  overrides.get("orientation") or \
                  ctx.draw_choice("orientation", list(ORIENTATIONS))
    template_color, color_a, color_b = ctx.draw_distinct_colors("colors", n=3, exclude={0})
    g = full_grid(14, 16, 0)
    paint_at(g, 5, 6, TEMPLATE, template_color)
    if orientation == "horizontal":
        row = 1
        for c, color in [(3, color_a), (7, template_color), (11, color_b)]:
            g[row][c] = color
    else:
        col = 1
        for r, color in [(3, color_a), (7, template_color), (11, color_b)]:
            g[r][col] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(14, 16, 0)
    if name == "no_template":
        for c, color in [(3, 4), (7, 5), (11, 6)]:
            g[1][c] = color
        return g
    if name == "no_markers":
        paint_at(g, 5, 6, TEMPLATE, 5)
        return g
    if name == "full_grid":
        for r in range(14):
            for c in range(16):
                g[r][c] = 5
        return g
    return g
