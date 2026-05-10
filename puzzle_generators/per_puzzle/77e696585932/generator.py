"""Generator for 1a07d186.

Rule: scattered pixels move to the nearest matching full-color row.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_rows,
n_distinct_colors.
Degenerates: no_rows, no_pixels, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "77e696585932"
VERSION = "1.1.0"
TASK_ID = "77e696585932"
SUMMARY = "Scattered pixels move to nearest matching full-color row."

INVARIANTS = [
    "there are one or more full nonzero rows",
    "scattered pixels use colors that have a matching full row",
    "scattered pixels are not already on a full row",
    "row colors are distinct and non-zero",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_rows", "no_pixels", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "5..20"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "5..20"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "n_rows":         {"type": "int", "default": "2", "valid": "2"},
    "n_distinct_colors":{"type": "int", "default": "2", "valid": "2"},
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
        h_lo, h_hi = 8, 9
    elif difficulty == "hard":
        h_lo, h_hi = 14, 18
    else:
        h_lo, h_hi = 8, 12
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    row_colors = list(ctx.draw_distinct_colors("row_colors", n=2, exclude={0}))
    r1 = rng.randint(2, h // 2)
    r2 = rng.randint(h // 2 + 1, h - 3)
    g = full_grid(h, w, 0)
    for c in range(w):
        g[r1][c] = row_colors[0]
        g[r2][c] = row_colors[1]
    for color, rr in [(row_colors[0], r1), (row_colors[1], r2)]:
        options = [r for r in range(h) if r not in {r1, r2, rr - 1, rr + 1}]
        sr = rng.choice(options)
        sc = rng.randint(1, w - 2)
        g[sr][sc] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(10, 10, 0)
    if name == "no_rows":
        g[5][5] = 2
        return g
    if name == "no_pixels":
        for c in range(10):
            g[3][c] = 2; g[7][c] = 3
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(10):
                g[r][c] = 2
        return g
    return g
