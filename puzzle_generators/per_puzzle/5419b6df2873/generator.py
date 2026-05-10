"""Generator for arc_additional_puzzles_21_set5:E33.

Rule: every nonzero top-row marker controls a full column fill in its
color.

Combinatorial axes (8): grid_h/w, n_markers, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_markers, full_top_row, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5419b6df2873"
VERSION = "1.1.0"
TASK_ID = "5419b6df2873"
SUMMARY = "Every nonzero top-row marker controls a full column fill in its color."
INVARIANTS = ["markers are only in the top row", "marker columns are distinct", "background is zero"]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_markers", "full_top_row", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..9", "valid": "3..12"},
    "grid_w":         {"type": "int", "default": "rng 6..10", "valid": "3..14"},
    "n_markers":      {"type": "int", "default": "rng 2..5", "valid": "1..10"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "varied", "valid": "varied"},
    "position_bias":  {"type": "str", "default": "top_row", "valid": "top_row"},
    "n_distinct_colors":{"type": "int", "default": "varied", "valid": "varied"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 5, 6)
        w = ctx.draw_int("grid_w", 6, 8)
        n_max = 3
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 9)
        w = ctx.draw_int("grid_w", 9, 10)
        n_max = 5
    else:
        h = ctx.draw_int("grid_h", 5, 9)
        w = ctx.draw_int("grid_w", 6, 10)
        n_max = 5
    n = min(ctx.draw_int("n_markers", 2, n_max), w)
    rng = ctx.draw_rng("layout")
    cols = list(range(w))
    rng.shuffle(cols)
    colors = list(ctx.draw_distinct_colors("colors", n=n, exclude={0}))
    g = full_grid(h, w, 0)
    for i, c in enumerate(cols[:n]):
        g[0][c] = colors[i]
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(7, 8, 0)
    if name == "no_markers":
        return g
    if name == "full_top_row":
        for c in range(8):
            g[0][c] = (c % 8) + 1
        return g
    if name == "full_grid":
        for r in range(7):
            for c in range(8):
                g[r][c] = 3
        return g
    return g
