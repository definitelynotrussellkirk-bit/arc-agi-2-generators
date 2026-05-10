"""Generator for 4290ef0e.

Rule: input L-corner sizes become concentric L-corner rings in the output.

Combinatorial axes (8): grid_h/w, shape_count, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_shapes, single_shape, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5a01897eb8be"
VERSION = "1.1.0"
TASK_ID = "5a01897eb8be"
SUMMARY = "Input L-corner sizes become concentric L-corner rings in output."

INVARIANTS = [
    "the upper-left cell defines the background color",
    "each non-background color forms either a singleton or an L-corner",
    "the L-corner bounding-box sizes are odd and distinct",
    "the canonical rule assigns those sizes to concentric output rings",
]

SHAPE_KINDS = ("S3", "S4")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_shapes", "single_shape", "full_grid")
HELPFUL_TEXTURES = SHAPE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "14", "valid": "14"},
    "grid_w":         {"type": "int", "default": "14", "valid": "14"},
    "shape_count":    {"type": "choice", "default": "rng helpful",
                       "valid": "3|4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "rng 3..4", "valid": "3..4"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "rng 3..4", "valid": "3..4"},
    "texture":        {"type": "str", "default": "alias for shape_count",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _draw_l(g, r, c, size, color):
    for k in range(size):
        g[r][c + k] = color
        g[r + k][c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    tx = overrides.get("texture")
    if tx in SHAPE_KINDS:
        count = int(tx[1])
    elif difficulty == "easy":
        count = 3
    elif difficulty == "hard":
        count = 4
    else:
        count = ctx.draw_choice("shape_count", [3, 4])
    colors = ctx.draw_distinct_colors("colors", n=count, exclude={0})
    g = full_grid(14, 14, 0)
    g[1][1] = colors[0]
    _draw_l(g, 1, 5, 3, colors[1])
    _draw_l(g, 6, 1, 5, colors[2])
    if count == 4:
        _draw_l(g, 6, 7, 7, colors[3])
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(14, 14, 0)
    if name == "no_shapes":
        return g
    if name == "single_shape":
        _draw_l(g, 1, 1, 3, 3)
        return g
    if name == "full_grid":
        for r in range(14):
            for c in range(14):
                g[r][c] = 3
        return g
    return g
