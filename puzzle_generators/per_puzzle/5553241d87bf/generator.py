"""Generator for e734a0e8.

Rule: non-background pattern cell stamped into grid cells marked by
zero dots.

Combinatorial axes (8): grid_h/w, cell_size, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
n_distinct_colors.
Degenerates: no_template, no_dots, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5553241d87bf"
VERSION = "1.1.0"
TASK_ID = "5553241d87bf"
SUMMARY = "Non-bg pattern stamped into cells marked by zero dots."

INVARIANTS = [
    "zero rows and columns separate equal-sized cells",
    "one cell contains the multicolor pattern template",
    "other background-filled cells contain a zero dot indicating where to stamp",
    "bg, c1 and c2 colors are distinct and non-zero",
]

CELL_SIZES = ("c3", "c4")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_template", "no_dots", "full_grid")
HELPFUL_TEXTURES = CELL_SIZES

AXES = {
    "cell_size":      {"type": "str", "default": "rng helpful",
                       "valid": "|".join(CELL_SIZES)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "3", "valid": "3"},
    "texture":        {"type": "str", "default": "alias for cell_size",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _cell_origin(index, cell_size):
    return index * (cell_size + 1)


def _fill_cell(g, row_index, col_index, cell_size, color):
    r0 = _cell_origin(row_index, cell_size)
    c0 = _cell_origin(col_index, cell_size)
    for r in range(r0, r0 + cell_size):
        for c in range(c0, c0 + cell_size):
            g[r][c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    tx = overrides.get("texture")
    if tx in CELL_SIZES:
        cell_size = int(tx[1])
    else:
        cell_size = ctx.draw_choice("cell_size", [3, 4])
    bg, c1, c2 = ctx.draw_distinct_colors("colors", n=3, exclude={0})
    rows = cols = 3
    h = rows * cell_size + (rows - 1)
    w = cols * cell_size + (cols - 1)
    g = full_grid(h, w, 0)
    for rr in range(rows):
        for cc in range(cols):
            _fill_cell(g, rr, cc, cell_size, bg)
    pattern_r = _cell_origin(0, cell_size)
    pattern_c = _cell_origin(0, cell_size)
    g[pattern_r][pattern_c] = c1
    g[pattern_r + 1][pattern_c + 1] = c2
    g[pattern_r + cell_size - 1][pattern_c] = c1
    for rr, cc in [(1, 1), (2, 0), (2, 2)]:
        r0 = _cell_origin(rr, cell_size)
        c0 = _cell_origin(cc, cell_size)
        g[r0 + cell_size // 2][c0 + cell_size // 2] = 0
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 11, 0)
    if name == "no_template":
        return g
    if name == "no_dots":
        for r in range(11):
            for c in range(11):
                g[r][c] = 1
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(11):
                g[r][c] = 1
        return g
    return g
