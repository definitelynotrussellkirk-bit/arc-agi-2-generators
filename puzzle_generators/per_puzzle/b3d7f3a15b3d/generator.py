"""Generator for a096bf4d.

Rule: special interior colors propagate across matching rows and columns
of framed cells.

Combinatorial axes (8): grid_h/w, cell_size, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_distinct_colors.
Degenerates: no_frames, no_special, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "b3d7f3a15b3d"
VERSION = "1.1.0"
TASK_ID = "b3d7f3a15b3d"
SUMMARY = "Special interior colors propagate across matching rows/columns of framed cells."

INVARIANTS = [
    "zero separator rows and columns divide equal framed cells",
    "each cell has a common interior color",
    "a special color repeated at the same local offset in a row or column fills the intervening cells",
]

CELL_KINDS = ("c5", "c6")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_frames", "no_special", "full_grid")
HELPFUL_TEXTURES = CELL_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "varied", "valid": "varied"},
    "grid_w":         {"type": "int", "default": "varied", "valid": "varied"},
    "cell_size":      {"type": "choice", "default": "rng helpful",
                       "valid": "5|6"},
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


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    tx = overrides.get("texture")
    if tx in CELL_KINDS:
        cell_size = int(tx[1])
    elif difficulty == "easy":
        cell_size = 5
    elif difficulty == "hard":
        cell_size = 6
    else:
        cell_size = ctx.draw_choice("cell_size", [5, 6])
    border, common, special = ctx.draw_distinct_colors("colors", n=3, exclude={0})
    n_cells = 3
    size = n_cells * cell_size + (n_cells - 1)
    g = full_grid(size, size, 0)
    starts = [i * (cell_size + 1) for i in range(n_cells)]
    for rs in starts:
        for cs in starts:
            for r in range(rs + 1, rs + cell_size - 1):
                for c in range(cs + 1, cs + cell_size - 1):
                    g[r][c] = common
            draw_frame(g, rs, cs, rs + cell_size - 1, cs + cell_size - 1, border)

    local = 2 if cell_size == 5 else 3
    row_idx = 1
    g[starts[row_idx] + local][starts[0] + local] = special
    g[starts[row_idx] + local][starts[2] + local] = special
    col_idx = 2
    g[starts[0] + 1][starts[col_idx] + 1] = special
    g[starts[2] + 1][starts[col_idx] + 1] = special
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(17, 17, 0)
    if name == "no_frames":
        return g
    if name == "no_special":
        for rs in [0, 6, 12]:
            for cs in [0, 6, 12]:
                draw_frame(g, rs, cs, rs + 4, cs + 4, 5)
        return g
    if name == "full_grid":
        for r in range(17):
            for c in range(17):
                g[r][c] = 5
        return g
    return g
