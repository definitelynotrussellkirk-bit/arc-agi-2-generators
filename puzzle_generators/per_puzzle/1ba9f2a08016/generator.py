"""Generator for arc_additional_puzzles_21_set2:E8.

Rule: for each cell of color 2, paint each cardinal neighbor with 6
(if in-bounds and currently 0).

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_seeds,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_seeds, seed_at_corner, adjacent_seeds.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1ba9f2a08016"
VERSION = "1.1.0"
TASK_ID = "1ba9f2a08016"
SUMMARY = "Scattered isolated 2-cells with empty cardinal neighbors."

INVARIANTS = [
    "≥3 cells of color 2",
    "no two 2-cells are within distance 1 of each other (so cross-decoration doesn't conflict)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_seeds", "seed_at_corner", "adjacent_seeds")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_seeds":        {"type": "int", "default": "rng 3..4", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
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
        h = ctx.draw_int("grid_h", 5, 5)
        w = ctx.draw_int("grid_w", 5, 6)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 6, 7)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 5, 7)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    placed = []
    for _ in range(40):
        if len(placed) >= rng.randint(3, 4):
            break
        r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
        if all(abs(r - pr) + abs(c - pc) > 2 for pr, pc in placed):
            placed.append((r, c))
            g[r][c] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 6
    g = full_grid(h, w, 0)
    if name == "no_seeds":
        # no 2-cells → no neighbors to decorate, output equals input
        return g
    if name == "seed_at_corner":
        # 2 at (0,0) → 2 of 4 cardinal neighbors are out-of-bounds, partial cross
        g[0][0] = 2
        g[h - 1][w - 1] = 2
        return g
    if name == "adjacent_seeds":
        # two 2-cells adjacent → cross decorations would mutually overwrite the source cells
        g[2][2] = 2
        g[2][3] = 2
        g[4][1] = 2
        return g
    return g
