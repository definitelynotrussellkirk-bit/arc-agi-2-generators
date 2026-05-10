"""Generator for arc_additional_puzzles_21_set3:E19 — Diagonal 8-pair → fill anti-diagonal corners with 1.

Rule: 2×2 block where (r,c) and (r+1,c+1) are 8 with (r,c+1) and
(r+1,c) being 0 → set those 0s to 1. Same for the other diagonal.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_pairs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, antidiag_filled, only_singletons.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "2826c36048c1"
VERSION = "1.1.0"
TASK_ID = "2826c36048c1"
SUMMARY = "2-3 diagonal 8-pairs with empty anti-diagonal corners."

INVARIANTS = [
    "≥2 8-pairs at diagonal positions",
    "anti-diagonal corners are 0 (will become 1)",
    "no two 8-pairs touch",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "antidiag_filled", "only_singletons")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 6..8", "valid": "5..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pairs":        {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "diag_8_pairs",
                       "valid": "diag_8_pairs"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1..1"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 6, 7)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 7, 8)
    else:
        h = ctx.draw_int("grid_h", 6, 8)
        w = ctx.draw_int("grid_w", 6, 8)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    placed = []
    for _ in range(40):
        if len(placed) >= rng.randint(2, 3): break
        r = rng.randint(0, h - 2); c = rng.randint(0, w - 2)
        if all(abs(r - pr) > 2 or abs(c - pc) > 2 for pr, pc in placed):
            d = rng.choice([(0, 0, 1, 1), (0, 1, 1, 0)])
            g[r + d[0]][c + d[1]] = 8
            g[r + d[2]][c + d[3]] = 8
            placed.append((r, c))
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 7
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # blank → no 8-pairs, rule has no antidiag corners to fill
        return g
    if name == "antidiag_filled":
        # 2x2 block with all 4 cells non-zero → antidiag corners aren't 0
        g[1][1] = 8; g[2][2] = 8
        g[1][2] = 4; g[2][1] = 6   # antidiag corners already non-zero
        return g
    if name == "only_singletons":
        # only isolated 8s → no diagonal pair, rule never fires
        g[1][1] = 8
        g[3][4] = 8
        g[5][2] = 8
        return g
    return g
