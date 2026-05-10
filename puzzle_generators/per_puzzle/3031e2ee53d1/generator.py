"""Generator for 53b68214.

Rule: detect smallest period p such that row r matches row r+p; output
is w x w grid by tiling the period rows across the full width.

Combinatorial axes (8): width, period, h_factor, color, n_cells_per_row,
left_band_width, palette_kind, anchor_corner.
Degenerates: no_period, full_grid, single_cell.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "3031e2ee53d1"
VERSION = "1.1.0"
TASK_ID = "3031e2ee53d1"
SUMMARY = "Tall narrow grid with a p-row periodic pattern (p in {2,3,4})."

INVARIANTS = [
    "h is a multiple of p where p in {2,3,4}",
    "h <= w (output is w x w)",
    "row r and row r+p are identical for all valid r",
    "cells appear only in the left band of the grid",
]

PERIODS = (2, 3, 4)
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_period", "full_grid", "single_cell")
HELPFUL_TEXTURES = ("p2", "p3", "p4")

AXES = {
    "width":           {"type": "int", "default": "rng 8..12", "valid": "6..16"},
    "period":          {"type": "int", "default": "rng 2..4", "valid": "2..4"},
    "h_factor":        {"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "color":           {"type": "color", "default": "rng 1..9", "valid": "1..9"},
    "n_cells_per_row": {"type": "int", "default": "rng 1..3", "valid": "1..4"},
    "left_band_width": {"type": "str", "default": "rng",
                        "valid": "third|half|full"},
    "palette_kind":    {"type": "str", "default": "rng helpful",
                        "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":   {"type": "bool", "default": "false",
                        "valid": "true|false"},
    "texture":         {"type": "str", "default": "alias for period",
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
        w_lo, w_hi = 6, 8
        p_choices = [2]
        cells_lo, cells_hi = 1, 2
    elif difficulty == "hard":
        w_lo, w_hi = 12, 16
        p_choices = [3, 4]
        cells_lo, cells_hi = 2, 4
    else:
        w_lo, w_hi = 8, 12
        p_choices = [2, 3, 4]
        cells_lo, cells_hi = 1, 3
    if overrides.get("texture") in HELPFUL_TEXTURES:
        p = int(overrides["texture"][1])
    else:
        p = int(overrides.get("period", rng.choice(p_choices)))
    p = max(2, min(4, p))
    w = int(overrides.get("width", ctx.draw_int("width", w_lo, w_hi)))
    h_factor = int(overrides.get("h_factor",
                                 ctx.draw_int("h_factor", 2, 3)))
    h = p * h_factor
    if h > w:
        h = max(p * 2, (w // p) * p)
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    palette = _build_palette(palette_kind, rng)
    color = int(overrides.get("color", rng.choice(palette)))
    band_kind = overrides.get("left_band_width",
                              ctx.draw_choice("left_band_width",
                                              ["third", "half", "full"]))
    if band_kind == "full":
        band_w = w
    elif band_kind == "half":
        band_w = max(1, w // 2)
    else:
        band_w = max(1, w // 3)
    cells_per_row = int(overrides.get("n_cells_per_row",
                                      ctx.draw_int("n_cells_per_row",
                                                   cells_lo, cells_hi)))
    cells_per_row = max(1, min(4, cells_per_row))
    tile = [[0] * w for _ in range(p)]
    for r in range(p):
        for _ in range(cells_per_row):
            c = rng.randint(0, max(0, band_w - 1))
            tile[r][c] = color
    g = full_grid(h, w, 0)
    for r in range(h):
        for c in range(w):
            g[r][c] = tile[r % p][c]
    return g


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    h, w = 8, 10
    g = full_grid(h, w, 0)
    color = rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    if name == "no_period":
        for r in range(h):
            c = rng.randint(0, w // 3)
            g[r][c] = color
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = color
        return g
    if name == "single_cell":
        g[h // 2][w // 4] = color
        return g
    return g
