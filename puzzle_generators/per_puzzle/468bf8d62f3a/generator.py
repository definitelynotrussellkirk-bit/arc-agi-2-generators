"""Generator for arc_puzzle_bank_21_set14_bundle:easy_n01.

Vertical same-color runs are present; the solver keeps only the topmost cell
of each run.

Combinatorial axes (8): grid_h, grid_w, palette_kind, run_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: all_singletons, runs_touching, no_runs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "468bf8d62f3a"
VERSION = "1.1.0"
TASK_ID = "468bf8d62f3a"
SUMMARY = "Several separated vertical runs of nonzero colors."

INVARIANTS = [
    "background is 0",
    "all nonzero cells belong to vertical runs of length at least 2",
    "same-column runs are separated by at least one zero",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("all_singletons", "runs_touching", "no_runs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..11", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng 6..10", "valid": "4..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "run_count":      {"type": "int", "default": "rng 3..5", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "scattered_cols",
                       "valid": "scattered_cols"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..5", "valid": "1..8"},
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
        w = ctx.draw_int("grid_w", 6, 7)
        run_count = ctx.draw_int("run_count", 3, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 9, 10)
        run_count = ctx.draw_int("run_count", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 7, 11)
        w = ctx.draw_int("grid_w", 6, 10)
        run_count = ctx.draw_int("run_count", 3, 5)
    colors = ctx.draw_distinct_colors("colors", n=min(run_count, 6), exclude={0})
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    placed = 0
    for _ in range(300):
        if placed >= run_count:
            break
        length = rng.randint(2, min(5, h))
        r1 = rng.randint(0, h - length)
        r2 = r1 + length - 1
        c = rng.randrange(w)
        band = range(max(0, r1 - 1), min(h, r2 + 2))
        if all(g[r][c] == 0 for r in band):
            color = colors[placed % len(colors)]
            for r in range(r1, r2 + 1):
                g[r][c] = color
            placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 7
    g = full_grid(h, w, 0)
    if name == "all_singletons":
        # nonzero cells are singletons (length 1) → "topmost of run" = the cell itself, rule is identity
        for r, c, v in [(1, 1, 4), (3, 4, 5), (6, 2, 6)]:
            g[r][c] = v
        return g
    if name == "runs_touching":
        # adjacent vertical runs of different colors with no zero gap → ambiguous run boundaries
        for r, v in [(1, 3), (2, 3), (3, 4), (4, 4), (5, 5)]:
            g[r][2] = v
        return g
    if name == "no_runs":
        # empty grid → no runs to extract topmost from
        return g
    return g
