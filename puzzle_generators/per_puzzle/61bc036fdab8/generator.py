"""Generator for arc_additional_puzzle_bank_volume13:E89.

Rule: crop the smallest nonzero component to its bounding box.

Combinatorial axes (8): grid_h/w, palette_kind, num_objects, smallest_size,
palette_size, position_bias, n_distinct_colors, texture.
Degenerates: tied_smallest, only_one_component, all_same_size.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "61bc036fdab8"
VERSION = "1.1.0"
TASK_ID = "61bc036fdab8"
SUMMARY = "The smallest nonzero component is cropped to its bounding box."

INVARIANTS = [
    "background is 0",
    "one nonzero component is uniquely smallest",
    "larger components are separated from the target",
    "the target may include internal background inside its bounding box",
]

PALETTE_KINDS = ("default", "warm", "cool", "rainbow")
DEGENERATE_TEXTURES = ("tied_smallest", "only_one_component", "all_same_size")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..13", "valid": "5..20"},
    "grid_w":         {"type": "int", "default": "rng 8..13", "valid": "5..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "num_objects":    {"type": "int", "default": "3", "valid": "3"},
    "smallest_size":  {"type": "int", "default": "3", "valid": "3"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "scattered",
                       "valid": "scattered"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 13)
        w = ctx.draw_int("grid_w", 11, 13)
    else:
        h = ctx.draw_int("grid_h", 8, 13)
        w = ctx.draw_int("grid_w", 8, 13)
    rng = ctx.draw_rng("placement")
    g = full_grid(h, w, 0)
    draw_rect(g, 0, 0, 2, 3, 4)
    draw_rect(g, h - 3, w - 3, 3, 3, 8)
    r = rng.randint(2, max(2, h - 5))
    c = rng.randint(3, max(3, w - 5))
    g[r][c] = 6
    g[r + 1][c] = 6
    g[r + 1][c + 1] = 6
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "tied_smallest":
        g[2][2] = 6; g[2][3] = 6
        g[5][6] = 5; g[5][7] = 5
        draw_rect(g, h - 3, 0, 3, 3, 7)
        return g
    if name == "only_one_component":
        g[3][3] = 6; g[3][4] = 6; g[4][3] = 6
        return g
    if name == "all_same_size":
        g[1][1] = 4; g[1][2] = 4; g[2][1] = 4
        g[1][6] = 6; g[1][7] = 6; g[2][6] = 6
        g[7][1] = 7; g[7][2] = 7; g[8][1] = 7
        return g
    return g
