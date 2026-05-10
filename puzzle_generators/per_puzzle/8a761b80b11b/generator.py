"""Generator for arc_puzzle_bank_21_set9_e:easy_i01.

Replace each horizontal same-color run by its endpoints.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_runs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_runs, vertical_only, all_singletons.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8a761b80b11b"
VERSION = "1.1.0"
TASK_ID = "8a761b80b11b"

SUMMARY = "Replace each horizontal same-color run by its endpoints."

INVARIANTS = [
    "background is 0",
    "nonzero cells form horizontal same-color runs",
    "runs are separated by zeros",
    "singletons and length-two runs are already endpoints",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_runs", "vertical_only", "all_singletons")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "3..12"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "5..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_runs":         {"type": "int", "default": "rng 3..5", "valid": "1..12"},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "horizontal_runs",
                       "valid": "horizontal_runs"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "1..9"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 5, 5)
        w = ctx.draw_int("grid_w", 8, 9)
        target = ctx.draw_int("n_runs", 3, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 10, 11)
        target = ctx.draw_int("n_runs", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        w = ctx.draw_int("grid_w", 8, 11)
        target = ctx.draw_int("n_runs", 3, 5)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    placed = 0
    for _ in range(160):
        if placed >= target:
            break
        length = rng.randint(2, min(5, w))
        r = rng.randrange(h)
        c = rng.randint(0, w - length)
        if any(g[r][cc] != 0 for cc in range(max(0, c - 1), min(w, c + length + 1))):
            continue
        color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
        for cc in range(c, c + length):
            g[r][cc] = color
        placed += 1
    if not any(
        c + 2 < w and g[r][c] != 0 and g[r][c] == g[r][c + 1] == g[r][c + 2]
        for r in range(h)
        for c in range(w - 2)
    ):
        color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
        g[h // 2][1:4] = [color, color, color]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 10
    g = full_grid(h, w, 0)
    if name == "no_runs":
        # blank → no horizontal runs to reduce
        return g
    if name == "vertical_only":
        # only vertical runs → "horizontal" precondition fails
        for r in range(2, 5): g[r][3] = 4
        for r in range(1, 4): g[r][7] = 6
        return g
    if name == "all_singletons":
        # only single cells → output identical to input (no signal)
        g[1][2] = 4
        g[3][5] = 6
        g[5][8] = 7
        return g
    return g
