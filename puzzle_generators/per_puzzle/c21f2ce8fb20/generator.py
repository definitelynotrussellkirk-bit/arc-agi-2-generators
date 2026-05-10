"""Generator for arc_additional_puzzle_bank_volume19:H129.

Rule: the gray-wall chamber with the most red seeds is emitted as cyan
on a blank output.

Combinatorial axes (8): grid_h/w, palette_kind, n_chambers,
palette_size, position_bias, n_distinct_colors, seed_balance, texture.
Degenerates: no_walls, no_seeds, all_chambers_tied.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "c21f2ce8fb20"
VERSION = "1.1.0"
TASK_ID = "c21f2ce8fb20"
SUMMARY = "The gray-wall chamber with the most red seeds is emitted as cyan on blank output."

INVARIANTS = [
    "walls are 5",
    "passable chamber cells are 0 or 2",
    "one chamber has strictly more red seeds than the others",
    "selected chamber has non-seed blank cells too",
]

PALETTE_KINDS = ("default", "tight_chambers", "wide_chambers", "balanced")
DEGENERATE_TEXTURES = ("no_walls", "no_seeds", "all_chambers_tied")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..13", "valid": "7..24"},
    "grid_w":         {"type": "int", "default": "rng 11..16", "valid": "9..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_chambers":     {"type": "int", "default": "2", "valid": "2"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "split", "valid": "split"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2"},
    "seed_balance":   {"type": "str", "default": "unbalanced",
                       "valid": "unbalanced"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _carve(g, r0, c0, r1, c1):
    for r in range(r0, r1 + 1):
        for c in range(c0, c1 + 1):
            g[r][c] = 0


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 9, 10)
        w = ctx.draw_int("grid_w", 11, 13)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 12, 13)
        w = ctx.draw_int("grid_w", 14, 16)
    else:
        h = ctx.draw_int("grid_h", 9, 13)
        w = ctx.draw_int("grid_w", 11, 16)
    g = full_grid(h, w, 5)
    mid = w // 2
    _carve(g, 1, 1, h - 2, mid - 1)
    _carve(g, 1, mid + 1, h - 2, w - 2)
    for r, c in [(1, 1), (2, 2), (h - 3, 2), (2, mid + 2)]:
        g[r][c] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 13
    if name == "no_walls":
        # no 5-walls → one big "chamber" (max is trivially everything)
        g = full_grid(h, w, 0)
        g[2][2] = 2
        g[5][5] = 2
        g[3][8] = 2
        return g
    if name == "no_seeds":
        # walls + chambers but no seeds — argmax over zeros is undefined
        g = full_grid(h, w, 5)
        mid = w // 2
        _carve(g, 1, 1, h - 2, mid - 1)
        _carve(g, 1, mid + 1, h - 2, w - 2)
        return g
    if name == "all_chambers_tied":
        # both chambers have same seed count → no strict max → ambiguous
        g = full_grid(h, w, 5)
        mid = w // 2
        _carve(g, 1, 1, h - 2, mid - 1)
        _carve(g, 1, mid + 1, h - 2, w - 2)
        for r, c in [(1, 1), (2, 2)]:
            g[r][c] = 2
        for r, c in [(1, mid + 1), (2, mid + 2)]:
            g[r][c] = 2
        return g
    return full_grid(h, w, 0)
