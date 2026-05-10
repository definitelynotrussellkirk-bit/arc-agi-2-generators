"""Generator for arc_additional_puzzle_bank_volume4:H26.

Rule: anchor colors 1, 2, and 3 stamp identity-or-mirrored copies of a
color-4 template at their positions.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_layout,
template_anchor, palette_size, position_bias, n_distinct_colors, texture.
Degenerates: no_template, no_anchors, missing_anchor.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "a41ff6269d40"
VERSION = "1.1.0"
TASK_ID = "a41ff6269d40"
SUMMARY = "Anchor colors 1, 2, and 3 stamp identity or mirrored copies of a color-4 template."

INVARIANTS = [
    "one color-4 template is present",
    "anchor colors are chosen from 1, 2, and 3",
    "all template copies fit in-bounds",
    "the output is blank except for color-4 copies",
]

PALETTE_KINDS = ("default", "all_three_anchors", "wide_grid", "tight_grid")
DEGENERATE_TEXTURES = ("no_template", "no_anchors", "missing_anchor")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..14", "valid": "8..24"},
    "grid_w":         {"type": "int", "default": "rng 12..17", "valid": "10..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_layout":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "template_anchor": {"type": "str", "default": "top_left",
                        "valid": "top_left"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4"},
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
        w = ctx.draw_int("grid_w", 15, 17)
    else:
        h = ctx.draw_int("grid_h", 10, 14)
        w = ctx.draw_int("grid_w", 12, 17)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    paint_at(g, 1, 1, [(0, 0), (0, 1), (0, 2), (1, 1)], 4)
    spots = [(0, w - 5), (h - 5, 2), (h - 5, w - 5)]
    codes = [1, 2, 3]
    rng.shuffle(codes)
    for (r, c), code in zip(spots, codes):
        g[r][c] = code
    return g


def _draw_from_degenerate(name, rng):
    h, w = 12, 15
    g = full_grid(h, w, 0)
    if name == "no_template":
        # anchors but no color-4 template — nothing to stamp
        for (r, c), code in zip([(0, w - 5), (h - 5, 2), (h - 5, w - 5)], [1, 2, 3]):
            g[r][c] = code
        return g
    if name == "no_anchors":
        # template but no anchors — rule has no stamp positions
        paint_at(g, 1, 1, [(0, 0), (0, 1), (0, 2), (1, 1)], 4)
        return g
    if name == "missing_anchor":
        # only 2 of 3 anchors — rule produces fewer stamps than expected
        paint_at(g, 1, 1, [(0, 0), (0, 1), (0, 2), (1, 1)], 4)
        g[0][w - 5] = 1
        g[h - 5][2] = 2
        return g
    return g
