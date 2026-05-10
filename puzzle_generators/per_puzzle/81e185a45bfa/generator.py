"""Generator for arc_puzzle_bank_21_set24_bundle:easy_p01 — bridge between distance-2 same-color endpoints.

Rule: same-color endpoints with one zero between them are bridged.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, bridge_count, texture.
Degenerates: no_pairs, distance_one, distance_three.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "81e185a45bfa"
VERSION = "1.1.0"
TASK_ID = "81e185a45bfa"
SUMMARY = "Same-color endpoints with one zero between them are bridged."

INVARIANTS = [
    "background is 0",
    "each bridge has two same-color endpoints separated by exactly one zero",
    "bridge patterns are isolated from one another",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "distance_one", "distance_three")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "bridge_count":   {"type": "int", "default": "rng 3..5", "valid": "1..10"},
    "palette_size":   {"type": "int", "default": "= bridge_count", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "scattered_axis_distance_2",
                       "valid": "scattered_axis_distance_2"},
    "n_distinct_colors": {"type": "int", "default": "= bridge_count", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _blocked(cells):
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 10)
        bridge_count = ctx.draw_int("bridge_count", 1, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 13)
        w = ctx.draw_int("grid_w", 12, 16)
        bridge_count = ctx.draw_int("bridge_count", 5, 7)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 8, 12)
        bridge_count = ctx.draw_int("bridge_count", 3, 5)
    rng = ctx.draw_rng("layout")
    grid = full_grid(h, w, 0)
    candidates = []
    for r in range(h):
        for c in range(w - 2):
            candidates.append([(r, c), (r, c + 2)])
    for r in range(h - 2):
        for c in range(w):
            candidates.append([(r, c), (r + 2, c)])
    rng.shuffle(candidates)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], min(bridge_count, 9))
    occupied = set()
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
        if placed >= bridge_count:
            break
    return grid


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        return g
    if name == "distance_one":
        g[3][1] = 4; g[3][2] = 4
        return g
    if name == "distance_three":
        g[3][1] = 4; g[3][4] = 4
        return g
    return g
