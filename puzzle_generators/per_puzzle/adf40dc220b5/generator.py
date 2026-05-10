"""Generator for arc_additional_puzzles_21_set9:H60.

Three panels are separated by full color-5 columns. The first two panels show
a translation vector, and the rule applies that vector to the third panel.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_separators, no_object, identical_panels.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "adf40dc220b5"
VERSION = "1.1.0"
TASK_ID = "adf40dc220b5"
SUMMARY = "Two example panels define a translation applied to the query panel."

INVARIANTS = [
    "two full color-5 separator columns create three panels",
    "each panel contains one connected nonzero component",
    "the example translation keeps the query component inside its panel",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_separators", "no_object", "identical_panels")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "delta":          {"type": "choice", "default": "rng",
                       "valid": "small row/column translations"},
    "shape":          {"type": "int", "default": "rng 0..3", "valid": "0..3"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "2", "valid": "2..2"},
    "position_bias":  {"type": "str", "default": "three_panels_5col",
                       "valid": "three_panels_5col"},
    "n_distinct_colors": {"type": "int", "default": "2", "valid": "2..2"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPES = [
    [(0, 0), (1, 0), (1, 1), (2, 1)],
    [(0, 1), (1, 0), (1, 1), (1, 2)],
    [(0, 0), (0, 1), (1, 1), (2, 1)],
    [(0, 0), (1, 0), (2, 0), (2, 1), (3, 1)],
]
_DELTAS = [(1, 1), (1, 2), (2, 1), (-1, 2), (2, -1)]


def _paint(g, panel_left, top, left, cells, color):
    for r, c in cells:
        g[top + r][panel_left + left + c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    cells = _SHAPES[ctx.draw_int("shape", 0, len(_SHAPES) - 1)]
    dr, dc = rng.choice(_DELTAS)
    if difficulty == "easy":
        ph, pw = 7, 6
    elif difficulty == "hard":
        ph, pw = 11, 9
    else:
        ph, pw = 9, 7
    h, w = ph, pw * 3 + 2
    g = full_grid(h, w, 0)
    sep1, sep2 = pw, pw * 2 + 1
    for r in range(h):
        g[r][sep1] = 5
        g[r][sep2] = 5

    mh = max(r for r, _c in cells) + 1
    mw = max(c for _r, c in cells) + 1
    top_a = rng.randint(max(0, -dr), ph - mh - max(0, dr))
    left_a = rng.randint(max(0, -dc), pw - mw - max(0, dc))
    top_c = rng.randint(max(0, -dr), ph - mh - max(0, dr))
    left_c = rng.randint(max(0, -dc), pw - mw - max(0, dc))
    color = rng.choice([1, 2, 3, 4, 6, 7, 8, 9])
    _paint(g, 0, top_a, left_a, cells, color)
    _paint(g, sep1 + 1, top_a + dr, left_a + dc, cells, color)
    _paint(g, sep2 + 1, top_c, left_c, cells, color)
    return g


def _draw_from_degenerate(name, rng):
    ph, pw = 9, 7
    h, w = ph, pw * 3 + 2
    g = full_grid(h, w, 0)
    sep1, sep2 = pw, pw * 2 + 1
    if name == "no_separators":
        # Three components but no 5-cols — rule's "3 panels"
        # split fails; vector inference undefined.
        for r, c in [(2, 1), (3, 1), (3, 2)]: g[r][c] = 4
        for r, c in [(3, 9), (4, 9), (4, 10)]: g[r][c] = 4
        for r, c in [(2, 17), (3, 17), (3, 18)]: g[r][c] = 4
        return g
    for r in range(h):
        g[r][sep1] = 5
        g[r][sep2] = 5
    if name == "no_object":
        # Separators present but query panel empty — rule has
        # nothing to translate.
        for r, c in [(2, 1), (3, 1), (3, 2)]: g[r][c] = 4
        for r, c in [(3, 9), (4, 9), (4, 10)]: g[r][c] = 4
        return g
    if name == "identical_panels":
        # Panels A and B identical (delta = 0,0) — rule's translate
        # vector collapses to identity; effect invisible on panel C.
        for r, c in [(2, 1), (3, 1), (3, 2)]: g[r][c] = 4
        for r, c in [(2, 9), (3, 9), (3, 10)]: g[r][c] = 4
        for r, c in [(2, 17), (3, 17), (3, 18)]: g[r][c] = 4
        return g
    return g
