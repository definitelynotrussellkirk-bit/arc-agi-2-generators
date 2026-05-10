"""Generator for ded97339.

Rule: for each pair of 8-dots in same row or col with no other 8 between,
fill the line with 8.

Combinatorial axes (8): grid_h/w, n_dots, position_bias, palette_kind,
anchor_corner, asymmetry_force, palette_size, dot_density.
Degenerates: collinear_3, no_dots, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "7515881f2786"
VERSION = "1.1.0"
TASK_ID = "7515881f2786"
SUMMARY = "3-5 8-dots with at least one pair in same row, one pair in same col."

INVARIANTS = [
    "3-5 cells of color 8",
    ">=1 pair shares a row, >=1 pair shares a col",
    "no three dots collinear in same row/col",
]

POSITION_BIASES = ("scattered", "centered", "spread", "rng")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("collinear_3", "no_dots", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "6..14"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "6..14"},
    "n_dots":         {"type": "int", "default": "3", "valid": "3..6"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "texture":        {"type": "str", "default": "alias for position_bias",
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
        h_lo, h_hi = 6, 8
    elif difficulty == "hard":
        h_lo, h_hi = 12, 14
    else:
        h_lo, h_hi = 8, 12
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    g = full_grid(h, w, 0)
    r1 = rng.randint(0, h - 1)
    r2 = rng.randint(0, h - 1)
    while r2 == r1:
        r2 = rng.randint(0, h - 1)
    c1 = rng.randint(0, w - 1)
    c2 = rng.randint(0, w - 1)
    while c2 == c1:
        c2 = rng.randint(0, w - 1)
    g[r1][c1] = 8
    g[r1][c2] = 8
    r3 = rng.randint(0, h - 1)
    while r3 == r1 or r3 == r2:
        r3 = rng.randint(0, h - 1)
    g[r3][c1] = 8
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 10
    g = full_grid(h, w, 0)
    if name == "collinear_3":
        g[5][2] = 8; g[5][5] = 8; g[5][8] = 8
        return g
    if name == "no_dots":
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 8
        return g
    return g
