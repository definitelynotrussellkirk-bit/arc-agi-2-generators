"""Generator for puzzle a78176bb.

Rule: diagonal of color X + 5-triangle on one side. Output: original
diagonal + parallel diagonals offset by the triangle's spread.

Combinatorial axes (8): grid_size, diag_color, diag_length, k_offset,
triangle_side, anchor_corner, asymmetry_force, palette_kind.
Degenerates: no_triangle, no_diag, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "516502422f5c"
VERSION = "1.1.0"
TASK_ID = "516502422f5c"
SUMMARY = "Diagonal + 5-triangle; rule emits parallel diagonals."

INVARIANTS = [
    "background is 0",
    "exactly one non-{0,5} color forming a diagonal of length L (4..7)",
    "5-triangle of length L-1 adjacent to diagonal",
    "diagonal and triangle don't overlap",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
TRIANGLE_SIDES = ("below", "above")
DEGENERATE_TEXTURES = ("no_triangle", "no_diag", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_size":      {"type": "int", "default": "10", "valid": "8..14"},
    "diag_color":     {"type": "color", "default": "rng (≠0,5)",
                       "valid": "1..9 (≠5)"},
    "diag_length":    {"type": "int", "default": "rng 4..6", "valid": "3..8"},
    "k_offset":       {"type": "int", "default": "auto",
                       "valid": "L-1..size-L"},
    "triangle_side":  {"type": "str", "default": "below",
                       "valid": "|".join(TRIANGLE_SIDES)},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
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
        size_lo, size_hi = 8, 9
    elif difficulty == "hard":
        size_lo, size_hi = 11, 14
    else:
        size_lo, size_hi = 9, 10
    size = int(overrides.get("grid_size",
                             ctx.draw_int("grid_size", size_lo, size_hi)))
    size = max(8, min(14, size))
    h = w = size
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind")
                    or ctx.draw_choice("palette_kind",
                                       list(PALETTE_KINDS)))
    L = int(overrides.get("diag_length",
                          ctx.draw_int("diag_length", 4, 6)))
    L = max(3, min(min(size - 2, 8), L))
    palette = _build_palette(palette_kind, rng)
    diag_color = int(overrides.get("diag_color", palette[0]))
    if diag_color == 5:
        diag_color = next((c for c in palette if c != 5), 1)
    g = full_grid(h, w, 0)
    k = rng.randint(L - 1, w - L)
    if k + L > w:
        k = w - L
    if k < L - 1:
        k = L - 1
    for i in range(L):
        if i + k < w:
            g[i][i + k] = diag_color
    for r in range(1, L):
        for c in range(k, min(k + r, w)):
            if g[r][c] == 0:
                g[r][c] = 5
    return g


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 6, 7, 8, 9]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    h = w = 10
    g = full_grid(h, w, 0)
    if name == "no_triangle":
        for i in range(5):
            g[i][i + 4] = 3
        return g
    if name == "no_diag":
        for r in range(1, 5):
            for c in range(4, 4 + r):
                g[r][c] = 5
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 3 if r == c else (5 if r > c else 0)
        return g
    return g
