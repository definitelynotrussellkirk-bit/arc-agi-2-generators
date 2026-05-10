"""Generator for arc_puzzle_bank_eighteenth_21_bundle:easy_120_complete_vertical_mirror.

Rule: copy each nonzero cell to its vertical mirror column.

Combinatorial axes (8): grid_h, grid_w, palette_kind, marks,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: empty_grid, on_axis_only, already_symmetric.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "099aeda5aa7b"
VERSION = "1.1.0"
TASK_ID = "099aeda5aa7b"
SUMMARY = "Copy each nonzero cell to its vertical mirror column."

INVARIANTS = [
    "background is 0",
    "input has sparse nonzero cells",
    "output keeps each source cell",
    "output adds the same color at the vertically mirrored column",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("empty_grid", "on_axis_only", "already_symmetric")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "4..14"},
    "grid_w":         {"type": "int", "default": "rng 9..12", "valid": "5..18"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "marks":          {"type": "int", "default": "rng 4..7", "valid": "1..20"},
    "palette_size":   {"type": "int", "default": "rng 1..9", "valid": "1..9"},
    "position_bias":  {"type": "str", "default": "left_half", "valid": "left_half"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..9", "valid": "1..9"},
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
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 10)
        marks = ctx.draw_int("marks", 3, 5)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 12)
        marks = ctx.draw_int("marks", 6, 7)
    else:
        h = ctx.draw_int("grid_h", 8, 10)
        w = ctx.draw_int("grid_w", 9, 12)
        marks = ctx.draw_int("marks", 4, 7)
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    left_cols = list(range(max(1, w // 2)))
    cells = [(r, c) for r in range(h) for c in left_cols if c != w - 1 - c]
    for r, c in rng.sample(cells, min(marks, len(cells))):
        g[r][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 11
    g = full_grid(h, w, 0)
    axis = w // 2
    if name == "empty_grid":
        # no cells to mirror — input equals output
        return g
    if name == "on_axis_only":
        # all sources on the vertical axis column → reflection is identity, no copy
        for r in [1, 3, 5, 7]:
            g[r][axis] = ((r % 7) + 1)
        return g
    if name == "already_symmetric":
        # input is already vertically symmetric → rule no-op, no visible change
        for r, c in [(1, 1), (1, w - 2), (3, 3), (3, w - 4), (5, 0), (5, w - 1)]:
            g[r][c] = 4
        return g
    return g
