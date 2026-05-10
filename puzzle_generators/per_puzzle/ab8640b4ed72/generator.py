"""Generator for arc_puzzle_bank_21_set20_bundle:easy_p07 — bridge midpoint of distance-2 same-color pair.

Rule: same-color endpoints separated by exactly one zero produce a
midpoint bridge in that color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, bridge_count, texture.
Degenerates: no_pairs, distance_one, distance_three.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ab8640b4ed72"
VERSION = "1.1.0"
TASK_ID = "ab8640b4ed72"
SUMMARY = "Same-color endpoints separated by one zero produce a midpoint bridge."

INVARIANTS = [
    "background is 0",
    "each active pattern has two same-color cells separated by one zero",
    "patterns are separated to avoid accidental extra midpoint bridges",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "distance_one", "distance_three")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "bridge_count":   {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "= bridge_count", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "scattered_axis_distance_2",
                       "valid": "scattered_axis_distance_2"},
    "n_distinct_colors": {"type": "int", "default": "= bridge_count", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _clear_cells(grid, cells):
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
        w = ctx.draw_int("grid_w", 8, 10)
        bridge_count = ctx.draw_int("bridge_count", 1, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 13)
        w = ctx.draw_int("grid_w", 12, 16)
        bridge_count = ctx.draw_int("bridge_count", 4, 6)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 8, 12)
        bridge_count = ctx.draw_int("bridge_count", 2, 4)
    rng = ctx.draw_rng("layout")
    grid = full_grid(h, w, 0)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], bridge_count)
    candidates = []
    for r in range(h):
        for c in range(w - 2):
            candidates.append(((r, c), (r, c + 1), (r, c + 2)))
    for r in range(h - 2):
        for c in range(w):
            candidates.append(((r, c), (r + 1, c), (r + 2, c)))
    rng.shuffle(candidates)
    placed = 0

    for a, mid, b in candidates:
        if placed >= bridge_count:
            break
        if not _clear_cells(grid, [a, mid, b]):
            continue
        color = colors[placed]
        grid[a[0]][a[1]] = color
        grid[b[0]][b[1]] = color
        placed += 1
    return grid


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        return g
    if name == "distance_one":
        # Adjacent same-color cells — rule's "one zero between"
        # precondition fails.
        g[2][2] = 4; g[2][3] = 4
        return g
    if name == "distance_three":
        # Pair separated by 2 zeros — rule's distance filter excludes.
        g[3][1] = 4; g[3][4] = 4
        return g
    return g
