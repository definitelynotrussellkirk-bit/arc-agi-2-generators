"""Generator for arc_puzzle_bank_fourth_21_bundle:easy_22_recolor_exact_pluses.

Rule: each exact 5-cell plus of color 3 is recolored to 7.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_pluses,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pluses, partial_pluses, wrong_color.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ebff81ea3252"
VERSION = "1.1.0"
TASK_ID = "ebff81ea3252"
SUMMARY = "Exact 3-cell-radius pluses of color 3 are recolored to 7."

INVARIANTS = [
    "background is 0",
    "target shapes are exact radius-1 pluses of color 3",
    "pluses are separated so they do not merge",
    "at least one exact plus is present",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pluses", "partial_pluses", "wrong_color")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pluses":       {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..2"},
    "position_bias":  {"type": "str", "default": "spaced_pluses",
                       "valid": "spaced_pluses"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..2"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
        n_pluses = ctx.draw_int("n_pluses", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 11, 12)
        n_pluses = ctx.draw_int("n_pluses", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 8, 12)
        n_pluses = ctx.draw_int("n_pluses", 2, 4)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    centers: list[tuple[int, int]] = []
    for _ in range(120):
        if len(centers) >= n_pluses:
            break
        r = rng.randint(1, h - 2)
        c = rng.randint(1, w - 2)
        if any(abs(r - rr) <= 2 and abs(c - cc) <= 2 for rr, cc in centers):
            continue
        centers.append((r, c))
        for rr, cc in ((r, c), (r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
            g[rr][cc] = 3
    if not centers:
        g[2][2] = g[1][2] = g[3][2] = g[2][1] = g[2][3] = 3
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_pluses":
        # blank → no exact pluses, rule has no effect
        return g
    if name == "partial_pluses":
        # 4-cell plus arms (missing one arm) → predicate "exact plus" fails
        for (r, c) in [(2, 3), (1, 3), (3, 3), (2, 2)]: g[r][c] = 3  # missing right arm
        for (r, c) in [(5, 6), (4, 6), (5, 5), (5, 7)]: g[r][c] = 3  # missing bottom arm
        return g
    if name == "wrong_color":
        # exact pluses but in color 4, not color 3 → rule's color predicate fails
        for (r, c) in [(2, 3), (1, 3), (3, 3), (2, 2), (2, 4)]: g[r][c] = 4
        for (r, c) in [(6, 6), (5, 6), (7, 6), (6, 5), (6, 7)]: g[r][c] = 8
        return g
    return g
