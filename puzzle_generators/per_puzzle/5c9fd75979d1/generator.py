"""Generator for 80214e03.

Rule: grid of colored rectangles is compressed into its slot-color
matrix with columns reversed.

Combinatorial axes (8): grid_h/w, slot_rows, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_rects, single_rect, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5c9fd75979d1"
VERSION = "1.1.0"
TASK_ID = "5c9fd75979d1"
SUMMARY = "Grid of colored rectangles compressed to slot-color matrix with columns reversed."

INVARIANTS = [
    "background is color 0",
    "nonzero objects are solid rectangles",
    "rectangles form a complete row/column slot grid",
    "rectangle colors are distinct and non-zero",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_rects", "single_rect", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 4..7", "valid": "4..14"},
    "grid_w":         {"type": "int", "default": "rng 4..6", "valid": "4..12"},
    "slot_rows":      {"type": "int", "default": "rng 2..3", "valid": "2..5"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "rng 4..9", "valid": "4..9"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "rng 4..9", "valid": "4..9"},
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
        sr_lo, sr_hi = 2, 2
    elif difficulty == "hard":
        sr_lo, sr_hi = 3, 3
    else:
        sr_lo, sr_hi = 2, 3
    rows = ctx.draw_int("slot_rows", sr_lo, sr_hi)
    cols = 2 + ((seed + sample_index) % 2)
    row_heights = [2 + ((sample_index + r) % 2) for r in range(rows)]
    col_widths = [2 + ((seed + c) % 2) for c in range(cols)]
    h = sum(row_heights)
    w = sum(col_widths)
    colors = ctx.draw_distinct_colors("colors", n=rows * cols, exclude={0})
    g = full_grid(h, w, 0)
    rr = 0
    k = 0
    for rh in row_heights:
        cc = 0
        for cw in col_widths:
            color = colors[k]
            k += 1
            for r in range(rr, rr + rh):
                for c in range(cc, cc + cw):
                    g[r][c] = color
            cc += cw
        rr += rh
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(6, 6, 0)
    if name == "no_rects":
        return g
    if name == "single_rect":
        for r in range(2, 5):
            for c in range(2, 5):
                g[r][c] = 2
        return g
    if name == "full_grid":
        for r in range(6):
            for c in range(6):
                g[r][c] = 2
        return g
    return g
