"""Generator for arc_puzzle_bank_21_set13_s:S13_M7.

Three gray-separated panels are compared by object hole-count multisets.

Combinatorial axes (8): grid_h, grid_w, palette_kind, odd_index,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_dividers, all_same, all_distinct.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "1ec92cd82c85"
VERSION = "1.1.0"
TASK_ID = "1ec92cd82c85"

SUMMARY = "Three gray-separated panels are compared by object hole-count multisets."

INVARIANTS = [
    "background is 0",
    "full gray separator columns split the grid into three panels",
    "two panels share the same sorted hole-count signature",
    "one panel has a unique hole-count signature and is marked in the output strip",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_dividers", "all_same", "all_distinct")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..12"},
    "grid_w":         {"type": "int", "default": "derived", "valid": "20..23"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "odd_index":      {"type": "int", "default": "rng 0..2", "valid": "0..2"},
    "palette_size":   {"type": "int", "default": "6", "valid": "6..6"},
    "position_bias":  {"type": "str", "default": "gray_separated_panels",
                       "valid": "gray_separated_panels"},
    "n_distinct_colors": {"type": "int", "default": "6", "valid": "6..6"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

SQUARE_2 = [(r, c) for r in range(2) for c in range(2)]
RING_8 = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]


def _paint_panel(g, left, signature, color_a, color_b):
    paint_at(g, 1, left + 1, SQUARE_2, color_a)
    if signature == "mixed":
        paint_at(g, 4, left + 2, RING_8, color_b)
    else:
        paint_at(g, 5, left + 3, SQUARE_2, color_b)


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        ph = ctx.draw_int("panel_height", 8, 8)
        pw = ctx.draw_int("panel_width", 6, 6)
    elif difficulty == "hard":
        ph = ctx.draw_int("panel_height", 9, 10)
        pw = ctx.draw_int("panel_width", 7, 7)
    else:
        ph = ctx.draw_int("panel_height", 8, 10)
        pw = ctx.draw_int("panel_width", 6, 7)
    odd_index = ctx.draw_int("odd_index", 0, 2)
    g = full_grid(ph, pw * 3 + 2, 0)

    sep1 = pw
    sep2 = pw * 2 + 1
    for r in range(ph):
        g[r][sep1] = 5
        g[r][sep2] = 5

    lefts = [0, pw + 1, pw * 2 + 2]
    for i, left in enumerate(lefts):
        sig = "double-solid" if i == odd_index else "mixed"
        _paint_panel(g, left, sig, 2 + i, 6 + i)
    return g


def _draw_from_degenerate(name, rng):
    ph, pw = 8, 6
    g = full_grid(ph, pw * 3 + 2, 0)
    sep1 = pw; sep2 = pw * 2 + 1
    if name == "no_dividers":
        # missing gray separators → no panel partition
        for i, left in enumerate([0, pw + 1, pw * 2 + 2]):
            paint_at(g, 1, left + 1, SQUARE_2, 2 + i)
        return g
    if name == "all_same":
        # all 3 panels share signature → no odd one out, ambiguous
        for r in range(ph):
            g[r][sep1] = 5; g[r][sep2] = 5
        for i, left in enumerate([0, pw + 1, pw * 2 + 2]):
            _paint_panel(g, left, "mixed", 2 + i, 6 + i)
        return g
    if name == "all_distinct":
        # 3 panels each unique → no shared signature, no rule applies
        for r in range(ph):
            g[r][sep1] = 5; g[r][sep2] = 5
        _paint_panel(g, 0, "mixed", 2, 6)
        _paint_panel(g, pw + 1, "double-solid", 3, 7)
        # third panel: just the square_2 — unique
        paint_at(g, 1, pw * 2 + 3, SQUARE_2, 4)
        return g
    return g
