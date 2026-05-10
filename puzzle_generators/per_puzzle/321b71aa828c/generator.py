"""Generator for fafd9572.

Rule: marker grid (2x2 distinct colors) in top-left + 1-shapes in 2x2
layout; recolor each shape by marker[ri][ci].

Combinatorial axes (8): grid_h/w, palette_kind, anchor_corner,
asymmetry_force, palette_size, shape_count, position_bias,
shape_variant.
Degenerates: no_shapes, no_markers, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "321b71aa828c"
VERSION = "1.1.0"
TASK_ID = "321b71aa828c"
SUMMARY = "Marker 2x2 + 1-shapes 2x2; recolor shapes by marker positions."

INVARIANTS = [
    "marker-grid: 4 cells in 2x2 with 4 distinct non-1 colors",
    "1-shapes laid out in 2x2 layout with 4 shapes total",
    "each 1-shape is 3 to 5 cells",
]

SHAPES = [
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (0, 1), (1, 1)],
    [(0, 0), (1, 0), (1, 1)],
    [(0, 1), (1, 0), (1, 1)],
]
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_shapes", "no_markers", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..12", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 12..14", "valid": "10..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "4", "valid": "4"},
    "shape_count":    {"type": "int", "default": "4", "valid": "4"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "shape_variant":  {"type": "str", "default": "rng", "valid": "rng"},
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
        h_lo, h_hi, w_lo, w_hi = 10, 10, 12, 12
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 12, 14, 14, 16
    else:
        h_lo, h_hi, w_lo, w_hi = 10, 12, 12, 14
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind") or
                    ctx.draw_choice("palette_kind", list(PALETTE_KINDS)))
    pool = _build_palette(palette_kind, rng)
    if len(pool) < 4:
        pool = pool + [c for c in [2, 3, 4, 5, 6, 7, 8, 9] if c not in pool]
    palette = pool[:4]
    g = full_grid(h, w, 0)
    g[0][0] = palette[0]
    g[0][2] = palette[1]
    g[2][0] = palette[2]
    g[2][2] = palette[3]
    shape_rows = [4, 7]
    shape_cols = [4, 9]
    for sr in shape_rows:
        for sc in shape_cols:
            shape = rng.choice(SHAPES)
            for dr, dc in shape:
                if sr + dr < h and sc + dc < w:
                    g[sr + dr][sc + dc] = 1
    return g


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [2, 3, 4, 6, 9]
    elif kind == "cool":
        pool = [5, 7, 8]
    elif kind == "primary":
        pool = [2, 3, 4, 8]
    else:
        pool = [2, 3, 4, 5, 6, 7, 8, 9]
    pool = [c for c in pool if c not in (0, 1)]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_shapes":
        g[0][0] = 2
        g[0][2] = 3
        g[2][0] = 4
        g[2][2] = 5
        return g
    if name == "no_markers":
        for sr in [4, 7]:
            for sc in [4, 9]:
                g[sr][sc] = 1
                g[sr][sc + 1] = 1
                g[sr + 1][sc] = 1
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 1
        return g
    return g
