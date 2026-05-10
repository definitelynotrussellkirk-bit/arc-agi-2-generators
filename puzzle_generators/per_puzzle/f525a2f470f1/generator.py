"""Generator for arc_puzzle_bank_21_set8:easy_h06.

Rule: add a gray one-step down-right shadow behind every nonzero cell.

Combinatorial axes (8): grid_h, grid_w, palette_kind, marks,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_marks, marks_at_bottom_right, shadow_already_filled.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f525a2f470f1"
VERSION = "1.1.0"
TASK_ID = "f525a2f470f1"
SUMMARY = "Add a gray one-step down-right shadow behind every nonzero cell."

INVARIANTS = [
    "background is 0",
    "input marks are sparse",
    "shadow target cells are initially background",
    "original nonzero cells are preserved",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_marks", "marks_at_bottom_right", "shadow_already_filled")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "4..14"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "5..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "marks":          {"type": "int", "default": "rng 3..5", "valid": "1..12"},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "interior_with_shadow_room",
                       "valid": "interior_with_shadow_room"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "1..8"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _clear(g, r, c):
    h, w = len(g), len(g[0])
    for rr, cc in [(r, c), (r + 1, c + 1)]:
        if not (0 <= rr < h and 0 <= cc < w) or g[rr][cc] != 0:
            return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 8, 9)
        target = ctx.draw_int("marks", 2, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 10, 11)
        target = ctx.draw_int("marks", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 6, 8)
        w = ctx.draw_int("grid_w", 8, 11)
        target = ctx.draw_int("marks", 3, 5)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    placed = 0
    for _ in range(160):
        if placed >= target:
            break
        r = rng.randint(0, h - 2)
        c = rng.randint(0, w - 2)
        if _clear(g, r, c):
            g[r][c] = rng.choice([1, 2, 3, 4, 6, 7, 8, 9])
            placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 10
    g = full_grid(h, w, 0)
    if name == "no_marks":
        # blank grid → no cells to shadow, rule is identity
        return g
    if name == "marks_at_bottom_right":
        # marks on bottom row or right column → no down-right cell exists, rule is identity
        g[h - 1][2] = 4; g[h - 1][6] = 6
        g[2][w - 1] = 3; g[5][w - 1] = 8
        return g
    if name == "shadow_already_filled":
        # mark + non-zero cell at down-right → shadow target is occupied, rule's paint clobbers it
        g[1][1] = 4; g[2][2] = 7   # already 7 (gray-ish), would get overwritten
        g[3][4] = 6; g[4][5] = 7
        return g
    return g
