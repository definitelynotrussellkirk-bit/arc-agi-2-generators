"""Generator for v0_original:easy_07.

Rule: horizontal same-color dominoes gain the two cells directly below them.

Combinatorial axes (8): grid_h, grid_w, palette_kind, dominoes,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_dominoes, blocked_below, dominoes_at_bottom.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "382eb0e592eb"
VERSION = "1.1.0"
TASK_ID = "382eb0e592eb"
SUMMARY = "Horizontal same-color dominoes gain the two cells directly below them."

INVARIANTS = [
    "background is 0",
    "each target is a horizontal domino",
    "the two cells below each domino are blank",
    "dominoes are separated",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_dominoes", "blocked_below", "dominoes_at_bottom")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "3..22"},
    "grid_w":         {"type": "int", "default": "rng 8..14", "valid": "3..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "dominoes":       {"type": "int", "default": "rng 3..5", "valid": "1..12"},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "scattered_with_clearance",
                       "valid": "scattered_with_clearance"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _free(g, r, c):
    h, w = len(g), len(g[0])
    if r + 1 >= h or c + 1 >= w:
        return False
    for rr in range(max(0, r - 1), min(h, r + 3)):
        for cc in range(max(0, c - 1), min(w, c + 3)):
            if g[rr][cc] != 0:
                return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 10)
        target = ctx.draw_int("dominoes", 2, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 12, 14)
        target = ctx.draw_int("dominoes", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 8, 14)
        target = ctx.draw_int("dominoes", 3, 5)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    placed = 0
    for _ in range(180):
        if placed >= target:
            break
        r = rng.randint(0, h - 2)
        c = rng.randint(0, w - 2)
        if _free(g, r, c):
            color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
            g[r][c] = color
            g[r][c + 1] = color
            placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_dominoes":
        # only single cells, never a horizontal pair → rule fires zero times
        g[2][3] = 4; g[5][7] = 6; g[7][1] = 3
        return g
    if name == "blocked_below":
        # domino present but cells below are non-zero → rule still fires (paints
        # over them) — visually identical to "shadow already there", no clear signal
        g[2][3] = 4; g[2][4] = 4
        g[3][3] = 5; g[3][4] = 5
        return g
    if name == "dominoes_at_bottom":
        # domino on the bottom row → no row below to paint, rule effect invisible
        g[h - 1][2] = 4; g[h - 1][3] = 4
        g[h - 1][6] = 6; g[h - 1][7] = 6
        return g
    return g
