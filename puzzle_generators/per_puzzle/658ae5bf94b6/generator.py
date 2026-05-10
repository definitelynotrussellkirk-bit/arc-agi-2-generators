"""Generator for arc_puzzle_bank_thirteenth21:M90 — XOR two panels.

Rule: two same-shape panels separated by a 9-col. Output cell = 2 if
exactly one panel has a non-zero cell at that position; else 0.

Combinatorial axes (8): grid_h, grid_w, palette_kind, panel_w,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_divider, identical_panels, one_panel_empty.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "658ae5bf94b6"
VERSION = "1.1.0"
TASK_ID = "658ae5bf94b6"
SUMMARY = "Two equal-width panels separated by a vertical 9-col, with sparse non-zero patterns."

INVARIANTS = [
    "background is 0",
    "exactly one full vertical 9-col separates two panels of equal width",
    "left and right panels have different (non-equal) sparse patterns",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_divider", "identical_panels", "one_panel_empty")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 4..6", "valid": "3..10"},
    "panel_w":        {"type": "int", "default": "rng 3..5", "valid": "2..8"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "2..6"},
    "position_bias":  {"type": "str", "default": "two_panels_with_9div",
                       "valid": "two_panels_with_9div"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "2..6"},
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
        pw = ctx.draw_int("panel_w", 3, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 5, 6)
        pw = ctx.draw_int("panel_w", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 4, 6)
        pw = ctx.draw_int("panel_w", 3, 5)
    w = pw * 2 + 1
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    sep = pw
    for r in range(h):
        g[r][sep] = 9
    for r in range(h):
        for c in range(pw):
            if rng.random() < 0.4:
                g[r][c] = rng.choice([2, 3, 4, 5, 6])
        for c in range(sep + 1, w):
            if rng.random() < 0.4:
                g[r][c] = rng.choice([2, 3, 4, 5, 6])
    return g


def _draw_from_degenerate(name, rng):
    h, pw = 5, 4
    w = pw * 2 + 1
    g = full_grid(h, w, 0)
    sep = pw
    if name == "no_divider":
        # no 9-col → no panel split
        for r in range(h):
            for c in range(pw): g[r][c] = 4 if (r + c) % 3 == 0 else 0
            for c in range(sep + 1, w): g[r][c] = 6 if (r + c) % 2 == 0 else 0
        return g
    for r in range(h): g[r][sep] = 9
    if name == "identical_panels":
        # left == right → XOR is empty (output all bg)
        for (dr, dc) in [(0, 1), (1, 2), (2, 0)]:
            g[dr][dc] = 4
            g[dr][sep + 1 + dc] = 6
        return g
    if name == "one_panel_empty":
        # one panel empty → XOR equals the other panel
        for (dr, dc) in [(0, 1), (1, 2), (2, 0)]:
            g[dr][dc] = 4
        return g
    return g
