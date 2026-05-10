"""Generator for arc_additional_puzzle_bank_volume7:H47.

Rule: the number of red cells gives the Manhattan distance from green
markers to paint as 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, red_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_green, no_red, distance_zero.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "3511f98c7b84"
VERSION = "1.1.0"
TASK_ID = "3511f98c7b84"
SUMMARY = "The number of red cells gives the Manhattan distance from green markers to paint as 8."

INVARIANTS = [
    "there is at least one green marker",
    "red cell count is small enough to leave visible blank cells at that distance",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_green", "no_red", "distance_zero")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "red_count":      {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
        k = ctx.draw_int("red_count", 1, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 11, 12)
        k = ctx.draw_int("red_count", 3, 3)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 8, 12)
        k = ctx.draw_int("red_count", 2, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    g[h // 2][w // 2] = 3
    if rng.random() < 0.5:
        g[2][w - 3] = 3
    placed = 0
    while placed < k:
        r = rng.randint(0, h - 1)
        c = rng.randint(0, w - 1)
        if g[r][c] == 0:
            g[r][c] = 2
            placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "no_green":
        # no green markers → distance has no source point
        g[2][3] = 2; g[5][7] = 2
        return g
    if name == "no_red":
        # no red cells → count is 0, distance 0, ring collapses to the marker
        g[h // 2][w // 2] = 3
        return g
    if name == "distance_zero":
        # red_count = 0 and only green present → ring is the marker itself, no 8s painted
        g[h // 2][w // 2] = 3
        g[2][w - 3] = 3
        return g
    return g
