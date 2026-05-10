"""Generator for arc_additional_puzzles_21_set19_bundle:E133.

Rule: row 0 has a single non-zero marker. Its column maps to one of
3 panels: cols<4 → panel A (cols 1-3), cols<8 → B (5-7), else C (9-11).
Output the 3-row × 3-col panel from rows 2-4.

Combinatorial axes (8): grid_h, grid_w, palette_kind, marker_panel,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_marker, multiple_markers, marker_off_panel.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at
from puzzle_generators.helpers.shape import PLUS_5

GENERATOR_ID = "5dbba35ed715"
VERSION = "1.1.0"
TASK_ID = "5dbba35ed715"
SUMMARY = "Fixed 5×13 grid: row 0 marker, rows 2-4 contain 3 panels."

INVARIANTS = [
    "grid is 5 rows × 13 cols",
    "row 0 has exactly 1 non-zero cell at any column",
    "3 panels at cols [1-3], [5-7], [9-11], rows 2-4 each with a different shape",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_marker", "multiple_markers", "marker_off_panel")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "5", "valid": "5"},
    "grid_w":         {"type": "int", "default": "13", "valid": "13"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "marker_panel":   {"type": "int", "default": "rng 0..2", "valid": "0..2"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed_5x13",
                       "valid": "fixed_5x13"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "density":        {"type": "str", "default": "panels", "valid": "panels"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    h, w = 5, 13
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    g[0][rng.randint(0, w - 1)] = rng.randint(1, 9)
    pal = rng.sample([2, 3, 4, 5, 6, 7], 3)
    shapes = [
        PLUS_5,
        [(0, 0), (0, 1), (0, 2), (2, 0), (2, 2)],
        [(0, 0), (1, 1), (2, 2)],
    ]
    rng.shuffle(shapes)
    paint_at(g, 2, 1, shapes[0], pal[0])
    paint_at(g, 2, 5, shapes[1], pal[1])
    paint_at(g, 2, 9, shapes[2], pal[2])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 5, 13
    g = full_grid(h, w, 0)
    pal = [4, 6, 7]
    shapes = [
        PLUS_5,
        [(0, 0), (0, 1), (0, 2), (2, 0), (2, 2)],
        [(0, 0), (1, 1), (2, 2)],
    ]
    paint_at(g, 2, 1, shapes[0], pal[0])
    paint_at(g, 2, 5, shapes[1], pal[1])
    paint_at(g, 2, 9, shapes[2], pal[2])
    if name == "no_marker":
        # row 0 empty → no panel selector, rule undefined
        return g
    if name == "multiple_markers":
        # two markers on row 0 → which one selects?
        g[0][2] = 4
        g[0][7] = 6
        return g
    if name == "marker_off_panel":
        # marker at col 12 (boundary) → may be ambiguous between panel C and out-of-range
        g[0][12] = 4
        return g
    return g
