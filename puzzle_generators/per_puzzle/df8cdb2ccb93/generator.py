"""Generator for arc_puzzle_bank_third_21_bundle:easy_19_grow_crosses_from_red_seeds.

Rule: red seeds grow blue orthogonal-neighbor arms.

Combinatorial axes (8): grid_h, grid_w, palette_kind, seeds,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_seeds, seeds_at_corner, overlapping_crosses.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "df8cdb2ccb93"
VERSION = "1.1.0"
TASK_ID = "df8cdb2ccb93"
SUMMARY = "Red seeds grow blue orthogonal-neighbor arms."

INVARIANTS = [
    "background is 0",
    "red seed cells are isolated from one another",
    "each seed keeps its red center",
    "orthogonal neighbor cells around seeds are initially blank",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_seeds", "seeds_at_corner", "overlapping_crosses")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "4..18"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "4..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "seeds":          {"type": "int", "default": "rng 2..4", "valid": "1..12"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "spaced_red_seeds",
                       "valid": "spaced_red_seeds"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _spaced(p, seeds):
    r, c = p
    return all(abs(r - rr) + abs(c - cc) >= 3 for rr, cc in seeds)


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 7, 8)
        target = ctx.draw_int("seeds", 2, 2)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
        target = ctx.draw_int("seeds", 3, 4)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 7, 10)
        target = ctx.draw_int("seeds", 2, 4)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    cells = [(r, c) for r in range(h) for c in range(w)]
    rng.shuffle(cells)
    seeds = []
    for r, c in cells:
        if len(seeds) >= target:
            break
        if _spaced((r, c), seeds):
            seeds.append((r, c))
            g[r][c] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "no_seeds":
        # blank → no seeds, no crosses to grow
        return g
    if name == "seeds_at_corner":
        # seeds at corners → 2 cross arms clip out of bounds
        g[0][0] = 2
        g[h - 1][w - 1] = 2
        return g
    if name == "overlapping_crosses":
        # adjacent seeds → cross arms overlap each other
        g[3][3] = 2
        g[3][4] = 2
        return g
    return g
