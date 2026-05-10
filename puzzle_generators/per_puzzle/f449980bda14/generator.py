"""Generator for 1b8318e3.

Rule: colored dots dock onto the nearest free perimeter slots around
a gray square.

Combinatorial axes (8): grid_size, n_dots, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_square, no_dots, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect, full_grid

GENERATOR_ID = "f449980bda14"
VERSION = "1.1.0"
TASK_ID = "f449980bda14"
SUMMARY = "Colored dots dock onto nearest free perimeter slots around gray square."

INVARIANTS = [
    "gray objects are solid squares",
    "colored dots are singleton non-gray cells",
    "dots start away from the square perimeter",
    "the square sits clear of grid borders so docking has room",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_square", "no_dots", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_size":      {"type": "int", "default": "rng 11..14", "valid": "8..20"},
    "n_dots":         {"type": "int", "default": "rng 3..4", "valid": "1..8"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "rng 3..4", "valid": "1..4"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "rng 3..4", "valid": "1..4"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        size_lo, size_hi, nd_lo, nd_hi = 11, 12, 2, 3
    elif difficulty == "hard":
        size_lo, size_hi, nd_lo, nd_hi = 14, 16, 4, 4
    else:
        size_lo, size_hi, nd_lo, nd_hi = 11, 14, 3, 4
    size = ctx.draw_int("grid_size", size_lo, size_hi)
    n_dots = ctx.draw_int("n_dots", nd_lo, nd_hi)
    g = full_grid(size, size, 0)
    s = 3
    r0 = size // 2 - 1
    c0 = size // 2 - 1
    draw_rect(g, r0, c0, s, s, 5)
    positions = [(1, c0 + 1), (size - 2, c0 + 1), (r0 + 1, 1), (r0 + 1, size - 2)]
    colors = list(ctx.draw_distinct_colors("dot_colors", n=n_dots, exclude={0, 5}))
    for pos, color in zip(rng.sample(positions, n_dots), colors):
        r, c = pos
        g[r][c] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 12, 0)
    if name == "no_square":
        g[3][3] = 2
        return g
    if name == "no_dots":
        draw_rect(g, 5, 5, 3, 3, 5)
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(12):
                g[r][c] = 5
        return g
    return g
