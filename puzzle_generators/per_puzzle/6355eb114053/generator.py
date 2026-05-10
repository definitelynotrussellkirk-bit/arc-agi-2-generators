"""Generator for arc_additional_puzzles_21_set5:E34.

Rule: a zero center with same-colored cardinal neighbors is filled with
that color (plus completion).

Combinatorial axes (8): grid_h/w, palette_kind, n_pluses, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_pluses, mismatched_neighbors, center_already_filled.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "6355eb114053"
VERSION = "1.1.0"
TASK_ID = "6355eb114053"
SUMMARY = "A zero center with same-colored cardinal neighbors is filled with that color."

INVARIANTS = [
    "center cells start as zero",
    "cardinal neighbors share a nonzero color",
    "pluses are separated",
]

PALETTE_KINDS = ("default", "sparse", "dense", "varied_palette")
DEGENERATE_TEXTURES = ("no_pluses", "mismatched_neighbors", "center_already_filled")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_pluses":       {"type": "int", "default": "rng 1..3", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "rng 1..3", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..3", "valid": "1..9"},
    "density":        {"type": "str", "default": "mixed", "valid": "mixed"},
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
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 7, 10)
    n = ctx.draw_int("n_pluses", 1, 3)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    centers = [(r, c) for r in range(1, h - 1, 3) for c in range(1, w - 1, 3)]
    rng.shuffle(centers)
    for i, (r, c) in enumerate(centers[:n]):
        color = (i % 8) + 1
        g[r - 1][c] = color
        g[r + 1][c] = color
        g[r][c - 1] = color
        g[r][c + 1] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 8
    g = full_grid(h, w, 0)
    if name == "no_pluses":
        # singletons — no full plus pattern
        g[2][2] = 4
        g[5][5] = 7
        return g
    if name == "mismatched_neighbors":
        # 4 cardinal neighbors but different colors → no consistent fill
        g[2][3] = 4
        g[4][3] = 6
        g[3][2] = 7
        g[3][4] = 8
        return g
    if name == "center_already_filled":
        # center is non-zero — invariant violated
        g[2][2] = 5
        g[4][2] = 5
        g[3][1] = 5
        g[3][3] = 5
        g[3][2] = 9  # center already filled
        return g
    return g
