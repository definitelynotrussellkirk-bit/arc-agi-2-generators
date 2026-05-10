"""Generator for arc_puzzle_bank_21_set24_bundle:easy_p05.

Rule: same-color diagonal corner pairs complete their rectangles.

Combinatorial axes (8): grid_h, grid_w, palette_kind, pair_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, collinear_pairs, mismatched_pair_colors.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f8bf11d8b63a"
VERSION = "1.1.0"
TASK_ID = "f8bf11d8b63a"
SUMMARY = "Same-color diagonal corner pairs complete their rectangles."

INVARIANTS = [
    "background is 0",
    "each active color appears exactly twice",
    "the two cells are opposite corners of a non-degenerate rectangle",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "collinear_pairs", "mismatched_pair_colors")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "4..16"},
    "grid_w":         {"type": "int", "default": "rng 9..13", "valid": "4..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "pair_count":     {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "spaced_diagonal_pairs",
                       "valid": "spaced_diagonal_pairs"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _blocked(cells: list[tuple[int, int]]) -> set[tuple[int, int]]:
    rs = [r for r, _ in cells]
    cs = [c for _, c in cells]
    return {(r, c)
            for r in range(min(rs) - 1, max(rs) + 2)
            for c in range(min(cs) - 1, max(cs) + 2)}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
        pair_count = ctx.draw_int("pair_count", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 12, 13)
        pair_count = ctx.draw_int("pair_count", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 9, 13)
        pair_count = ctx.draw_int("pair_count", 2, 4)
    rng = ctx.draw_rng("layout")
    grid = full_grid(h, w, 0)
    candidates: list[list[tuple[int, int]]] = []
    for r0 in range(h - 2):
        for r1 in range(r0 + 2, h):
            for c0 in range(w - 2):
                for c1 in range(c0 + 2, w):
                    if rng.choice([True, False]):
                        candidates.append([(r0, c0), (r1, c1)])
                    else:
                        candidates.append([(r0, c1), (r1, c0)])
    rng.shuffle(candidates)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], min(pair_count, 9))
    occupied: set[tuple[int, int]] = set()
    placed = 0

    for cells in candidates:
        blocked = _blocked(cells)
        if blocked & occupied:
            continue
        color = colors[placed % len(colors)]
        for r, c in cells:
            grid[r][c] = color
        occupied |= blocked
        placed += 1
        if placed >= pair_count:
            break
    return grid


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # blank → no diagonal corners, rule has no rectangles to complete
        return g
    if name == "collinear_pairs":
        # both cells in same row → degenerate rectangle (zero height), rule undefined
        g[2][1] = 4; g[2][5] = 4  # same row
        g[5][2] = 6; g[5][7] = 6  # same row
        return g
    if name == "mismatched_pair_colors":
        # two cells but in different colors → no actual pair, rule's predicate fails
        g[1][1] = 4; g[3][5] = 6  # different colors at "would-be diagonal"
        g[5][2] = 3; g[7][6] = 8
        return g
    return g
