"""Generator for arc_puzzle_bank_21_set21_bundle:easy_p02 — diagonal midpoint bridge.

Rule: same-color diagonal endpoints two steps apart have a blank
midpoint that gets filled in their color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, pair_count, texture.
Degenerates: no_pairs, axis_aligned, distance_three.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a5df658a2503"
VERSION = "1.1.0"
TASK_ID = "a5df658a2503"
SUMMARY = "Same-color diagonal endpoints two steps apart have a blank midpoint."

INVARIANTS = [
    "background is 0",
    "each pattern has two same-color diagonal endpoints and one zero midpoint",
    "patterns are separated so no midpoint belongs to multiple pairs",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "axis_aligned", "distance_three")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "pair_count":     {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "= pair_count", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "scattered_diagonal_distance_2",
                       "valid": "scattered_diagonal_distance_2"},
    "n_distinct_colors": {"type": "int", "default": "= pair_count", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _clear_neighborhood(grid, cells):
    h = len(grid)
    w = len(grid[0])
    for r, c in cells:
        for rr in range(max(0, r - 1), min(h, r + 2)):
            for cc in range(max(0, c - 1), min(w, c + 2)):
                if grid[rr][cc] != 0:
                    return False
    return True


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 7, 8)
        pair_count = ctx.draw_int("pair_count", 1, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 13)
        w = ctx.draw_int("grid_w", 10, 13)
        pair_count = ctx.draw_int("pair_count", 4, 6)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 7, 10)
        pair_count = ctx.draw_int("pair_count", 2, 4)
    rng = ctx.draw_rng("layout")
    grid = full_grid(h, w, 0)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], pair_count)

    candidates = []
    for r in range(h - 2):
        for c in range(w):
            if c + 2 < w:
                candidates.append(((r, c), (r + 1, c + 1), (r + 2, c + 2)))
            if c - 2 >= 0:
                candidates.append(((r, c), (r + 1, c - 1), (r + 2, c - 2)))
    rng.shuffle(candidates)
    placed = 0
    for a, mid, b in candidates:
        if placed >= pair_count:
            break
        if not _clear_neighborhood(grid, [a, mid, b]):
            continue
        color = colors[placed]
        grid[a[0]][a[1]] = color
        grid[b[0]][b[1]] = color
        placed += 1
    return grid


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        return g
    if name == "axis_aligned":
        # Pair shares row or column rather than diagonal — rule's
        # diagonal-only filter excludes them.
        g[3][2] = 4; g[3][6] = 4
        return g
    if name == "distance_three":
        # Diagonal pair separated by 2 zeros (distance 3) — rule's
        # exact-distance-2 filter excludes.
        g[1][1] = 4; g[4][4] = 4
        return g
    return g
