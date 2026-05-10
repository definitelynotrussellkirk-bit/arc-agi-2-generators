"""Generator for arc_additional_puzzle_bank_volume19:H130.

Rule: corner and flip controls crop-transform a red shape into a cyan
output grid.

Combinatorial axes (8): grid_h, grid_w, palette_kind, corner_position,
flip_present, palette_size, position_bias, n_distinct_colors, texture.
Degenerates: no_corner_marker, no_red_shape, ambiguous_corner.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "aa41a5bf64d7"
VERSION = "1.1.0"
TASK_ID = "aa41a5bf64d7"
SUMMARY = "Corner and flip controls crop-transform a red shape into a cyan output grid."

INVARIANTS = [
    "exactly one corner contains the rotation marker 1",
    "an optional color-3 marker requests a horizontal flip",
    "one asymmetric red shape is present",
    "the output is the normalized transformed shape only",
]

PALETTE_KINDS = ("default", "tl_corner", "tr_corner", "bl_or_br_corner")
DEGENERATE_TEXTURES = ("no_corner_marker", "no_red_shape", "ambiguous_corner")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "6..18"},
    "grid_w":         {"type": "int", "default": "rng 10..15", "valid": "8..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "corner_position": {"type": "str", "default": "rng",
                        "valid": "tl|tr|bl|br"},
    "flip_present":   {"type": "bool", "default": "rng", "valid": "rng"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 13, 15)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 10, 15)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    corners = [(0, 0), (0, w - 1), (h - 1, w - 1), (h - 1, 0)]
    cr, cc = rng.choice(corners)
    g[cr][cc] = 1
    if rng.choice([True, False]):
        g[0][w // 2] = 3
    for dr, dc in [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]:
        g[2 + dr][w // 2 + dc] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_corner_marker":
        # red shape but no rotation marker → which transform to apply?
        for dr, dc in [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]:
            g[2 + dr][w // 2 + dc] = 2
        return g
    if name == "no_red_shape":
        # corner marker but nothing to transform
        g[0][0] = 1
        g[0][w // 2] = 3
        return g
    if name == "ambiguous_corner":
        # 1-markers in two corners → corner selection is undefined
        g[0][0] = 1
        g[h - 1][w - 1] = 1
        for dr, dc in [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]:
            g[2 + dr][w // 2 + dc] = 2
        return g
    return g
