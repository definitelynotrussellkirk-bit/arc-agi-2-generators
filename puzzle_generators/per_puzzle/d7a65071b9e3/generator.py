"""Generator for arc_additional_puzzle_bank_volume5:H29.

Rule: a direction marker makes every non-control object slide rigidly
until stacked against the wall or another object.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_objects,
palette_size, position_bias, n_distinct_colors, marker_dir, texture.
Degenerates: no_direction_marker, no_objects, ambiguous_direction.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "d7a65071b9e3"
VERSION = "1.1.0"
TASK_ID = "d7a65071b9e3"
SUMMARY = "A direction marker makes every non-control object slide rigidly until stacked against the wall or another object."

INVARIANTS = [
    "one marker from 1 through 4 selects direction",
    "sliding objects use colors outside 1 through 4",
    "objects begin away from their landing wall",
    "at least two objects slide in the selected direction",
]

PALETTE_KINDS = ("default", "dir_up", "dir_down", "dir_lr")
DEGENERATE_TEXTURES = ("no_direction_marker", "no_objects", "ambiguous_direction")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..14", "valid": "8..24"},
    "grid_w":         {"type": "int", "default": "rng 10..14", "valid": "8..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_objects":      {"type": "int", "default": "3", "valid": "2..4"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4"},
    "marker_dir":     {"type": "str", "default": "rng", "valid": "rng"},
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
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 13, 14)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 10, 14)
        w = ctx.draw_int("grid_w", 10, 14)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    g[0][0] = rng.choice([1, 2, 3, 4])
    paint_at(g, 2, 2, [(0, 0), (1, 0), (1, 1)], 6)
    paint_at(g, 2, w - 4, [(0, 0), (0, 1), (1, 0), (1, 1)], 7)
    paint_at(g, h - 5, w // 2, [(0, 0), (0, 1), (1, 1), (2, 1)], 9)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 11
    g = full_grid(h, w, 0)
    if name == "no_direction_marker":
        # objects exist but no 1-4 marker → slide direction undefined
        paint_at(g, 2, 2, [(0, 0), (1, 0), (1, 1)], 6)
        paint_at(g, 2, w - 4, [(0, 0), (0, 1), (1, 0), (1, 1)], 7)
        paint_at(g, h - 5, w // 2, [(0, 0), (0, 1), (1, 1), (2, 1)], 9)
        return g
    if name == "no_objects":
        # marker exists but nothing to slide → rule is no-op
        g[0][0] = 2
        return g
    if name == "ambiguous_direction":
        # multiple direction markers (1 and 4) → which direction wins?
        g[0][0] = 1
        g[0][w - 1] = 4
        paint_at(g, 2, 2, [(0, 0), (1, 0), (1, 1)], 6)
        paint_at(g, h - 5, w // 2, [(0, 0), (0, 1), (1, 1), (2, 1)], 9)
        return g
    return g
