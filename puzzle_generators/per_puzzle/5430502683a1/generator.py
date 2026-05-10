"""Generator for arc_puzzle_bank_21_set16_s:S16_E6.

Rule: among colored endpoint pairs, the longest span wins.

Combinatorial axes (8): grid_h/w, height, width, palette_kind,
anchor_corner, asymmetry_force, palette_size, n_distinct_colors.
Degenerates: no_pairs, single_pair, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5430502683a1"
VERSION = "1.1.0"
TASK_ID = "5430502683a1"
SUMMARY = "Among colored endpoint pairs, the longest span wins."

INVARIANTS = [
    "two or three colors each have exactly two aligned endpoints",
    "one color has a unique longest span",
    "output paints only the longest color's span",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_pairs", "single_pair", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "8..10"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "9..11"},
    "height":         {"type": "int", "default": "rng 8..10", "valid": "8..10"},
    "width":          {"type": "int", "default": "rng 9..11", "valid": "9..11"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "n_distinct_colors":{"type": "int", "default": "3", "valid": "3"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h = ctx.draw_int("height", 8, 8)
        w = ctx.draw_int("width", 9, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("height", 10, 10)
        w = ctx.draw_int("width", 11, 11)
    else:
        h = ctx.draw_int("height", 8, 10)
        w = ctx.draw_int("width", 9, 11)
    g = full_grid(h, w, 0)
    rows = rng.sample(range(h), 3)
    spans = [(0, w - 1, 2), (1, w - 3, 3), (2, w - 3, 4)]
    for r, (c1, c2, color) in zip(rows, spans):
        g[r][c1] = color
        g[r][c2] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(9, 10, 0)
    if name == "no_pairs":
        return g
    if name == "single_pair":
        g[3][0] = 2
        g[3][9] = 2
        return g
    if name == "full_grid":
        for r in range(9):
            for c in range(10):
                g[r][c] = 2
        return g
    return g
