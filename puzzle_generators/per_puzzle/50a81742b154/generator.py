"""Generator for arc_additional_puzzle_bank_volume6:M37.

Rule: take normalized cells of the 8-blob as template. For each
2-blob, if normalized cells == template, recolor to 3.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blobs,
palette_size, position_bias, n_distinct_colors, shape_spread, texture.
Degenerates: no_template, all_match, no_match.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "50a81742b154"
VERSION = "1.1.0"
TASK_ID = "50a81742b154"
SUMMARY = "1 8-blob (template) + 2-3 2-blobs (one matches template, others differ)."

INVARIANTS = [
    "exactly one 8-blob",
    "between 2 and 3 2-blobs",
    "exactly one 2-blob has same normalized shape as 8-blob",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_template", "all_match", "no_match")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..12", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 11..14", "valid": "9..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blobs":        {"type": "int", "default": "4", "valid": "3..4"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "spread_corners",
                       "valid": "spread_corners"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
    "shape_spread":   {"type": "str", "default": "one_match_others_diff",
                       "valid": "one_match_others_diff"},
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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 13, 14)
    else:
        h = ctx.draw_int("grid_h", 9, 12)
        w = ctx.draw_int("grid_w", 11, 14)
    g = full_grid(h, w, 0)
    template = [(0, 0), (1, 0), (2, 0), (2, 1)]
    different = [(0, 0), (0, 1), (1, 0), (1, 1)]
    different2 = [(0, 0), (1, 0), (2, 0)]
    paint_at(g, 1, 1, template, 8)
    paint_at(g, 1, w - 4, template, 2)
    paint_at(g, h - 4, 1, different, 2)
    paint_at(g, h - 4, w - 4, different2, 2)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    template = [(0, 0), (1, 0), (2, 0), (2, 1)]
    different = [(0, 0), (0, 1), (1, 0), (1, 1)]
    different2 = [(0, 0), (1, 0), (2, 0)]
    if name == "no_template":
        # no 8-blob → template is undefined, no 2-blob can be matched
        paint_at(g, 1, w - 4, template, 2)
        paint_at(g, h - 4, 1, different, 2)
        paint_at(g, h - 4, w - 4, different2, 2)
        return g
    if name == "all_match":
        # every 2-blob matches the 8 template → all 2s become 3s, no decoy
        paint_at(g, 1, 1, template, 8)
        paint_at(g, 1, w - 4, template, 2)
        paint_at(g, h - 4, 1, template, 2)
        paint_at(g, h - 4, w - 4, template, 2)
        return g
    if name == "no_match":
        # no 2-blob matches the template → rule recolors nothing, output equals input
        paint_at(g, 1, 1, template, 8)
        paint_at(g, 1, w - 4, different, 2)
        paint_at(g, h - 4, 1, different2, 2)
        return g
    return g
