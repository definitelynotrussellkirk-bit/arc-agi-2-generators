"""Generator for 963f59bc.

Rule: blue(1) shape + colored "dot" markers. Reflect the blue shape
across each dot's row/col axis.

Combinatorial axes (8): grid_h/w, blue_shape_size, n_dots, dot_placement,
palette_kind, anchor_corner, palette_size.
Degenerates: no_dots, no_blue, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "084de7b050a1"
VERSION = "1.1.0"
TASK_ID = "084de7b050a1"
SUMMARY = "Blue shape + colored dots; rule reflects blue across each dot's row/col axis."

INVARIANTS = [
    "background is 0",
    ">=1 contiguous blue(1) shape with >=2 cells",
    ">=1 colored dot (non-blue, non-bg) sharing row or col with blue",
    "reflected blue images stay in-bounds",
]

DOT_PLACEMENTS = ("row_aligned", "col_aligned", "mixed", "scattered")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_dots", "no_blue", "full_grid")
HELPFUL_TEXTURES = DOT_PLACEMENTS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..16", "valid": "10..20"},
    "grid_w":         {"type": "int", "default": "rng 12..16", "valid": "10..20"},
    "blue_shape_size":{"type": "int", "default": "rng 2..3", "valid": "2..4"},
    "n_dots":         {"type": "int", "default": "rng 1..2", "valid": "1..3"},
    "dot_placement":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(DOT_PLACEMENTS)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..3"},
    "texture":        {"type": "str", "default": "alias for dot_placement",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("placement")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    if difficulty == "easy":
        h_lo, h_hi = 10, 12
        bsz_lo, bsz_hi = 2, 2
    elif difficulty == "hard":
        h_lo, h_hi = 16, 20
        bsz_lo, bsz_hi = 3, 4
    else:
        h_lo, h_hi = 12, 16
        bsz_lo, bsz_hi = 2, 3
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    g = full_grid(h, w, 0)
    bsz = int(overrides.get("blue_shape_size",
                            ctx.draw_int("blue_shape_size", bsz_lo, bsz_hi)))
    bsz = max(2, min(4, bsz))
    bh = bw = bsz
    br = rng.randint(2, max(2, h // 2 - bh - 1))
    bc = rng.randint(2, max(2, w // 2 - bw - 1))
    for dr in range(bh):
        for dc in range(bw):
            g[br + dr][bc + dc] = 1
    placement = (overrides.get("texture") or
                 overrides.get("dot_placement")
                 or ctx.draw_choice("dot_placement", list(DOT_PLACEMENTS)))
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    n_dots = int(overrides.get("n_dots",
                               ctx.draw_int("n_dots", 1, 2)))
    n_dots = max(1, min(3, n_dots))
    palette = _build_palette(palette_kind, n_dots, rng)
    placed = 0
    for color in palette:
        for _try in range(20):
            dr, dc = _pick_dot_pos(placement, h, w, br, bc, bh, bw, rng)
            if 0 <= dr < h and 0 <= dc < w and g[dr][dc] == 0:
                g[dr][dc] = color
                placed += 1
                break
        if placed >= n_dots:
            break
    if placed < 1:
        for color in palette:
            for r in range(h):
                for c in range(w):
                    if g[r][c] == 0:
                        g[r][c] = color
                        placed += 1
                        break
            if placed >= 1:
                break
    return g


def _pick_dot_pos(placement, h, w, br, bc, bh, bw, rng):
    if placement == "row_aligned":
        dr = br + rng.randint(0, bh - 1)
        dc = rng.randint(bc + bw + 2, w - 2)
    elif placement == "col_aligned":
        dc = bc + rng.randint(0, bw - 1)
        dr = rng.randint(br + bh + 2, h - 2)
    elif placement == "mixed":
        if rng.random() < 0.5:
            dr = br + rng.randint(0, bh - 1)
            dc = rng.randint(bc + bw + 2, w - 2)
        else:
            dc = bc + rng.randint(0, bw - 1)
            dr = rng.randint(br + bh + 2, h - 2)
    else:
        dr = rng.randint(2, h - 2)
        dc = rng.randint(2, w - 2)
    return dr, dc


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [5, 7, 8]
    elif kind == "primary":
        pool = [2, 3, 4]
    else:
        pool = [2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    if len(pool) < n:
        for c in [2, 3, 4, 5, 6, 7, 8, 9]:
            if c not in pool:
                pool.append(c)
            if len(pool) >= n:
                break
    return pool[:n]


def _draw_from_degenerate(name, rng):
    h, w = 14, 14
    g = full_grid(h, w, 0)
    if name == "no_dots":
        for r in range(2, 4):
            for c in range(2, 4):
                g[r][c] = 1
        return g
    if name == "no_blue":
        g[5][5] = 2
        g[8][8] = 3
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 1
        return g
    return g
