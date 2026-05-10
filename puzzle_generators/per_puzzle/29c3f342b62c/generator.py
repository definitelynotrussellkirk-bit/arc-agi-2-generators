"""Generator for arc_additional_puzzles_21_set14_bundle:E95.

Rule: find full-height col of 5s. For each non-{0,5} cell at (r, c) on
the left, set (r, 2*guide-c) on the right to that color.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_cells,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_divider, source_on_right, source_on_divider.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "29c3f342b62c"
VERSION = "1.1.0"
TASK_ID = "29c3f342b62c"
SUMMARY = "Full-height 5-col divider in middle; left side has scattered non-5 cells."

INVARIANTS = [
    "exactly 1 full-height col of 5s",
    "left side has 2-3 isolated non-{0,5} cells",
    "right side empty",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_divider", "source_on_right", "source_on_divider")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 4..6", "valid": "3..10"},
    "grid_w":         {"type": "int", "default": "9", "valid": "9"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_cells":        {"type": "int", "default": "rng 2..3", "valid": "1..6"},
    "palette_size":   {"type": "int", "default": "rng 2..8", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "left_of_divider",
                       "valid": "left_of_divider"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..8", "valid": "1..8"},
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
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 5, 6)
    else:
        h = ctx.draw_int("grid_h", 4, 6)
    w = 9
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    gc = 4
    for r in range(h):
        g[r][gc] = 5
    palette = [1, 2, 3, 4, 6, 7, 8, 9]
    for _ in range(rng.randint(2, 3)):
        for _ in range(20):
            r = rng.randint(0, h - 1); c = rng.randint(0, gc - 1)
            if g[r][c] == 0:
                g[r][c] = rng.choice(palette)
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 5, 9
    g = full_grid(h, w, 0)
    if name == "no_divider":
        # no full-height 5-col → mirror axis is undefined
        g[1][1] = 3; g[3][2] = 7
        return g
    gc = 4
    for r in range(h):
        g[r][gc] = 5
    if name == "source_on_right":
        # all source cells already on the right → rule's "left source" assumption violated
        g[1][6] = 3; g[3][7] = 7
        return g
    if name == "source_on_divider":
        # source overlaps the divider column → ambiguous which side it belongs to
        g[1][gc] = 3
        g[3][1] = 7
        return g
    return g
