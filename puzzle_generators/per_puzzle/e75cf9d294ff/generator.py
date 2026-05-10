"""Generator for arc_puzzle_bank_fourteenth_21_bundle:hard_92_decode_templates_into_2x2_gallery.

Rule: top five rows hold four 5-col template panels separated by blank
columns. Each template has a distinct selector color. Row 6 stores four
selector + transform pairs. Output arranges the decoded transformed
templates as a 2x2 gallery with one-cell gaps.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_program (row 6 empty → no codes to decode);
no_library (template area empty → rule's lookup returns nothing);
identity_transforms (every transform code = 1 → output gallery is
just recolored templates).
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "e75cf9d294ff"
VERSION = "1.1.0"
TASK_ID = "e75cf9d294ff"
SUMMARY = "Decode four selector-color and transform-code pairs into a 2x2 transformed template gallery."

INVARIANTS = [
    "the top five rows contain four five-column template panels separated by blank columns",
    "each template panel has a distinct selector color",
    "row 6 stores four selector-color and transform-code pairs",
    "the output arranges the decoded transformed templates as a 2x2 gallery with one-cell gaps",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_program", "no_library", "identity_transforms")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "library":           {"type": "int", "default": "rng 0..3", "valid": "0..3"},
    "program":           {"type": "int", "default": "rng 0..4", "valid": "0..4"},
    "palette_kind":      {"type": "str", "default": "rng helpful",
                          "valid": "|".join(PALETTE_KINDS)},
    "palette_size":      {"type": "int", "default": "rng 4..4", "valid": "4..4"},
    "position_bias":     {"type": "str", "default": "fixed_4_panel_library",
                          "valid": "fixed_4_panel_library"},
    "n_distinct_colors": {"type": "int", "default": "rng 4..4", "valid": "4..4"},
    "density":           {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":           {"type": "str", "default": "alias for palette_kind",
                          "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_LIBRARIES = [
    [
        [(0, 0), (1, 0), (2, 0), (2, 1)],
        [(0, 1), (1, 1), (2, 0), (2, 1), (2, 2)],
        [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)],
        [(0, 2), (1, 0), (1, 1), (1, 2), (2, 0)],
    ],
    [
        [(0, 0), (0, 1), (1, 1), (2, 1), (3, 1)],
        [(0, 2), (1, 0), (1, 1), (1, 2), (2, 0)],
        [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2)],
        [(0, 1), (1, 1), (2, 0), (2, 1), (2, 2)],
    ],
    [
        [(0, 1), (1, 1), (2, 0), (2, 1), (2, 2)],
        [(0, 0), (1, 0), (1, 1), (1, 2)],
        [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)],
        [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1)],
    ],
    [
        [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1)],
        [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2), (3, 2)],
        [(0, 1), (1, 0), (1, 1), (2, 1), (3, 1)],
        [(0, 0), (0, 1), (1, 0), (2, 0), (2, 1)],
    ],
]

_PROGRAMS = [
    [(0, 1), (1, 2), (2, 3), (3, 4)],
    [(3, 5), (0, 6), (1, 1), (2, 2)],
    [(1, 3), (2, 4), (0, 5), (3, 6)],
    [(2, 2), (3, 1), (2, 5), (0, 4)],
    [(0, 6), (1, 5), (3, 3), (2, 1)],
]


def _paint(g, top, left, cells, color):
    for r, c in cells:
        g[top + r][left + c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    library = ctx.draw_int("library", 0, len(_LIBRARIES) - 1)
    program = ctx.draw_int("program", 0, len(_PROGRAMS) - 1)
    colors = rng.sample([1, 2, 3, 4, 5, 6, 7, 8], 4)

    g = full_grid(7, 23, 0)
    for idx, (cells, color) in enumerate(zip(_LIBRARIES[library], colors)):
        _paint(g, 1, idx * 6 + 1, cells, color)
    for pos, (selector_idx, code) in enumerate(_PROGRAMS[program]):
        g[6][pos * 2] = colors[selector_idx]
        g[6][pos * 2 + 1] = code
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(7, 23, 0)
    if name == "no_program":
        # Row 6 empty.
        for idx, (cells, color) in enumerate(zip(_LIBRARIES[0], [3, 4, 5, 6])):
            _paint(g, 1, idx * 6 + 1, cells, color)
        return g
    if name == "no_library":
        # No templates in rows 1-4.
        for pos, (selector_idx, code) in enumerate(_PROGRAMS[0]):
            g[6][pos * 2] = [3, 4, 5, 6][selector_idx]
            g[6][pos * 2 + 1] = code
        return g
    if name == "identity_transforms":
        for idx, (cells, color) in enumerate(zip(_LIBRARIES[0], [3, 4, 5, 6])):
            _paint(g, 1, idx * 6 + 1, cells, color)
        for pos in range(4):
            g[6][pos * 2] = [3, 4, 5, 6][pos]
            g[6][pos * 2 + 1] = 1   # all identity
        return g
    return g
