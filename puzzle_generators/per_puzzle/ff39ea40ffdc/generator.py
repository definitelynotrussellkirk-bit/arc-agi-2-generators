"""Generator for arc_additional_puzzle_bank_volume4:H22.

Rule: corner controls select a size-ranked colored object and transform
its tight crop.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_objects,
palette_size, position_bias, n_distinct_colors, transform_kind, texture.
Degenerates: no_size_control, no_transform_control, equal_sizes.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "ff39ea40ffdc"
VERSION = "1.1.0"
TASK_ID = "ff39ea40ffdc"
SUMMARY = "Corner controls select a size-ranked colored object and transform its tight crop."

INVARIANTS = [
    "top-left control selects smallest, middle, or largest object",
    "top-right control selects identity, mirror, or rotation",
    "candidate objects use colors 7, 8, and 9",
    "candidate sizes are distinct",
]

PALETTE_KINDS = ("default", "rank_smallest", "rank_middle", "rank_largest")
DEGENERATE_TEXTURES = ("no_size_control", "no_transform_control", "equal_sizes")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 11..15", "valid": "9..24"},
    "grid_w":         {"type": "int", "default": "rng 12..17", "valid": "10..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_objects":      {"type": "int", "default": "3", "valid": "3"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5"},
    "position_bias":  {"type": "str", "default": "corners_plus_objects",
                       "valid": "corners_plus_objects"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "5"},
    "transform_kind": {"type": "str", "default": "rng", "valid": "rng"},
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
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 12, 14)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 14, 15)
        w = ctx.draw_int("grid_w", 15, 17)
    else:
        h = ctx.draw_int("grid_h", 11, 15)
        w = ctx.draw_int("grid_w", 12, 17)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    g[0][0] = rng.choice([1, 2, 3])
    g[0][w - 1] = rng.choice([4, 5, 6])
    paint_at(g, 2, 1, [(0, 0), (1, 0)], 8)
    paint_at(g, 2, w - 5, [(0, 0), (0, 1), (1, 1)], 7)
    paint_at(g, h - 5, w // 2, [(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)], 9)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 14
    g = full_grid(h, w, 0)
    if name == "no_size_control":
        # transform control + objects but no size-ranking control → which obj undefined
        g[0][w - 1] = 4
        paint_at(g, 2, 1, [(0, 0), (1, 0)], 8)
        paint_at(g, 2, w - 5, [(0, 0), (0, 1), (1, 1)], 7)
        paint_at(g, h - 5, w // 2, [(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)], 9)
        return g
    if name == "no_transform_control":
        # size control + objects but no transform control → action undefined
        g[0][0] = 2
        paint_at(g, 2, 1, [(0, 0), (1, 0)], 8)
        paint_at(g, 2, w - 5, [(0, 0), (0, 1), (1, 1)], 7)
        paint_at(g, h - 5, w // 2, [(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)], 9)
        return g
    if name == "equal_sizes":
        # all candidate objects have the same size → ranking is ambiguous
        g[0][0] = 1
        g[0][w - 1] = 5
        for top, left, color in [(2, 1, 8), (2, w - 5, 7), (h - 5, w // 2, 9)]:
            paint_at(g, top, left, [(0, 0), (1, 0)], color)
        return g
    return g
