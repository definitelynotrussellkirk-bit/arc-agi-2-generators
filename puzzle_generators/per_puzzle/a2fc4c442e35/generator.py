"""Generator for arc_puzzle_bank_fourth21:E24.

Rule: each horizontal length-3 run with empty neighbors gets its
matching transform.

Combinatorial axes (8): grid_h, grid_w, palette_kind, runs,
palette_size, position_bias, n_distinct_colors, run_density, texture.
Degenerates: no_runs, run_too_long, runs_touching.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a2fc4c442e35"
VERSION = "1.1.0"
TASK_ID = "a2fc4c442e35"
SUMMARY = "Place exact horizontal length-3 runs with blank cells on both sides."

INVARIANTS = [
    "background is 0",
    "each target run is horizontal and length exactly 3",
    "the cells immediately left and right of each target run are zero",
    "runs are row-separated to avoid accidental merging",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_runs", "run_too_long", "runs_touching")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..8", "valid": "3..14"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "5..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "runs":           {"type": "int", "default": "rng 1..3", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 1..3", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "row_separated", "valid": "row_separated"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..3", "valid": "1..9"},
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
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 8, 10)
        target = min(ctx.draw_int("runs", 1, 2), h)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 10, 12)
        target = min(ctx.draw_int("runs", 2, 3), h)
    else:
        h = ctx.draw_int("grid_h", 5, 8)
        w = ctx.draw_int("grid_w", 8, 12)
        target = min(ctx.draw_int("runs", 1, 3), h)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    rows = rng.sample(range(h), target)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8, 9], target)
    for r, color in zip(rows, colors):
        c0 = rng.randint(1, w - 5)
        for dc in range(3):
            g[r][c0 + dc] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 10
    g = full_grid(h, w, 0)
    if name == "no_runs":
        # empty grid — rule has no run to act on
        return g
    if name == "run_too_long":
        # length-4 horizontal — predicate "exactly length 3" fails
        for dc in range(4):
            g[2][2 + dc] = 5
        return g
    if name == "runs_touching":
        # two length-3 runs adjacent — the empty-neighbor invariant fails
        for dc in range(3):
            g[2][1 + dc] = 4
            g[2][4 + dc] = 6
        return g
    return g
