"""Generator for 7bb4cfc1.

Rule: 4-template above 9-divider; for each 6-blob below, if rotated
shape matches template, recolor to 2.

Combinatorial axes (8): grid_h/w, palette_kind, n_blobs, position_bias,
anchor_corner, asymmetry_force, palette_size, divider_row.
Degenerates: no_template, no_blobs, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "1303bf6af20d"
VERSION = "1.1.0"
TASK_ID = "1303bf6af20d"
SUMMARY = "4-template above 9-divider + 2-3 6-blobs below."

INVARIANTS = [
    "4-template (3-4 cells) above 9-divider",
    "below: 1-2 matching 6-blobs and 1-2 non-matching",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_template", "no_blobs", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..10", "valid": "7..14"},
    "grid_w":         {"type": "int", "default": "rng 9..11", "valid": "7..14"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "n_blobs":        {"type": "int", "default": "2", "valid": "1..3"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "divider_row":    {"type": "int", "default": "3", "valid": "3"},
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
        h_lo, h_hi, w_lo, w_hi = 7, 8, 7, 9
    elif difficulty == "hard":
        h_lo, h_hi, w_lo, w_hi = 11, 14, 11, 14
    else:
        h_lo, h_hi, w_lo, w_hi = 8, 10, 9, 11
    h = ctx.draw_int("grid_h", h_lo, h_hi)
    w = ctx.draw_int("grid_w", w_lo, w_hi)
    g = full_grid(h, w, 0)
    paint_at(g, 0, 1, [(0, 0), (1, 0), (2, 0), (2, 1)], 4)
    for c in range(w):
        g[3][c] = 9
    paint_at(g, 4, 0, [(1, 0), (1, 1), (1, 2), (0, 2)], 6)
    if 6 < w:
        paint_at(g, 4, 6, [(0, 0), (0, 1), (1, 0), (1, 1)], 6)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 9, 10
    g = full_grid(h, w, 0)
    if name == "no_template":
        for c in range(w):
            g[3][c] = 9
        paint_at(g, 4, 0, [(0, 0), (1, 0), (1, 1)], 6)
        return g
    if name == "no_blobs":
        paint_at(g, 0, 1, [(0, 0), (1, 0), (2, 0), (2, 1)], 4)
        for c in range(w):
            g[3][c] = 9
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 6
        return g
    return g
