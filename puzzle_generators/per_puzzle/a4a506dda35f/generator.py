"""Generator for arc_additional_puzzles_21_set19_bundle:E131 — Single-row tally of cells sorted by count desc.

Rule: count cells by color; sort by count desc, color asc on ties;
emit one cell per occurrence in a single row.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_colors,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: tied_counts, single_color, no_colors.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid
from puzzle_generators.helpers.palette import random_palette

GENERATOR_ID = "a4a506dda35f"
VERSION = "1.1.0"
TASK_ID = "a4a506dda35f"
SUMMARY = "Scattered single-cell markers in 3-4 colors with distinct counts."

INVARIANTS = [
    "≥3 distinct non-bg colors with distinct counts",
    "1..3 cells per color",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("tied_counts", "single_color", "no_colors")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 4..6", "valid": "3..10"},
    "grid_w":         {"type": "int", "default": "rng 7..10", "valid": "6..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_colors":       {"type": "int", "default": "rng 3..4", "valid": "2..5"},
    "palette_size":   {"type": "int", "default": "rng 3..4", "valid": "2..5"},
    "position_bias":  {"type": "str", "default": "scattered_distinct_count_colors",
                       "valid": "scattered_distinct_count_colors"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..4", "valid": "2..5"},
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
        w = ctx.draw_int("grid_w", 9, 10)
    else:
        h = ctx.draw_int("grid_h", 4, 6)
        w = ctx.draw_int("grid_w", 7, 10)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    n_colors = rng.randint(3, 4)
    palette = random_palette(rng, n_colors)
    counts = rng.sample([1, 2, 3, 4], n_colors)
    cells = [(r, c) for r in range(h) for c in range(w)]
    rng.shuffle(cells)
    idx = 0
    for color, cnt in zip(palette, counts):
        for _ in range(cnt):
            r, c = cells[idx]; idx += 1
            g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 5, 8
    g = full_grid(h, w, 0)
    if name == "tied_counts":
        # 3 colors all with count 2 → all tied, sort by color-asc tiebreak only
        g[0][0] = 4; g[0][1] = 4
        g[1][0] = 6; g[1][1] = 6
        g[2][0] = 3; g[2][1] = 3
        return g
    if name == "single_color":
        # only 1 color → trivial single-bar tally
        g[0][0] = 4; g[1][2] = 4; g[2][3] = 4; g[3][1] = 4
        return g
    if name == "no_colors":
        # blank → no cells to count
        return g
    return g
