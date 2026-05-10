"""Generator for arc_additional_puzzle_bank_volume11:H74.

Rule: top-row controls rotate the blue shape, then select a boolean
operation with the red shape; result is rendered as a minimal cyan grid.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_shapes,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: missing_op_code, missing_rotation_code, no_overlap.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.shape import PLUS_5

GENERATOR_ID = "974fee515740"
VERSION = "1.1.0"
TASK_ID = "974fee515740"
SUMMARY = "Top-row controls rotate the blue shape, then select a boolean operation with the red shape."

INVARIANTS = [
    "the first nonzero top-row value is an operation code",
    "the second nonzero top-row value is a rotation code",
    "red and blue normalized masks have stable overlap under rotations",
    "the rendered result is a minimal cyan grid",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("missing_op_code", "missing_rotation_code", "no_overlap")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..14", "valid": "8..24"},
    "grid_w":         {"type": "int", "default": "rng 12..17", "valid": "10..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_shapes":       {"type": "int", "default": "2", "valid": "2"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "control_top_left",
                       "valid": "control_top_left"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 14)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 14)
        w = ctx.draw_int("grid_w", 16, 17)
    else:
        h = ctx.draw_int("grid_h", 10, 14)
        w = ctx.draw_int("grid_w", 12, 17)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    g[0][0] = rng.choice([3, 4, 6, 7])
    g[0][1] = rng.choice([1, 2, 3, 4])
    red = PLUS_5
    blue = [(0, 0), (0, 1), (1, 1), (2, 1)]
    paint_at(g, 3, 1, red, 2)
    paint_at(g, 4, w - 5, blue, 1)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 14
    g = full_grid(h, w, 0)
    red = PLUS_5
    blue = [(0, 0), (0, 1), (1, 1), (2, 1)]
    if name == "missing_op_code":
        # first top-row cell is bg → operation undefined
        g[0][1] = 2  # rotation code present
        paint_at(g, 3, 1, red, 2)
        paint_at(g, 4, w - 5, blue, 1)
        return g
    if name == "missing_rotation_code":
        # second top-row cell is bg → rotation defaults / undefined
        g[0][0] = 4  # op code present
        paint_at(g, 3, 1, red, 2)
        paint_at(g, 4, w - 5, blue, 1)
        return g
    if name == "no_overlap":
        # red and blue cannot overlap under any rotation → AND is empty, ambiguous output
        g[0][0] = 4; g[0][1] = 2
        single_red = [(0, 0)]
        single_blue = [(0, 0)]
        paint_at(g, 3, 1, single_red, 2)
        paint_at(g, 4, w - 5, single_blue, 1)
        return g
    return g
