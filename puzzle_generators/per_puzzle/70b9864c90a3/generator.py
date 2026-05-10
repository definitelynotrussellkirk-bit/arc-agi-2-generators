"""Generator for arc_puzzle_bank_21_set21_bundle:easy_p03.

Rule: blank centers with four same-color diagonal neighbors are filled.

Combinatorial axes (8): grid_h, grid_w, palette_kind, cross_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_motifs, partial_diagonals, mismatched_diagonals.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "70b9864c90a3"
VERSION = "1.1.0"
TASK_ID = "70b9864c90a3"
SUMMARY = "Four same-color diagonal neighbors surround one blank center cell."

INVARIANTS = [
    "background is 0",
    "each active center is blank",
    "the four diagonal neighbors around each center share one nonzero color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_motifs", "partial_diagonals", "mismatched_diagonals")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "cross_count":    {"type": "int", "default": "rng 2..3", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "spaced_diagonal_x",
                       "valid": "spaced_diagonal_x"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _cross_cells(r, c):
    return {(r - 1, c - 1), (r - 1, c + 1), (r + 1, c - 1), (r + 1, c + 1)}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 7)
        w = ctx.draw_int("grid_w", 7, 8)
        cross_count = ctx.draw_int("cross_count", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
        cross_count = ctx.draw_int("cross_count", 3, 3)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 7, 10)
        cross_count = ctx.draw_int("cross_count", 2, 3)
    rng = ctx.draw_rng("layout")
    grid = full_grid(h, w, 0)
    occupied: set[tuple[int, int]] = set()
    centers = [(r, c) for r in range(1, h - 1) for c in range(1, w - 1)]
    rng.shuffle(centers)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], cross_count)
    placed = 0
    for r, c in centers:
        cells = _cross_cells(r, c)
        if cells & occupied or (r, c) in occupied:
            continue
        color = colors[placed]
        for rr, cc in cells:
            grid[rr][cc] = color
        occupied |= cells
        occupied.add((r, c))
        placed += 1
        if placed >= cross_count:
            break
    return grid


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_motifs":
        # blank → no diagonal corners, rule has no centers to fill
        return g
    if name == "partial_diagonals":
        # only 3 of 4 diagonals → predicate fails
        g[2][2] = 4; g[2][4] = 4; g[4][2] = 4  # missing BR
        g[5][6] = 6; g[5][8] = 6; g[7][8] = 6  # missing BL
        return g
    if name == "mismatched_diagonals":
        # all 4 diagonals present but in different colors → predicate fails
        g[2][2] = 4; g[2][4] = 6; g[4][2] = 3; g[4][4] = 8
        return g
    return g
