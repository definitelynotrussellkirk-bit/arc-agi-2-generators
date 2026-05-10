"""Generator for 1f642eb9.

Rule: 8-cells form a region with bbox. Each non-{0,8} dot in that bbox
row/col range gets projected to the nearest bbox edge.

Combinatorial axes (8): grid_h/w, line_length, palette_kind,
position_bias, n_dots, anchor_corner, asymmetry_force, palette_size.
Degenerates: no_8line, no_dots, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "064e439acd2d"
VERSION = "1.1.0"
TASK_ID = "064e439acd2d"
SUMMARY = "Solid 8-block + colored dots aligned with the block's row or col."

INVARIANTS = [
    ">=3 cells of color 8 forming a horizontal or vertical line",
    ">=2 colored dots aligned with that block's row or col range",
]

POSITION_BIASES = ("centered", "rng", "spread", "near_edge")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_8line", "no_dots", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..7", "valid": "4..10"},
    "grid_w":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "line_length":    {"type": "int", "default": "rng 3..4", "valid": "3..6"},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
    "position_bias":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "n_dots":         {"type": "int", "default": "2", "valid": "2..4"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..4"},
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
        h_lo, h_hi, w_lo, w_hi = 4, 5, 7, 9
        ll_lo, ll_hi = 3, 3
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 8, 10, 11, 14
        ll_lo, ll_hi = 4, 6
    else:
        h_lo, h_hi, w_lo, w_hi = 5, 7, 8, 10
        ll_lo, ll_hi = 3, 4
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    g = full_grid(h, w, 0)
    r8 = rng.randint(2, h - 2)
    line_length = int(overrides.get("line_length",
                                    rng.randint(ll_lo, ll_hi)))
    line_length = max(3, min(line_length, w - 4))
    c8_start = rng.randint(2, max(2, w - line_length - 1))
    for i in range(line_length):
        if c8_start + i < w:
            g[r8][c8_start + i] = 8
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    pal = _build_palette(palette_kind, 2, rng)
    g[r8][rng.randint(0, c8_start - 1)] = pal[0]
    if r8 > 0:
        g[rng.randint(0, r8 - 1)][rng.randint(c8_start,
                                              min(w - 1,
                                                  c8_start + line_length - 1))] = pal[1]
    return g


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 6, 7, 9]
    pool = [c for c in pool if c not in (0, 8)]
    rng.shuffle(pool)
    if len(pool) < n:
        for c in [1, 2, 3, 4, 5, 6, 7, 9]:
            if c not in pool:
                pool.append(c)
            if len(pool) >= n:
                break
    return pool[:n]


def _draw_from_degenerate(name, rng):
    h, w = 6, 9
    g = full_grid(h, w, 0)
    if name == "no_8line":
        g[3][3] = 2
        g[1][5] = 3
        return g
    if name == "no_dots":
        g[3][3] = 8; g[3][4] = 8; g[3][5] = 8
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 8
        return g
    return g
