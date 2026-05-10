"""Generator for arc_puzzle_bank_21_set13_bundle:easy_m01.

Horizontal same-color runs are present; the solver keeps only the leftmost
cell of each run.

Combinatorial axes (8): grid_h, grid_w, palette_kind, run_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: all_singletons, runs_touching, no_runs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "bdaef728db34"
VERSION = "1.1.0"
TASK_ID = "bdaef728db34"
SUMMARY = "Several separated horizontal runs of nonzero colors."

INVARIANTS = [
    "background is 0",
    "all nonzero cells belong to horizontal runs of length at least 2",
    "same-row runs are separated by at least one zero",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("all_singletons", "runs_touching", "no_runs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "4..12"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "run_count":      {"type": "int", "default": "rng 3..5", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 3..5", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "scattered_rows",
                       "valid": "scattered_rows"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 8, 9)
        run_count = ctx.draw_int("run_count", 3, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 11, 12)
        run_count = ctx.draw_int("run_count", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 8, 12)
        run_count = ctx.draw_int("run_count", 3, 5)
    colors = ctx.draw_distinct_colors("colors", n=min(run_count, 6), exclude={0})
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    placed = 0
    for _ in range(300):
        if placed >= run_count:
            break
        length = rng.randint(2, min(5, w))
        r = rng.randrange(h)
        c1 = rng.randint(0, w - length)
        c2 = c1 + length - 1
        band = range(max(0, c1 - 1), min(w, c2 + 2))
        if all(g[r][c] == 0 for c in band):
            color = colors[placed % len(colors)]
            for c in range(c1, c2 + 1):
                g[r][c] = color
            placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 10
    g = full_grid(h, w, 0)
    if name == "all_singletons":
        # nonzero cells are singletons (length 1) → "leftmost of run" = the cell itself, rule is identity
        for r, c, v in [(1, 2, 4), (3, 5, 5), (5, 7, 6)]:
            g[r][c] = v
        return g
    if name == "runs_touching":
        # adjacent runs of different colors with no zero gap → ambiguous run boundaries
        for c, v in [(1, 3), (2, 3), (3, 4), (4, 4), (5, 5)]:
            g[2][c] = v
        return g
    if name == "no_runs":
        # empty grid → no runs to extract leftmost from
        return g
    return g
