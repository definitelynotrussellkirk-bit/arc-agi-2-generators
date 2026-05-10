"""Generator for arc_puzzle_bank_eleventh21:M74 — mask one panel with another.

Rule: two equal-width panels separated by a vertical 9-col. Left panel
is a binary mask (1s and 0s). Right panel has colored content. Output:
right panel cells where mask is 1 keep their value, others are 0.

Combinatorial axes (8): grid_h, grid_w, palette_kind, panel_w,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_divider, mask_all_zero, mask_all_one.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f569e8bbe6a8"
VERSION = "1.1.0"
TASK_ID = "f569e8bbe6a8"
SUMMARY = "Two equal-width panels separated by 9-col; left is 1-mask, right is colored content."

INVARIANTS = [
    "background is 0",
    "exactly one full vertical 9-col",
    "left panel cells are 0 or 1 (binary mask)",
    "right panel cells are non-zero colored values",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_divider", "mask_all_zero", "mask_all_one")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 4..6", "valid": "3..10"},
    "panel_w":        {"type": "int", "default": "rng 4..5", "valid": "3..8"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "2..8"},
    "position_bias":  {"type": "str", "default": "two_panels_with_9div",
                       "valid": "two_panels_with_9div"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "2..8"},
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
        h = ctx.draw_int("grid_h", 4, 4)
        pw = ctx.draw_int("panel_w", 4, 4)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 5, 6)
        pw = ctx.draw_int("panel_w", 5, 5)
    else:
        h = ctx.draw_int("grid_h", 4, 6)
        pw = ctx.draw_int("panel_w", 4, 5)
    w = pw * 2 + 1
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    sep = pw
    for r in range(h):
        g[r][sep] = 9
    for r in range(h):
        for c in range(pw):
            if rng.random() < 0.4:
                g[r][c] = 1
        for c in range(sep + 1, w):
            g[r][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8])
    return g


def _draw_from_degenerate(name, rng):
    h, pw = 5, 4
    w = pw * 2 + 1
    g = full_grid(h, w, 0)
    sep = pw
    if name == "no_divider":
        # no 9-col → no panel split, mask vs content distinction undefined
        for r in range(h):
            for c in range(pw): g[r][c] = 1 if (r + c) % 2 == 0 else 0
            for c in range(sep + 1, w): g[r][c] = (r + c) % 7 + 2
        return g
    for r in range(h): g[r][sep] = 9
    if name == "mask_all_zero":
        # mask is entirely 0 → output is entirely bg (rule erases everything)
        for r in range(h):
            for c in range(sep + 1, w): g[r][c] = 4
        return g
    if name == "mask_all_one":
        # mask is entirely 1 → output equals right panel (rule keeps everything)
        for r in range(h):
            for c in range(pw): g[r][c] = 1
            for c in range(sep + 1, w): g[r][c] = 4 + (r + c) % 5
        return g
    return g
