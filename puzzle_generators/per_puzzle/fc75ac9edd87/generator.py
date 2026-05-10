"""Generator for arc_puzzle_bank_21_set13_s:S13_H4.

Rule: row-0 count picks symmetry class; row-1 count picks rank;
selected component cropped + recolored 8.

Combinatorial axes (8): grid_h, grid_w, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_class_header, no_rank_header, no_matching_class.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "fc75ac9edd87"
VERSION = "1.1.0"
TASK_ID = "fc75ac9edd87"
SUMMARY = "Header counts choose a symmetry class and rank among matching components."

INVARIANTS = [
    "row 0 contains 1, 2, or 3 color-1 header cells",
    "row 1 contains one or two color-2 rank cells",
    "the body contains at least two components in the requested symmetry class",
    "matching components have distinct areas so rank selection is unambiguous",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_class_header", "no_rank_header", "no_matching_class")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "sym_code":       {"type": "int", "default": "rng 1..3", "valid": "1..3"},
    "rank":           {"type": "int", "default": "rng 1..2", "valid": "1..2"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "5", "valid": "5..5"},
    "position_bias":  {"type": "str", "default": "two_header_rows_with_body",
                       "valid": "two_header_rows_with_body"},
    "n_distinct_colors": {"type": "int", "default": "5", "valid": "5..5"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_ROW_SYM = [
    [(0, 0), (0, 1), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1)],
    [(0, 0), (1, 0), (1, 1), (1, 2), (2, 0)],
]
_COL_SYM = [
    [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)],
]
_BOTH_SYM = [
    [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)],
    [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
]
_ASYM = [(0, 0), (1, 0), (1, 1), (2, 1)]


def _paint(g, top, left, cells, color):
    for dr, dc in cells:
        g[top + dr][left + dc] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(
        seed=seed,
        sample_index=sample_index,
        version=VERSION,
        task_id=TASK_ID,
        difficulty=difficulty,
        overrides=overrides,
    )
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    sym_code = ctx.draw_int("sym_code", 1, 3)
    rank = ctx.draw_int("rank", 1, 2)
    class_shapes = {1: _COL_SYM, 2: _ROW_SYM, 3: _BOTH_SYM}[sym_code]
    g = full_grid(12, 14, 0)

    for c in range(1, 1 + sym_code):
        g[0][c] = 1
    for c in range(1, 1 + rank):
        g[1][c] = 2

    colors = rng.sample([3, 4, 5, 6, 7, 9], 3)
    _paint(g, 3, 1, class_shapes[0], colors[0])
    _paint(g, 3, 7, class_shapes[1], colors[1])
    _paint(g, 8, 2, _ASYM, colors[2])
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(12, 14, 0)
    if name == "no_class_header":
        # Row 0 empty (no class marker count) — rule's class
        # selector has no input.
        for c in range(1, 2): g[1][c] = 2
        _paint(g, 3, 1, _COL_SYM[0], 3)
        _paint(g, 3, 7, _COL_SYM[1], 4)
        _paint(g, 8, 2, _ASYM, 5)
        return g
    if name == "no_rank_header":
        # Row 0 says "col-sym class" but row 1 is empty —
        # rule's rank selector has no input.
        for c in range(1, 2): g[0][c] = 1
        _paint(g, 3, 1, _COL_SYM[0], 3)
        _paint(g, 3, 7, _COL_SYM[1], 4)
        _paint(g, 8, 2, _ASYM, 5)
        return g
    if name == "no_matching_class":
        # Class header asks for col-sym, but body has only
        # asymmetric blobs — no candidates match.
        for c in range(1, 2): g[0][c] = 1
        for c in range(1, 2): g[1][c] = 2
        _paint(g, 3, 1, _ASYM, 3)
        _paint(g, 3, 7, _ASYM, 4)
        _paint(g, 8, 2, _ASYM, 5)
        return g
    return g
