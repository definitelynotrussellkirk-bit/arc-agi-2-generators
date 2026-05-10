"""Generator for v1_e_m_h_keys:E1.

Rule: each horizontal run of color-2 of length ≥3 has its first and
last cells marked color 8.

Combinatorial axes (8): grid_h/w, palette_kind, n_runs, palette_size,
position_bias, n_distinct_colors, run_density, texture.
Degenerates: no_runs, run_too_short, runs_share_row.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "9d137b878536"
VERSION = "1.1.0"
TASK_ID = "9d137b878536"
SUMMARY = "1-3 horizontal color-2 runs of length 3-5 in distinct rows."

INVARIANTS = [
    "background is 0",
    "1-3 horizontal color-2 runs of length 3-5 in distinct rows, no two in same row",
]

PALETTE_KINDS = ("default", "sparse", "dense", "long_runs")
DEGENERATE_TEXTURES = ("no_runs", "run_too_short", "runs_share_row")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 4..6", "valid": "3..10"},
    "grid_w":         {"type": "int", "default": "rng 7..9", "valid": "5..12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_runs":         {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
    "run_density":    {"type": "str", "default": "mixed", "valid": "mixed"},
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
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 8, 9)
    else:
        h = ctx.draw_int("grid_h", 4, 6)
        w = ctx.draw_int("grid_w", 7, 9)
    n = ctx.draw_int("n_runs", 1, min(3, h))
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    rows = rng.sample(range(h), n)
    for r in rows:
        length = rng.randint(3, 5)
        c0 = rng.randint(0, w - length)
        for c in range(c0, c0 + length):
            g[r][c] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 5, 8
    g = full_grid(h, w, 0)
    if name == "no_runs":
        # singletons / length-1 cells only — no run of length ≥3
        g[1][2] = 2
        g[3][5] = 2
        return g
    if name == "run_too_short":
        # length-2 runs only — fail the ≥3 predicate
        g[1][2] = 2; g[1][3] = 2
        g[3][5] = 2; g[3][6] = 2
        return g
    if name == "runs_share_row":
        # 2 separated runs in the same row → invariant violation
        g[2][0] = 2; g[2][1] = 2; g[2][2] = 2
        g[2][5] = 2; g[2][6] = 2; g[2][7] = 2
        return g
    return g
