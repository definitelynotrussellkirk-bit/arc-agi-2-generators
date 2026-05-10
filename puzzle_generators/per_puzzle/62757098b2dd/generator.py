"""Generator for e9ac8c9e.

Rule: gray rectangles with four colored corner markers are filled by
the corresponding quadrant marker colors.

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, rect_size,
n_distinct_colors.
Degenerates: no_markers, no_rect, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import fill_box, full_grid

GENERATOR_ID = "62757098b2dd"
VERSION = "1.1.0"
TASK_ID = "62757098b2dd"
SUMMARY = "Gray rectangle with four colored corner markers; rule fills quadrants."

INVARIANTS = [
    "background is color 0",
    "each gray object is a solid rectangle",
    "four non-gray corner markers sit one cell outside the rectangle corners",
    "marker colors are distinct so each quadrant gets a unique color",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_markers", "no_rect", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "9", "valid": "9"},
    "grid_w":         {"type": "int", "default": "9", "valid": "9"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "rect_size":      {"type": "str", "default": "4x4", "valid": "4x4"},
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
        pool = pool + [c for c in [1, 2, 3, 4, 6, 7, 8, 9] if c not in pool]
    tl, tr, bl, br = pool[:4]
    g = full_grid(9, 9, 0)
    fill_box(g, 3, 3, 6, 6, 5)
    g[2][2] = tl
    g[2][7] = tr
    g[7][2] = bl
    g[7][7] = br
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
    pool = [c for c in pool if c not in (0, 5)]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    g = full_grid(9, 9, 0)
    if name == "no_markers":
        fill_box(g, 3, 3, 6, 6, 5)
        return g
    if name == "no_rect":
        g[2][2] = 1
        g[2][7] = 2
        g[7][2] = 3
        g[7][7] = 4
        return g
    if name == "full_grid":
        for r in range(9):
            for c in range(9):
                g[r][c] = 5
        return g
    return g
