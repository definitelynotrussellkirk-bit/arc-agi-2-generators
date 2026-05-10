"""Generator for arc_additional_puzzle_bank_volume10:M67.

Rule: three blue objects of different sizes are recolored by size rank.

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_blue,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: tied_sizes, single_blue, no_blue.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "8118155d8959"
VERSION = "1.1.0"
TASK_ID = "8118155d8959"
SUMMARY = "Three blue objects of different sizes are recolored by size rank."

INVARIANTS = [
    "background is 0",
    "there are exactly three blue connected components",
    "blue components have distinct sizes",
    "components are separated by background",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("tied_sizes", "single_blue", "no_blue")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..13", "valid": "6..24"},
    "grid_w":         {"type": "int", "default": "rng 10..15", "valid": "6..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_blue":         {"type": "int", "default": "3", "valid": "1..5"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "scattered",
                       "valid": "scattered"},
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
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 10, 12)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 13, 15)
    else:
        h = ctx.draw_int("grid_h", 9, 13)
        w = ctx.draw_int("grid_w", 10, 15)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    top = rng.randint(0, max(0, h - 8))
    left = rng.randint(0, max(0, w - 10))
    shapes = [
        [(top, left)],
        [(top + 2, left + 3), (top + 2, left + 4), (top + 3, left + 3)],
        [(top + 5, left + 6), (top + 5, left + 7), (top + 5, left + 8),
         (top + 6, left + 6), (top + 6, left + 7), (top + 6, left + 8)],
    ]
    rng.shuffle(shapes)
    for shape in shapes:
        for r, c in shape:
            g[r][c] = 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 11, 12
    g = full_grid(h, w, 0)
    if name == "tied_sizes":
        # two blue components share a size → rank tie, recolor mapping ambiguous
        for r, c in [(1, 1), (2, 1)]: g[r][c] = 1
        for r, c in [(5, 5), (5, 6)]: g[r][c] = 1
        for r, c in [(8, 1), (8, 2), (9, 1)]: g[r][c] = 1
        return g
    if name == "single_blue":
        # one blue component → no comparison, rule trivially recolors that one
        for r, c in [(3, 3), (3, 4), (4, 3)]: g[r][c] = 1
        return g
    if name == "no_blue":
        # other-colored objects but no blue → rule has no targets
        for r, c in [(2, 2), (3, 2)]: g[r][c] = 4
        for r, c in [(6, 5), (6, 6)]: g[r][c] = 6
        return g
    return g
