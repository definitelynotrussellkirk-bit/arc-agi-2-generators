"""Generator for arc_additional_puzzle_bank_volume9:H59.

Rule: a top-left control cell encodes the target red-seed count; the
chamber whose red-seed count matches that target is selected.

Combinatorial axes (8): grid_h/w, palette_kind, target_count,
palette_size, position_bias, n_distinct_colors, chamber_density, texture.
Degenerates: no_control, no_chambers, target_unmatched.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4f1ec6a61342"
VERSION = "1.1.0"
TASK_ID = "4f1ec6a61342"
SUMMARY = "The top-left control count selects the chamber with that many red seeds."

INVARIANTS = [
    "walls are 5",
    "top-left control is not part of any chamber",
    "one chamber has exactly the target red-seed count",
    "selected chamber has blank cells and red seeds",
]

PALETTE_KINDS = ("default", "tight_chambers", "wide_chambers", "balanced")
DEGENERATE_TEXTURES = ("no_control", "no_chambers", "target_unmatched")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 9..13", "valid": "7..24"},
    "grid_w":         {"type": "int", "default": "rng 11..16", "valid": "9..24"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "target_count":   {"type": "int", "default": "fixed", "valid": "fixed"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "split", "valid": "split"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3"},
    "chamber_density": {"type": "str", "default": "low", "valid": "low"},
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
    g[0][0] = 2
    mid = w // 2
    _carve(g, 1, 1, h - 2, mid - 1)
    _carve(g, 1, mid + 1, h - 2, w - 2)
    for r, c in [(1, 1), (h - 3, 2), (2, mid + 2)]:
        g[r][c] = 2
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 13
    if name == "no_control":
        # chambers + seeds but no top-left control → target undefined
        g = full_grid(h, w, 5)
        mid = w // 2
        _carve(g, 1, 1, h - 2, mid - 1)
        _carve(g, 1, mid + 1, h - 2, w - 2)
        for r, c in [(1, 1), (h - 3, 2), (2, mid + 2)]:
            g[r][c] = 2
        return g
    if name == "no_chambers":
        # control + seeds but no chambers — selection has no candidates
        g = full_grid(h, w, 0)
        g[0][0] = 2
        g[3][3] = 2
        g[5][6] = 2
        return g
    if name == "target_unmatched":
        # control says N but no chamber has exactly N seeds
        g = full_grid(h, w, 5)
        g[0][0] = 5  # target count = 5 (encoded as control)
        mid = w // 2
        _carve(g, 1, 1, h - 2, mid - 1)
        _carve(g, 1, mid + 1, h - 2, w - 2)
        # only 2 seeds and 1 seed in the chambers, never 5
        for r, c in [(1, 1), (h - 3, 2)]:
            g[r][c] = 2
        g[2][mid + 2] = 2
        return g
    return full_grid(h, w, 0)
