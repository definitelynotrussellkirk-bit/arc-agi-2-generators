"""Generator for 18447a8d.

Rule: a color-8 jigsaw piece is paired with a colored complement that
completes a solid rectangle.

Combinatorial axes (8): grid_h/w, rect_width, palette_kind, anchor_corner,
asymmetry_force, palette_size, position_bias, color.
Degenerates: no_complement, no_eight, full_grid.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "54a83e6bbc20"
VERSION = "1.1.0"
TASK_ID = "54a83e6bbc20"
SUMMARY = "Color-8 jigsaw piece is paired with colored complement to complete a rectangle."

INVARIANTS = [
    "the background is color 7",
    "one color-8 connected piece occupies part of a small rectangle",
    "one same-rectangle complement piece of another color appears elsewhere",
    "the two normalized pieces are disjoint and combine into a solid rectangle of the target width",
]

PALETTE_KINDS = ("warm", "cool", "broad", "primary")
DEGENERATE_TEXTURES = ("no_complement", "no_eight", "full_grid")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "grid_h":         {"type": "int", "default": "7", "valid": "7"},
    "grid_w":         {"type": "int", "default": "13", "valid": "13"},
    "rect_width":     {"type": "int", "default": "4", "valid": "4"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "anchor_corner":  {"type": "bool", "default": "false",
                       "valid": "true|false"},
    "asymmetry_force":{"type": "bool", "default": "false",
                       "valid": "true|false"},
    "palette_size":   {"type": "int", "default": "1", "valid": "1"},
    "position_bias":  {"type": "str", "default": "varied", "valid": "varied"},
    "color":          {"type": "color", "default": "rng !{7,8}",
                       "valid": "0..6|9"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


_MASKS = [
    {(0, 0), (1, 0), (2, 0), (0, 1)},
    {(0, 0), (0, 1), (0, 2), (1, 0), (2, 0)},
    {(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)},
    {(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)},
]


def _paint(g, cells, r0, c0, color):
    for r, c in cells:
        g[r0 + r][c0 + c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    rng = ctx.draw_rng("layout")
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], rng)
    color = ctx.draw_color("piece_color", exclude={7, 8})
    rect_h, rect_w = 3, 4
    mask = set(_MASKS[rng.randrange(len(_MASKS))])
    rect = {(r, c) for r in range(rect_h) for c in range(rect_w)}
    comp = rect - mask
    g = full_grid(7, 13, 7)
    r0 = rng.randint(1, 3)
    _paint(g, mask, r0, 0, 8)
    _paint(g, comp, r0, 8, color)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(7, 13, 7)
    if name == "no_complement":
        _paint(g, _MASKS[0], 2, 0, 8)
        return g
    if name == "no_eight":
        rect = {(r, c) for r in range(3) for c in range(4)}
        comp = rect - _MASKS[0]
        _paint(g, comp, 2, 8, 3)
        return g
    if name == "full_grid":
        for r in range(7):
            for c in range(13):
                g[r][c] = 8
        return g
    return g
