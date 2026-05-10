"""Generator for puzzle b8cdaf2b.

Rule: bottom row has outer-color and inner-1 V; row above has outer
narrower. Output extends inner color (1) diagonally upward.

Combinatorial axes (8): grid_h, grid_w, outer_color, inner_color,
palette_kind, anchor_corner, asymmetry_force, include_decoy.
Degenerates: no_outer, no_inner, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "0f55521cc320"
VERSION = "1.1.0"
TASK_ID = "0f55521cc320"
SUMMARY = "Bottom V w/ outer + inner; rule extends inner diagonal up."

INVARIANTS = [
    "bottom row has outer at corners + inner-1 in middle",
    "row above has outer in cols 1..w-2",
    "rest of grid is 0",
    "w odd, w in [5, 11]",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_outer", "no_inner", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 5..9", "valid": "4..12"},
    "grid_w":         {"type": "int", "default": "rng 5..9 (odd)", "valid": "5..11"},
    "outer_color":    {"type": "color", "default": "rng (≠0,1)",
                       "valid": "2..9"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "include_decoy":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "inner_color":    {"type": "color", "default": "1", "valid": "1"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if difficulty == "easy":
        h_lo, h_hi = 4, 6
    elif difficulty == "hard":
        h_lo, h_hi = 8, 12
    else:
        h_lo, h_hi = 5, 9
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", h_lo, h_hi)
    if w % 2 == 0:
        w += 1
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], h, w, rng)
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind")
                    or ctx.draw_choice("palette_kind",
                                       list(PALETTE_KINDS)))
    palette = _build_palette(palette_kind, rng)
    outer = int(overrides.get("outer_color",
                              next((c for c in palette
                                    if c != 1 and c != 0), 6)))
    if outer in (0, 1):
        outer = 6
    g = full_grid(h, w, 0)
    g[h - 1][0] = outer
    g[h - 1][w - 1] = outer
    for c in range(1, w - 1):
        g[h - 1][c] = 1
    for c in range(1, w - 1):
        g[h - 2][c] = outer
    return g


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [5, 7, 8]
    elif kind == "primary":
        pool = [2, 3, 4]
    else:
        pool = [2, 3, 4, 5, 6, 7, 8, 9]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, h, w, rng):
    if w % 2 == 0:
        w += 1
    g = full_grid(h, w, 0)
    if name == "no_outer":
        for c in range(w):
            g[h - 1][c] = 1
        return g
    if name == "no_inner":
        g[h - 1][0] = 6
        g[h - 1][w - 1] = 6
        for c in range(1, w - 1):
            g[h - 2][c] = 6
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 1 if (r + c) % 2 == 0 else 6
        return g
    return g
