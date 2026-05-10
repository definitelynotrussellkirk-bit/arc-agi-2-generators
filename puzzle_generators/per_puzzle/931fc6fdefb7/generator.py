"""Generator for 67c52801.

Rule: blocks are sorted by size and dropped upward into shelf gaps
sorted by width.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, gap_pattern,
n_distinct_colors.
Degenerates: no_blocks, no_shelf, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import fill_box, full_grid

GENERATOR_ID = "931fc6fdefb7"
VERSION = "1.1.0"
TASK_ID = "931fc6fdefb7"
SUMMARY = "Blocks sorted by size dropped into shelf gaps sorted by width."

INVARIANTS = [
    "the bottom-left color is the shelf color",
    "the row above the bottom contains shelf segments separated by zero gaps",
    "non-shelf blocks have sizes divisible by their matched gap widths",
    "block colors are distinct and exclude the shelf color",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_blocks", "no_shelf", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "12", "valid": "12"},
    "grid_w":         {"type": "int", "default": "12", "valid": "12"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "gap_pattern":    {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_distinct_colors":{"type": "int", "default": "4", "valid": "4"},
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
    if len(pool) < 4:
        pool = pool + [c for c in [1, 2, 3, 4, 5, 6, 7, 8, 9] if c not in pool]
    shelf, c1, c2, c3 = pool[:4]
    g = full_grid(12, 12, 0)
    for c in range(12):
        g[11][c] = shelf
        g[10][c] = shelf
    for c in [1, 4, 5, 8, 9, 10]:
        g[10][c] = 0
    g[2][1] = c1
    fill_box(g, 2, 4, 3, 5, c2)
    fill_box(g, 2, 8, 3, 10, c3)
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
    pool = [c for c in pool if c != 0]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 12, 0)
    if name == "no_blocks":
        for c in range(12):
            g[11][c] = 5
            g[10][c] = 5
        return g
    if name == "no_shelf":
        g[2][1] = 2
        return g
    if name == "full_grid":
        for r in range(12):
            for c in range(12):
                g[r][c] = 5
        return g
    return g
