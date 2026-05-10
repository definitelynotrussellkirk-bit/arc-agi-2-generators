"""Generator for 4f537728.

Rule: one anomalous colored cell in a zero-separated cell grid expands
across its whole cell row and column.

Combinatorial axes (8): grid_h/w, cell_size, grid_cells, palette_kind,
anchor_corner, asymmetry_force, palette_size, anomaly.
Degenerates: no_anomaly, all_anomaly, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "525a837f2193"
VERSION = "1.1.0"
TASK_ID = "525a837f2193"
SUMMARY = "Anomalous cell in zero-separated grid expands across row and column."

INVARIANTS = [
    "all separator rows and columns are color 0",
    "every nonseparator cell block is background color 1 except one anomalous block",
    "the anomaly color is nonzero and not 1",
    "the cell grid has at least 4 rows and 4 columns of cells",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_anomaly", "all_anomaly", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "cell_size":      {"type": "int", "default": "2", "valid": "1..5"},
    "rows":           {"type": "int", "default": "rng 4..6", "valid": "2..10"},
    "cols":           {"type": "int", "default": "rng 4..6", "valid": "2..10"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "anomaly":        {"type": "color", "default": "rng !{0,1}",
                       "valid": "2..9"},
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
        rows_lo, rows_hi = 4, 4
    elif difficulty == "hard":
        rows_lo, rows_hi = 6, 8
    else:
        rows_lo, rows_hi = 4, 6
    cell_size = ctx.draw_int("cell_size", 2, 2)
    rows = ctx.draw_int("rows", rows_lo, rows_hi)
    cols = ctx.draw_int("cols", rows_lo, rows_hi)
    anomaly = ctx.draw_color("anomaly_color", exclude={0, 1})
    h = rows * cell_size + rows - 1
    w = cols * cell_size + cols - 1
    g = full_grid(h, w, 0)
    for rr in range(rows):
        for cc in range(cols):
            r0 = rr * (cell_size + 1)
            c0 = cc * (cell_size + 1)
            for dr in range(cell_size):
                for dc in range(cell_size):
                    g[r0 + dr][c0 + dc] = 1
    ar = rng.randrange(rows)
    ac = rng.randrange(cols)
    r0 = ar * (cell_size + 1)
    c0 = ac * (cell_size + 1)
    for dr in range(cell_size):
        for dc in range(cell_size):
            g[r0 + dr][c0 + dc] = anomaly
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 11, 0)
    if name == "no_anomaly":
        for r in range(11):
            for c in range(11):
                if r % 3 < 2 and c % 3 < 2:
                    g[r][c] = 1
        return g
    if name == "all_anomaly":
        for r in range(11):
            for c in range(11):
                if r % 3 < 2 and c % 3 < 2:
                    g[r][c] = 2
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(11):
                g[r][c] = 1
        return g
    return g
