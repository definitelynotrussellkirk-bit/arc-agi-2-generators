"""Generator for arc_additional_puzzles_21_set4:E22.

Rule: each cell of color 2 walks in the four cardinal directions painting
color 7 until it hits a non-zero cell or the grid edge.

Combinatorial axes (8): grid_h/w, palette_kind, seed_count, seed_color,
palette_size, position_bias, n_distinct_colors, texture.
Degenerates: seed_at_corner, seeds_aligned, no_seeds.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "983d0ea3bd17"
VERSION = "1.1.0"
TASK_ID = "983d0ea3bd17"
SUMMARY = "1-2 isolated 2-cells with empty rays in all directions."

INVARIANTS = [
    "1-2 cells of color 2 with no other non-bg cells in their cardinal rays",
]

PALETTE_KINDS = ("scattered", "diagonal_pair", "single_seed", "edge_anchored")
DEGENERATE_TEXTURES = ("seed_at_corner", "seeds_aligned", "no_seeds")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 4..6", "valid": "3..10"},
    "grid_w":         {"type": "int", "default": "rng 6..8", "valid": "5..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "seed_count":     {"type": "int", "default": "1..2", "valid": "1..3"},
    "seed_color":     {"type": "int", "default": "2", "valid": "2"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "uniform"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
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
        h = ctx.draw_int("grid_h", 4, 5)
        w = ctx.draw_int("grid_w", 6, 7)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 7, 8)
    else:
        h = ctx.draw_int("grid_h", 4, 6)
        w = ctx.draw_int("grid_w", 6, 8)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    rs = sorted(rng.sample(range(h), 2))
    cs = rng.sample(range(w), 2)
    g[rs[0]][cs[0]] = 2
    if rs[1] - rs[0] >= 2 and cs[0] != cs[1]:
        g[rs[1]][cs[1]] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 5, 7
    g = full_grid(h, w, 0)
    if name == "seed_at_corner":
        g[0][0] = 2
        return g
    if name == "seeds_aligned":
        g[1][3] = 2
        g[3][3] = 2
        return g
    if name == "no_seeds":
        return g
    return g
