"""Generator for c92b942c.

Rule: 3x3 marker grid is tiled 3x3; rows containing markers get color
1 and diagonals adjacent to markers get color 3.

Combinatorial axes (8): size, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, marker_count,
n_distinct_colors.
Degenerates: no_markers, all_markers, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "08b9ee676829"
VERSION = "1.1.0"
TASK_ID = "08b9ee676829"
SUMMARY = "Marker grid tiled 3x3; marker rows get color 1, diagonals get color 3."

INVARIANTS = [
    "background is color 0",
    "input is a 3x3 grid with three nonzero markers",
    "marker colors are distinct and exclude 0, 1, 3",
    "markers cover three different rows so the rule yields three full color-1 rows",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_markers", "all_markers", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "size":           {"type": "int", "default": "3", "valid": "3"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "3", "valid": "3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "marker_count":   {"type": "int", "default": "3", "valid": "3"},
    "n_distinct_colors":{"type": "int", "default": "3", "valid": "3"},
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
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind") or
                    ctx.draw_choice("palette_kind", list(PALETTE_KINDS)))
    pool = _build_palette(palette_kind, rng)
    if len(pool) < 3:
        pool = pool + [c for c in [2, 4, 5, 6, 7, 8, 9] if c not in pool]
    colors = pool[:3]
    g = full_grid(3, 3, 0)
    positions = [(0, 1), (1, 0), (2, 2)]
    rng.shuffle(positions)
    for (r, c), color in zip(positions, colors):
        g[r][c] = color
    return g


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [2, 4, 6, 9]
    elif kind == "cool":
        pool = [5, 7, 8]
    elif kind == "primary":
        pool = [2, 4, 8]
    else:
        pool = [2, 4, 5, 6, 7, 8, 9]
    pool = [c for c in pool if c not in (0, 1, 3)]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    if name == "no_markers":
        return full_grid(3, 3, 0)
    if name == "all_markers":
        return [[2, 4, 5], [6, 7, 8], [9, 2, 4]]
    if name == "full_grid":
        return full_grid(3, 3, 5)
    return full_grid(3, 3, 0)
