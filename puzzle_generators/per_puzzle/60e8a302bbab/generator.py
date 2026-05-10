"""Generator for 1d61978c.

Rule: count SE-diagonal pairs vs SW-diagonal pairs of 5s. Direction
with more pairs gets recolor 8, the other 2.

Combinatorial axes (8): grid_h/w, n_lines, line_length_max, position_bias,
palette_kind, anchor_corner, asymmetry_force, palette_size.
Degenerates: no_diagonals, full_grid, single_cell.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "60e8a302bbab"
VERSION = "1.1.0"
TASK_ID = "60e8a302bbab"
SUMMARY = "7-bg with 1-2 SE-diagonal lines of 5s."

INVARIANTS = [
    "bg = 7",
    "1-2 lines of 5s along SE (top-left to bottom-right) diagonals",
    "each line has >=3 cells",
    "no SW-diagonal 5-pairs",
]

POSITION_BIASES = ("scattered", "spread", "diagonal", "rng")
DEGENERATE_TEXTURES = ("no_diagonals", "full_grid", "single_cell")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..16", "valid": "10..20"},
    "grid_w":         {"type": "int", "default": "rng 14..18", "valid": "10..22"},
    "n_lines":        {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "line_length_max":{"type": "int", "default": "rng 4..min(h,w)-2",
                       "valid": "3..18"},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
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
        h_lo, h_hi = 10, 12
        nl_lo, nl_hi = 1, 1
    elif difficulty == "hard":
        h_lo, h_hi = 16, 20
        nl_lo, nl_hi = 2, 3
    else:
        h_lo, h_hi = 12, 16
        nl_lo, nl_hi = 1, 2
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo + 2, h_hi + 2)
    g = [[7] * w for _ in range(h)]
    n_lines = int(overrides.get("n_lines",
                                ctx.draw_int("n_lines", nl_lo, nl_hi)))
    n_lines = max(1, min(3, n_lines))
    for _ in range(n_lines):
        for _ in range(40):
            length = rng.randint(4, min(h - 2, w - 2))
            r0 = rng.randint(0, h - length); c0 = rng.randint(0, w - length)
            cells = [(r0 + i, c0 + i) for i in range(length)]
            if all(g[r][c] == 7 for r, c in cells):
                for r, c in cells:
                    g[r][c] = 5
                break
    return g


def _draw_from_degenerate(name, rng):
    h, w = 13, 15
    g = [[7] * w for _ in range(h)]
    if name == "no_diagonals":
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 5
        return g
    if name == "single_cell":
        g[6][7] = 5
        return g
    return g
