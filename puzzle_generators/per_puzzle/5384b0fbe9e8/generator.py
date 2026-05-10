"""Generator for arc_puzzle_bank_fourteenth_21_bundle:easy_94_mirror_left_panel_to_right.

Rule: build a left panel with a full color-5 divider; the right panel
is initially empty and gets filled by mirroring the left.

Combinatorial axes (8): grid_h, grid_w, palette_kind, panel_w,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_divider, no_left_marks, right_already_filled.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5384b0fbe9e8"
VERSION = "1.1.0"
TASK_ID = "5384b0fbe9e8"
SUMMARY = "Build a left panel with a full color-5 divider and an empty mirrored right panel."

INVARIANTS = [
    "background is 0",
    "the center column is fully color 5",
    "all non-divider pattern cells are left of the divider",
    "the right panel is initially empty",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_divider", "no_left_marks", "right_already_filled")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "3..16"},
    "panel_w":        {"type": "int", "default": "rng 4..5", "valid": "2..7"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "marks":          {"type": "int", "default": "rng 4..8", "valid": "1..20"},
    "palette_size":   {"type": "int", "default": "rng 4..8", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "left_panel_only",
                       "valid": "left_panel_only"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..8", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        panel_w = ctx.draw_int("panel_w", 4, 4)
        mark_count = ctx.draw_int("marks", 4, 5)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        panel_w = ctx.draw_int("panel_w", 5, 5)
        mark_count = ctx.draw_int("marks", 6, 8)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        panel_w = ctx.draw_int("panel_w", 4, 5)
        mark_count = ctx.draw_int("marks", 4, 8)
    w = panel_w * 2 + 1
    divider = panel_w
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    for r in range(h):
        g[r][divider] = 5
    spots = [(r, c) for r in range(h) for c in range(panel_w)]
    for r, c in rng.sample(spots, min(mark_count, len(spots))):
        g[r][c] = rng.choice([1, 2, 3, 4, 6, 7, 8, 9])
    return g


def _draw_from_degenerate(name, rng):
    h, panel_w = 8, 4
    w = panel_w * 2 + 1
    g = full_grid(h, w, 0)
    if name == "no_divider":
        # marks without divider → no axis to mirror across
        for r, c in [(1, 1), (3, 2), (5, 3)]:
            g[r][c] = 4
        return g
    if name == "no_left_marks":
        # divider but empty left panel → nothing to mirror
        for r in range(h): g[r][panel_w] = 5
        return g
    if name == "right_already_filled":
        # right panel non-empty → mirror would overwrite, invariant violated
        for r in range(h): g[r][panel_w] = 5
        for r, c in [(1, 1), (3, 2)]:
            g[r][c] = 4
        for r, c in [(2, panel_w + 2), (4, panel_w + 3)]:
            g[r][c] = 6
        return g
    return g
