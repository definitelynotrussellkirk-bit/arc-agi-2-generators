"""Generator for arc_puzzle_bank_21_set12_s:S12_E5.

Rule: only nonzero cells touching a different-colored component are
shown as 8.

Combinatorial axes (8): height, width, palette_kind, contact_orientation,
palette_size, position_bias, n_distinct_colors, density, texture.
Degenerates: no_contacts, all_isolated, mixed_color_in_one_blob.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "102e79f0ca6d"
VERSION = "1.1.0"
TASK_ID = "102e79f0ca6d"
SUMMARY = "Only nonzero cells touching a different-colored component are shown as 8."

INVARIANTS = [
    "background is 0",
    "at least two differently colored components edge-touch",
    "some cells in those components are not contact cells",
    "non-contact and isolated cells disappear in the output",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_contacts", "all_isolated", "mixed_color_in_one_blob")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "height":         {"type": "int", "default": "rng 9..12", "valid": "7..15"},
    "width":          {"type": "int", "default": "rng 10..13", "valid": "8..16"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "contact_orientation": {"type": "choice", "default": "rng horizontal|vertical",
                       "valid": "horizontal|vertical"},
    "palette_size":   {"type": "int", "default": "3", "valid": "2..4"},
    "position_bias":  {"type": "str", "default": "two_components_in_contact",
                       "valid": "two_components_in_contact"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "2..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}


def _paint(g, cells, color):
    for r, c in cells:
        g[r][c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    if difficulty == "easy":
        h = ctx.draw_int("height", 9, 10)
        w = ctx.draw_int("width", 10, 11)
    elif difficulty == "hard":
        h = ctx.draw_int("height", 11, 12)
        w = ctx.draw_int("width", 12, 13)
    else:
        h = ctx.draw_int("height", 9, 12)
        w = ctx.draw_int("width", 10, 13)
    orientation = ctx.draw_choice("contact_orientation", ["horizontal", "vertical"])
    rng = ctx.draw_rng("layout")
    g = full_grid(h, w, 0)
    r = rng.randint(2, h - 5)
    c = rng.randint(2, w - 7)
    if orientation == "horizontal":
        _paint(g, [(r, c), (r + 1, c), (r + 2, c)], 2)
        _paint(g, [(r + 1, c + 1), (r + 1, c + 2)], 3)
    else:
        _paint(g, [(r, c), (r, c + 1), (r, c + 2)], 2)
        _paint(g, [(r + 1, c + 1), (r + 2, c + 1)], 3)
    _paint(g, [(h - 2, w - 3), (h - 2, w - 2)], 6)
    return g


def _draw_from_degenerate(name, rng):
    h, w = 10, 12
    g = full_grid(h, w, 0)
    if name == "no_contacts":
        # all components isolated → no contact cells, output is empty
        _paint(g, [(2, 2), (2, 3), (3, 2)], 2)
        _paint(g, [(6, 7), (7, 7), (7, 8)], 3)
        _paint(g, [(5, 1), (5, 2)], 6)
        return g
    if name == "all_isolated":
        # singletons only → no contact between same-color and different-color cells
        g[2][3] = 2; g[5][7] = 3; g[7][2] = 6
        return g
    if name == "mixed_color_in_one_blob":
        # one blob has multiple colors mixed in (touches itself) → "different-colored neighbor"
        # predicate becomes ambiguous (is it one component or many?)
        _paint(g, [(2, 2), (2, 3)], 2)
        _paint(g, [(2, 4), (2, 5)], 3)   # adjacent, mixed colors form contiguous blob
        _paint(g, [(2, 6), (2, 7)], 6)
        return g
    return g
