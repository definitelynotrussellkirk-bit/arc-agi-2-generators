"""Generator for arc_additional_puzzles_21_set20_bundle:E136.

Rule: find full row OR full col of 8s. Mirror each non-{0,8} cell across
that line.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_cells,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_divider, no_cells_to_mirror, cells_on_both_sides.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c1e45a501ca9"
VERSION = "1.1.0"
TASK_ID = "c1e45a501ca9"
SUMMARY = "Full-height 8-col divider in middle; left side has scattered non-8 cells."

INVARIANTS = [
    "exactly 1 full-height col of 8s (or full-width row)",
    "left/upper side has 2-3 isolated non-{0,8} cells",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_divider", "no_cells_to_mirror", "cells_on_both_sides")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_cells":        {"type": "int", "default": "rng 2..3", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..7"},
    "position_bias":  {"type": "str", "default": "left_of_divider",
                       "valid": "left_of_divider"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..7"},
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
        h = ctx.draw_int("grid_h", 5, 5)
        w = ctx.draw_int("grid_w", 9, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 9, 11)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    gc = w // 2
    for r in range(h):
        g[r][gc] = 8
    palette = [1, 2, 3, 4, 5, 6, 7, 9]
    for _ in range(rng.randint(2, 3)):
        for _ in range(20):
            r = rng.randint(0, h - 1); c = rng.randint(0, gc - 1)
            if g[r][c] == 0:
                g[r][c] = rng.choice(palette)
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 10
    g = full_grid(h, w, 0)
    if name == "no_divider":
        # cells without an 8-divider → rule has no mirror axis
        g[1][2] = 4; g[3][3] = 6
        return g
    if name == "no_cells_to_mirror":
        # divider but empty side → nothing to reflect
        gc = w // 2
        for r in range(h):
            g[r][gc] = 8
        return g
    if name == "cells_on_both_sides":
        # cells already on both sides → mirror would overwrite existing cells
        gc = w // 2
        for r in range(h):
            g[r][gc] = 8
        g[1][2] = 4; g[3][3] = 6
        g[2][gc + 1] = 5; g[4][gc + 2] = 7
        return g
    return g
