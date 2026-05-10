"""Generator for arc_puzzle_bank_21_set19_s:S19_M4.

Rule: corner header marker selects boolean op (union, intersection, XOR,
A-minus-B); apply to two operand panels; render in color 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_marker, no_panels, identical_operands.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "d8b498586958"
VERSION = "1.1.0"
TASK_ID = "d8b498586958"
SUMMARY = "A corner header marker selects union, intersection, XOR, or A-minus-B."

INVARIANTS = [
    "full color-9 rows split the header and two operand panels",
    "the header contains exactly one color-5 operation marker",
    "both operand panels are 5x5 and have non-empty overlap and differences",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_marker", "no_panels", "identical_operands")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "operation":      {"type": "int", "default": "rng 0..3", "valid": "0..3"},
    "shared_cells":   {"type": "int", "default": "rng 1..4", "valid": "1..6"},
    "a_only_cells":   {"type": "int", "default": "rng 2..5", "valid": "1..8"},
    "b_only_cells":   {"type": "int", "default": "rng 2..5", "valid": "1..8"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "rng 3..4", "valid": "3..4"},
    "position_bias":  {"type": "str", "default": "header_with_two_operands",
                       "valid": "header_with_two_operands"},
    "n_distinct_colors": {"type": "int", "default": "rng 3..4", "valid": "3..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_HEADER_MARKERS = [
    (0, 0),  # union
    (0, 4),  # intersection
    (1, 0),  # XOR
    (1, 4),  # A minus B
]


def _paint(g, top, cells, color):
    for r, c in cells:
        g[top + r][c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index,
                  version=VERSION, task_id=TASK_ID,
                  difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    operation = ctx.draw_int("operation", 0, 3)
    if difficulty == "easy":
        shared_n = ctx.draw_int("shared_cells", 1, 2)
        a_only_n = ctx.draw_int("a_only_cells", 1, 2)
        b_only_n = ctx.draw_int("b_only_cells", 1, 2)
    elif difficulty == "hard":
        shared_n = ctx.draw_int("shared_cells", 4, 6)
        a_only_n = ctx.draw_int("a_only_cells", 5, 8)
        b_only_n = ctx.draw_int("b_only_cells", 5, 8)
    else:
        shared_n = ctx.draw_int("shared_cells", 1, 4)
        a_only_n = ctx.draw_int("a_only_cells", 2, 5)
        b_only_n = ctx.draw_int("b_only_cells", 2, 5)

    cells = [(r, c) for r in range(5) for c in range(5)]
    rng.shuffle(cells)
    shared = cells[:shared_n]
    a_only = cells[shared_n:shared_n + a_only_n]
    b_only = cells[shared_n + a_only_n:shared_n + a_only_n + b_only_n]

    g = full_grid(14, 5, 0)
    marker_r, marker_c = _HEADER_MARKERS[operation]
    g[marker_r][marker_c] = 5
    for c in range(5):
        g[2][c] = 9
        g[8][c] = 9

    a_color = 2
    b_color = rng.choice([3, 4, 6, 7])
    _paint(g, 3, shared + a_only, a_color)
    _paint(g, 9, shared + b_only, b_color)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(14, 5, 0)
    for c in range(5):
        g[2][c] = 9
        g[8][c] = 9
    if name == "no_marker":
        # Operand panels but no header marker — rule's op
        # selector has no input; output undefined.
        for r, c in [(3, 0), (3, 1), (4, 1)]: g[r][c] = 2
        for r, c in [(9, 0), (9, 1), (10, 1)]: g[r][c] = 3
        return g
    if name == "no_panels":
        # Header marker but both panels empty — rule has nothing
        # to apply the boolean op to.
        g[0][0] = 5
        return g
    if name == "identical_operands":
        # A and B identical — union/intersection/A-minus-B all
        # yield A (XOR yields empty); rule's branch invariance.
        g[0][0] = 5
        for r, c in [(3, 0), (3, 1), (4, 1)]: g[r][c] = 2
        for r, c in [(9, 0), (9, 1), (10, 1)]: g[r][c] = 3
        return g
    return g
