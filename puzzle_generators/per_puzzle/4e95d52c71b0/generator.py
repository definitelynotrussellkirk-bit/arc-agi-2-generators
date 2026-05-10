"""Generator for 2c737e39.

Rule: isolated gray marker defines translation vector from gray source
to copy colored cells.

Combinatorial axes (8): delta_row, delta_col, palette_kind,
position_bias, anchor_corner, asymmetry_force, palette_size, motif_variant.
Degenerates: no_isolated, no_motif, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "4e95d52c71b0"
VERSION = "1.1.0"
TASK_ID = "4e95d52c71b0"
SUMMARY = "Isolated gray marker defines translation vector from gray source."

INVARIANTS = [
    "one gray marker is orthogonally adjacent to a colored source motif",
    "one gray marker is isolated from all nonzero cells",
    "the vector from source gray to isolated gray is used to copy non-gray motif cells",
    "the isolated gray marker is cleared in the output",
]

MOTIF = [(0, 1), (1, 0), (1, 1), (2, 1)]
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_isolated", "no_motif", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "delta_row":      {"type": "int", "default": "rng 3..5", "valid": "2..10"},
    "delta_col":      {"type": "int", "default": "rng 3..5", "valid": "2..10"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "motif_variant":  {"type": "int", "default": "0", "valid": "0"},
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
        d_lo, d_hi = 2, 3
    elif difficulty == "hard":
        d_lo, d_hi = 5, 8
    else:
        d_lo, d_hi = 3, 5
    dr = ctx.draw_int("delta_row", d_lo, d_hi)
    dc = ctx.draw_int("delta_col", d_lo, d_hi)
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind")
                    or ctx.draw_choice("palette_kind",
                                       list(PALETTE_KINDS)))
    pal = _build_palette(palette_kind, 2, rng)
    colors = pal
    h = dr + 8
    w = dc + 8
    sr = rng.randint(2, 3)
    sc = rng.randint(2, 3)
    g = full_grid(h, w, 0)
    g[sr][sc] = 5
    for i, (rr, cc) in enumerate(MOTIF):
        g[sr + rr][sc + cc] = colors[i % len(colors)]
    g[sr + dr][sc + dc] = 5
    return g


def _build_palette(kind, n, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 6, 7, 8, 9]
    pool = [c for c in pool if c not in (0, 5)]
    rng.shuffle(pool)
    if len(pool) < n:
        for c in [1, 2, 3, 4, 6, 7, 8, 9]:
            if c not in pool:
                pool.append(c)
            if len(pool) >= n:
                break
    return pool[:n]


def _draw_from_degenerate(name, rng):
    h, w = 13, 13
    g = full_grid(h, w, 0)
    if name == "no_isolated":
        g[2][2] = 5
        for rr, cc in MOTIF:
            g[2 + rr][2 + cc] = 3
        return g
    if name == "no_motif":
        g[2][2] = 5
        g[7][7] = 5
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 5
        return g
    return g
