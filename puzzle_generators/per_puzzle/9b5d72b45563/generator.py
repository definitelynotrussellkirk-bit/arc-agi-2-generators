"""Generator for arc_puzzle_bank_21_set4_d:easy_d04 — singleton seeds expand to clipped diagonal X.

Rule: each singleton seed expands to a clipped diagonal X.

Combinatorial axes (8): grid_h, grid_w, palette_kind, seed_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_seeds, multi_cell_blobs, seeds_at_corner.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "9b5d72b45563"
VERSION = "1.1.0"
TASK_ID = "9b5d72b45563"

SUMMARY = "Each singleton seed expands to a clipped diagonal X."

INVARIANTS = [
    "background is 0",
    "all nonzero input cells are isolated singleton seeds",
    "seed X footprints are separated",
    "seeds may sit near borders so clipping is represented",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_seeds", "multi_cell_blobs", "seeds_at_corner")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "4..14"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "4..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "seed_count":     {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "spaced_singletons",
                       "valid": "spaced_singletons"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _clear(placed, r, c):
    return all(abs(r - rr) > 2 or abs(c - cc) > 2 for rr, cc in placed)


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 7, 8)
        count = ctx.draw_int("seed_count", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
        count = ctx.draw_int("seed_count", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 7, 10)
        count = ctx.draw_int("seed_count", 2, 4)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    placed = []
    for color in rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], count):
        for _attempt in range(300):
            r = rng.randrange(h)
            c = rng.randrange(w)
            if g[r][c] == 0 and _clear(placed, r, c):
                g[r][c] = color
                placed.append((r, c))
                break
        else:
            raise ValueError("could not place seed")
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
        # seeds at corners → 2 of 4 diagonal arms are out of bounds
        g[0][0] = 3
        g[h - 1][w - 1] = 7
        return g
    return g
