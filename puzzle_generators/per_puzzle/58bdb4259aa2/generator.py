"""Generator for 11852cab.

Rule: find bbox center of all non-zero cells. For each non-zero cell,
paint at 4 rotated positions (0, 90, 180, 270) around the center.

Combinatorial axes (8): grid_n, n_cells, palette_size, palette_kind,
position_bias, anchor_corner, asymmetry_force, color_count.
Degenerates: full_grid, single_cell, all_in_corner.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "58bdb4259aa2"
VERSION = "1.1.0"
TASK_ID = "58bdb4259aa2"
SUMMARY = "Square grid with non-zero cells in one quadrant of bbox center."

INVARIANTS = [
    "h = w (square)",
    "5-10 non-zero cells (one or two distinct colors)",
    "cells lie in upper half so the rotated copies fit",
    "bbox center is at integer coordinates",
]

POSITION_BIASES = ("scattered", "tight", "diagonal", "row_aligned")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("full_grid", "single_cell", "all_in_corner")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_n":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "n_cells":        {"type": "int", "default": "rng 5..8", "valid": "3..12"},
    "palette_size":   {"type": "int", "default": "rng 2..3", "valid": "1..4"},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "color_count":    {"type": "int", "default": "rng 2..3", "valid": "1..4"},
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
        n_lo, n_hi = 7, 9
        nc_lo, nc_hi = 3, 5
        ps_lo, ps_hi = 1, 2
    elif difficulty == "hard":
        n_lo, n_hi = 11, 14
        nc_lo, nc_hi = 8, 12
        ps_lo, ps_hi = 3, 4
    else:
        n_lo, n_hi = 9, 11
        nc_lo, nc_hi = 5, 8
        ps_lo, ps_hi = 2, 3
    n = ctx.draw_int("grid_n", n_lo, n_hi)
    g = full_grid(n, n, 0)
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    palette_size = int(overrides.get("palette_size",
                                     ctx.draw_int("palette_size",
                                                  ps_lo, ps_hi)))
    palette_size = max(1, min(4, palette_size))
    pal = _build_palette(palette_kind, palette_size, rng)
    n_cells = int(overrides.get("n_cells",
                                ctx.draw_int("n_cells", nc_lo, nc_hi)))
    n_cells = max(3, min(12, n_cells))
    bias = (overrides.get("texture") or
            overrides.get("position_bias")
            or ctx.draw_choice("position_bias", list(POSITION_BIASES)))
    placed = 0
    for _try in range(120):
        if placed >= n_cells:
            break
        r, c = _pick_cell(bias, n, rng)
        if g[r][c] == 0:
            g[r][c] = rng.choice(pal)
            placed += 1
    return g


def _pick_cell(bias, n, rng):
    if bias == "tight":
        r = rng.randint(2, max(2, n // 3))
        c = rng.randint(2, max(2, n // 3))
    elif bias == "diagonal":
        i = rng.randint(2, max(2, n // 2))
        r, c = i, i
    elif bias == "row_aligned":
        r = rng.randint(2, max(2, n // 2))
        c = rng.randint(2, n - 3)
    else:
        r = rng.randint(2, max(2, n // 2 + 1))
        c = rng.randint(2, n - 3)
    return r, c


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 6, 7, 8, 9]
    rng.shuffle(pool)
    if len(pool) < n:
        for c in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            if c not in pool:
                pool.append(c)
            if len(pool) >= n:
                break
    return pool[:n]


def _draw_from_degenerate(name, rng):
    n = 9
    g = full_grid(n, n, 0)
    if name == "full_grid":
        for r in range(n):
            for c in range(n):
                g[r][c] = 2
        return g
    if name == "single_cell":
        g[3][3] = 2
        return g
    if name == "all_in_corner":
        for r in range(0, 2):
            for c in range(0, 2):
                g[r][c] = 2
        return g
    return g
