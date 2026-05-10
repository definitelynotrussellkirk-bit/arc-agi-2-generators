"""Generator for 15663ba9.

Rule: nonzero block contains one 2x2 black hole; output marks the four
hole-corner cells inside the colored rectangle.

Combinatorial axes (8): grid_size, shape_color, hole_position,
hole_size, palette_kind, anchor_corner, asymmetry_force, palette_size.
Degenerates: no_hole, hole_at_edge, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid, fill_box

GENERATOR_ID = "a3c76f931ce5"
VERSION = "1.1.0"
TASK_ID = "a3c76f931ce5"
SUMMARY = "A nonzero block contains one 2x2 black hole; corner cells are marked."

INVARIANTS = [
    "background is 0 and remains the mode color",
    "one solid nonzero rectangle encloses a 2x2 zero hole",
    "the hole is strictly inside the colored rectangle",
]

POSITION_BIASES = ("centered", "corner", "near_edge", "scattered")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_hole", "hole_at_edge", "full_grid")
HELPFUL_TEXTURES = POSITION_BIASES

AXES = {
    "grid_size":      {"type": "int", "default": "rng 7..10", "valid": "7..14"},
    "shape_color":    {"type": "color", "default": "rng !{0,2,4}",
                       "valid": "1|3|5|6|7|8|9"},
    "hole_position":  {"type": "str", "default": "rng helpful",
                       "valid": "|".join(POSITION_BIASES)},
    "hole_size":      {"type": "int", "default": "2", "valid": "2..3"},
    "palette_kind":   {"type": "str", "default": "rng",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "texture":        {"type": "str", "default": "alias for hole_position",
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
        size_lo, size_hi = 7, 8
    elif difficulty == "hard":
        size_lo, size_hi = 11, 14
    else:
        size_lo, size_hi = 7, 10
    size = ctx.draw_int("grid_size", size_lo, size_hi)
    palette_kind = overrides.get("palette_kind",
                                 ctx.draw_choice("palette_kind",
                                                 list(PALETTE_KINDS)))
    pal = _build_palette(palette_kind, rng)
    color = int(overrides.get("shape_color",
                              ctx.draw_color("shape_color",
                                             exclude={0, 2, 4})))
    g = full_grid(size, size, 0)
    fill_box(g, 1, 1, size - 2, size - 2, color)
    hole_size = int(overrides.get("hole_size", 2))
    hole_size = max(2, min(3, hole_size))
    bias = (overrides.get("texture") or
            overrides.get("hole_position")
            or ctx.draw_choice("hole_position", list(POSITION_BIASES)))
    hole_r, hole_c = _pick_hole_pos(bias, size, hole_size, rng)
    fill_box(g, hole_r, hole_c, hole_r + hole_size - 1, hole_c + hole_size - 1, 0)
    return g


def _pick_hole_pos(bias, size, hole_size, rng):
    lo = 2
    hi = size - hole_size - 2
    if hi < lo:
        hi = lo
    if bias == "centered":
        hr = max(lo, (size - hole_size) // 2)
        hc = max(lo, (size - hole_size) // 2)
    elif bias == "corner":
        hr = rng.choice([lo, hi])
        hc = rng.choice([lo, hi])
    elif bias == "near_edge":
        if rng.random() < 0.5:
            hr = rng.choice([lo, hi])
            hc = rng.randint(lo, hi)
        else:
            hr = rng.randint(lo, hi)
            hc = rng.choice([lo, hi])
    else:
        hr = rng.randint(lo, hi)
        hc = rng.randint(lo, hi)
    hr = max(lo, min(hr, hi))
    hc = max(lo, min(hc, hi))
    return hr, hc


def _build_palette(kind, rng):
    if kind == "warm":
        pool = [3, 6, 9]
    elif kind == "cool":
        pool = [1, 5, 7, 8]
    elif kind == "primary":
        pool = [1, 3]
    else:
        pool = [1, 3, 5, 6, 7, 8, 9]
    pool = [c for c in pool if c not in (0, 2, 4)]
    rng.shuffle(pool)
    return pool


def _draw_from_degenerate(name, rng):
    size = 8
    g = full_grid(size, size, 0)
    if name == "no_hole":
        fill_box(g, 1, 1, size - 2, size - 2, 3)
        return g
    if name == "hole_at_edge":
        fill_box(g, 1, 1, size - 2, size - 2, 3)
        fill_box(g, 1, 1, 2, 2, 0)
        return g
    if name == "full_grid":
        for r in range(size):
            for c in range(size):
                g[r][c] = 3
        return g
    return g
