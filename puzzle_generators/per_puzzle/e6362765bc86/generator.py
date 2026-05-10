"""Generator for arc_puzzle_bank_eighteenth21:M126 — pick odd-color panel, output its crop.

Rule: full-height 5-cols divide the grid into 3 panels. Two panels
share a color; one panel is the odd one out (different color).
Output is the bbox crop of that odd panel's content.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_separators, all_same_color, all_different_colors.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, fill_box, paint_at
from puzzle_generators.helpers.palette import random_palette

GENERATOR_ID = "e6362765bc86"
VERSION = "1.1.0"
TASK_ID = "e6362765bc86"
SUMMARY = "3 panels separated by 5-cols; 2 share a color, 1 is unique."

INVARIANTS = [
    "background is 0",
    "exactly two 5-color full-height divider columns at fixed positions",
    "3 panels (cols left of div1, between div1 and div2, right of div2)",
    "two panels have the same color marker shape; one panel uses a different color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_separators", "all_same_color", "all_different_colors")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "h":              {"type": "int", "default": "4", "valid": "3..6"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "three_panels_5col_split",
                       "valid": "three_panels_5col_split"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..3"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = [
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (1, 1)],
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    [(0, 0), (0, 1), (1, 1), (1, 2)],
    [(0, 0), (0, 1), (0, 2), (1, 1)],
]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("h", 3, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("h", 5, 6)
    else:
        h = ctx.draw_int("h", 4, 4)
    rng = ctx.draw_rng("layout")
    panel_w = 4
    w = panel_w * 3 + 2
    g = full_grid(h, w, 0)
    fill_box(g, 0, panel_w, h - 1, panel_w, 5)
    fill_box(g, 0, panel_w * 2 + 1, h - 1, panel_w * 2 + 1, 5)
    panel_starts = [0, panel_w + 1, panel_w * 2 + 2]
    common_color, odd_color = list(random_palette(rng, 2))
    odd_idx = rng.randint(0, 2)
    common_shape = rng.choice(_SHAPES)
    odd_shape = rng.choice(_SHAPES)
    sh = max(c[0] for c in common_shape) + 1
    sw = max(c[1] for c in common_shape) + 1
    osh = max(c[0] for c in odd_shape) + 1
    osw = max(c[1] for c in odd_shape) + 1
    for i, ps in enumerate(panel_starts):
        if i == odd_idx:
            r0 = rng.randint(0, max(0, h - osh))
            c0 = ps + rng.randint(0, max(0, panel_w - osw))
            paint_at(g, r0, c0, odd_shape, odd_color)
        else:
            r0 = rng.randint(0, max(0, h - sh))
            c0 = ps + rng.randint(0, max(0, panel_w - sw))
            paint_at(g, r0, c0, common_shape, common_color)
    return g


def _draw_from_degenerate(name, rng):
    h = 4
    panel_w = 4
    w = panel_w * 3 + 2
    g = full_grid(h, w, 0)
    if name == "no_separators":
        # 3 motifs but no 5-col dividers — rule's panel decomposition
        # fails; "odd panel" is undefined.
        paint_at(g, 0, 0, [(0, 0), (1, 0)], 4)
        paint_at(g, 0, 5, [(0, 0), (1, 0)], 4)
        paint_at(g, 0, 10, [(0, 0), (1, 0)], 7)
        return g
    fill_box(g, 0, panel_w, h - 1, panel_w, 5)
    fill_box(g, 0, panel_w * 2 + 1, h - 1, panel_w * 2 + 1, 5)
    if name == "all_same_color":
        # All 3 panels share a color — no odd panel; rule's
        # selector finds none.
        paint_at(g, 0, 0, [(0, 0), (1, 0)], 4)
        paint_at(g, 0, 5, [(0, 0), (1, 0)], 4)
        paint_at(g, 0, 10, [(0, 0), (1, 0)], 4)
        return g
    if name == "all_different_colors":
        # All 3 panels have distinct colors — rule's "two share"
        # precondition fails; tie-break ambiguous.
        paint_at(g, 0, 0, [(0, 0), (1, 0)], 4)
        paint_at(g, 0, 5, [(0, 0), (1, 0)], 6)
        paint_at(g, 0, 10, [(0, 0), (1, 0)], 7)
        return g
    return g
