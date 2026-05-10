"""Generator for arc_additional_puzzles_21_set7:E44 — Connect diagonal pairs.

Rule: for each cell (r, c) with the same value at (r±2, c±2) along
diagonals (2,2) and (2,-2), fill the midpoint (r±1, c±1) with that value.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_pairs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, midpoint_filled, axis_aligned.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "69927005ac25"
VERSION = "1.1.0"
TASK_ID = "69927005ac25"
SUMMARY = "2-3 pairs of same-color cells at diagonal distance 2 (NE or NW)."

INVARIANTS = [
    "2-3 diagonal pairs",
    "each pair: cells at (r, c) and (r+2, c±2) of the same color",
    "midpoint cells are 0",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "midpoint_filled", "axis_aligned")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pairs":        {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "diagonal_distance_2_pairs",
                       "valid": "diagonal_distance_2_pairs"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..8"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 8, 11)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    n_pairs = rng.randint(2, 3)
    palette = rng.sample([1, 2, 3, 4, 6, 7, 8, 9], n_pairs)
    placed = set()
    for color in palette:
        for _ in range(40):
            dc = rng.choice([2, -2])
            r1 = rng.randint(0, h - 3)
            c1 = rng.randint(max(0, -dc), min(w - 1, w - 1 - dc))
            r2 = r1 + 2; c2 = c1 + dc
            mr = r1 + 1; mc = c1 + dc // 2
            if any((rr, cc) in placed for rr in [r1, r2, mr] for cc in [c1, c2, mc]):
                continue
            if g[r1][c1] != 0 or g[r2][c2] != 0 or g[mr][mc] != 0:
                continue
            g[r1][c1] = color
            g[r2][c2] = color
            placed.update({(r1, c1), (r2, c2), (mr, mc)})
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 9
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # blank → no diagonal pairs to bridge
        return g
    if name == "midpoint_filled":
        # midpoint already filled → rule is identity, no change
        g[1][1] = 4; g[2][2] = 4; g[3][3] = 4
        return g
    if name == "axis_aligned":
        # 2 cells in same row → not diagonal, rule won't fire
        g[3][1] = 4; g[3][3] = 4
        return g
    return g
