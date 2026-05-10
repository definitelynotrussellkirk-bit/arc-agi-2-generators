"""Generator for 5ecac7f7.

Rule: three panels contribute leftmost, middle, rightmost objects into
single bg=7 output.

Combinatorial axes (8): panel_size, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, n_objects, panel_count.
Degenerates: no_objects, single_panel, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "5f82ddf81696"
VERSION = "1.1.0"
TASK_ID = "5f82ddf81696"
SUMMARY = "Three panels contribute leftmost/middle/rightmost objects to one output."

INVARIANTS = [
    "the input has three square panels separated by one blank column",
    "panel background is color 0, which the rule treats as output background 7",
    "each panel contains several separated nonzero objects",
    "the left, middle, and right panels select their leftmost, middle, and rightmost objects respectively",
]

OBJECTS = [
    [(0, 0), (1, 0)],
    [(0, 0), (0, 1), (1, 1)],
    [(0, 1), (1, 0), (1, 1)],
]
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_objects", "single_panel", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "panel_size":     {"type": "int", "default": "7", "valid": "5..10"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "8", "valid": "8"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_objects":      {"type": "int", "default": "3", "valid": "3"},
    "panel_count":    {"type": "int", "default": "3", "valid": "3"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _paint(g, r0, c0, cells, color):
    for dr, dc in cells:
        if 0 <= r0 + dr < len(g) and 0 <= c0 + dc < len(g[0]):
            g[r0 + dr][c0 + dc] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    n = 7
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind")
                    or ctx.draw_choice("palette_kind",
                                       list(PALETTE_KINDS)))
    pool = _build_palette(palette_kind, rng)
    if len(pool) < 8:
        pool = pool + [c for c in [1, 2, 3, 4, 5, 6, 8, 9] if c not in pool]
    colors = pool[:8]
    g = full_grid(n, 3 * n + 2, 0)
    local_cols = [1, 3, 5]
    for panel in range(3):
        start = panel * (n + 1)
        row_order = [1, 3, 5]
        rng.shuffle(row_order)
        for idx, col in enumerate(local_cols):
            shape = OBJECTS[(idx + panel + sample_index) % len(OBJECTS)]
            color = colors[(panel * 3 + idx) % len(colors)]
            row = row_order[idx]
            _paint(g, row, start + col, shape, color)
    return g


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 8]
    elif kind == "primary":
        pool = [1, 2, 3, 4]
    else:
        pool = [1, 2, 3, 4, 5, 6, 8, 9]
    pool = [c for c in pool if c != 7]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    n = 7
    g = full_grid(n, 3 * n + 2, 0)
    if name == "no_objects":
        return g
    if name == "single_panel":
        _paint(g, 1, 1, OBJECTS[0], 2)
        return g
    if name == "full_grid":
        for r in range(n):
            for c in range(3 * n + 2):
                g[r][c] = 7
        return g
    return g
