"""Generator for arc_puzzle_bank_21_set5_s:S5_E3.

Rule: a magenta marker in column 0 selects a row, returned without col 0.

Combinatorial axes (8): grid_h, grid_w, palette_kind, density,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_marker, multiple_markers, marker_row_empty.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d07a6cba78c7"
VERSION = "1.1.0"
TASK_ID = "d07a6cba78c7"
SUMMARY = "A magenta marker in column 0 selects a row, returned without the marker column."

INVARIANTS = [
    "background is 0",
    "there is exactly one magenta cell in the first column",
    "the marked row may contain arbitrary non-marker payload cells",
    "output is the marked row excluding column 0",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_marker", "multiple_markers", "marker_row_empty")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..8", "valid": "3..14"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "4..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "density":        {"type": "int", "default": "rng 35..60", "valid": "0..100"},
    "palette_size":   {"type": "int", "default": "6", "valid": "2..7"},
    "position_bias":  {"type": "str", "default": "row_marker",
                       "valid": "row_marker"},
    "n_distinct_colors": {"type": "int", "default": "6", "valid": "2..7"},
    "n_markers":      {"type": "int", "default": "1", "valid": "1..1"},
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
        w = ctx.draw_int("grid_w", 7, 8)
        density = ctx.draw_int("density", 30, 45)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 9, 10)
        density = ctx.draw_int("density", 50, 60)
    else:
        h = ctx.draw_int("grid_h", 5, 8)
        w = ctx.draw_int("grid_w", 7, 10)
        density = ctx.draw_int("density", 35, 60)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    marked_r = rng.randrange(h)
    g[marked_r][0] = 6
    palette = [1, 2, 3, 4, 5, 7]
    for r in range(h):
        for c in range(1, w):
            if rng.randrange(100) < density:
                g[r][c] = rng.choice(palette)
    if all(v == 0 for v in g[marked_r][1:]):
        g[marked_r][rng.randint(1, w - 1)] = rng.choice(palette)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 6, 8
    g = full_grid(h, w, 0)
    palette = [1, 2, 3, 4, 5, 7]
    if name == "no_marker":
        # no magenta marker → no row selected, rule has no anchor
        for r in range(h):
            for c in range(1, w):
                if (r + c) % 2 == 0:
                    g[r][c] = palette[(r + c) % len(palette)]
        return g
    if name == "multiple_markers":
        # multiple magenta cells in col 0 → ambiguous which row to extract
        g[1][0] = 6
        g[3][0] = 6
        g[5][0] = 6
        for r in range(h):
            for c in range(1, w):
                if (r * 3 + c) % 3 == 0:
                    g[r][c] = palette[(r + c) % len(palette)]
        return g
    if name == "marker_row_empty":
        # marked row has no payload → output is all-zero row, no information transmitted
        g[2][0] = 6
        for r in [0, 1, 3, 4, 5]:
            for c in [2, 5]:
                g[r][c] = palette[(r + c) % len(palette)]
        return g
    return g
