"""Generator for arc_puzzle_bank_twentyfirst_21_bundle:easy_142_expand_singletons_to_diagonal_xs.

Rule: singleton seeds expand to radius-1 diagonal X shapes on a blank
output.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_seeds,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_seeds, multi_cell_blobs, seeds_at_corner.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "78da31e156b0"
VERSION = "1.1.0"
TASK_ID = "78da31e156b0"

SUMMARY = "Singleton seeds expand to radius-1 diagonal X shapes on a blank output."

INVARIANTS = [
    "background is 0",
    "all nonzero input cells are singleton seeds",
    "seeds are spaced so diagonal Xs do not conflict",
    "diagonal arms clip at grid edges",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_seeds", "multi_cell_blobs", "seeds_at_corner")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..11", "valid": "3..20"},
    "grid_w":         {"type": "int", "default": "rng 8..13", "valid": "3..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_seeds":        {"type": "int", "default": "rng 3..5", "valid": "1..12"},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "spaced_singletons",
                       "valid": "spaced_singletons"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _far(p, points):
    r, c = p
    return all(max(abs(r - rr), abs(c - cc)) >= 3 for rr, cc in points)


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
        target = ctx.draw_int("n_seeds", 3, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 13)
        target = ctx.draw_int("n_seeds", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 7, 11)
        w = ctx.draw_int("grid_w", 8, 13)
        target = ctx.draw_int("n_seeds", 3, 5)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    points = []
    choices = [(r, c) for r in range(h) for c in range(w)]
    rng.shuffle(choices)
    for r, c in choices:
        if len(points) >= target:
            break
        if _far((r, c), points):
            points.append((r, c))
            g[r][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_seeds":
        # blank → no Xs to grow
        return g
    if name == "multi_cell_blobs":
        # multi-cell blobs (not singletons) → "singleton" precondition fails
        g[2][2] = 4; g[2][3] = 4
        g[5][5] = 6; g[6][5] = 6
        return g
    if name == "seeds_at_corner":
        # seeds at corners → 3 of 4 diagonal arms are out of bounds
        g[0][0] = 3
        g[h - 1][w - 1] = 7
        return g
    return g
