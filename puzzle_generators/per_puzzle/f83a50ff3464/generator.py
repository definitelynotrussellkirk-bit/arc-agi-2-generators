"""Generator for arc_puzzle_bank_21_set22_bundle:easy_p01.

Rule: blank cells whose 4 orthogonal neighbors are all the same color get
filled with that color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, cross_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_crosses, partial_cross, mismatched_cross.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f83a50ff3464"
VERSION = "1.1.0"
TASK_ID = "f83a50ff3464"
SUMMARY = "Blank centers have four same-color orthogonal neighbors."

INVARIANTS = [
    "background is 0",
    "each active center is 0",
    "the four orthogonal neighbors around each active center share one nonzero color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_crosses", "partial_cross", "mismatched_cross")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "cross_count":    {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "spaced_orthogonal_crosses",
                       "valid": "spaced_orthogonal_crosses"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _ortho_cells(r, c):
    return {(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
        cross_count = ctx.draw_int("cross_count", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
        cross_count = ctx.draw_int("cross_count", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 8, 12)
        cross_count = ctx.draw_int("cross_count", 2, 4)
    rng = ctx.draw_rng("layout")
    grid = full_grid(h, w, 0)
    occupied: set[tuple[int, int]] = set()
    centers = [(r, c) for r in range(1, h - 1) for c in range(1, w - 1)]
    rng.shuffle(centers)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], cross_count)

    placed = 0
    for r, c in centers:
        cells = _ortho_cells(r, c)
        if (r, c) in occupied or cells & occupied:
            continue
        color = colors[placed]
        for rr, cc in cells:
            grid[rr][cc] = color
        occupied.add((r, c))
        occupied |= cells
        placed += 1
        if placed >= cross_count:
            break
    return grid


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    if name == "no_crosses":
        # blank → no neighbors anywhere, rule fires zero times
        return g
    if name == "partial_cross":
        # only 3 of 4 neighbors present → predicate "all 4 same color" fails
        g[1][2] = 4; g[3][2] = 4; g[2][3] = 4  # missing left neighbor
        g[5][6] = 6; g[5][8] = 6; g[6][7] = 6  # missing top neighbor
        return g
    if name == "mismatched_cross":
        # all 4 neighbors present but different colors → predicate fails
        g[1][3] = 4; g[3][3] = 6; g[2][2] = 3; g[2][4] = 8
        return g
    return g
