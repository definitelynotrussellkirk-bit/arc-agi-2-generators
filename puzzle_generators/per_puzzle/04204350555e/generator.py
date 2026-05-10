"""Generator for arc_puzzle_bank_21_set10_e:easy_j01.

Rule: for each non-bg cell at (r0, c0, color), set out[r][c] = color
for all (r, c) with |r - r0| + |c - c0| ≤ 2 (in bounds).

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_seeds,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_seeds, overlapping_diamonds, seed_at_corner.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "04204350555e"
VERSION = "1.1.0"
TASK_ID = "04204350555e"
SUMMARY = "1-2 isolated non-bg cells that paint diamonds."

INVARIANTS = [
    "1-2 non-bg cells, ≥4 cells apart so diamonds don't overlap",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_seeds", "overlapping_diamonds", "seed_at_corner")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 7..9", "valid": "6..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_seeds":        {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..2", "valid": "1..3"},
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
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 8, 9)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 7, 9)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    palette = [2, 3, 4, 5, 6, 7, 8, 9]
    n = rng.randint(1, 2)
    placed = []
    for _ in range(40):
        if len(placed) >= n: break
        r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
        if all(abs(r - pr) + abs(c - pc) > 4 for pr, pc in placed):
            g[r][c] = rng.choice(palette)
            placed.append((r, c))
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 8
    g = full_grid(h, w, 0)
    if name == "no_seeds":
        # no source cells → diamond paint has no centers, output equals input
        return g
    if name == "overlapping_diamonds":
        # two seeds within distance 4 → their diamonds overlap, painting order matters
        g[2][2] = 3
        g[3][3] = 5
        return g
    if name == "seed_at_corner":
        # seed at (0,0) → most diamond cells are out-of-bounds, only a quarter visible
        g[0][0] = 4
        g[h - 1][w - 1] = 7
        return g
    return g
