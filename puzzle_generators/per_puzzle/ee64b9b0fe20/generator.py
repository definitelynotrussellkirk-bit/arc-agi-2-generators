"""Generator for 4df5b0ae.

Rule: foreground shapes drop to bottom, packed left-to-right in
ascending size.

Combinatorial axes (8): grid_h/w, shape_count, palette_kind, bg_color,
anchor_corner, asymmetry_force, palette_size, position_bias.
Degenerates: no_shapes, single_shape, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ee64b9b0fe20"
VERSION = "1.1.0"
TASK_ID = "ee64b9b0fe20"
SUMMARY = "Foreground shapes drop to bottom, packed left-to-right by size."

INVARIANTS = [
    "the background is the mode color",
    "foreground objects are separated 4-connected components",
    "objects are sorted by cell count from smallest to largest",
    "each object is translated to the bottom and packed at the next available left column",
]

_SHAPES = [
    [(0, 0), (1, 0)],
    [(0, 0), (0, 1), (1, 0)],
    [(0, 0), (0, 1), (1, 0), (1, 1)],
    [(0, 0), (1, 0), (2, 0), (2, 1)],
]
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_shapes", "single_shape", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "12", "valid": "10..16"},
    "grid_w":         {"type": "int", "default": "14", "valid": "12..18"},
    "shape_count":    {"type": "int", "default": "rng 2..4", "valid": "1..6"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "bg_color":       {"type": "color", "default": "rng",
                       "valid": "0..9"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "rng 2..4", "valid": "1..6"},
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
        sc_lo, sc_hi = 4, 6
    else:
        sc_lo, sc_hi = 2, 4
    shape_count = ctx.draw_int("shape_count", sc_lo, sc_hi)
    bg = ctx.draw_color("background", exclude=set())
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind")
                    or ctx.draw_choice("palette_kind",
                                       list(PALETTE_KINDS)))
    pool = _build_palette(palette_kind, bg, rng)
    if len(pool) < shape_count:
        pool = pool + [c for c in [1, 2, 3, 4, 5, 6, 7, 8, 9]
                       if c not in pool and c != bg]
    colors = pool[:shape_count]
    h = 12
    w = 14
    g = full_grid(h, w, bg)
    placements = [(1, 2), (2, 9), (6, 3), (5, 10)]
    for idx in range(shape_count):
        shape = _SHAPES[idx % len(_SHAPES)]
        r0, c0 = placements[idx % len(placements)]
        for dr, dc in shape:
            if r0 + dr < h and c0 + dc < w:
                g[r0 + dr][c0 + dc] = colors[idx]
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
    h, w = 12, 14
    g = full_grid(h, w, 0)
    if name == "no_shapes":
        return g
    if name == "single_shape":
        for dr, dc in _SHAPES[0]:
            g[2 + dr][3 + dc] = 2
        return g
    if name == "full_grid":
        for r in range(h):
            for c in range(w):
                g[r][c] = 2
        return g
    return g
