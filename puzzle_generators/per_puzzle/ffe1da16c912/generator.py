"""Generator for arc_puzzle_bank_nineteenth21:H131.

Three prototype panels define shape families. The fourth panel is a transformed
copy of one prototype, recolored with the query color.
"""
from __future__ import annotations

from puzzle_generators.base import gen_ctx
from puzzle_generators.helpers.grid import full_grid

GENERATOR_ID = "ffe1da16c912"
VERSION = "1.1.0"
TASK_ID = "ffe1da16c912"
SUMMARY = "Match a transformed query support to one of three prototype panels."

INVARIANTS = [
    "the input has four 3x3 panels separated by color-5 columns",
    "the first three panels are non-equivalent prototype shape families",
    "the query panel is a dihedral transform of exactly one prototype",
    "the output is the matched prototype support recolored by the query color",
]

AXES = {
    "match_index": {"type": "int", "default": "rng 0..2", "valid": "0..2"},
    "transform": {"type": "enum", "default": "rng", "valid": "id|r1|r2|r3|fh|fv|tr|atr"},
}

_PROTOS = [
    [(0, 0), (1, 0), (1, 1)],
    [(0, 0), (0, 1), (0, 2), (1, 1)],
    [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)],
]
_CODES = ["id", "r1", "r2", "r3", "fh", "fv", "tr", "atr"]


def _normalize(cells):
    min_r = min(r for r, _ in cells)
    min_c = min(c for _, c in cells)
    return sorted((r - min_r, c - min_c) for r, c in cells)


def _dims(cells):
    return max(r for r, _ in cells) + 1, max(c for _, c in cells) + 1


def _xform(cells, code):
    h, w = _dims(cells)
    if code == "id":
        raw = cells
    elif code == "r1":
        raw = [(c, h - 1 - r) for r, c in cells]
    elif code == "r2":
        raw = [(h - 1 - r, w - 1 - c) for r, c in cells]
    elif code == "r3":
        raw = [(w - 1 - c, r) for r, c in cells]
    elif code == "fh":
        raw = [(r, w - 1 - c) for r, c in cells]
    elif code == "fv":
        raw = [(h - 1 - r, c) for r, c in cells]
    elif code == "tr":
        raw = [(c, r) for r, c in cells]
    else:
        raw = [(w - 1 - c, h - 1 - r) for r, c in cells]
    return _normalize(raw)


def _paint_panel(g, panel, cells, color):
    left = panel * 4
    for r, c in cells:
        g[r][left + c] = color


def generate(seed, sample_index, *, difficulty=None, **overrides):
    ctx = gen_ctx(
        seed=seed,
        sample_index=sample_index,
        version=VERSION,
        task_id=TASK_ID,
        difficulty=difficulty,
        overrides=overrides,
    )
    rng = ctx.draw_rng("layout")
    match_index = ctx.draw_int("match_index", 0, 2)
    code = ctx.draw_choice("transform", _CODES)
    proto_colors = rng.sample([1, 2, 3, 4, 6, 7, 8], 3)
    query_color = rng.choice([6, 7, 8, 9])

    g = full_grid(3, 15, 0)
    for sep in (3, 7, 11):
        for r in range(3):
            g[r][sep] = 5
    for idx, cells in enumerate(_PROTOS):
        _paint_panel(g, idx, cells, proto_colors[idx])
    _paint_panel(g, 3, _xform(_PROTOS[match_index], code), query_color)
    return g
