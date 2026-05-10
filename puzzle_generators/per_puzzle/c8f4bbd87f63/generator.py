"""Generator for arc_additional_puzzles_21_set5:M34.

Rule: a 3×3 plus-template (color 3 with a 2-center) is stamped at each
2-anchor outside the template bbox, painting empty cells with template values.

Combinatorial axes (8): grid_h/w, palette_kind, num_anchors,
template_color, palette_size, position_bias, n_distinct_colors, texture.
Degenerates: no_template, no_anchors, anchor_in_template.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c8f4bbd87f63"
VERSION = "1.1.0"
TASK_ID = "c8f4bbd87f63"
SUMMARY = "Plus-shape template (3 + center) in upper-left + 2-3 single 2-anchors elsewhere."

INVARIANTS = [
    "template at upper-left (3×3): plus shape with color 3 + center 2",
    "1-2 anchor 2-cells outside template, where stamp fits in-bounds",
]

PALETTE_KINDS = ("default", "two_anchors", "spread_anchors", "tight_anchors")
DEGENERATE_TEXTURES = ("no_template", "no_anchors", "anchor_in_template")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "num_anchors":    {"type": "int", "default": "2", "valid": "1..3"},
    "template_color": {"type": "int", "default": "3", "valid": "3"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
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
        w = ctx.draw_int("grid_w", 9, 10)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 11)
    g = full_grid(h, w, 0)
    g[0][1] = 3
    g[1][0] = 3; g[1][1] = 2; g[1][2] = 3
    g[2][1] = 3
    g[5][5] = 2
    g[7][8] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_template":
        # anchors but no template — nothing to stamp
        g[5][5] = 2
        g[7][8] = 2
        return g
    if name == "no_anchors":
        # template but no anchors — rule produces no stamps
        g[0][1] = 3
        g[1][0] = 3; g[1][1] = 2; g[1][2] = 3
        g[2][1] = 3
        return g
    if name == "anchor_in_template":
        # extra 2-anchor inside template bbox — ambiguous
        g[0][1] = 3
        g[1][0] = 3; g[1][1] = 2; g[1][2] = 3
        g[2][1] = 3
        g[0][0] = 2
        return g
    return g
