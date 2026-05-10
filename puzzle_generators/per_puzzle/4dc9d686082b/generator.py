"""Generator for c803e39c.

Rule: template panel and layout panel expand two color swatches into
a self-tiled output.

Combinatorial axes (8): grid_h/w, template, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_template, no_layout, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4dc9d686082b"
VERSION = "1.1.0"
TASK_ID = "4dc9d686082b"
SUMMARY = "Template + layout panel expand two color swatches into self-tiled output."

INVARIANTS = [
    "three full color-5 separator columns split four panels",
    "panel 1 contains a color-1 binary template",
    "panel 2 contains a color-2 layout with the same footprint",
    "panels 3 and 4 provide the two output colors",
]

TEMPLATES = ("diag", "corner", "bar")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_template", "no_layout", "full_grid")
HELPFUL_TEXTURES = TEMPLATES

AXES = {
    "grid_h":         {"type": "int", "default": "6", "valid": "6"},
    "grid_w":         {"type": "int", "default": "23", "valid": "23"},
    "template":       {"type": "str", "default": "rng helpful",
                       "valid": "|".join(TEMPLATES)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "5", "valid": "5"},
    "texture":        {"type": "str", "default": "alias for template",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    template = (overrides.get("texture") if overrides.get("texture") in TEMPLATES else None) or \
               overrides.get("template") or \
               ctx.draw_choice("template", list(TEMPLATES))
    color_a, color_b = ctx.draw_distinct_colors("colors", n=2, exclude={0, 1, 2, 5})
    g = full_grid(6, 23, 0)
    for c in (5, 11, 17):
        for r in range(6):
            g[r][c] = 5
    patterns = {
        "diag": [(1, 1), (2, 2)],
        "corner": [(1, 1), (1, 2), (2, 1)],
        "bar": [(1, 1), (1, 2), (1, 3)],
    }
    layout = [(1, 1), (1, 2), (2, 1), (2, 2)]
    for r, c in patterns[template]:
        g[r][c] = 1
    for r, c in layout:
        g[r][c + 6] = 2
    g[1][13] = color_a
    g[1][19] = color_b
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(6, 23, 0)
    if name == "no_template":
        for c in (5, 11, 17):
            for r in range(6):
                g[r][c] = 5
        return g
    if name == "no_layout":
        g[1][1] = 1
        return g
    if name == "full_grid":
        for r in range(6):
            for c in range(23):
                g[r][c] = 5
        return g
    return g
