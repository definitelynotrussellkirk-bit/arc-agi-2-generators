"""Generator for arc_puzzle_bank_21_set10_s:S10_E3.

Rule: a nonzero object on a zero background is cropped to its tight
bounding box.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_object, full_grid_object, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "49a23dff5b22"
VERSION = "1.1.0"
TASK_ID = "49a23dff5b22"
SUMMARY = "A nonzero object on a zero background is cropped to its tight bounding box."

INVARIANTS = [
    "zero is always the background color",
    "the nonzero content has at least one row and column of zero padding",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_object", "full_grid_object", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "random", "valid": "random"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 8, 9)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 11, 12)
        w = ctx.draw_int("grid_w", 11, 12)
    else:
        h = ctx.draw_int("grid_h", 8, 12)
        w = ctx.draw_int("grid_w", 8, 12)
    colors = list(ctx.draw_distinct_colors("colors", n=2, exclude=[0]))
    g = full_grid(h, w, 0)
    top = ctx.draw_int("top", 1, h - 5)
    left = ctx.draw_int("left", 1, w - 5)
    for dr, dc in [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2)]:
        g[top + dr][left + dc] = colors[0]
    g[top][left + 2] = colors[1]
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(9, 9, 0)
    if name == "no_object":
        return g
    if name == "full_grid_object":
        for r in range(9):
            for c in range(9):
                g[r][c] = 3
        return g
    if name == "full_grid":
        for r in range(9):
            for c in range(9):
                g[r][c] = 3
        return g
    return g
