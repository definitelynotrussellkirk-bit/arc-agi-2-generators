"""Generator for additional_bank:E4.

Rule: a colored motif left of a vertical 5-divider is mirrored to
the right.

Combinatorial axes (8): grid_h, grid_w, palette_kind, half_w,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_divider, source_on_right, source_on_divider.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import fill_box, full_grid

GENERATOR_ID = "55c08ab3ce73"
VERSION = "1.1.0"
TASK_ID = "55c08ab3ce73"
SUMMARY = "A colored motif left of a vertical 5-divider is mirrored to the right."

INVARIANTS = [
    "background is 0",
    "there is exactly one full-height divider column of color 5",
    "all non-divider motif cells are left of the divider",
    "the divider is far enough from the left edge to allow a right mirror",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_divider", "source_on_right", "source_on_divider")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..9", "valid": "4..16"},
    "half_w":         {"type": "int", "default": "rng 3..5", "valid": "3..8"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "motif_color":    {"type": "color", "default": "rng", "valid": "1..9 != 5"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "left_of_divider",
                       "valid": "left_of_divider"},
    "n_distinct_colors": {"type": "int", "default": "1", "valid": "1"},
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
        h = ctx.draw_int("grid_h", 5, 6)
        half_w = ctx.draw_int("half_w", 3, 3)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        half_w = ctx.draw_int("half_w", 4, 5)
    else:
        h = ctx.draw_int("grid_h", 5, 9)
        half_w = ctx.draw_int("half_w", 3, 5)
    color = ctx.draw_color("motif_color", exclude={0, 5})
    rng = ctx.draw_rng("motif")
    w = half_w * 2 + 1
    div = half_w
    g = full_grid(h, w, 0)
    fill_box(g, 0, div, h - 1, div, 5)
    cells = [(r, c) for r in range(h) for c in range(1, div)]
    rng.shuffle(cells)
    for r, c in cells[:rng.randint(3, min(6, len(cells)))]:
        g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 9
    g = full_grid(h, w, 0)
    if name == "no_divider":
        # no full-height 5-col → mirror axis is undefined
        g[1][1] = 3; g[3][2] = 3
        return g
    div = 4
    fill_box(g, 0, div, h - 1, div, 5)
    if name == "source_on_right":
        # all source cells already on the right → "left source" assumption violated
        g[1][6] = 3; g[3][7] = 3
        return g
    if name == "source_on_divider":
        # source overlaps the divider column → ambiguous which side it belongs to
        g[1][div] = 3
        g[3][1] = 3
        return g
    return g
