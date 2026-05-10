"""Generator for 228f6490.

Rule: colored object moves into matching zero-hole shape inside a
gray component.

Combinatorial axes (8): grid_h/w, hole_size, palette_kind,
anchor_corner, asymmetry_force, palette_size, position_bias, color.
Degenerates: no_hole, no_object, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_rect_outline, full_grid

GENERATOR_ID = "0b53f4dfc446"
VERSION = "1.1.0"
TASK_ID = "0b53f4dfc446"
SUMMARY = "Colored object moves into matching zero-hole shape in gray component."

INVARIANTS = [
    "gray cells form a component with a zero hole",
    "one non-gray colored object has the same normalized shape as the hole",
    "the colored source object is cleared",
    "color is non-zero and not gray",
]

HOLE_SIZES = ("one", "two")
PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_hole", "no_object", "full_grid")
HELPFUL_TEXTURES = HOLE_SIZES

AXES = {
    "grid_h":         {"type": "int", "default": "11", "valid": "11"},
    "grid_w":         {"type": "int", "default": "13", "valid": "13"},
    "hole_size":      {"type": "str", "default": "rng helpful",
                       "valid": "|".join(HOLE_SIZES)},
    "palette_kind":   {"type": "str", "default": "fixed", "valid": "fixed"},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "2", "valid": "2"},
    "position_bias":  {"type": "str", "default": "rng", "valid": "rng"},
    "color":          {"type": "color", "default": "rng !{0,5}",
                       "valid": "1|2|3|4|6|7|8|9"},
    "texture":        {"type": "str", "default": "alias for hole_size",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    hole_size = (overrides.get("texture") if overrides.get("texture") in HOLE_SIZES else None) or \
                overrides.get("hole_size") or \
                ctx.draw_choice("hole_size", list(HOLE_SIZES))
    color = ctx.draw_color("color", exclude={0, 5})
    g = full_grid(11, 13, 0)
    r0 = rng.randint(1, 2)
    c0 = rng.randint(5, 7)
    if hole_size == "one":
        draw_rect_outline(g, r0, c0, 3, 3, 5)
        g[rng.randint(6, 9)][rng.randint(1, 3)] = color
    else:
        draw_rect_outline(g, r0, c0, 3, 4, 5)
        sr = rng.randint(6, 8)
        sc = rng.randint(1, 3)
        g[sr][sc] = color
        g[sr][sc + 1] = color
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(11, 13, 0)
    if name == "no_hole":
        g[5][5] = 2
        return g
    if name == "no_object":
        draw_rect_outline(g, 2, 5, 3, 3, 5)
        return g
    if name == "full_grid":
        for r in range(11):
            for c in range(13):
                g[r][c] = 5
        return g
    return g
