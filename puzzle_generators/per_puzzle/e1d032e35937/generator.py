"""Generator for arc_puzzle_bank_21_set8_s:S8_E3.

Rule: cells on the left of a full color-8 vertical bar are mirrored
to the right side.

Combinatorial axes (8): grid_h, grid_w, palette_kind, source_count,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_divider, source_on_right, already_mirrored.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e1d032e35937"
VERSION = "1.1.0"
TASK_ID = "e1d032e35937"
SUMMARY = "Cells on the left of a full color-8 vertical bar are mirrored to the right."

INVARIANTS = [
    "background is 0",
    "there is exactly one full-height color-8 divider",
    "all source cells are left of the divider",
    "mirrored destinations on the right are blank and in bounds",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_divider", "source_on_right", "already_mirrored")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 7..10", "valid": "5..14"},
    "grid_w":         {"type": "int", "default": "rng odd 9..13", "valid": "7..17"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "source_count":   {"type": "int", "default": "rng 3..6", "valid": "1..12"},
    "palette_size":   {"type": "int", "default": "rng 2..6", "valid": "1..6"},
    "position_bias":  {"type": "str", "default": "left_of_divider",
                       "valid": "left_of_divider"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..6", "valid": "1..6"},
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
        h = ctx.draw_int("grid_h", 7, 8)
        w = ctx.draw_int("grid_w", 9, 9)
        count = ctx.draw_int("source_count", 2, 4)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 13)
        count = ctx.draw_int("source_count", 5, 6)
    else:
        h = ctx.draw_int("grid_h", 7, 10)
        w = ctx.draw_int("grid_w", 9, 13)
        count = ctx.draw_int("source_count", 3, 6)
    if w % 2 == 0:
        w += 1
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    b = w // 2
    for r in range(h):
        g[r][b] = 8
    palette = [2, 3, 4, 6, 7, 9]
    for idx, (r, c) in enumerate(rng.sample([(r, c) for r in range(h) for c in range(b)], count)):
        g[r][c] = palette[idx % len(palette)]
    return g


def _draw_from_degenerate(name, rng):
    h, w = 8, 11
    g = full_grid(h, w, 0)
    b = w // 2
    if name == "no_divider":
        # no full-height 8-col → mirror axis undefined
        g[1][1] = 3; g[3][2] = 7; g[5][3] = 4
        return g
    for r in range(h):
        g[r][b] = 8
    if name == "source_on_right":
        # all sources placed right of divider → no left-side cells to mirror
        g[1][b + 2] = 3; g[3][b + 3] = 7; g[5][b + 1] = 4
        return g
    if name == "already_mirrored":
        # left and right are already mirror-symmetric → rule no-op
        for r, c in [(1, 1), (1, w - 2), (3, 2), (3, w - 3)]:
            g[r][c] = 3
        return g
    return g
