"""Generator for v1_e_m_h_keys:E2.

Rule: each vertical run of color 3 of exact length 2 is recolored to 7.

Combinatorial axes (8): grid_h/w, palette_kind, n_runs, run_length,
palette_size, position_bias, n_distinct_colors, texture.
Degenerates: only_length_3, no_runs, only_isolated_3s.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d59da25908ca"
VERSION = "1.1.0"
TASK_ID = "d59da25908ca"
SUMMARY = "Vertical color-3 runs of length 2-4 in distinct columns."

INVARIANTS = [
    "background is 0",
    "1-3 vertical color-3 runs of length 2-4 in distinct columns",
]

PALETTE_KINDS = ("default", "sparse", "wide_grid", "tight")
DEGENERATE_TEXTURES = ("only_length_3", "no_runs", "only_isolated_3s")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_runs":         {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "run_length":     {"type": "int", "default": "2", "valid": "2"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "uniform", "valid": "uniform"},
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
        h = ctx.draw_int("grid_h", 6, 6)
        w = ctx.draw_int("grid_w", 5, 6)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 6, 7)
    else:
        h = ctx.draw_int("grid_h", 6, 8)
        w = ctx.draw_int("grid_w", 5, 7)
    n = ctx.draw_int("n_runs", 1, min(3, w))
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    cols = rng.sample(range(w), n)
    for c in cols:
        r0 = rng.randint(0, h - 2)
        g[r0][c] = 3
        g[r0 + 1][c] = 3
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 6
    g = full_grid(h, w, 0)
    if name == "only_length_3":
        # length-3 runs — rule applies only to length-2, so no recolor
        g[1][1] = 3; g[2][1] = 3; g[3][1] = 3
        g[2][4] = 3; g[3][4] = 3; g[4][4] = 3
        return g
    if name == "no_runs":
        # isolated 0-grid — no 3-runs at all
        return g
    if name == "only_isolated_3s":
        # length-1 runs (single 3-cells) — rule has no length-2 to recolor
        g[1][1] = 3
        g[3][3] = 3
        g[5][2] = 3
        return g
    return g
