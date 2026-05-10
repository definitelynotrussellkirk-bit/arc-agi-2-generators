"""Generator for arc_puzzle_bank_21_set6:easy_f03.

Rule: each seed paints a same-color knight-move halo.

Combinatorial axes (8): grid_h, grid_w, palette_kind, seeds,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_seeds, seeds_overlap, seed_at_corner.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a82753d0e28f"
VERSION = "1.1.0"
TASK_ID = "a82753d0e28f"
SUMMARY = "Each seed paints a same-color knight-move halo."

INVARIANTS = [
    "background is 0",
    "inputs contain isolated singleton seeds",
    "halo cells are the eight chess-knight offsets",
    "halo positions clip at the grid border",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_seeds", "seeds_overlap", "seed_at_corner")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..9", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "seeds":          {"type": "int", "default": "rng 2..4", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "interior_separated",
                       "valid": "interior_separated"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..4", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _far(cells, r, c):
    return all(abs(r - rr) > 4 or abs(c - cc) > 4 for rr, cc in cells)


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
        target = ctx.draw_int("seeds", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 10, 11)
        target = ctx.draw_int("seeds", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 8, 11)
        target = ctx.draw_int("seeds", 2, 4)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    seeds = []
    for _ in range(120):
        if len(seeds) >= target:
            break
        r = rng.randrange(h)
        c = rng.randrange(w)
        if _far(seeds, r, c):
            seeds.append((r, c))
            g[r][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    if not seeds:
        g[h // 2][w // 2] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_seeds":
        # empty grid → no halos to paint
        return g
    if name == "seeds_overlap":
        # adjacent seeds → halos overlap, color resolution is order-dependent
        g[3][3] = 4
        g[3][4] = 6
        return g
    if name == "seed_at_corner":
        # seed at (0,0) → many halo cells clip off-grid
        g[0][0] = 5
        return g
    return g
