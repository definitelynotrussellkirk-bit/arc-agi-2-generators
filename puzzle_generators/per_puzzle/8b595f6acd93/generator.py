"""Generator for arc_puzzle_bank_next_21_bundle:easy_09_fill_plus_centers.

Rule: each hollow 3-color plus sign has its zero center filled.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_pluses,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pluses, partial_arms, mismatched_arms.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8b595f6acd93"
VERSION = "1.1.0"
TASK_ID = "8b595f6acd93"
SUMMARY = "Hollow 3-color plus signs with zero centers for the rule to fill."

INVARIANTS = [
    "background is 0",
    "each target is a radius-1 plus with four arms of color 3 and center 0",
    "plus arms do not overlap",
    "at least one center is fillable",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pluses", "partial_arms", "mismatched_arms")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "7..16"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "7..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pluses":       {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..2"},
    "position_bias":  {"type": "str", "default": "spaced_pluses_color3",
                       "valid": "spaced_pluses_color3"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _clear(g, r, c) -> bool:
    h, w = len(g), len(g[0])
    cells = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
    return all(0 <= rr < h and 0 <= cc < w and g[rr][cc] == 0 for rr, cc in cells)


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
    placed = 0
    for _ in range(120):
        if placed >= n_pluses:
            break
        r = rng.randint(1, h - 2)
        c = rng.randint(1, w - 2)
        if not _clear(g, r, c):
            continue
        for rr, cc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
            g[rr][cc] = 3
        placed += 1
    if placed == 0:
        g[1][2] = g[2][1] = g[2][3] = g[3][2] = 3
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_pluses":
        # blank → no centers to fill
        return g
    if name == "partial_arms":
        # only 3 of 4 arms → predicate fails, no center filled
        g[1][3] = 3; g[2][2] = 3; g[2][4] = 3  # missing bottom arm
        g[5][6] = 3; g[5][8] = 3; g[6][7] = 3  # missing top arm
        return g
    if name == "mismatched_arms":
        # arms in different colors (not all color 3) → predicate fails
        g[1][3] = 4; g[3][3] = 4; g[2][2] = 4; g[2][4] = 4  # color 4 instead of 3
        g[5][6] = 6; g[7][6] = 6; g[6][5] = 6; g[6][7] = 6
        return g
    return g
