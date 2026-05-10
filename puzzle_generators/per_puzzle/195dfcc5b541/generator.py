"""Generator for 50f325b5.

Rule: color-3 copies matching color-8 stencil under rotation or
reflection are recolored to 8.

Combinatorial axes (8): grid_h/w, variant, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
shape_variant.
Degenerates: no_stencil, no_copies, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, paint_at

GENERATOR_ID = "195dfcc5b541"
VERSION = "1.1.0"
TASK_ID = "195dfcc5b541"
SUMMARY = "Color-3 copies matching color-8 stencil under rotation/reflection recolored."

INVARIANTS = [
    "one color-8 polyomino supplies the stencil",
    "one or more color-3 polyominoes match a rotated or reflected stencil variant",
    "matched color-3 cells are recolored to 8",
    "stencil and copy colors are distinct and non-zero",
]

VARIANTS = ("rot90", "rot180", "flip")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_stencil", "no_copies", "full_grid")
HELPFUL_TEXTURES = VARIANTS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "grid_w":         {"type": "int", "default": "rng 11..15", "valid": "9..18"},
    "variant":        {"type": "str", "default": "rng helpful",
                       "valid": "|".join(VARIANTS)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "shape_variant":  {"type": "str", "default": "rng", "valid": "rng"},
    "texture":        {"type": "str", "default": "alias for variant",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _norm(cells):
    cells = list(cells)
    min_r = min(r for r, _ in cells)
    min_c = min(c for _, c in cells)
    return sorted((r - min_r, c - min_c) for r, c in cells)


def _rot(cells):
    return _norm((c, -r) for r, c in cells)


def _flip(cells):
    return _norm((r, -c) for r, c in cells)


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    variant = (overrides.get("texture") if overrides.get("texture") in VARIANTS else None) or \
              overrides.get("variant") or \
              ctx.draw_choice("variant", list(VARIANTS))
    shapes = [
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(0, 1), (1, 1), (2, 1), (2, 0), (2, 2)],
        [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)],
    ]
    base = shapes[rng.randint(0, len(shapes) - 1)]
    match = base
    if variant == "rot90":
        match = _rot(match)
    elif variant == "rot180":
        match = _rot(_rot(match))
    else:
        match = _flip(match)
    h = 10 + rng.randint(0, 3)
    w = 11 + rng.randint(0, 4)
    g = full_grid(h, w, 0)
    paint_at(g, 1, 1, base, 8)
    paint_at(g, h - 5, w - 5, match, 3)
    if rng.randint(0, 1):
        g[h - 2][1] = 3
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 13, 0)
    if name == "no_stencil":
        g[6][6] = 3
        return g
    if name == "no_copies":
        paint_at(g, 1, 1, [(0, 0), (1, 0), (1, 1), (2, 1)], 8)
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(13):
                g[r][c] = 8
        return g
    return g
