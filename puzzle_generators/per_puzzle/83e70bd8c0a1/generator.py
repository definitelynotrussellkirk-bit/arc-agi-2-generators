"""Generator for arc_puzzle_bank_21_set5_e:easy_e04.

Rule: reflect the square grid across the anti-diagonal.

Combinatorial axes (8): grid_h/w, size, marks, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias.
Degenerates: empty_grid, single_mark, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "83e70bd8c0a1"
VERSION = "1.1.0"
TASK_ID = "83e70bd8c0a1"

SUMMARY = "Reflect square grid across the anti-diagonal."

INVARIANTS = [
    "background is 0",
    "grid is square",
    "colored cells are sparse",
    "at least one cell is not fixed by the anti-diagonal reflection",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("empty_grid", "single_mark", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "5..7"},
    "grid_w":         {"type": "int", "default": "rng 5..7", "valid": "5..7"},
    "size":           {"type": "int", "default": "rng 5..7", "valid": "5..7"},
    "marks":          {"type": "int", "default": "rng 4..7", "valid": "4..7"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "varied", "valid": "varied"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        n = ctx.draw_int("size", 5, 5)
    elif difficulty == "hard":
        n = ctx.draw_int("size", 7, 7)
    else:
        n = ctx.draw_int("size", 5, 7)
    marks = ctx.draw_int("marks", 4, min(7, n * n // 2))
    g = full_grid(n, n, 0)
    colors = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    cells = [(r, c) for r in range(n) for c in range(n) if r + c != n - 1]
    for r, c in rng.sample(cells, marks):
        g[r][c] = rng.choice(colors)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(6, 6, 0)
    if name == "empty_grid":
        return g
    if name == "single_mark":
        g[1][2] = 3
        return g
    if name == "full_grid":
        for r in range(6):
            for c in range(6):
                g[r][c] = 3
        return g
    return g
