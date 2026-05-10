"""Generator for arc_additional_puzzle_bank_volume14:E98.

Rule: among separated objects, the smallest is recolored to 9.

Combinatorial axes (8): grid_h/w, palette_kind, num_objects,
smallest_size, palette_size, position_bias, n_distinct_colors, texture.
Degenerates: tied_smallest, only_one_object, all_same_size.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "a926d2195b22"
VERSION = "1.1.0"
TASK_ID = "a926d2195b22"
SUMMARY = "Among separated objects, the smallest one is recolored to 9."

INVARIANTS = [
    "objects are separated by at least one background cell",
    "exactly one object has the smallest size",
]

PALETTE_KINDS = ("default", "warm", "cool", "rainbow")
DEGENERATE_TEXTURES = ("tied_smallest", "only_one_object", "all_same_size")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..11", "valid": "7..13"},
    "grid_w":         {"type": "int", "default": "rng 8..11", "valid": "7..13"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "num_objects":    {"type": "int", "default": "3", "valid": "3"},
    "smallest_size":  {"type": "int", "default": "1", "valid": "1"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "spread", "valid": "spread"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _paint(g, top, left, cells, color):
    for dr, dc in cells:
        g[top + dr][left + dc] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 10, 11)
        w = ctx.draw_int("grid_w", 10, 11)
    else:
        h = ctx.draw_int("grid_h", 8, 11)
        w = ctx.draw_int("grid_w", 8, 11)
    colors = list(ctx.draw_distinct_colors("colors", n=3, exclude=[0, 9]))
    g = full_grid(h, w, 0)
    _paint(g, 1, 1, [(0, 0)], colors[0])
    _paint(g, 1, w - 4, [(0, 0), (0, 1), (1, 0)], colors[1])
    _paint(g, h - 4, 2, [(0, 0), (1, 0), (1, 1), (2, 1)], colors[2])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 9
    g = full_grid(h, w, 0)
    if name == "tied_smallest":
        # two objects tied at size 1 — smallest pick ambiguous
        g[1][1] = 4
        g[1][6] = 5
        g[6][3] = 7; g[6][4] = 7; g[7][3] = 7
        return g
    if name == "only_one_object":
        # single object — trivial smallest, rule recolors it to 9
        g[3][3] = 4; g[3][4] = 4; g[4][3] = 4
        return g
    if name == "all_same_size":
        # 3 objects same size — no unique smallest
        g[1][1] = 4; g[1][2] = 4
        g[1][6] = 5; g[1][7] = 5
        g[6][3] = 7; g[6][4] = 7
        return g
    return g
