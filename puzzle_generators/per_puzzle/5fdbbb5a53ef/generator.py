"""Generator for arc_puzzle_bank_ninth_21_bundle:hard_59_typed_relation_matrix.

Rule: compare left-gallery and top-gallery framed shapes by
rotation-equivalent shape and color, encoded as a relation matrix.

Combinatorial axes (8): family, palette, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_top_gallery, no_left_gallery, all_same_palette.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import draw_frame, full_grid

GENERATOR_ID = "5fdbbb5a53ef"
VERSION = "1.1.0"
TASK_ID = "5fdbbb5a53ef"
SUMMARY = "Compare left-gallery and top-gallery framed shapes by rotation-equivalent shape and color."

INVARIANTS = [
    "color-9 frames form a top gallery and a left gallery",
    "top-gallery frames share the minimum frame row and left-gallery frames share the minimum frame column",
    "each frame interior contains a single colored shape crop",
    "the output matrix encodes same shape and same color relations",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_top_gallery", "no_left_gallery", "all_same_palette")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "family":         {"type": "int", "default": "rng 0..3", "valid": "0..3"},
    "palette":        {"type": "int", "default": "rng 0..2", "valid": "0..2"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..3"},
    "position_bias":  {"type": "str", "default": "top_left_galleries",
                       "valid": "top_left_galleries"},
    "n_distinct_colors": {"type": "int", "default": "4", "valid": "4..4"},
    "density":        {"type": "str", "default": "balanced", "valid": "balanced"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_FAMILIES = [
    ([(0, 0), (1, 0), (1, 1), (2, 1)], [(0, 1), (1, 1), (2, 0), (2, 1)]),
    ([(0, 0), (0, 1), (1, 1), (2, 1)], [(0, 1), (1, 0), (1, 1), (2, 0)]),
    ([(0, 0), (1, 0), (1, 1), (1, 2)], [(0, 2), (1, 0), (1, 1), (1, 2)]),
    ([(0, 1), (1, 1), (2, 0), (2, 1)], [(0, 0), (0, 1), (1, 1), (2, 1)]),
]

_PALETTES = [
    (2, 3, 4),
    (4, 6, 7),
    (1, 5, 8),
]


def _paint(g, top, left, cells, color):
    for r, c in cells:
        g[top + r][left + c] = color


def _draw_panel(g, top, left, cells, color):
    draw_frame(g, top, left, top + 4, left + 4, 9)
    _paint(g, top + 1, left + 1, cells, color)


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    family = ctx.draw_int("family", 0, len(_FAMILIES) - 1)
    palette = ctx.draw_int("palette", 0, len(_PALETTES) - 1)
    same_shape, other_shape = _FAMILIES[family]
    c0, c1, c2 = _PALETTES[palette]

    g = full_grid(13, 16, 0)
    _draw_panel(g, 0, 5, same_shape, c0)
    _draw_panel(g, 0, 11, same_shape, c1)
    _draw_panel(g, 6, 0, same_shape, c0)
    _draw_panel(g, 6, 6, other_shape, c1)
    _draw_panel(g, 6, 11, other_shape, c2)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(13, 16, 0)
    same_shape, other_shape = _FAMILIES[0]
    if name == "no_top_gallery":
        # Left gallery only (no top-row frames) — rule's matrix has
        # no column dimension; relation table is empty along one axis.
        _draw_panel(g, 6, 0, same_shape, 2)
        _draw_panel(g, 6, 6, other_shape, 3)
        _draw_panel(g, 6, 11, other_shape, 4)
        return g
    if name == "no_left_gallery":
        # Top gallery only — rule's matrix has no row dimension; the
        # relation matrix has zero rows.
        _draw_panel(g, 0, 5, same_shape, 2)
        _draw_panel(g, 0, 11, same_shape, 3)
        return g
    if name == "all_same_palette":
        # All panels share one color — rule's "same color" relation
        # is true everywhere; relation matrix is all-on, the
        # color-distinguishing signal collapses.
        _draw_panel(g, 0, 5, same_shape, 2)
        _draw_panel(g, 0, 11, same_shape, 2)
        _draw_panel(g, 6, 0, same_shape, 2)
        _draw_panel(g, 6, 6, other_shape, 2)
        _draw_panel(g, 6, 11, other_shape, 2)
        return g
    return g
