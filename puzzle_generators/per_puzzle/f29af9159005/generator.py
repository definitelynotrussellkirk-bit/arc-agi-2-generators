"""Generator for additional_bank:H3.

Rule: for each empty cell on the same row/col as a 2-seed (with no 1
between), paint 4. Existing values keep.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_seeds,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_seeds, no_blockers, seed_at_corner.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f29af9159005"
VERSION = "1.1.0"
TASK_ID = "f29af9159005"
SUMMARY = "1-2 2-seeds + 1-2 1-blockers."

INVARIANTS = [
    "between 1 and 2 2-seeds",
    "1-2 1-blockers in same row or col as a seed",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_seeds", "no_blockers", "seed_at_corner")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 7..9", "valid": "5..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_seeds":        {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "interior", "valid": "interior"},
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
    n_seeds = rng.randint(1, 2)
    used = set()
    for _ in range(n_seeds):
        while True:
            r = rng.randint(1, h - 2); c = rng.randint(2, w - 3)
            if (r, c) not in used:
                used.add((r, c)); g[r][c] = 2
                if (r - 1, c) not in used:
                    g[r - 1][c] = 1
                    used.add((r - 1, c))
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 8
    g = full_grid(h, w, 0)
    if name == "no_seeds":
        # only 1-blockers → no LoS source, no 4 cells painted
        g[2][3] = 1
        g[4][5] = 1
        return g
    if name == "no_blockers":
        # 2-seed without any 1 → entire row + column gets painted, no clipping
        g[3][4] = 2
        return g
    if name == "seed_at_corner":
        # seed at (0,0) → only down/right rays; up/left have no LoS targets
        g[0][0] = 2
        g[h - 1][w - 1] = 2
        return g
    return g
