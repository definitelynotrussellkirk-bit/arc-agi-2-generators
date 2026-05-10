"""Generator for arc_puzzle_bank_fourteenth_21_bundle:easy_97_mirror_top_panel_to_bottom.

Rule: build a top panel with a full color-5 divider row and an empty
mirrored bottom panel.

Combinatorial axes (8): grid_h, grid_w, palette_kind, panel_h,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_divider, no_top_marks, bottom_already_filled.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "774e0d59a5ff"
VERSION = "1.1.0"
TASK_ID = "774e0d59a5ff"
SUMMARY = "Build a top panel with a full color-5 divider row and an empty mirrored bottom panel."

INVARIANTS = [
    "background is 0",
    "the center row is fully color 5",
    "all non-divider pattern cells are above the divider",
    "the bottom panel is initially empty",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_divider", "no_top_marks", "bottom_already_filled")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "panel_h":        {"type": "int", "default": "rng 4..5", "valid": "2..7"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "3..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "marks":          {"type": "int", "default": "rng 4..8", "valid": "1..20"},
    "palette_size":   {"type": "int", "default": "rng 4..8", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "top_panel_only",
                       "valid": "top_panel_only"},
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
        panel_h = ctx.draw_int("panel_h", 4, 4)
        w = ctx.draw_int("grid_w", 8, 9)
        mark_count = ctx.draw_int("marks", 4, 5)
    elif difficulty == "hard":
        panel_h = ctx.draw_int("panel_h", 5, 5)
        w = ctx.draw_int("grid_w", 10, 11)
        mark_count = ctx.draw_int("marks", 6, 8)
    else:
        panel_h = ctx.draw_int("panel_h", 4, 5)
        w = ctx.draw_int("grid_w", 8, 11)
        mark_count = ctx.draw_int("marks", 4, 8)
    h = panel_h * 2 + 1
    divider = panel_h
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    for c in range(w):
        g[divider][c] = 5
    spots = [(r, c) for r in range(panel_h) for c in range(w)]
    for r, c in rng.sample(spots, min(mark_count, len(spots))):
        g[r][c] = rng.choice([1, 2, 3, 4, 6, 7, 8, 9])
    return g


def _draw_from_degenerate(name, rng):
    panel_h, w = 4, 9
    h = panel_h * 2 + 1
    g = full_grid(h, w, 0)
    if name == "no_divider":
        # marks without divider row → no axis to mirror across
        for r, c in [(1, 2), (1, 5), (2, 6)]:
            g[r][c] = 4
        return g
    if name == "no_top_marks":
        # divider but empty top panel → nothing to mirror
        for c in range(w): g[panel_h][c] = 5
        return g
    if name == "bottom_already_filled":
        # bottom panel non-empty → mirror would overwrite, invariant violated
        for c in range(w): g[panel_h][c] = 5
        for r, c in [(1, 2), (2, 5)]: g[r][c] = 4
        for r, c in [(panel_h + 1, 6), (panel_h + 2, 3)]: g[r][c] = 6
        return g
    return g
