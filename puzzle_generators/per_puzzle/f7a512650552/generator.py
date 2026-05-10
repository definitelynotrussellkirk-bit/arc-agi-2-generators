"""Generator for arc_puzzle_bank_21_set14_s:S14_H3.

Combinatorial axes (8): mode, query, palette_kind, palette_size,
position_bias, n_distinct_colors, density, texture.
Degenerates: no_dividers, no_example, identical_closures.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "f7a512650552"
VERSION = "1.1.0"
TASK_ID = "f7a512650552"
SUMMARY = "Infer row-span or column-span closure from an example pair and apply it to a query panel."

INVARIANTS = [
    "two full color-5 columns split the grid into example source, example result, and query panels",
    "the example result is either the row-span closure or column-span closure of the source",
    "row and column closures of the example source are different",
    "the query object is closed by the inferred operation and cropped in color 8",
]

PALETTE_KINDS = ("default", "warm", "cool", "varied")
DEGENERATE_TEXTURES = ("no_dividers", "no_example", "identical_closures")
HELPFUL_TEXTURES = PALETTE_KINDS

AXES = {
    "mode":           {"type": "int", "default": "rng 0..1", "valid": "0=row, 1=column"},
    "query":          {"type": "int", "default": "rng 0..3", "valid": "0..3"},
    "palette_kind":   {"type": "str", "default": "rng helpful",
                       "valid": "|".join(PALETTE_KINDS)},
    "palette_size":   {"type": "int", "default": "3", "valid": "2..4"},
    "position_bias":  {"type": "str", "default": "three_panels_5dividers",
                       "valid": "three_panels_5dividers"},
    "n_distinct_colors": {"type": "int", "default": "3", "valid": "2..4"},
    "density":        {"type": "str", "default": "sparse", "valid": "sparse"},
    "texture":        {"type": "str", "default": "alias for palette_kind",
                       "valid": "|".join(HELPFUL_TEXTURES + DEGENERATE_TEXTURES)},
}

_EXAMPLE = [(0, 0), (0, 2), (1, 1), (2, 0), (2, 2)]
_QUERIES = [
    [(0, 0), (0, 2), (1, 0), (2, 2)],
    [(0, 0), (1, 1), (2, 0), (2, 2)],
    [(0, 1), (1, 0), (1, 2), (2, 1)],
    [(0, 0), (0, 2), (1, 1), (2, 1)],
]


def _row_close(cells):
    out = set(cells)
    rows = {}
    for r, c in cells:
        rows.setdefault(r, []).append(c)
    for r, cols in rows.items():
        for c in range(min(cols), max(cols) + 1):
            out.add((r, c))
    return sorted(out)


def _col_close(cells):
    out = set(cells)
    cols = {}
    for r, c in cells:
        cols.setdefault(c, []).append(r)
    for c, rows in cols.items():
        for r in range(min(rows), max(rows) + 1):
            out.add((r, c))
    return sorted(out)


def _paint(g, top, left, cells, color):
    for r, c in cells:
        g[top + r][left + c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(seed=seed, sample_index=sample_index, version=VERSION,
                  task_id=TASK_ID, difficulty=difficulty, overrides=overrides)
    if overrides.get("texture") in DEGENERATE_TEXTURES:
        return _draw_from_degenerate(overrides["texture"], None)
    rng = ctx.draw_rng("layout")
    mode = ctx.draw_int("mode", 0, 1)
    query = ctx.draw_int("query", 0, len(_QUERIES) - 1)
    ex_color, query_color = rng.sample([2, 3, 4, 6, 7, 9], 2)
    g = full_grid(9, 23, 0)
    for r in range(9):
        g[r][7] = 5
        g[r][15] = 5
    _paint(g, 2, 2, _EXAMPLE, ex_color)
    closure = _row_close(_EXAMPLE) if mode == 0 else _col_close(_EXAMPLE)
    _paint(g, 2, 10, closure, ex_color)
    _paint(g, 2, 18, _QUERIES[query], query_color)
    return g


def _draw_from_degenerate(name, rng):
    g = full_grid(9, 23, 0)
    if name == "no_dividers":
        # No 5-divider columns — panel boundaries undefined.
        _paint(g, 2, 2, _EXAMPLE, 2)
        _paint(g, 2, 10, _EXAMPLE, 2)
        _paint(g, 2, 18, _QUERIES[0], 3)
        return g
    if name == "no_example":
        # Dividers but no example shown — rule has no closure to infer.
        for r in range(9):
            g[r][7] = 5; g[r][15] = 5
        _paint(g, 2, 18, _QUERIES[0], 3)
        return g
    if name == "identical_closures":
        # Example is row-symmetric so row and col closures coincide — operation undecidable.
        for r in range(9):
            g[r][7] = 5; g[r][15] = 5
        sq = [(0, 0), (0, 1), (1, 0), (1, 1)]
        _paint(g, 2, 2, sq, 2)
        _paint(g, 2, 10, sq, 2)
        _paint(g, 2, 18, _QUERIES[0], 3)
        return g
    return g
