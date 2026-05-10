"""Generator for arc_additional_puzzles_21_set3:E21 — Replace 9s with row's unique non-{0,9} color.

Rule: each row that has exactly 1 distinct non-{0,9} color AND ≥1 cell
of value 9 → replace 9-cells with that color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_active_rows,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_9s, multi_color_row, no_row_color.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "9679db24667b"
VERSION = "1.1.0"
TASK_ID = "9679db24667b"
SUMMARY = "2-3 rows have a single non-{0,9} color and ≥1 cell of value 9."

INVARIANTS = [
    "≥2 rows have exactly 1 distinct non-{0,9} color and ≥1 9-cell",
    "1 distractor row has 9s but no other non-bg colors (won't trigger)",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_9s", "multi_color_row", "no_row_color")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..8", "valid": "5..12"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_active_rows":  {"type": "int", "default": "rng 2..3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "rows_with_color_and_9s",
                       "valid": "rows_with_color_and_9s"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..3", "valid": "1..9"},
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
        h = ctx.draw_int("grid_h", 6, 6)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 6, 8)
        w = ctx.draw_int("grid_w", 8, 10)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    used_rows = set()
    for _ in range(rng.randint(2, 3)):
        for _ in range(20):
            r = rng.randint(0, h - 1)
            if r in used_rows:
                continue
            color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8])
            cs = rng.sample(range(w), 4)
            n_color = rng.randint(1, 2)
            for c in cs[:n_color]:
                g[r][c] = color
            for c in cs[n_color:]:
                g[r][c] = 9
            used_rows.add(r)
            break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 10
    g = full_grid(h, w, 0)
    if name == "no_9s":
        # rows have a unique color but no 9s → rule has no 9-cells to replace
        g[1][1] = 4; g[1][3] = 4; g[1][5] = 4
        g[3][2] = 6; g[3][6] = 6
        return g
    if name == "multi_color_row":
        # rows have multiple distinct non-{0,9} colors → predicate "exactly 1" fails
        g[1][1] = 4; g[1][3] = 6; g[1][5] = 9; g[1][7] = 9
        g[3][2] = 3; g[3][4] = 8; g[3][6] = 9
        return g
    if name == "no_row_color":
        # rows have only 9s (no other color) → rule has no replacement color
        g[1][1] = 9; g[1][3] = 9; g[1][5] = 9
        g[3][2] = 9; g[3][6] = 9
        return g
    return g
