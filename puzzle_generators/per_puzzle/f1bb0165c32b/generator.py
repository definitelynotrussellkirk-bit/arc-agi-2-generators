"""Generator for arc_puzzle_bank_next_21_bundle:easy_08_exact_vertical_quadruples.

Rule: several vertical 1-runs; exact length-4 runs are recolored by the rule.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_runs,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_length4, all_length4, no_runs.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f1bb0165c32b"
VERSION = "1.1.0"
TASK_ID = "f1bb0165c32b"
SUMMARY = "Several vertical 1-runs; exact length-4 runs are recolored by the rule."

INVARIANTS = [
    "background is 0",
    "all source runs are vertical runs of color 1",
    "at least one run has exact length 4",
    "other runs have non-4 lengths so the selector has contrast",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_length4", "all_length4", "no_runs")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "8..16"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "8..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_runs":         {"type": "int", "default": "rng 3..5", "valid": "2..8"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1..1"},
    "position_bias":  {"type": "str", "default": "vertical_runs_with_length4",
                       "valid": "vertical_runs_with_length4"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
        n_runs = ctx.draw_int("n_runs", 3, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 11, 12)
        n_runs = ctx.draw_int("n_runs", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 8, 12)
        n_runs = ctx.draw_int("n_runs", 3, 5)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)

    cols = rng.sample(range(1, w - 1), min(n_runs, w - 2))
    lengths = [4] + [rng.choice([2, 3, 5]) for _ in range(len(cols) - 1)]
    rng.shuffle(lengths)
    for c, run_len in zip(cols, lengths):
        r0 = rng.randint(0, h - run_len)
        for r in range(r0, r0 + run_len):
            g[r][c] = 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "no_length4":
        # all runs ≠ 4 → no runs match, rule has nothing to recolor
        for r in range(1, 4): g[r][1] = 1     # length 3
        for r in range(2, 4): g[r][4] = 1     # length 2
        for r in range(1, 6): g[r][7] = 1     # length 5
        return g
    if name == "all_length4":
        # all runs length 4 → all recolored uniformly (no contrast)
        for r in range(1, 5): g[r][1] = 1
        for r in range(3, 7): g[r][4] = 1
        for r in range(2, 6): g[r][7] = 1
        return g
    if name == "no_runs":
        # blank → no runs at all
        return g
    return g
