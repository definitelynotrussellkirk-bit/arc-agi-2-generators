"""Generator for arc_puzzle_bank_next_21_bundle:easy_14_mark_vertical_run_endpoints.

Rule: vertical 6-runs whose endpoints are marked by the rule.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_runs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_runs, all_singletons, runs_overlap.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0c1bec3fcbdc"
VERSION = "1.1.0"
TASK_ID = "0c1bec3fcbdc"
SUMMARY = "Vertical 6-runs whose endpoints are marked by the rule."

INVARIANTS = [
    "background is 0",
    "all source objects are vertical runs of color 6",
    "at least one run has length at least 3",
    "runs are column-separated to avoid accidental merging",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_runs", "all_singletons", "runs_full_column")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..11", "valid": "6..16"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_runs":         {"type": "int", "default": "rng 2..5", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "vertical_columns",
                       "valid": "vertical_columns"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
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
        w = ctx.draw_int("grid_w", 8, 10)
        n_runs = ctx.draw_int("n_runs", 2, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 11)
        w = ctx.draw_int("grid_w", 11, 12)
        n_runs = ctx.draw_int("n_runs", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 7, 11)
        w = ctx.draw_int("grid_w", 8, 12)
        n_runs = ctx.draw_int("n_runs", 2, 5)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)

    cols = rng.sample(range(w), min(n_runs, w))
    for c in cols:
        run_len = rng.randint(3, min(5, h))
        r0 = rng.randint(0, h - run_len)
        for r in range(r0, r0 + run_len):
            g[r][c] = 6
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    if name == "no_runs":
        # empty grid → no runs to mark endpoints of
        return g
    if name == "all_singletons":
        # only single 6-cells, no length-≥2 runs → no endpoints (a singleton has no distinct ends)
        for c in [1, 4, 7]:
            g[3][c] = 6
        return g
    if name == "runs_full_column":
        # runs span the full column → endpoints are at rows 0 and h-1, no body to distinguish
        for c in [2, 5]:
            for r in range(h):
                g[r][c] = 6
        return g
    return g
