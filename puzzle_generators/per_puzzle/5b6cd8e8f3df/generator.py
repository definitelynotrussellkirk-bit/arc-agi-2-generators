"""Generator for arc_puzzle_bank_21_set20_bundle:easy_p03 — interior seeds grow into pluses.

Rule: isolated interior seeds grow into same-color radius-one plus signs.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_seeds,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_seeds, multi_cell_blobs, seeds_at_corner.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5b6cd8e8f3df"
VERSION = "1.1.0"
TASK_ID = "5b6cd8e8f3df"
SUMMARY = "Isolated interior seeds grow into same-color radius-one plus signs."

INVARIANTS = [
    "background is 0",
    "all seeds are isolated interior cells",
    "plus footprints do not overlap",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_seeds", "multi_cell_blobs", "seeds_at_corner")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_seeds":        {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "spaced_interior_singletons",
                       "valid": "spaced_interior_singletons"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _plus_cells(r, c):
    return {(r, c), (r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
        seed_count = ctx.draw_int("n_seeds", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
        seed_count = ctx.draw_int("n_seeds", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 8, 12)
        seed_count = ctx.draw_int("n_seeds", 2, 4)
    rng = ctx.draw_rng("layout")
    grid = full_grid(h, w, 0)
    occupied: set[tuple[int, int]] = set()

    candidates = [(r, c) for r in range(1, h - 1) for c in range(1, w - 1)]
    rng.shuffle(candidates)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], seed_count)
    placed = 0
    for r, c in candidates:
        footprint = _plus_cells(r, c)
        if footprint & occupied:
            continue
        grid[r][c] = colors[placed]
        occupied |= footprint
        placed += 1
        if placed >= seed_count:
            break
    return grid


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_seeds":
        # blank → no pluses to grow
        return g
    if name == "multi_cell_blobs":
        # seeds form blobs (not singletons) → "isolated" precondition fails
        g[2][2] = 4; g[2][3] = 4
        g[5][5] = 6; g[6][5] = 6
        return g
    if name == "seeds_at_corner":
        # seeds at corners → 2 of 4 cardinal arms out of bounds
        g[0][0] = 3
        g[h - 1][w - 1] = 7
        return g
    return g
