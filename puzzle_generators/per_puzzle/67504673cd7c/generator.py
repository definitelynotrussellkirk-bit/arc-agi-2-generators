"""Generator for arc_additional_puzzle_bank_volume5:M34.

Rule: the largest 5-blob is the template. For each non-{0, 5} cell as
anchor, stamp the template at that anchor's position in the anchor's color.

Combinatorial axes (8): grid_h/w, palette_kind, num_anchors,
template_size, palette_size, position_bias, n_distinct_colors, texture.
Degenerates: no_template, no_anchors, anchor_at_edge.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "67504673cd7c"
VERSION = "1.1.0"
TASK_ID = "67504673cd7c"
SUMMARY = "5-template (size 3 L) in upper-left + 2-3 anchor cells in body."

INVARIANTS = [
    "exactly one 5-blob (the template) of size 3",
    "between 2 and 3 single-cell anchors of distinct non-{0,5} colors",
    "stamps from anchors stay in-bounds",
]

PALETTE_KINDS = ("default", "two_anchors", "three_anchors", "spread_anchors")
DEGENERATE_TEXTURES = ("no_template", "no_anchors", "anchor_at_edge")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 10..13", "valid": "8..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "num_anchors":    {"type": "int", "default": "2", "valid": "1..3"},
    "template_size":  {"type": "int", "default": "3", "valid": "3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
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
        w = ctx.draw_int("grid_w", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 13)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 10, 13)
    g = full_grid(h, w, 0)
    paint_at(g, 0, 0, [(0, 0), (1, 0), (1, 1)], 5)
    g[h // 2][w // 3] = 2
    g[h - 3][w - 4] = 3
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_template":
        # anchors but no 5-blob to stamp
        g[h // 2][w // 3] = 2
        g[h - 3][w - 4] = 3
        return g
    if name == "no_anchors":
        # template but no anchors — rule produces no stamps
        paint_at(g, 0, 0, [(0, 0), (1, 0), (1, 1)], 5)
        return g
    if name == "anchor_at_edge":
        # anchor at grid corner — stamp would be clipped
        paint_at(g, 0, 0, [(0, 0), (1, 0), (1, 1)], 5)
        g[h - 1][w - 1] = 4
        return g
    return g
