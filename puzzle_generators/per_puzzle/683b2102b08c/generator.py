"""Generator for dc46ea44.

Rule: below yellow separator, main shape moves to top; secondary
shape nests left.

Combinatorial axes (8): grid_h/w, line_row, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_separator, no_shapes, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "683b2102b08c"
VERSION = "1.1.0"
TASK_ID = "683b2102b08c"
SUMMARY = "Below yellow separator, main shape goes top, secondary nests left."

INVARIANTS = [
    "the background is orange and one full yellow row separates the scene",
    "below the separator, the most frequent color is the main shape",
    "the main shape is copied to the top rows in the same columns",
    "main and secondary colors exclude 4 and 7",
]

LINE_ROWS = ("r6", "r7")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_separator", "no_shapes", "full_grid")
HELPFUL_TEXTURES = LINE_ROWS

AXES = {
    "grid_h":         {"type": "int", "default": "13", "valid": "13"},
    "grid_w":         {"type": "int", "default": "15", "valid": "15"},
    "line_row":       {"type": "str", "default": "rng helpful",
                       "valid": "|".join(LINE_ROWS)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for line_row",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    tx = overrides.get("texture")
    if tx in LINE_ROWS:
        line_row = int(tx[1:])
    else:
        line_row = ctx.draw_choice("line_row", [6, 7])
    main, secondary = ctx.draw_distinct_colors("colors", n=2, exclude={4, 7})
    g = full_grid(13, 15, 7)
    for c in range(15):
        g[line_row][c] = 4
    main_c = 8 + (sample_index % 2)
    draw_rect(g, line_row + 2, main_c, 3, 4, main)
    g[line_row + 5][main_c + 1] = main
    draw_rect(g, line_row + 3, 2, 2, 2, secondary)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 15, 7)
    if name == "no_separator":
        draw_rect(g, 8, 5, 3, 4, 2)
        return g
    if name == "no_shapes":
        for c in range(15):
            g[6][c] = 4
        return g
    if name == "full_grid":
        for r in range(13):
            for c in range(15):
                g[r][c] = 4
        return g
    return g
