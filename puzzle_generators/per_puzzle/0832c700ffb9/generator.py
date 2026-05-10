"""Generator for f35d900a.

Rule: four colored corner dots expand into blocks and dotted gray
rectangle guides.

Combinatorial axes (8): grid_h/w, rectangle_size, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_dots, single_dot, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0832c700ffb9"
VERSION = "1.1.0"
TASK_ID = "0832c700ffb9"
SUMMARY = "Four colored corner dots expand into blocks with dotted gray guides."

INVARIANTS = [
    "the background is zero",
    "exactly four nonzero dots occupy corners of an axis-aligned rectangle",
    "each row contains two dots so each block borrows the opposite row color",
    "dot spacings leave room for 3x3 blocks and dotted guide lines",
]

RECTANGLE_SIZES = ("wide", "tall", "large")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_dots", "single_dot", "full_grid")
HELPFUL_TEXTURES = RECTANGLE_SIZES

AXES = {
    "grid_h":         {"type": "int", "default": "13", "valid": "13"},
    "grid_w":         {"type": "int", "default": "13", "valid": "13"},
    "rectangle_size": {"type": "str", "default": "rng helpful",
                       "valid": "|".join(RECTANGLE_SIZES)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for rectangle_size",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    layout = (overrides.get("texture") if overrides.get("texture") in RECTANGLE_SIZES else None) or \
             overrides.get("rectangle_size") or \
             ctx.draw_choice("rectangle_size", list(RECTANGLE_SIZES))
    color_a, color_b = ctx.draw_distinct_colors("colors", n=2, exclude={0, 5})
    g = full_grid(13, 13, 0)
    if layout == "wide":
        r1, r2, c1, c2 = 3, 9, 2, 10
    elif layout == "tall":
        r1, r2, c1, c2 = 2, 10, 3, 9
    else:
        r1, r2, c1, c2 = 2, 10, 2, 10
    g[r1][c1] = color_a
    g[r1][c2] = color_b
    g[r2][c1] = color_b
    g[r2][c2] = color_a
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 13, 0)
    if name == "no_dots":
        return g
    if name == "single_dot":
        g[6][6] = 2
        return g
    if name == "full_grid":
        for r in range(13):
            for c in range(13):
                g[r][c] = 2
        return g
    return g
