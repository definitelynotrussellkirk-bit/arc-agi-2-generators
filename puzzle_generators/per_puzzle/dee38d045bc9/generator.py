"""Generator for arc_puzzle_bank_21_set23_bundle:easy_p01.

Rule: blank cells with four same-color diagonal neighbors are filled.

Combinatorial axes (8): grid_h, grid_w, palette_kind, target_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_motifs, partial_diagonals, mismatched_diagonals.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "dee38d045bc9"
VERSION = "1.1.0"
TASK_ID = "dee38d045bc9"
SUMMARY = "Blank cells have four same-color diagonal neighbors."

INVARIANTS = [
    "background is 0",
    "each active center is 0",
    "the four diagonal neighbors around each active center share one nonzero color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_motifs", "partial_diagonals", "mismatched_diagonals")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "target_count":   {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "spaced_diagonal_x",
                       "valid": "spaced_diagonal_x"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _footprint(r: int, c: int) -> set[tuple[int, int]]:
    return {(rr, cc) for rr in range(r - 1, r + 2) for cc in range(c - 1, c + 2)}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
        target_count = ctx.draw_int("target_count", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
        target_count = ctx.draw_int("target_count", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 8, 12)
        target_count = ctx.draw_int("target_count", 2, 4)
    rng = ctx.draw_rng("layout")
    grid = full_grid(h, w, 0)
    centers = [(r, c) for r in range(1, h - 1) for c in range(1, w - 1)]
    rng.shuffle(centers)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], min(target_count, 9))
    occupied: set[tuple[int, int]] = set()

    placed = 0
    for r, c in centers:
        footprint = _footprint(r, c)
        if footprint & occupied:
            continue
        color = colors[placed % len(colors)]
        for dr, dc in ((-1, -1), (-1, 1), (1, -1), (1, 1)):
            grid[r + dr][c + dc] = color
        occupied |= footprint
        placed += 1
        if placed >= target_count:
            break
    return grid


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_motifs":
        # blank → no diagonal corners, rule has no centers to fill
        return g
    if name == "partial_diagonals":
        # only 3 of 4 diagonals → predicate "all 4 same color" fails
        g[2][2] = 4; g[2][4] = 4; g[4][2] = 4  # missing BR
        g[5][6] = 6; g[5][8] = 6; g[7][8] = 6  # missing BL
        return g
    if name == "mismatched_diagonals":
        # all 4 diagonals present but in different colors → predicate fails
        g[2][2] = 4; g[2][4] = 6; g[4][2] = 3; g[4][4] = 8
        return g
    return g
