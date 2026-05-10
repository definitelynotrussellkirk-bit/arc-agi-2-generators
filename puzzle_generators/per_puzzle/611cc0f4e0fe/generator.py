"""Generator for arc_puzzle_bank_eighth_21_bundle:easy_50_diagonal_bridge.

Matching colored endpoints define diagonal line segments.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_pairs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, axis_aligned, single_endpoint.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "611cc0f4e0fe"
VERSION = "1.1.0"
TASK_ID = "611cc0f4e0fe"
SUMMARY = "Matching colored endpoints define diagonal line segments."

INVARIANTS = [
    "background is 0",
    "each active color appears exactly twice",
    "the two cells of each active color are diagonal endpoints",
    "at least one diagonal has an interior gap",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "axis_aligned", "single_endpoint")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_size":      {"type": "int", "default": "rng 7..11", "valid": "5..16"},
    "grid_h":         {"type": "int", "default": "= grid_size", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pairs":        {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "position_bias":  {"type": "str", "default": "diagonal_endpoints",
                       "valid": "diagonal_endpoints"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..5"},
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
        n = ctx.draw_int("grid_size", 7, 8)
        n_pairs = ctx.draw_int("n_pairs", 2, 2)
    elif difficulty == "hard":
        n = ctx.draw_int("grid_size", 10, 11)
        n_pairs = ctx.draw_int("n_pairs", 3, 3)
    else:
        n = ctx.draw_int("grid_size", 7, 11)
        n_pairs = ctx.draw_int("n_pairs", 2, 3)
    colors = ctx.draw_distinct_colors("colors", n=n_pairs, exclude={0})
    rng = ctx.draw_rng("placement")
    g = full_grid(n, n, 0)
    used: set[tuple[int, int]] = set()

    for color in colors:
        for _ in range(80):
            length = rng.randint(2, min(4, n - 2))
            sr = rng.choice([-1, 1])
            sc = rng.choice([-1, 1])
            r1 = rng.randint(max(0, -sr * length), min(n - 1, n - 1 - sr * length))
            c1 = rng.randint(max(0, -sc * length), min(n - 1, n - 1 - sc * length))
            r2, c2 = r1 + sr * length, c1 + sc * length
            if (r1, c1) in used or (r2, c2) in used:
                continue
            g[r1][c1] = color
            g[r2][c2] = color
            used.add((r1, c1)); used.add((r2, c2))
            break
    return g


def _draw_from_degenerate(name, rng):
    n = 8
    g = full_grid(n, n, 0)
    if name == "no_pairs":
        # blank → no diagonal endpoint pairs to bridge
        return g
    if name == "axis_aligned":
        # endpoints share a row → not diagonal, rule won't fire
        g[3][1] = 4; g[3][6] = 4
        g[5][2] = 6; g[5][7] = 6
        return g
    if name == "single_endpoint":
        # only one endpoint per color → no pair to bridge between
        g[2][2] = 4
        g[5][5] = 6
        return g
    return g
