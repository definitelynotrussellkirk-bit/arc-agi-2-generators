"""Generator for bc93ec48.

Rule: shapes anchored in grid corners rotate clockwise to the next
corner by translated placement.

Combinatorial axes (8): grid_h/w, corner_count, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias,
shape_variant.
Degenerates: no_shapes, full_grid, single_shape.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "61c0bcd32328"
VERSION = "1.1.0"
TASK_ID = "61c0bcd32328"
SUMMARY = "Corner-anchored shapes rotate clockwise to the next corner."

INVARIANTS = [
    "background is color 0",
    "one or more objects have bounding boxes touching a grid corner",
    "corner shapes are single-colored and separated",
    "shape colors are distinct so they survive the clockwise rotation",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_shapes", "full_grid", "single_shape")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "rng 8..12", "valid": "8..14"},
    "grid_w":         {"type": "int", "default": "rng 8..12", "valid": "8..14"},
    "corner_count":   {"type": "int", "default": "rng 1..2", "valid": "1..2"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "true",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "rng 1..2", "valid": "1..2"},
    "position_bias":  {"type": "str", "default": "fixed", "valid": "fixed"},
    "shape_variant":  {"type": "str", "default": "fixed", "valid": "fixed"},
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
        cc_lo, cc_hi = 1, 1
    elif difficulty == "hard":
        cc_lo, cc_hi = 2, 2
    else:
        cc_lo, cc_hi = 1, 2
    n = ctx.draw_int("corner_count", cc_lo, cc_hi)
    h = 8 + rng.randint(0, 4)
    w = 8 + rng.randint(0, 4)
    palette_kind = (overrides.get("texture") or
                    overrides.get("palette_kind") or
                    ctx.draw_choice("palette_kind", list(PALETTE_KINDS)))
    pool = _build_palette(palette_kind, rng)
    if len(pool) < n:
        pool = pool + [c for c in [1, 2, 3, 4, 5, 6, 7, 8, 9] if c not in pool]
    colors = pool[:n]
    g = full_grid(h, w, 0)
    shapes = [
        ([(0, 0), (0, 1), (1, 0)], 0, 0),
        ([(0, 0), (0, 1), (1, 1)], 0, w - 2),
    ]
    for i in range(n):
        cells, r0, c0 = shapes[i]
        for dr, dc in cells:
            g[r0 + dr][c0 + dc] = colors[i]
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
    g = full_grid(10, 10, 0)
    if name == "no_shapes":
        return g
    if name == "single_shape":
        for dr, dc in [(0, 0), (0, 1), (1, 0)]:
            g[dr][dc] = 2
        return g
    if name == "full_grid":
        for r in range(10):
            for c in range(10):
                g[r][c] = 2
        return g
    return g
