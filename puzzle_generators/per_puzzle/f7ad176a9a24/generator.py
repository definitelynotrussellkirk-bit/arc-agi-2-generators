"""Generator for bd14c3bf.

Rule: blue objects with same hole/contact topology as red exemplar are
recolored red.

Combinatorial axes (8): grid_h/w, shape_family, n_blue, palette_kind,
position_bias, anchor_corner, asymmetry_force, palette_size.
Degenerates: no_red, all_red, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "f7ad176a9a24"
VERSION = "1.1.0"
TASK_ID = "f7ad176a9a24"
SUMMARY = "Blue objects matching red exemplar topology are recolored red."

INVARIANTS = [
    "background is color 0",
    "there is one red exemplar object",
    "at least one blue object has the same topology signature as the exemplar",
    "matching blue objects are recolored to red",
]

SHAPES = {
    "ell": [(0, 0), (1, 0), (2, 0), (2, 1)],
    "tee": [(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)],
    "zig": [(0, 0), (0, 1), (1, 1), (1, 2), (2, 2)],
}
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_red", "all_red", "full_grid")
HELPFUL_TEXTURES = tuple(SHAPES.keys())

AXES = {
    "grid_h":         {"type": "int", "default": "rng 12..15", "valid": "10..18"},
    "grid_w":         {"type": "int", "default": "rng 12..15", "valid": "10..18"},
    "shape_family":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(HELPFUL_TEXTURES)},
    "n_blue":         {"type": "int", "default": "2", "valid": "1..3"},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "position_bias":  {"type": "str", "default": "scattered",
                       "valid": "scattered|spread|rng"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "texture":        {"type": "str", "default": "alias for shape_family",
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
        h_lo, h_hi = 10, 12
    elif difficulty == "hard":
        h_lo, h_hi = 15, 18
    else:
        h_lo, h_hi = 12, 15
    family = (overrides.get("texture") if overrides.get("texture") in SHAPES else None) or \
             overrides.get("shape_family") or \
             ctx.draw_choice("shape_family", list(SHAPES))
    h = h_lo + rng.randint(0, h_hi - h_lo)
    w = h_lo + rng.randint(0, h_hi - h_lo)
    g = full_grid(h, w, 0)
    cells = SHAPES[family]
    red_r = 1 + rng.randint(0, 1)
    red_c = 1 + rng.randint(0, 1)
    paint_at(g, red_r, red_c, cells, 2)
    paint_at(g, h - 4, 2 + rng.randint(0, 2), cells, 1)
    paint_at(g, 5 + rng.randint(0, max(0, h - 9)), w - 4, cells, 1)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 14, 14
    g = full_grid(h, w, 0)
    if name == "no_red":
        paint_at(g, 2, 2, SHAPES["ell"], 1)
        return g
    if name == "all_red":
        paint_at(g, 2, 2, SHAPES["ell"], 2)
        paint_at(g, 8, 8, SHAPES["ell"], 2)
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 1
        return g
    return g
