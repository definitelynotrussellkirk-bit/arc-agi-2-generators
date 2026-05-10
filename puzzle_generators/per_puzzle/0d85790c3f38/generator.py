"""Generator for arc_puzzle_bank_21_set4_d:easy_d06.

Rule: the right half of the grid is horizontally mirrored onto the left
half (overwriting the left).

Combinatorial axes (8): grid_h, half_w, palette_kind, mark_count,
palette_size, position_bias, n_distinct_colors, texture.
Degenerates: already_symmetric, left_half_filled, no_marks.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0d85790c3f38"
VERSION = "1.1.0"
TASK_ID = "0d85790c3f38"
SUMMARY = "The right half is horizontally mirrored onto the left half."

INVARIANTS = [
    "background is 0",
    "grid width is even",
    "source marks live in the right half",
    "the right half remains unchanged after mirroring",
]

PALETTE_KINDS = ("default", "sparse", "dense", "rainbow")
DEGENERATE_TEXTURES = ("already_symmetric", "left_half_filled", "no_marks")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..8", "valid": "3..14"},
    "half_w":         {"type": "int", "default": "rng 4..6", "valid": "2..10"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "mark_count":     {"type": "int", "default": "rng 4..7", "valid": "1..16"},
    "palette_size":   {"type": "int", "default": "9", "valid": "9"},
    "position_bias":  {"type": "str", "default": "right_half",
                       "valid": "right_half"},
    "n_distinct_colors": {"type": "int", "default": "rng 1..7",
                          "valid": "1..9"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("grid_h", 5, 6)
        half_w = ctx.draw_int("half_w", 4, 5)
        target_max = 5
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 8)
        half_w = ctx.draw_int("half_w", 5, 6)
        target_max = 7
    else:
        h = ctx.draw_int("grid_h", 5, 8)
        half_w = ctx.draw_int("half_w", 4, 6)
        target_max = 7
    mark_count = ctx.draw_int("mark_count", 4, min(target_max, h * half_w))
    rng = ctx.draw_rng("layout")
    g = full_grid(h, half_w * 2, 0)
    cells = rng.sample([(r, c) for r in range(h) for c in range(half_w, half_w * 2)], mark_count)
    for r, c in cells:
        g[r][c] = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    return g


def _draw_from_degenerate(name, rng):
    h, half_w = 6, 5
    w = 2 * half_w
    g = full_grid(h, w, 0)
    if name == "already_symmetric":
        # both halves already mirrored — rule output identical to input
        for r, c, v in [(1, 8, 4), (1, 1, 4), (3, 7, 7), (3, 2, 7)]:
            g[r][c] = v
        return g
    if name == "left_half_filled":
        # left half has its own marks — rule overwrites them silently
        for r, c, v in [(1, 1, 5), (3, 3, 6)]:
            g[r][c] = v
        for r, c, v in [(2, 7, 4), (4, 8, 7)]:
            g[r][c] = v
        return g
    if name == "no_marks":
        return g
    return g
