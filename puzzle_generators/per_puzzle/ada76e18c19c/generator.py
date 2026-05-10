"""Generator for arc_additional_puzzles_21_set15_bundle:E101 — Fill segment between 2 same-color cells in row.

Rule: each row with exactly 2 cells of single color → fill between
them (inclusive) with that color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_rows,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_pairs, mismatched_endpoints, span_already_filled.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ada76e18c19c"
VERSION = "1.1.0"
TASK_ID = "ada76e18c19c"
SUMMARY = "2-3 rows have exactly 2 cells of same color separated by gap."

INVARIANTS = [
    "≥2 rows have exactly 2 cells of one color, separated by ≥2 0-cells",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_pairs", "mismatched_endpoints", "span_already_filled")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 4..6", "valid": "3..10"},
    "grid_w":         {"type": "int", "default": "rng 7..9", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_rows":         {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "position_bias":  {"type": "str", "default": "row_color_pairs_gap",
                       "valid": "row_color_pairs_gap"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..5"},
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
        h = ctx.draw_int("grid_h", 4, 5)
        w = ctx.draw_int("grid_w", 7, 8)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 8, 9)
    else:
        h = ctx.draw_int("grid_h", 4, 6)
        w = ctx.draw_int("grid_w", 7, 9)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    used_rows = set()
    palette = [2, 3, 4, 5, 6, 7, 8, 9]
    for _ in range(rng.randint(2, 3)):
        for _ in range(20):
            r = rng.randint(0, h - 1)
            if r in used_rows:
                continue
            color = rng.choice(palette)
            cs = sorted(rng.sample(range(w), 2))
            if cs[1] - cs[0] >= 3:
                g[r][cs[0]] = color; g[r][cs[1]] = color
                used_rows.add(r)
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 5, 8
    g = full_grid(h, w, 0)
    if name == "no_pairs":
        # singletons only → no pair to fill span between
        g[1][2] = 4
        g[3][6] = 6
        return g
    if name == "mismatched_endpoints":
        # mismatched colors → "exactly 2 cells of single color" precondition fails
        g[1][1] = 4; g[1][5] = 6
        g[3][2] = 3; g[3][6] = 7
        return g
    if name == "span_already_filled":
        # span already non-zero → "all-0 between" precondition fails
        g[1][1] = 4; g[1][3] = 9; g[1][5] = 4   # midpoint already non-zero
        return g
    return g
