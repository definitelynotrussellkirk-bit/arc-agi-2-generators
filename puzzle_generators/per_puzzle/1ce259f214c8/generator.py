"""Generator for 14b:m98 — boolean xor of two halves.

Rule: a vertical 5-line splits the grid into left and right halves
of equal width. Output is the half-width grid where cells are 8 iff
exactly one half has non-bg in that row-position (XOR).

Combinatorial axes (8): grid_h, half_w, palette_kind, density,
palette_size, position_bias, n_distinct_colors, texture.
Degenerates: no_separator, identical_halves, empty_halves.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "1ce259f214c8"
VERSION = "1.1.0"
TASK_ID = "1ce259f214c8"
SUMMARY = "Two equal-width halves separated by a vertical 5-divider; XOR of their non-bg masks."

INVARIANTS = [
    "background is 0",
    "exactly one full-height column of 5s separates the grid into two equal-width halves",
    "left half has only color-A non-bg cells; right half has only color-B non-bg cells",
    "the XOR of their masks has at least 1 hit",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_separator", "identical_halves", "empty_halves")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..9"},
    "half_w":         {"type": "int", "default": "rng 4..6", "valid": "3..8"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "density":        {"type": "str", "default": "0.3", "valid": "0.2..0.5"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "vertical_5_split",
                       "valid": "vertical_5_split"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
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
        h = ctx.draw_int("grid_h", 5, 5)
        half = ctx.draw_int("half_w", 4, 4)
    elif difficulty == "hard":
        h = ctx.draw_int("grid_h", 7, 9)
        half = ctx.draw_int("half_w", 6, 8)
    else:
        h = ctx.draw_int("grid_h", 5, 7)
        half = ctx.draw_int("half_w", 4, 6)
    rng = ctx.draw_rng("layout")
    w = half * 2 + 1
    g = full_grid(h, w, 0)
    for r in range(h):
        g[r][half] = 5
    palette = rng.sample([1, 2, 3, 4, 6, 7, 9], 2)
    a, b = palette
    while True:
        for r in range(h):
            for c in range(half):
                g[r][c] = a if rng.random() < 0.30 else 0
            for c in range(half + 1, w):
                g[r][c] = b if rng.random() < 0.30 else 0
        xor = False
        for r in range(h):
            for c in range(half):
                la = g[r][c] != 0
                rb = g[r][c + half + 1] != 0
                if la ^ rb: xor = True; break
            if xor: break
        if xor: break
    return g


def _draw_from_degenerate(name, rng):
    h, half = 5, 4
    w = half * 2 + 1
    g = full_grid(h, w, 0)
    if name == "no_separator":
        # Two halves with content but no 5-divider — rule has no
        # fold axis to identify the halves.
        g[1][1] = 4; g[2][2] = 4
        g[1][6] = 6; g[3][7] = 6
        return g
    if name == "identical_halves":
        # Both halves have content at exactly the same positions —
        # the XOR everywhere is 0, so the rule produces an empty output.
        for r in range(h):
            g[r][half] = 5
        for r, c in [(1, 1), (2, 2), (3, 0)]:
            g[r][c] = 4
            g[r][c + half + 1] = 6
        return g
    if name == "empty_halves":
        # Separator present but both halves are empty — XOR has no hits.
        for r in range(h):
            g[r][half] = 5
        return g
    return g
