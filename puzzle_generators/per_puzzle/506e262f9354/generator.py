"""Generator for puzzle db3e9e38.

Rule: vertical column of 7s "explodes" into an upward triangle of
alternating 7/8 by Chebyshev distance from each cell to the bottom of
the column.

Combinatorial axes (8): grid_h/w, n_sevens, column_position,
bottom_row_position, decoy_palette_size, decoy_density,
column_clearance, vertical_padding.
Degenerates: single_seven, full_column, no_sevens.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "506e262f9354"
VERSION = "1.1.0"
TASK_ID = "506e262f9354"
SUMMARY = "Column of 7s; rule expands them upward into alternating 7/8 triangle."

INVARIANTS = [
    "background is 0",
    "all non-bg cells are 7 and form a single vertical column",
    "column has >=2 cells",
    "triangle (half-width = rbot) fits horizontally in the grid",
    "rows above top_row of triangle are bg in input",
]

COLUMN_POSITIONS = ("center", "left", "right", "random")
DEGENERATE_TEXTURES = ("single_seven", "full_column", "no_sevens")
HELPFUL_TEXTURES = COLUMN_POSITIONS

AXES = {
    "grid_h":             {"type": "int", "default": "rng 8..14", "valid": "5..18"},
    "grid_w":             {"type": "int", "default": "rng 10..16", "valid": "7..22"},
    "n_sevens":           {"type": "int", "default": "rng 2..4",  "valid": "2..6"},
    "column_position":    {"type": "str", "default": "rng helpful",
                           "valid": "|".join(COLUMN_POSITIONS)},
    "bottom_row_offset":  {"type": "int", "default": "rng 2..max", "valid": "2..h-1"},
    "decoy_palette_size": {"type": "int", "default": "rng 0..2", "valid": "0..4"},
    "decoy_density":      {"type": "float", "default": "rng 0..0.03",
                           "valid": "0..0.1"},
    "vertical_padding":   {"type": "int", "default": "rng 0..2", "valid": "0..4"},
    "texture":            {"type": "str", "default": "alias for column_position",
                           "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi, w_lo, w_hi, n_lo, n_hi = 6, 8, 8, 11, 2, 2
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi, n_lo, n_hi = 12, 16, 14, 22, 3, 5
    else:
        h_lo, h_hi, w_lo, w_hi, n_lo, n_hi = 8, 14, 10, 16, 2, 4
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    n_sevens = int(overrides.get("n_sevens",
                                 ctx.draw_int("n_sevens", n_lo, n_hi)))
    n_sevens = max(2, min(6, n_sevens))
    pos_kind = (overrides.get("texture") or overrides.get("column_position")
                or ctx.draw_choice("column_position", list(COLUMN_POSITIONS)))
    n_decoy = int(overrides.get("decoy_palette_size",
                                ctx.draw_int("decoy_palette_size", 0, 2)))
    decoy_d = float(overrides.get("decoy_density",
                                  ctx.draw_rng("decoy_density").uniform(0.0, 0.03)))
    max_rbot = min(h - 1, (w - 1) // 2)
    if max_rbot < 2:
        return _draw_from_degenerate("single_seven", h, w, rng)
    bottom_row = max(2, min(max_rbot, n_sevens))
    bottom_row = rng.randint(bottom_row, max_rbot)
    top_row = max(0, bottom_row - n_sevens + 1)
    col_lo = bottom_row
    col_hi = w - 1 - bottom_row
    if col_hi < col_lo:
        col = w // 2
    elif pos_kind == "center":
        col = (col_lo + col_hi) // 2
    elif pos_kind == "left":
        col = col_lo
    elif pos_kind == "right":
        col = col_hi
    else:
        col = rng.randint(col_lo, col_hi)
    g = full_grid(h, w, 0)
    for r in range(top_row, bottom_row + 1):
        g[r][col] = 7
    decoy_pool = [c for c in range(1, 10) if c not in (0, 7, 8)]
    rng.shuffle(decoy_pool)
    decoy_palette = decoy_pool[:max(0, n_decoy)]
    if decoy_palette and decoy_d > 0:
        # Place decoys far from the triangle (below the column or off to the
        # side beyond bbox_extent).
        for r in range(bottom_row + 1, h):
            for c in range(w):
                if rng.random() < decoy_d:
                    g[r][c] = rng.choice(decoy_palette)
    return g


def _draw_from_degenerate(name, h, w, rng):
    g = full_grid(h, w, 0)
    if name == "single_seven":
        g[h // 2][w // 2] = 7
        return g
    if name == "full_column":
        col = w // 2
        for r in range(h):
            g[r][col] = 7
        return g
    if name == "no_sevens":
        return g
    return g
