"""Generator for arc_puzzle_bank_21_set9_s:S9_E1 — seeds expand to color-8 halo.

Rule: sparse colored seeds expand to their orthogonal distance-one
frontier in color 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_seeds,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_seeds, multi_cell_blobs, seeds_at_corner.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ad8f89160989"
VERSION = "1.1.0"
TASK_ID = "ad8f89160989"
SUMMARY = "Sparse colored seeds expand to their orthogonal distance-one frontier in color 8."

INVARIANTS = [
    "background is 0",
    "there are two to four isolated nonzero seed cells",
    "seeds are separated so their halos do not erase other seeds",
    "output keeps seeds and paints adjacent background cells 8",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_seeds", "multi_cell_blobs", "seeds_at_corner")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_seeds":        {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "position_bias":  {"type": "str", "default": "spaced_singletons",
                       "valid": "spaced_singletons"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _far_enough(cells, r, c):
    return all(abs(r - rr) + abs(c - cc) >= 3 for rr, cc in cells)


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 7, 8)
        count = ctx.draw_int("n_seeds", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
        count = ctx.draw_int("n_seeds", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 7, 10)
        count = ctx.draw_int("n_seeds", 2, 4)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    placed = []
    palette = [2, 3, 4, 6, 7, 9]
    for color in palette[:count]:
        for _ in range(80):
            r = rng.randrange(h)
            c = rng.randrange(w)
            if g[r][c] == 0 and _far_enough(placed, r, c):
                g[r][c] = color
                placed.append((r, c))
                break
        else:
            raise ValueError("could not place separated seed")
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "no_seeds":
        # blank → no halos to paint
        return g
    if name == "multi_cell_blobs":
        # multi-cell blobs (not singletons) → halos overlap with self
        g[2][2] = 4; g[2][3] = 4
        g[5][5] = 6; g[6][5] = 6
        return g
    if name == "seeds_at_corner":
        # seeds at corners → 2 of 4 cardinal halo cells out of bounds
        g[0][0] = 3
        g[h - 1][w - 1] = 7
        return g
    return g
