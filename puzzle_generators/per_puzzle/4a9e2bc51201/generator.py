"""Generator for arc_additional_puzzles_21_set16_bundle:E110 — Reflect across vertical 5-divider.

Rule: find vertical 5-column. For each non-zero non-5 cell, paint a
copy at the mirror position (only if that position is empty).

Combinatorial axes (8): grid_h, grid_w, palette_kind, n_marks,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_divider, no_marks, already_symmetric.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4a9e2bc51201"
VERSION = "1.1.0"
TASK_ID = "4a9e2bc51201"
SUMMARY = "Vertical 5-column near center; non-zero cells distributed asymmetrically across the divider."

INVARIANTS = [
    "exactly one full-height column of 5s",
    "≥3 non-zero non-5 cells",
    "for each non-zero non-5 cell, the mirror position across the 5-axis is initially 0",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_divider", "no_marks", "already_symmetric")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 6..9", "valid": "5..11"},
    "grid_w":         {"type": "int", "default": "rng 7..9", "valid": "6..11"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "n_marks":        {"type": "int", "default": "rng 4..6", "valid": "3..10"},
    "palette_size":   {"type": "int", "default": "rng 2..6", "valid": "1..8"},
    "position_bias":  {"type": "str", "default": "vertical_5_divider_with_marks",
                       "valid": "vertical_5_divider_with_marks"},
    "n_distinct_colors": {"type": "int", "default": "rng 2..6", "valid": "1..8"},
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
        h = ctx.draw_int("grid_h", 6, 7)
        w = ctx.draw_int("grid_w", 7, 7)
        n_marks = ctx.draw_int("n_marks", 3, 4)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 8, 9)
        w = ctx.draw_int("grid_w", 9, 9)
        n_marks = ctx.draw_int("n_marks", 5, 6)
    else:
        h = ctx.draw_int("grid_h", 6, 9)
        w = ctx.draw_int("grid_w", 7, 9)
        n_marks = ctx.draw_int("n_marks", 4, 6)
    g = full_grid(h, w, 0)
    rng = ctx.draw_rng("layout")
    div = w // 2
    for r in range(h):
        g[r][div] = 5
    palette = [1, 2, 3, 4, 6, 7, 8, 9]
    placed = 0
    for _ in range(80):
        if placed >= n_marks:
            break
        r = rng.randint(0, h - 1); c = rng.randint(0, w - 1)
        if c == div or g[r][c] != 0:
            continue
        mc = 2 * div - c
        if 0 <= mc < w and g[r][mc] == 0:
            g[r][c] = rng.choice(palette)
            placed += 1
    return g


def _draw_from_degenerate(name, rng):
    h, w = 7, 9
    g = full_grid(h, w, 0)
    div = w // 2
    if name == "no_divider":
        # marks without 5-divider → no axis to mirror across
        g[2][2] = 4
        g[4][6] = 6
        return g
    if name == "no_marks":
        # divider alone → nothing to mirror
        for r in range(h):
            g[r][div] = 5
        return g
    if name == "already_symmetric":
        # marks already mirrored across divider → rule has no effect
        for r in range(h):
            g[r][div] = 5
        g[2][1] = 4; g[2][7] = 4
        g[4][2] = 6; g[4][6] = 6
        return g
    return g
