"""Generator for arc_puzzle_bank_21_set16_bundle:easy_p03.

Rule: left-border seeds beam rightward through zeros until the first
nonzero blocker or the row edge.

Combinatorial axes (8): grid_h, grid_w, palette_kind, row_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_seeds, blockers_at_col0, all_rows_blocked_immediately.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f358bc90694d"
VERSION = "1.1.0"
TASK_ID = "f358bc90694d"
SUMMARY = "Rows with a left-border beam seed and optional blocker."

INVARIANTS = [
    "background is 0",
    "active rows have one nonzero seed in column 0",
    "some active rows contain a later nonzero blocker",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_seeds", "blockers_at_col0", "all_rows_blocked_immediately")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "4..12"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "5..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "row_count":      {"type": "int", "default": "rng 3..5", "valid": "1..8"},
    "palette_size":   {"type": "int", "default": "rng 4..6", "valid": "2..9"},
    "position_bias":  {"type": "str", "default": "left_seed_with_optional_blocker",
                       "valid": "left_seed_with_optional_blocker"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..6", "valid": "2..9"},
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
        row_count = min(ctx.draw_int("row_count", 2, 3), h)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 11, 12)
        row_count = min(ctx.draw_int("row_count", 4, 5), h)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 8, 12)
        row_count = min(ctx.draw_int("row_count", 3, 5), h)
    colors = ctx.draw_distinct_colors("colors", n=row_count + 2, exclude={0})
    rng = ctx.draw_rng("layout")

    g = full_grid(h, w, 0)
    rows = rng.sample(range(h), row_count)
    for i, r in enumerate(rows):
        g[r][0] = colors[i]
        if rng.choice([True, False]):
            g[r][rng.randint(3, w - 1)] = colors[(i + 1) % len(colors)]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 10
    g = full_grid(h, w, 0)
    if name == "no_seeds":
        # blank col 0 → no seeds, rule has nothing to beam
        g[2][5] = 4; g[5][8] = 6
        return g
    if name == "blockers_at_col0":
        # cell at col 0 in some rows is non-zero but not the seed (e.g. blockers stacked) →
        # ambiguous which is the seed
        g[1][0] = 4; g[1][1] = 6   # 4 at col 0, 6 immediately to the right
        g[3][0] = 8; g[3][2] = 3   # 8 at col 0, blocker at col 2 leaves no beam path
        return g
    if name == "all_rows_blocked_immediately":
        # blocker at col 1 in every active row → beam extends 0 cells
        g[1][0] = 4; g[1][1] = 6
        g[3][0] = 8; g[3][1] = 3
        g[5][0] = 9; g[5][1] = 7
        return g
    return g
