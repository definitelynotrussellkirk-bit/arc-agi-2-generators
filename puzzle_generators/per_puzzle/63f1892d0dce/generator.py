"""Generator for arc_puzzle_bank_21_set14_s:S14_M7 — column-profile match across panels.

Rule: a left-panel anchor's column profile identifies the matching
candidate in the right panel.

Combinatorial axes (8): grid_h, grid_w, palette_kind, target_row,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_separator, no_left_anchor, no_right_match.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "63f1892d0dce"
VERSION = "1.1.0"
TASK_ID = "63f1892d0dce"

SUMMARY = "A left-panel anchor's column profile identifies the matching candidate in the right panel."

INVARIANTS = [
    "background is 0",
    "a full gray separator column splits source and candidate panels",
    "the left panel's largest object supplies the column profile",
    "exactly one right-panel object matches that column profile",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_separator", "no_left_anchor", "no_right_match")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..12"},
    "panel_w":        {"type": "int", "default": "rng 7..8", "valid": "7..9"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "target_row":     {"type": "int", "default": "rng", "valid": "1..7"},
    "palette_size":   {"type": "int", "default": "5", "valid": "5..5"},
    "position_bias":  {"type": "str", "default": "two_panels_with_separator",
                       "valid": "two_panels_with_separator"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "5..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

PROFILE_SHAPE = [(0, 0), (0, 2), (1, 0), (1, 1), (1, 2), (2, 1)]
SMALL_L = [(0, 0), (1, 0), (1, 1)]
ODD_COLS = [(0, 0), (1, 0), (2, 0), (2, 1)]


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        ph = ctx.draw_int("grid_h", 8, 9)
        pw = ctx.draw_int("panel_w", 7, 7)
    elif difficulty == "hard":
        ph = ctx.draw_int("grid_h", 9, 10)
        pw = ctx.draw_int("panel_w", 8, 8)
    else:
        ph = ctx.draw_int("grid_h", 8, 10)
        pw = ctx.draw_int("panel_w", 7, 8)
    target_row = ctx.draw_int("target_row", 1, ph - 4)
    g = full_grid(ph, pw * 2 + 1, 0)
    sep = pw
    for r in range(ph):
        g[r][sep] = 5

    paint_at(g, 1, 1, PROFILE_SHAPE, 2)
    paint_at(g, ph - 3, 4, SMALL_L, 3)
    right = pw + 1
    paint_at(g, target_row, right + 1, PROFILE_SHAPE, 4)
    paint_at(g, ph - 4, right + 4, ODD_COLS, 6)
    return g


def _draw_from_degenerate(name, rng):
    ph, pw = 9, 7
    g = full_grid(ph, pw * 2 + 1, 0)
    sep = pw
    if name == "no_separator":
        # left/right shapes but no gray separator → cannot split panels
        paint_at(g, 1, 1, PROFILE_SHAPE, 2)
        paint_at(g, 1, sep + 2, PROFILE_SHAPE, 4)
        return g
    if name == "no_left_anchor":
        # separator + right candidates but no left object → no profile to match against
        for r in range(ph): g[r][sep] = 5
        paint_at(g, 1, sep + 2, PROFILE_SHAPE, 4)
        paint_at(g, ph - 4, sep + 5, ODD_COLS, 6)
        return g
    if name == "no_right_match":
        # left anchor present but no right-panel object matches its profile
        for r in range(ph): g[r][sep] = 5
        paint_at(g, 1, 1, PROFILE_SHAPE, 2)
        paint_at(g, 2, sep + 2, SMALL_L, 4)
        paint_at(g, ph - 4, sep + 4, ODD_COLS, 6)
        return g
    return g
