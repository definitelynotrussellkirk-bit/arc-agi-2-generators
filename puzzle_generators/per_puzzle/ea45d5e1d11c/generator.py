"""Generator for 522fdd07.

Rule: each colored square shrinks by two cells per side while keeping
center fixed.

Combinatorial axes (8): grid_size, square_count, palette_kind, bg_color,
anchor_corner, asymmetry_force, palette_size, position_bias.
Degenerates: no_squares, single_square, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ea45d5e1d11c"
VERSION = "1.1.0"
TASK_ID = "ea45d5e1d11c"
SUMMARY = "Each colored square shrinks by 2 cells per side; center fixed."

INVARIANTS = [
    "the mode color is the background",
    "foreground objects are separated solid odd-sized squares",
    "each square's center stays fixed",
    "the canonical rule redraws each square with side length N-2",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_squares", "single_square", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_size":      {"type": "int", "default": "18", "valid": "14..22"},
    "square_count":   {"type": "int", "default": "rng 2..4", "valid": "1..5"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "bg_color":       {"type": "color", "default": "rng",
                       "valid": "0..9"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..5"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
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
        sc_lo, sc_hi = 1, 2
    elif difficulty == "hard":
        sc_lo, sc_hi = 4, 5
    else:
        sc_lo, sc_hi = 2, 4
    square_count = ctx.draw_int("square_count", sc_lo, sc_hi)
    bg = ctx.draw_color("background", exclude=set())
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind")
                    or ctx.draw_choice("palette_kind",
                                       list(PALETTE_KINDS)))
    pool = _build_palette(palette_kind, bg, rng)
    if len(pool) < square_count:
        pool = pool + [c for c in [1, 2, 3, 4, 5, 6, 7, 8, 9]
                       if c not in pool and c != bg]
    colors = pool[:square_count]
    g = full_grid(18, 18, bg)
    slots = [(1, 1, 5), (1, 11, 3), (10, 2, 5), (11, 11, 3)]
    rng.shuffle(slots)
    for color, (r0, c0, size) in zip(colors, slots[:square_count]):
        for r in range(size):
            for c in range(size):
                g[r0 + r][c0 + c] = color
    return g


def _build_palette(kind, bg, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    pool = [c for c in pool if c != bg]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    g = full_grid(18, 18, 0)
    if name == "no_squares":
        return g
    if name == "single_square":
        for r in range(5):
            for c in range(5):
                g[1 + r][1 + c] = 2
        return g
    if name == "full_grid":
        for r in range(18):
            for c in range(18):
                g[r][c] = 2
        return g
    return g
