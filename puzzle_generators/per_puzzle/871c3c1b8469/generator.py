"""Generator for arc_puzzle_bank_thirteenth_21_bundle:hard_90_decode_sequence_of_library_shapes.

Combinatorial axes (8): shape_family, sequence, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_library, no_sequence, mismatched_selectors.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "871c3c1b8469"
VERSION = "1.1.0"
TASK_ID = "871c3c1b8469"
SUMMARY = "Decode selector-color and transform-code pairs into a left-to-right strip of library shapes."

INVARIANTS = [
    "the top band has three five-column library panels separated by one blank column",
    "each library panel contains one distinct selector color",
    "row 6 is a sequence of selector-color and transform-code pairs",
    "the output selects the matching crops, transforms them, and packs them with one-cell gaps",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_library", "no_sequence", "mismatched_selectors")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "shape_family":   {"type": "int", "default": "rng 0..3", "valid": "0..3"},
    "sequence":       {"type": "int", "default": "rng 0..3", "valid": "0..3"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "3..4"},
    "position_bias":  {"type": "str", "default": "library_top_sequence_bottom",
                       "valid": "library_top_sequence_bottom"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "3..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_SHAPE_FAMILIES = [
    [
        [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)],
        [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
        [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)],
    ],
    [
        [(0, 2), (1, 0), (1, 1), (1, 2), (2, 2)],
        [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)],
        [(0, 0), (1, 0), (1, 1), (2, 1)],
    ],
    [
        [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
        [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)],
        [(0, 1), (1, 1), (2, 0), (2, 1)],
    ],
    [
        [(0, 0), (0, 1), (1, 0), (2, 0), (2, 1)],
        [(0, 1), (0, 2), (1, 1), (2, 0), (2, 1)],
        [(0, 0), (1, 0), (1, 1), (1, 2), (2, 0)],
    ],
]

_SEQUENCE_PATTERNS = [
    [(0, 1), (1, 2), (2, 3), (0, 4)],
    [(2, 2), (0, 5), (1, 1), (2, 4)],
    [(1, 3), (2, 1), (0, 2)],
    [(0, 5), (0, 3), (2, 2), (1, 4)],
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
    if difficulty == "easy":
        family = ctx.draw_int("shape_family", 0, 1)
        sequence = ctx.draw_int("sequence", 0, 1)
    elif difficulty == "hard":
        family = ctx.draw_int("shape_family", 2, 3)
        sequence = ctx.draw_int("sequence", 2, 3)
    else:
        family = ctx.draw_int("shape_family", 0, len(_SHAPE_FAMILIES) - 1)
        sequence = ctx.draw_int("sequence", 0, len(_SEQUENCE_PATTERNS) - 1)
    colors = rng.sample([2, 3, 4, 5, 6, 7, 8, 9], 3)

    g = full_grid(7, 17, 0)
    for idx, cells in enumerate(_SHAPE_FAMILIES[family]):
        _paint(g, 1, idx * 6 + 1, cells, colors[idx])

    for pos, (selector_idx, code) in enumerate(_SEQUENCE_PATTERNS[sequence]):
        g[6][pos * 2] = colors[selector_idx]
        g[6][pos * 2 + 1] = code
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(7, 17, 0)
    if name == "no_library":
        # Library panels empty — rule has no shapes to decode.
        for pos, (selector_idx, code) in enumerate(_SEQUENCE_PATTERNS[0]):
            g[6][pos * 2] = 4; g[6][pos * 2 + 1] = code
        return g
    if name == "no_sequence":
        # Library present but sequence empty — rule has no decode plan.
        for idx, cells in enumerate(_SHAPE_FAMILIES[0]):
            _paint(g, 1, idx * 6 + 1, cells, [2, 3, 4][idx])
        return g
    if name == "mismatched_selectors":
        # Sequence references colors not in library — rule selects nothing.
        for idx, cells in enumerate(_SHAPE_FAMILIES[0]):
            _paint(g, 1, idx * 6 + 1, cells, [2, 3, 4][idx])
        for pos in range(4):
            g[6][pos * 2] = 9  # not in library
            g[6][pos * 2 + 1] = 1
        return g
    return g
